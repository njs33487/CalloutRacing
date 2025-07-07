"""
Enhanced OTP Service for phone and email verification

This service implements secure OTP generation, delivery, and verification
with rate limiting, brute force protection, and audit logging.
"""

import secrets
import string
import re
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from .models.auth import OTP, User
import logging

# SMS Integration
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    Client = None

logger = logging.getLogger(__name__)


class OTPService:
    """Enhanced service for handling OTP operations with security best practices."""
    
    # Rate limiting constants
    MAX_ATTEMPTS_PER_HOUR = 5
    MAX_ATTEMPTS_PER_DAY = 20
    LOCKOUT_DURATION_MINUTES = 30
    RESEND_COOLDOWN_SECONDS = 60
    
    @staticmethod
    def generate_secure_otp():
        """Generate a cryptographically secure 6-digit OTP code."""
        return ''.join(secrets.choice(string.digits) for _ in range(6))
    
    @staticmethod
    def check_rate_limit(identifier, action='send'):
        """Check rate limiting for OTP operations."""
        cache_key = f"otp_rate_limit:{action}:{identifier}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= OTPService.MAX_ATTEMPTS_PER_HOUR:
            return False, f"Too many {action} attempts. Please try again later."
        
        # Increment attempt counter
        cache.set(cache_key, attempts + 1, 3600)  # 1 hour expiry
        return True, None
    
    @staticmethod
    def check_daily_limit(identifier):
        """Check daily rate limiting."""
        cache_key = f"otp_daily_limit:{identifier}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= OTPService.MAX_ATTEMPTS_PER_DAY:
            return False, "Daily OTP limit exceeded. Please try again tomorrow."
        
        # Increment daily counter
        cache.set(cache_key, attempts + 1, 86400)  # 24 hours expiry
        return True, None
    
    @staticmethod
    def check_resend_cooldown(identifier):
        """Check if enough time has passed since last OTP send."""
        cache_key = f"otp_resend_cooldown:{identifier}"
        last_sent = cache.get(cache_key)
        
        if last_sent:
            time_diff = timezone.now() - last_sent
            if time_diff.total_seconds() < OTPService.RESEND_COOLDOWN_SECONDS:
                remaining = OTPService.RESEND_COOLDOWN_SECONDS - int(time_diff.total_seconds())
                return False, f"Please wait {remaining} seconds before requesting another OTP."
        
        return True, None
    
    @staticmethod
    def create_otp(user, identifier, otp_type, purpose='login', expiry_minutes=10):
        """Create a new OTP with enhanced security."""
        # Check rate limits
        rate_ok, rate_error = OTPService.check_rate_limit(identifier, 'send')
        if not rate_ok:
            return False, rate_error
        
        daily_ok, daily_error = OTPService.check_daily_limit(identifier)
        if not daily_ok:
            return False, daily_error
        
        resend_ok, resend_error = OTPService.check_resend_cooldown(identifier)
        if not resend_ok:
            return False, resend_error
        
        with transaction.atomic():
            # Invalidate any existing unused OTPs for this user and identifier
            OTP.objects.filter(
                user=user,
                identifier=identifier,
                otp_type=otp_type,
                is_used=False
            ).update(is_used=True)
            
            # Create new OTP with secure generation
            otp = OTP.objects.create(
                user=user,
                identifier=identifier,
                otp_type=otp_type,
                code=OTPService.generate_secure_otp(),
                expires_at=timezone.now() + timedelta(minutes=expiry_minutes),
                purpose=purpose
            )
            
            # Set resend cooldown
            cache_key = f"otp_resend_cooldown:{identifier}"
            cache.set(cache_key, timezone.now(), OTPService.RESEND_COOLDOWN_SECONDS)
            
            # Log OTP creation (without exposing the code)
            masked_identifier = OTPService._mask_identifier(identifier)
            logger.info(f"OTP created for {masked_identifier} ({otp_type}) - User: {user.username}")
            
            return True, otp
    
    @staticmethod
    def _mask_identifier(identifier):
        """Mask identifier for logging purposes."""
        if '@' in identifier:  # Email
            parts = identifier.split('@')
            return f"{parts[0][:3]}***@{parts[1]}"
        else:  # Phone
            if len(identifier) > 5:
                return f"{identifier[:3]}***{identifier[-2:]}"
            return "***"
    
    @staticmethod
    def send_phone_otp(phone_number, otp_code):
        """Send OTP via SMS with enhanced error handling."""
        if not TWILIO_AVAILABLE:
            logger.warning("Twilio not available, logging OTP instead")
            masked_phone = OTPService._mask_identifier(phone_number)
            print(f"📱 SMS OTP sent to {masked_phone}: {otp_code}")
            return True
        
        try:
            # Get Twilio credentials from settings
            account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
            auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
            from_number = getattr(settings, 'TWILIO_FROM_NUMBER', None)
            
            if not all([account_sid, auth_token, from_number]):
                logger.warning("Twilio credentials not configured, logging OTP instead")
                masked_phone = OTPService._mask_identifier(phone_number)
                print(f"📱 SMS OTP sent to {masked_phone}: {otp_code}")
                return True
            
            # Send SMS via Twilio with clear message
            client = Client(account_sid, auth_token)
            message_body = f"Your CalloutRacing verification code is: {otp_code}\n\nThis code will expire in 10 minutes. If you didn't request this code, please ignore this message."
            
            message = client.messages.create(
                body=message_body,
                from_=from_number,
                to=phone_number
            )
            
            masked_phone = OTPService._mask_identifier(phone_number)
            logger.info(f"SMS OTP sent to {masked_phone} via Twilio: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS OTP: {str(e)}")
            # Fallback to logging in development
            masked_phone = OTPService._mask_identifier(phone_number)
            print(f"📱 SMS OTP sent to {masked_phone}: {otp_code}")
            return True
    
    @staticmethod
    def send_email_otp(email, otp_code):
        """Send OTP via email with enhanced templates."""
        subject = "Your CalloutRacing Verification Code"
        
        # Enhanced email template
        message = f"""
Hello!

Your CalloutRacing verification code is: {otp_code}

This code will expire in 10 minutes.

If you didn't request this verification code, please ignore this email.

For security reasons, never share this code with anyone.

Best regards,
The CalloutRacing Team

---
This is an automated message. Please do not reply to this email.
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            masked_email = OTPService._mask_identifier(email)
            logger.info(f"Email OTP sent to {masked_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email OTP: {str(e)}")
            return False
    
    @staticmethod
    def verify_otp(user, identifier, otp_code, otp_type, purpose='login'):
        """Verify an OTP code with enhanced security."""
        # Check rate limiting for verification attempts
        rate_ok, rate_error = OTPService.check_rate_limit(identifier, 'verify')
        if not rate_ok:
            return False, rate_error
        
        try:
            otp = OTP.objects.get(
                user=user,
                identifier=identifier,
                otp_type=otp_type,
                code=otp_code,
                is_used=False,
                purpose=purpose
            )
            
            if otp.is_expired:
                logger.warning(f"Expired OTP attempt for {OTPService._mask_identifier(identifier)}")
                return False, "OTP has expired. Please request a new code."
            
            # Mark OTP as used immediately to prevent replay attacks
            otp.is_used = True
            otp.save()
            
            # Log successful verification
            masked_identifier = OTPService._mask_identifier(identifier)
            logger.info(f"OTP verified successfully for {masked_identifier} ({otp_type}) - User: {user.username}")
            
            return True, "OTP verified successfully"
            
        except OTP.DoesNotExist:
            # Log failed verification attempt
            masked_identifier = OTPService._mask_identifier(identifier)
            logger.warning(f"Invalid OTP attempt for {masked_identifier} ({otp_type}) - User: {user.username}")
            return False, "Invalid OTP code. Please check and try again."
    
    @staticmethod
    def send_otp(user, identifier, otp_type, purpose='login'):
        """Send OTP to user via phone or email with enhanced security."""
        # Create OTP
        success, result = OTPService.create_otp(user, identifier, otp_type, purpose)
        if not success:
            return False, result
        
        # At this point, result is an OTP object
        otp = result
        
        # Send OTP based on type
        if otp_type == 'phone':
            delivery_success = OTPService.send_phone_otp(identifier, otp.code)
        else:  # email
            delivery_success = OTPService.send_email_otp(identifier, otp.code)
        
        if not delivery_success:
            # Mark OTP as used if delivery failed
            otp.is_used = True
            otp.save()
            return False, "Failed to deliver OTP. Please try again."
        
        return True, otp
    
    @staticmethod
    def get_remaining_attempts(identifier):
        """Get remaining OTP attempts for rate limiting display."""
        cache_key = f"otp_rate_limit:send:{identifier}"
        attempts = cache.get(cache_key, 0)
        return max(0, OTPService.MAX_ATTEMPTS_PER_HOUR - attempts)
    
    @staticmethod
    def get_resend_cooldown_remaining(identifier):
        """Get remaining time before resend is allowed."""
        cache_key = f"otp_resend_cooldown:{identifier}"
        last_sent = cache.get(cache_key)
        
        if last_sent:
            time_diff = timezone.now() - last_sent
            remaining = OTPService.RESEND_COOLDOWN_SECONDS - int(time_diff.total_seconds())
            return max(0, remaining)
        
        return 0 