"""
OTP Service for phone and email verification
"""

import random
import string
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models.auth import OTP, User
import logging

# SMS Integration
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

logger = logging.getLogger(__name__)


class OTPService:
    """Service for handling OTP operations with SMS/Email integration."""
    
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP code."""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def create_otp(user, identifier, otp_type, expiry_minutes=10):
        """Create a new OTP for the user."""
        # Invalidate any existing unused OTPs for this user and identifier
        OTP.objects.filter(
            user=user,
            identifier=identifier,
            otp_type=otp_type,
            is_used=False
        ).update(is_used=True)
        
        # Create new OTP
        otp = OTP.objects.create(
            user=user,
            identifier=identifier,
            otp_type=otp_type,
            code=OTPService.generate_otp(),
            expires_at=timezone.now() + timedelta(minutes=expiry_minutes)
        )
        
        return otp
    
    @staticmethod
    def send_phone_otp(phone_number, otp_code):
        """Send OTP via SMS using Twilio."""
        if not TWILIO_AVAILABLE:
            logger.warning("Twilio not available, logging OTP instead")
            masked_phone = f"{phone_number[:3]}***{phone_number[-2:]}" if len(phone_number) > 5 else "***"
            print(f"📱 SMS OTP sent to {masked_phone}")
            return True
        
        try:
            # Get Twilio credentials from settings
            account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
            auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
            from_number = getattr(settings, 'TWILIO_FROM_NUMBER', None)
            
            if not all([account_sid, auth_token, from_number]):
                logger.warning("Twilio credentials not configured, logging OTP instead")
                masked_phone = f"{phone_number[:3]}***{phone_number[-2:]}" if len(phone_number) > 5 else "***"
                print(f"📱 SMS OTP sent to {masked_phone}")
                return True
            
            # Send SMS via Twilio
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f"Your CalloutRacing verification code is: {otp_code}. Valid for 10 minutes.",
                from_=from_number,
                to=phone_number
            )
            
            masked_phone = f"{phone_number[:3]}***{phone_number[-2:]}" if len(phone_number) > 5 else "***"
            logger.info(f"SMS OTP sent to {masked_phone} via Twilio: {message.sid}")
            return True
            
        except Exception as e:
            logger.error("Failed to send SMS OTP")
            # Fallback to logging in development
            masked_phone = f"{phone_number[:3]}***{phone_number[-2:]}" if len(phone_number) > 5 else "***"
            print(f"📱 SMS OTP sent to {masked_phone}")
            return True
    
    @staticmethod
    def send_email_otp(email, otp_code):
        """Send OTP via email."""
        subject = "Your CalloutRacing Verification Code"
        message = f"""
        Your verification code has been sent.
        
        This code will expire in 10 minutes.
        
        If you didn't request this code, please ignore this email.
        
        Best regards,
        The CalloutRacing Team
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            masked_email = f"{email[:3]}***@{email.split('@')[1]}" if '@' in email else "***@***"
            logger.info(f"Email OTP sent to {masked_email}")
            return True
        except Exception as e:
            logger.error("Failed to send email OTP")
            return False
    
    @staticmethod
    def verify_otp(user, identifier, otp_code, otp_type):
        """Verify an OTP code."""
        try:
            otp = OTP.objects.get(
                user=user,
                identifier=identifier,
                otp_type=otp_type,
                code=otp_code,
                is_used=False
            )
            
            if otp.is_expired:
                return False, "OTP has expired"
            
            # Mark OTP as used
            otp.is_used = True
            otp.save()
            
            return True, "OTP verified successfully"
            
        except OTP.DoesNotExist:
            return False, "Invalid OTP code"
    
    @staticmethod
    def send_otp(user, identifier, otp_type):
        """Send OTP to user via phone or email."""
        otp = OTPService.create_otp(user, identifier, otp_type)
        
        if otp_type == 'phone':
            success = OTPService.send_phone_otp(identifier, otp.code)
        else:  # email
            success = OTPService.send_email_otp(identifier, otp.code)
        
        return success, otp 