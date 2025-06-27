"""
Django Models for CalloutRacing Application

This module contains all the database models for the CalloutRacing application, including:
- User profiles and authentication
- Racing events, tracks, and callouts
- Marketplace functionality
- Social features (friends, messages, posts)
- Car profiles and modifications

All models use Django's ORM and include proper relationships, validations, and metadata.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class UserProfile(models.Model):
    """
    Extended user profile for racers.
    
    This model extends the default Django User model with racing-specific information
    including car details, race statistics, and profile images.
    """
    # One-to-one relationship with Django User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal information
    bio = models.TextField(max_length=500, blank=True, help_text="User's biography or description")
    location = models.CharField(max_length=100, blank=True, help_text="User's location (city, state)")
    
    # Current car information
    car_make = models.CharField(max_length=50, blank=True, help_text="Make of user's current car")
    car_model = models.CharField(max_length=50, blank=True, help_text="Model of user's current car")
    car_year = models.IntegerField(blank=True, null=True, help_text="Year of user's current car")
    car_mods = models.TextField(blank=True, help_text="Modifications on user's current car")
    
    # Profile images
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, help_text="User's profile picture")
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True, help_text="User's cover photo")
    
    # Race statistics
    wins = models.IntegerField(default=0, help_text="Number of races won")
    losses = models.IntegerField(default=0, help_text="Number of races lost")
    total_races = models.IntegerField(default=0, help_text="Total number of races participated in")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the profile was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the profile was last updated")

    def __str__(self):
        """String representation of the user profile."""
        return f"{self.user.username}'s Profile"

    @property
    def win_rate(self):
        """
        Calculate the user's win rate as a percentage.
        
        Returns:
            float: Win rate percentage (0-100), or 0 if no races completed
        """
        if self.total_races == 0:
            return 0
        return (self.wins / self.total_races) * 100


class Track(models.Model):
    """
    Racing tracks and facilities.
    
    This model stores information about racing tracks where events can be held,
    including track type, surface, and location details.
    """
    # Basic information
    name = models.CharField(max_length=100, help_text="Name of the racing track")
    location = models.CharField(max_length=200, help_text="Location of the track (city, state)")
    description = models.TextField(blank=True, help_text="Detailed description of the track")
    
    # Track specifications
    track_type = models.CharField(max_length=50, choices=[
        ('drag', 'Drag Strip'),
        ('road', 'Road Course'),
        ('oval', 'Oval Track'),
    ], help_text="Type of racing track")
    
    surface_type = models.CharField(max_length=50, choices=[
        ('asphalt', 'Asphalt'),
        ('concrete', 'Concrete'),
        ('dirt', 'Dirt'),
    ], help_text="Surface material of the track")
    
    length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="Track length in miles")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Whether the track is currently active")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the track was added")

    def __str__(self):
        """String representation of the track."""
        return self.name


class Event(models.Model):
    """
    Racing events and competitions.
    
    This model represents racing events that users can participate in,
    including races, car meets, shows, and test & tune sessions.
    """
    # Basic information
    title = models.CharField(max_length=200, help_text="Title of the event")
    description = models.TextField(help_text="Detailed description of the event")
    
    # Event details
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='events', help_text="Track where the event is held")
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events', help_text="User organizing the event")
    
    event_type = models.CharField(max_length=50, choices=[
        ('race', 'Race Event'),
        ('meet', 'Car Meet'),
        ('show', 'Car Show'),
        ('test', 'Test & Tune'),
    ], help_text="Type of event")
    
    # Timing
    start_date = models.DateTimeField(help_text="When the event starts")
    end_date = models.DateTimeField(help_text="When the event ends")
    
    # Participation
    max_participants = models.IntegerField(blank=True, null=True, help_text="Maximum number of participants allowed")
    entry_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Entry fee for the event")
    
    # Visibility and status
    is_public = models.BooleanField(default=True, help_text="Whether the event is public or private")
    is_active = models.BooleanField(default=True, help_text="Whether the event is currently active")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the event was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the event was last updated")

    def __str__(self):
        """String representation of the event."""
        return self.title

    @property
    def is_upcoming(self):
        """
        Check if the event is in the future.
        
        Returns:
            bool: True if event hasn't started yet
        """
        return self.start_date > timezone.now()

    @property
    def is_ongoing(self):
        """
        Check if the event is currently happening.
        
        Returns:
            bool: True if event is currently in progress
        """
        now = timezone.now()
        return self.start_date <= now <= self.end_date


class Callout(models.Model):
    """
    Race callouts between users.
    
    This model represents challenges between users for races, including
    track or street races with optional wagers.
    """
    # Participants
    challenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_callouts', help_text="User sending the challenge")
    challenged = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_callouts', help_text="User receiving the challenge")
    
    # Event and location
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='callouts', blank=True, null=True, help_text="Associated event (optional)")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='callouts', blank=True, null=True, help_text="Track for the race (optional)")
    
    location_type = models.CharField(max_length=20, choices=[
        ('track', 'Track'),
        ('street', 'Street'),
    ], help_text="Type of location for the race")
    
    street_location = models.CharField(max_length=200, blank=True, help_text="Street location for street races")
    
    # Race details
    race_type = models.CharField(max_length=50, choices=[
        ('quarter_mile', 'Quarter Mile'),
        ('eighth_mile', 'Eighth Mile'),
        ('roll_race', 'Roll Race'),
        ('dig_race', 'Dig Race'),
    ], help_text="Type of race")
    
    wager_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Amount wagered on the race")
    message = models.TextField(blank=True, help_text="Message from challenger to challenged")
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending', help_text="Current status of the callout")
    
    scheduled_date = models.DateTimeField(blank=True, null=True, help_text="When the race is scheduled")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='won_races', help_text="Winner of the race (if completed)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the callout was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the callout was last updated")

    def __str__(self):
        """String representation of the callout."""
        return f"{self.challenger.username} vs {self.challenged.username}"

    class Meta:
        ordering = ['-created_at']  # Most recent first


class RaceResult(models.Model):
    """
    Results of completed races.
    
    This model stores detailed results from completed races, including
    times, speeds, and other performance metrics.
    """
    # Race reference
    callout = models.OneToOneField(Callout, on_delete=models.CASCADE, related_name='result', help_text="Associated callout")
    
    # Participants
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='race_wins', help_text="Winner of the race")
    loser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='race_losses', help_text="Loser of the race")
    
    # Performance metrics
    winner_time = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, help_text="Winner's race time")
    loser_time = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, help_text="Loser's race time")
    winner_speed = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, help_text="Winner's trap speed")
    loser_speed = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, help_text="Loser's trap speed")
    
    # Additional information
    notes = models.TextField(blank=True, help_text="Additional notes about the race")
    completed_at = models.DateTimeField(auto_now_add=True, help_text="When the race was completed")

    def __str__(self):
        """String representation of the race result."""
        return f"{self.winner.username} defeated {self.loser.username}"


class Marketplace(models.Model):
    """
    Marketplace for buying, selling, and trading.
    
    This model represents items listed for sale in the marketplace,
    including cars, parts, tools, and other racing-related items.
    """
    # Seller information
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marketplace_items', help_text="User selling the item")
    
    # Item details
    title = models.CharField(max_length=200, help_text="Title of the item")
    description = models.TextField(help_text="Detailed description of the item")
    
    category = models.CharField(max_length=50, choices=[
        ('car', 'Car'),
        ('parts', 'Parts'),
        ('wheels', 'Wheels & Tires'),
        ('electronics', 'Electronics'),
        ('tools', 'Tools'),
        ('other', 'Other'),
    ], help_text="Category of the item")
    
    condition = models.CharField(max_length=20, choices=[
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ], help_text="Condition of the item")
    
    # Pricing and negotiation
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the item")
    is_negotiable = models.BooleanField(default=True, help_text="Whether the price is negotiable")
    trade_offered = models.BooleanField(default=False, help_text="Whether trade offers are accepted")
    trade_description = models.TextField(blank=True, help_text="Description of what trades are accepted")
    
    # Location and contact
    location = models.CharField(max_length=200, help_text="Location of the item")
    contact_phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    contact_email = models.EmailField(blank=True, help_text="Contact email address")
    
    # Status and metrics
    is_active = models.BooleanField(default=True, help_text="Whether the listing is active")
    views = models.IntegerField(default=0, help_text="Number of times the listing has been viewed")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the listing was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the listing was last updated")

    def __str__(self):
        """String representation of the marketplace item."""
        return self.title

    class Meta:
        ordering = ['-created_at']  # Most recent first


class MarketplaceImage(models.Model):
    """
    Images for marketplace items.
    
    This model stores images associated with marketplace listings,
    with support for primary images and multiple images per item.
    """
    marketplace_item = models.ForeignKey(Marketplace, on_delete=models.CASCADE, related_name='images', help_text="Associated marketplace item")
    image = models.ImageField(upload_to='marketplace_images/', help_text="Image file")
    is_primary = models.BooleanField(default=False, help_text="Whether this is the primary image for the item")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the image was uploaded")

    def __str__(self):
        """String representation of the marketplace image."""
        return f"Image for {self.marketplace_item.title}"


class EventParticipant(models.Model):
    """
    Participants in events.
    
    This model tracks which users are participating in which events,
    including registration information and car details.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants', help_text="Event being participated in")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_participations', help_text="User participating in the event")
    car_info = models.TextField(blank=True, help_text="Information about the car being used")
    registration_date = models.DateTimeField(auto_now_add=True, help_text="When the user registered for the event")
    is_confirmed = models.BooleanField(default=False, help_text="Whether participation is confirmed")

    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class Friendship(models.Model):
    """Friendship between users"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('blocked', 'Blocked'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['sender', 'receiver']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"


class Message(models.Model):
    """Direct messages between users"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.content[:50]}"


