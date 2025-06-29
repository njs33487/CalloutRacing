"""
Authentication and User Profile Models

This module contains models related to user authentication and profiles:
- User: Custom user model with email verification
- UserProfile: Extended user profile information
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


class User(AbstractUser):
    """Custom User model with email verification."""
    email_verified = models.BooleanField(default=False, help_text="Whether email has been verified")
    email_verification_token = models.UUIDField(null=True, blank=True, unique=True, help_text="Token for email verification")
    email_verification_sent_at = models.DateTimeField(blank=True, null=True, help_text="When verification email was sent")
    email_verification_expires_at = models.DateTimeField(blank=True, null=True, help_text="When verification token expires")
    
    # OTP fields for enhanced security
    otp_enabled = models.BooleanField(default=False, help_text="Whether OTP is enabled for this user")
    otp_secret = models.CharField(max_length=32, blank=True, null=True, help_text="TOTP secret key")
    otp_backup_codes = models.JSONField(default=list, blank=True, help_text="Backup codes for OTP")
    
    # Password reset fields
    password_reset_token = models.UUIDField(null=True, blank=True, unique=True, help_text="Token for password reset")
    password_reset_expires_at = models.DateTimeField(blank=True, null=True, help_text="When password reset token expires")
    password_reset_sent_at = models.DateTimeField(blank=True, null=True, help_text="When password reset email was sent")
    
    # Override email field to make it unique
    email = models.EmailField(unique=True, help_text="User's email address")
    
    # Override username field to allow email format
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Username (can be email format)"
    )
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class UserProfile(models.Model):
    """User profile model for additional user information."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, help_text="User's bio or description")
    location = models.CharField(max_length=200, blank=True, help_text="User's location")
    car_make = models.CharField(max_length=50, blank=True, help_text="User's car make")
    car_model = models.CharField(max_length=50, blank=True, help_text="User's car model")
    car_year = models.IntegerField(blank=True, null=True, help_text="User's car year")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    wins = models.IntegerField(default=0, help_text="Number of races won")
    losses = models.IntegerField(default=0, help_text="Number of races lost")
    total_races = models.IntegerField(default=0, help_text="Total number of races")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def win_rate(self):
        """Calculate win rate percentage."""
        if self.total_races == 0:
            return 0
        return (self.wins / self.total_races) * 100

    class Meta:
        ordering = ['-created_at'] 