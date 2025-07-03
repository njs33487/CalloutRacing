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
from django.contrib.auth.models import User
import uuid

logger = logging.getLogger(__name__)


def send_email_verification(user):
    """
    Send email verification email to user.
    
    Args:
        user: User instance to send verification email to
    """
    try:
        # Get or create user profile
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        
        # Generate new verification token and set expiration
        profile.email_verification_token = uuid.uuid4()
        profile.email_verification_sent_at = timezone.now()
        profile.email_verification_expires_at = timezone.now() + timedelta(hours=24)
        profile.save()
        
        # Build verification URL
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{profile.email_verification_token}"
        
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
        # Find user profile with this token
        from core.models.auth import UserProfile
        profile = UserProfile.objects.get(email_verification_token=token)
        user = profile.user
        
        # Check if token is expired
        if profile.email_verification_expires_at and profile.email_verification_expires_at < timezone.now():
            return False, None, "Email verification link has expired. Please request a new one."
        
        # Mark email as verified
        profile.email_verified = True
        profile.email_verification_token = None
        profile.email_verification_sent_at = None
        profile.email_verification_expires_at = None
        profile.save()
        
        # Send welcome email
        send_welcome_email(user)
        
        logger.info(f"Email verified for user {user.email}")
        return True, user, "Email verified successfully!"
        
    except UserProfile.DoesNotExist:
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
        profile = user.profile
        
        if profile.email_verified:
            return False, "Email is already verified."
        
        # Check if we can resend (rate limiting)
        if (profile.email_verification_sent_at and 
            timezone.now() - profile.email_verification_sent_at < timedelta(minutes=5)):
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


def send_password_reset_email(user):
    """
    Send password reset email to user.
    
    Args:
        user: User instance to send password reset email to
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        profile = user.profile
        
        # Generate password reset token
        profile.password_reset_token = uuid.uuid4()
        profile.password_reset_expires_at = timezone.now() + timedelta(hours=1)
        profile.password_reset_sent_at = timezone.now()
        profile.save()
        
        # Build reset URL
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{profile.password_reset_token}"
        
        # Render email template
        context = {
            'user': user,
            'reset_url': reset_url,
        }
        
        html_message = render_to_string('emails/password_reset.html', context)
        plain_message = render_to_string('emails/password_reset.txt', context)
        
        # Send email
        send_mail(
            subject='Reset Your Password - CalloutRacing',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Password reset email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send password reset email to {user.email}: {str(e)}")
        return False


def verify_password_reset_token(token):
    """
    Verify password reset token.
    
    Args:
        token: UUID token to verify
        
    Returns:
        tuple: (success: bool, user: User or None, message: str)
    """
    try:
        from core.models.auth import UserProfile
        profile = UserProfile.objects.get(password_reset_token=token)
        user = profile.user
        
        # Check if token is expired
        if profile.password_reset_expires_at and profile.password_reset_expires_at < timezone.now():
            return False, None, "Password reset link has expired. Please request a new one."
        
        return True, user, "Token is valid."
        
    except UserProfile.DoesNotExist:
        return False, None, "Invalid password reset token."
    except Exception as e:
        logger.error(f"Error verifying password reset token: {str(e)}")
        return False, None, "An error occurred while verifying the token."


def reset_password_with_token(token, new_password):
    """
    Reset password using token.
    
    Args:
        token: UUID token for password reset
        new_password: New password to set
        
    Returns:
        tuple: (success: bool, user: User or None, message: str)
    """
    try:
        from core.models.auth import UserProfile
        profile = UserProfile.objects.get(password_reset_token=token)
        user = profile.user
        
        # Check if token is expired
        if profile.password_reset_expires_at and profile.password_reset_expires_at < timezone.now():
            return False, None, "Password reset link has expired. Please request a new one."
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        # Clear reset token
        profile.password_reset_token = None
        profile.password_reset_expires_at = None
        profile.password_reset_sent_at = None
        profile.save()
        
        logger.info(f"Password reset successfully for user {user.email}")
        return True, user, "Password reset successfully. You can now log in with your new password."
        
    except UserProfile.DoesNotExist:
        return False, None, "Invalid password reset token."
    except Exception as e:
        logger.error(f"Error resetting password: {str(e)}")
        return False, None, "An error occurred while resetting your password." 