class CarProfile(models.Model):
    """Detailed car profiles for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField(max_length=100)  # e.g., "My Daily Driver", "Race Car"
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    trim = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)
    vin = models.CharField(max_length=17, blank=True)
    
    # Engine specs
    engine_size = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)  # in liters
    engine_type = models.CharField(max_length=50, blank=True)  # e.g., "V8", "Inline-4", "V6"
    fuel_type = models.CharField(max_length=20, choices=[
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ], default='gasoline')
    
    # Performance specs
    horsepower = models.IntegerField(blank=True, null=True)
    torque = models.IntegerField(blank=True, null=True)  # lb-ft
    weight = models.IntegerField(blank=True, null=True)  # lbs
    transmission = models.CharField(max_length=50, blank=True)
    drivetrain = models.CharField(max_length=20, choices=[
        ('fwd', 'Front-Wheel Drive'),
        ('rwd', 'Rear-Wheel Drive'),
        ('awd', 'All-Wheel Drive'),
        ('4wd', 'Four-Wheel Drive'),
    ], blank=True)
    
    # Racing stats
    best_quarter_mile = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    best_eighth_mile = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    best_trap_speed = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    
    # Description and photos
    description = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)  # User's main car
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"{self.user.username}'s {self.year} {self.make} {self.model}"


class CarModification(models.Model):
    """Modifications for car profiles"""
    CATEGORY_CHOICES = [
        ('engine', 'Engine'),
        ('exhaust', 'Exhaust'),
        ('intake', 'Intake'),
        ('turbo', 'Turbo/Supercharger'),
        ('suspension', 'Suspension'),
        ('wheels', 'Wheels & Tires'),
        ('brakes', 'Brakes'),
        ('interior', 'Interior'),
        ('exterior', 'Exterior'),
        ('electronics', 'Electronics'),
        ('other', 'Other'),
    ]
    
    car = models.ForeignKey(CarProfile, on_delete=models.CASCADE, related_name='modifications')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    part_number = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    installed_date = models.DateField(blank=True, null=True)
    is_installed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-installed_date', '-created_at']

    def __str__(self):
        return f"{self.car} - {self.name}"


class CarImage(models.Model):
    """Images for car profiles"""
    car = models.ForeignKey(CarProfile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"Image for {self.car}"


class UserPost(models.Model):
    """User posts/status updates"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    car = models.ForeignKey(CarProfile, on_delete=models.CASCADE, blank=True, null=True, related_name='posts')
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

    @property
    def like_count(self):
        return self.likes.count()


class PostComment(models.Model):
    """Comments on user posts"""
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username} on {self.post}: {self.content[:30]}" 