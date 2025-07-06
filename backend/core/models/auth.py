"""
User Profile Models

This module contains models related to user profiles:
- UserProfile: Extended user profile information for Django's built-in User model
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser."""
    email = models.EmailField(unique=True, help_text="User's email address")
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True, help_text="User's phone number")
    phone_verified = models.BooleanField(default=False, help_text="Whether phone number has been verified")
    # Stripe Connect fields
    stripe_connect_account_id = models.CharField(max_length=255, blank=True, null=True, help_text='Stripe Connect account ID for marketplace sellers')
    # Add any additional custom fields here if needed

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """User profile model for additional user information."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    
    # Basic profile fields
    bio = models.TextField(blank=True, help_text="User's bio or description")
    location = models.CharField(max_length=200, blank=True, help_text="User's location")
    car_make = models.CharField(max_length=50, blank=True, help_text="User's car make")
    car_model = models.CharField(max_length=50, blank=True, help_text="User's car model")
    car_year = models.IntegerField(blank=True, null=True, help_text="User's car year")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    
    # Racing statistics
    wins = models.IntegerField(default=0, help_text="Number of races won")
    losses = models.IntegerField(default=0, help_text="Number of races lost")
    total_races = models.IntegerField(default=0, help_text="Total number of races")
    
    # Email verification fields
    email_verified = models.BooleanField(default=False, help_text='Whether email has been verified')
    email_verification_token = models.UUIDField(null=True, blank=True, unique=True, help_text='Token for email verification')
    email_verification_sent_at = models.DateTimeField(blank=True, help_text='When verification email was sent', null=True)
    email_verification_expires_at = models.DateTimeField(blank=True, help_text='When verification token expires', null=True)
    
    # Password reset fields
    password_reset_token = models.UUIDField(null=True, blank=True, unique=True, help_text='Token for password reset')
    password_reset_expires_at = models.DateTimeField(null=True, blank=True, help_text='When password reset token expires')
    password_reset_sent_at = models.DateTimeField(null=True, blank=True, help_text='When password reset email was sent')
    
    # OTP fields
    otp_enabled = models.BooleanField(default=False, help_text='Whether OTP is enabled for this account')
    otp_secret = models.CharField(max_length=32, null=True, blank=True, help_text='TOTP secret key')
    otp_backup_codes = models.JSONField(default=list, blank=True, help_text='Backup codes for OTP')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{getattr(self.user, 'username', 'UserProfile')}'s profile"

    @property
    def win_rate(self):
        wins = self.wins if isinstance(self.wins, int) else 0
        total_races = self.total_races if isinstance(self.total_races, int) else 0
        if total_races:
            return (float(wins) / float(total_races)) * 100
        return 0.0

    class Meta:
        ordering = ['-created_at'] 


class OTP(models.Model):
    """OTP model for phone and email verification."""
    OTP_TYPE_CHOICES = [
        ('phone', 'Phone'),
        ('email', 'Email'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='otps')
    otp_type = models.CharField(max_length=10, choices=OTP_TYPE_CHOICES, help_text='Type of OTP (phone or email)')
    identifier = models.CharField(max_length=255, help_text='Phone number or email address')
    code = models.CharField(max_length=6, help_text='6-digit OTP code')
    is_used = models.BooleanField(default=False, help_text='Whether OTP has been used')
    expires_at = models.DateTimeField(help_text='When OTP expires')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['identifier', 'code', 'is_used']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"OTP for {self.identifier} ({self.otp_type})"
    
    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at 