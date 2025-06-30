"""
Location Models

This module contains models related to locations and geographic features:
- HotSpot: Racing hot spots and locations
- RacingCrew: Racing crews and car clubs
- CrewMembership: Crew membership management
- LocationBroadcast: Real-time location broadcasting
- OpenChallenge: Public open challenges
- ChallengeResponse: Responses to open challenges
"""

from django.db import models
from django.conf import settings


class HotSpot(models.Model):
    """Racing hot spot model."""
    name = models.CharField(max_length=200, help_text="Name of the hot spot")
    description = models.TextField(blank=True, help_text="Description of the location")
    address = models.CharField(max_length=500, help_text="Full address")
    city = models.CharField(max_length=100, help_text="City")
    state = models.CharField(max_length=50, help_text="State")
    zip_code = models.CharField(max_length=20, help_text="ZIP code")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Latitude coordinate")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Longitude coordinate")
    spot_type = models.CharField(max_length=20, choices=[
        ('track', 'Official Track'),
        ('street_meet', 'Street Meet Point'),
        ('parking_lot', 'Parking Lot'),
        ('industrial', 'Industrial Area'),
        ('other', 'Other'),
    ], help_text="Type of racing location")
    rules = models.TextField(blank=True, help_text="Specific rules for this location")
    amenities = models.TextField(blank=True, help_text="Available amenities")
    peak_hours = models.CharField(max_length=100, blank=True, help_text="Typical peak hours (e.g., 'Friday 8PM-12AM')")
    is_verified = models.BooleanField(default=False, help_text="Whether this is a verified official location")
    is_active = models.BooleanField(default=True, help_text="Whether this hot spot is currently active")
    total_races = models.IntegerField(default=0, help_text="Total number of races held here")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_hotspots')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.city}, {self.state}"

    class Meta:
        ordering = ['name']


class LocationBroadcast(models.Model):
    """Location broadcast model."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='location_broadcasts')
    location = models.CharField(max_length=200, help_text="Current location")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Latitude coordinate")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Longitude coordinate")
    message = models.TextField(blank=True, help_text="Optional message")
    is_active = models.BooleanField(default=True, help_text="Whether broadcast is active")
    expires_at = models.DateTimeField(help_text="When broadcast expires")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} at {self.location}"

    class Meta:
        ordering = ['-created_at']


class OpenChallenge(models.Model):
    """Open challenge model."""
    challenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='open_challenges_created')
    title = models.CharField(max_length=200, help_text="Challenge title")
    description = models.TextField(help_text="Challenge description")
    location = models.CharField(max_length=200, help_text="Challenge location")
    race_type = models.CharField(max_length=50, choices=[
        ('quarter_mile', 'Quarter Mile'),
        ('eighth_mile', 'Eighth Mile'),
        ('roll_race', 'Roll Race'),
        ('dig_race', 'Dig Race'),
        ('other', 'Other'),
    ], help_text="Type of race")
    wager_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Wager amount")
    max_respondents = models.IntegerField(blank=True, null=True, help_text="Maximum number of respondents")
    expires_at = models.DateTimeField(help_text="When challenge expires")
    is_active = models.BooleanField(default=True, help_text="Whether challenge is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.challenger.username}"

    class Meta:
        ordering = ['-created_at']


class ChallengeResponse(models.Model):
    """Challenge response model."""
    challenge = models.ForeignKey(OpenChallenge, on_delete=models.CASCADE, related_name='responses')
    respondent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='challenge_responses')
    message = models.TextField(blank=True, help_text="Response message")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending', help_text="Response status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.respondent.username} responds to {self.challenge.title}"

    class Meta:
        unique_together = ['challenge', 'respondent']
        ordering = ['created_at'] 