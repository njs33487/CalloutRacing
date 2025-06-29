"""
Racing Models for CalloutRacing Application

This module contains models related to racing activities:
- Callout: Race challenges between users
- Track: Racing track information
- Event: Racing events and car meets
- RaceResult: Results from completed races
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Track(models.Model):
    """Racing track model."""
    TRACK_TYPES = [
        ('drag', 'Drag Strip'),
        ('road_course', 'Road Course'),
        ('oval', 'Oval Track'),
        ('street', 'Street Circuit'),
    ]
    
    SURFACE_TYPES = [
        ('asphalt', 'Asphalt'),
        ('concrete', 'Concrete'),
        ('dirt', 'Dirt'),
        ('mixed', 'Mixed'),
    ]
    
    name = models.CharField(max_length=200, help_text='Track name')
    location = models.CharField(max_length=200, help_text='Track location')
    description = models.TextField(blank=True, help_text='Track description')
    track_type = models.CharField(
        max_length=50, 
        choices=TRACK_TYPES, 
        help_text='Type of track'
    )
    surface_type = models.CharField(
        max_length=50, 
        choices=SURFACE_TYPES, 
        help_text='Track surface type'
    )
    length = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text='Track length in miles'
    )
    is_active = models.BooleanField(default=True, help_text='Whether track is currently active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Track"
        verbose_name_plural = "Tracks"
    
    def __str__(self):
        return f"{self.name} - {self.location}"


class Event(models.Model):
    """Racing event model."""
    title = models.CharField(max_length=200, help_text="Event title")
    description = models.TextField(help_text="Event description")
    event_type = models.CharField(max_length=50, choices=[
        ('race', 'Race Event'),
        ('meet', 'Car Meet'),
        ('show', 'Car Show'),
        ('test', 'Test & Tune'),
    ], help_text="Type of event")
    start_date = models.DateTimeField(help_text="Event start date and time")
    end_date = models.DateTimeField(help_text="Event end date and time")
    max_participants = models.IntegerField(blank=True, null=True, help_text="Maximum number of participants")
    entry_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Entry fee")
    is_public = models.BooleanField(default=True, help_text="Whether event is public")
    is_active = models.BooleanField(default=True, help_text="Whether event is active")
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']


class Callout(models.Model):
    """Callout (race challenge) model."""
    LOCATION_TYPES = [
        ('track', 'Track'),
        ('street', 'Street'),
    ]
    
    RACE_TYPES = [
        ('quarter_mile', 'Quarter Mile'),
        ('eighth_mile', 'Eighth Mile'),
        ('roll_race', 'Roll Race'),
        ('dig_race', 'Dig Race'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    EXPERIENCE_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('experienced', 'Experienced'),
        ('pro', 'Pro'),
    ]
    
    # Basic callout info
    challenger = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_callouts',
        help_text='User who sent the callout'
    )
    challenged = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_callouts',
        help_text='User who received the callout'
    )
    
    # Location details
    location_type = models.CharField(
        max_length=20, 
        choices=LOCATION_TYPES, 
        help_text='Type of racing location'
    )
    track = models.ForeignKey(
        Track, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='callouts',
        help_text='Track if location_type is track'
    )
    street_location = models.CharField(
        max_length=200, 
        blank=True, 
        help_text='Street location if location_type is street'
    )
    city = models.CharField(max_length=100, blank=True, help_text='City')
    state = models.CharField(max_length=50, blank=True, help_text='State')
    
    # Race details
    race_type = models.CharField(
        max_length=50, 
        choices=RACE_TYPES, 
        help_text='Type of race'
    )
    wager_amount = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=0, 
        help_text='Wager amount'
    )
    message = models.TextField(blank=True, help_text='Callout message')
    
    # Requirements and restrictions
    experience_level = models.CharField(
        max_length=20, 
        choices=EXPERIENCE_LEVELS, 
        default='intermediate', 
        help_text='Required experience level'
    )
    min_horsepower = models.IntegerField(
        blank=True, 
        null=True, 
        help_text='Minimum horsepower requirement'
    )
    max_horsepower = models.IntegerField(
        blank=True, 
        null=True, 
        help_text='Maximum horsepower requirement'
    )
    tire_requirement = models.CharField(
        max_length=200, 
        blank=True, 
        help_text='Tire requirements for the race'
    )
    rules = models.TextField(blank=True, help_text='Special rules or conditions for the race')
    
    # Privacy and access
    is_private = models.BooleanField(
        default=False, 
        help_text='Whether callout is private (only visible to participants)'
    )
    is_invite_only = models.BooleanField(
        default=False, 
        help_text='Whether callout requires invitation approval'
    )
    
    # Status and timing
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        help_text='Callout status'
    )
    scheduled_date = models.DateTimeField(
        blank=True, 
        null=True, 
        help_text='Scheduled race date'
    )
    
    # Results
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name='won_races',
        help_text='Winner of the race'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Callout"
        verbose_name_plural = "Callouts"
    
    def __str__(self):
        return f"{self.challenger.username} vs {self.challenged.username} - {self.race_type}"
    
    @property
    def location_display(self):
        """Get display name for location."""
        if self.location_type == 'track' and self.track:
            return f"{self.track.name} - {self.track.location}"
        elif self.street_location:
            return f"{self.street_location}, {self.city}, {self.state}"
        return "Location not specified"
    
    @property
    def is_expired(self):
        """Check if callout is expired (older than 7 days and not completed)."""
        from django.utils import timezone
        from datetime import timedelta
        if self.status in ['completed', 'cancelled']:
            return False
        return self.created_at < timezone.now() - timedelta(days=7)


class RaceResult(models.Model):
    """Race result model for completed races."""
    callout = models.OneToOneField(
        Callout, 
        on_delete=models.CASCADE, 
        related_name='race_result',
        help_text='Associated callout',
        null=True,  # Make nullable for migration
        blank=True
    )
    
    # Race times
    challenger_time = models.DecimalField(
        max_digits=6, 
        decimal_places=3, 
        blank=True, 
        null=True, 
        help_text='Challenger race time'
    )
    challenged_time = models.DecimalField(
        max_digits=6, 
        decimal_places=3, 
        blank=True, 
        null=True, 
        help_text='Challenged race time'
    )
    
    # Speeds
    challenger_speed = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text='Challenger speed (mph)'
    )
    challenged_speed = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text='Challenged speed (mph)'
    )
    
    # Reaction times
    challenger_reaction = models.DecimalField(
        max_digits=4, 
        decimal_places=3, 
        blank=True, 
        null=True, 
        help_text='Challenger reaction time'
    )
    challenged_reaction = models.DecimalField(
        max_digits=4, 
        decimal_places=3, 
        blank=True, 
        null=True, 
        help_text='Challenged reaction time'
    )
    
    # Additional details
    weather_conditions = models.CharField(
        max_length=100, 
        blank=True, 
        help_text='Weather conditions during race'
    )
    track_conditions = models.CharField(
        max_length=100, 
        blank=True, 
        help_text='Track conditions during race'
    )
    notes = models.TextField(blank=True, help_text='Additional race notes')
    
    # Verification
    is_verified = models.BooleanField(
        default=False, 
        help_text='Whether race result is verified'
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name='verified_races',
        help_text='User who verified the result'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Race Result"
        verbose_name_plural = "Race Results"
    
    def __str__(self):
        return f"Race Result: {self.callout}"
    
    @property
    def winner(self):
        """Determine winner based on times."""
        if not self.challenger_time or not self.challenged_time:
            return None
        
        if self.challenger_time < self.challenged_time:
            return self.callout.challenger
        elif self.challenged_time < self.challenger_time:
            return self.callout.challenged
        return None  # Tie


class EventParticipant(models.Model):
    """Event participant model."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_participations')
    registration_date = models.DateTimeField(auto_now_add=True, help_text="When user registered")
    is_confirmed = models.BooleanField(default=False, help_text="Whether participation is confirmed")

    def __str__(self):
        return f"{self.user} - {self.event}"

    class Meta:
        unique_together = ['event', 'user']
        ordering = ['registration_date'] 