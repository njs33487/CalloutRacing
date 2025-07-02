"""
User Profile Models

This module contains models related to user profiles:
- UserProfile: Extended user profile information for Django's built-in User model
"""

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid


class UserProfile(models.Model):
    """User profile model for additional user information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
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