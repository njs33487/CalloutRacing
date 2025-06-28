"""
Email Service for CalloutRacing Application

This module handles sending various types of emails including:
- Email verification emails
- Welcome emails
- Password reset emails
- Notification emails
"""

import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .models.auth import User
import uuid

logger = logging.getLogger(__name__)


def send_email_verification(user):
    """
    Send email verification email to user.
    
    Args:
        user: User instance to send verification email to
    """
    try:
        # Generate new verification token and set expiration
        user.email_verification_token = uuid.uuid4()
        user.email_verification_sent_at = timezone.now()
        user.email_verification_expires_at = timezone.now() + timedelta(hours=24)
        user.save()
        
        # Build verification URL
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{user.email_verification_token}"
        
        # Render email template
        context = {
            'user': user,
            'verification_url': verification_url,
        }
        
        html_message = render_to_string('emails/email_verification.html', context)
        plain_message = render_to_string('emails/email_verification.txt', context)
        
        # Send email
        send_mail(
            subject='Verify Your Email - CalloutRacing',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Email verification sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email verification to {user.email}: {str(e)}")
        return False


def send_welcome_email(user):
    """
    Send welcome email to user after email verification.
    
    Args:
        user: User instance to send welcome email to
    """
    try:
        # Build URLs
        app_url = f"{settings.FRONTEND_URL}/app"
        help_url = f"{settings.FRONTEND_URL}/help"
        
        # Render email template
        context = {
            'user': user,
            'app_url': app_url,
            'help_url': help_url,
        }
        
        html_message = render_to_string('emails/welcome_email.html', context)
        plain_message = render_to_string('emails/welcome_email.txt', context)
        
        # Send email
        send_mail(
            subject='Welcome to CalloutRacing! 🏁',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Welcome email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")
        return False


def verify_email_token(token):
    """
    Verify email verification token.
    
    Args:
        token: UUID token to verify
        
    Returns:
        tuple: (success: bool, user: User or None, message: str)
    """
    try:
        # Find user with this token
        user = User.objects.get(email_verification_token=token)
        
        # Check if token is expired
        if user.email_verification_expires_at and user.email_verification_expires_at < timezone.now():
            return False, None, "Email verification link has expired. Please request a new one."
        
        # Mark email as verified
        user.email_verified = True
        user.email_verification_token = None
        user.email_verification_sent_at = None
        user.email_verification_expires_at = None
        user.save()
        
        # Send welcome email
        send_welcome_email(user)
        
        logger.info(f"Email verified for user {user.email}")
        return True, user, "Email verified successfully!"
        
    except User.DoesNotExist:
        return False, None, "Invalid verification token."
    except Exception as e:
        logger.error(f"Error verifying email token: {str(e)}")
        return False, None, "An error occurred while verifying your email."


def resend_verification_email(email):
    """
    Resend verification email to user.
    
    Args:
        email: Email address to resend verification to
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        user = User.objects.get(email=email)
        
        if user.email_verified:
            return False, "Email is already verified."
        
        # Check if we can resend (rate limiting)
        if (user.email_verification_sent_at and 
            timezone.now() - user.email_verification_sent_at < timedelta(minutes=5)):
            return False, "Please wait 5 minutes before requesting another verification email."
        
        # Send verification email
        success = send_email_verification(user)
        
        if success:
            return True, "Verification email sent successfully!"
        else:
            return False, "Failed to send verification email. Please try again later."
            
    except User.DoesNotExist:
        return False, "No account found with this email address."
    except Exception as e:
        logger.error(f"Error resending verification email: {str(e)}")
        return False, "An error occurred. Please try again later." 