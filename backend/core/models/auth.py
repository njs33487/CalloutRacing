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