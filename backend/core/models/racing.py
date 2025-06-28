"""
Racing Models

This module contains models related to racing activities:
- Track: Racing track information
- Event: Racing events and meets
- Callout: Race challenges between users
- RaceResult: Results of completed races
- EventParticipant: Users participating in events
"""

from django.db import models
from django.conf import settings


class Track(models.Model):
    """Racing track model."""
    name = models.CharField(max_length=200, help_text="Track name")
    location = models.CharField(max_length=200, help_text="Track location")
    description = models.TextField(blank=True, help_text="Track description")
    track_type = models.CharField(max_length=50, choices=[
        ('drag', 'Drag Strip'),
        ('road_course', 'Road Course'),
        ('oval', 'Oval Track'),
        ('street', 'Street Circuit'),
    ], help_text="Type of track")
    surface_type = models.CharField(max_length=50, choices=[
        ('asphalt', 'Asphalt'),
        ('concrete', 'Concrete'),
        ('dirt', 'Dirt'),
        ('mixed', 'Mixed'),
    ], help_text="Track surface type")
    length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="Track length in miles")
    is_active = models.BooleanField(default=True, help_text="Whether track is currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


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
    """Race callout model."""
    challenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_callouts')
    challenged = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_callouts')
    location_type = models.CharField(max_length=20, choices=[
        ('track', 'Track'),
        ('street', 'Street'),
    ], help_text="Type of racing location")
    street_location = models.CharField(max_length=200, blank=True, help_text="Street location if applicable")
    race_type = models.CharField(max_length=50, choices=[
        ('quarter_mile', 'Quarter Mile'),
        ('eighth_mile', 'Eighth Mile'),
        ('roll_race', 'Roll Race'),
        ('dig_race', 'Dig Race'),
        ('heads_up', 'Heads Up'),
        ('bracket', 'Bracket Racing'),
    ], help_text="Type of race")
    wager_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Wager amount")
    message = models.TextField(blank=True, help_text="Callout message")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending', help_text="Callout status")
    scheduled_date = models.DateTimeField(blank=True, null=True, help_text="Scheduled race date")
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='won_races')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='callouts', blank=True, null=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='callouts', blank=True, null=True)
    
    # New privacy and visibility fields
    is_private = models.BooleanField(default=False, help_text="Whether callout is private (only visible to participants)")
    is_invite_only = models.BooleanField(default=False, help_text="Whether callout requires invitation approval")
    
    # New racing requirements fields
    max_horsepower = models.IntegerField(blank=True, null=True, help_text="Maximum horsepower requirement")
    min_horsepower = models.IntegerField(blank=True, null=True, help_text="Minimum horsepower requirement")
    tire_requirement = models.CharField(max_length=200, blank=True, help_text="Tire requirements for the race")
    rules = models.TextField(blank=True, help_text="Special rules or conditions for the race")
    experience_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('experienced', 'Experienced'),
        ('pro', 'Pro'),
    ], default='intermediate', help_text="Required experience level")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.challenger.username} vs {self.challenged.username}"

    class Meta:
        ordering = ['-created_at']


class RaceResult(models.Model):
    """Race result model."""
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='race_wins')
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='race_losses')
    winner_time = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, help_text="Winner's time")
    loser_time = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, help_text="Loser's time")
    winner_speed = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, help_text="Winner's speed")
    loser_speed = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, help_text="Loser's speed")
    completed_at = models.DateTimeField(auto_now_add=True, help_text="When race was completed")

    def __str__(self):
        return f"{self.winner.username} defeated {self.loser.username}"

    class Meta:
        ordering = ['-completed_at']


class EventParticipant(models.Model):
    """Event participant model."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_participations')
    registration_date = models.DateTimeField(auto_now_add=True, help_text="When user registered")
    is_confirmed = models.BooleanField(default=False, help_text="Whether participation is confirmed")

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

    class Meta:
        unique_together = ['event', 'user']
        ordering = ['registration_date'] 