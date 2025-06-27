from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile for racers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    car_make = models.CharField(max_length=50, blank=True)
    car_model = models.CharField(max_length=50, blank=True)
    car_year = models.IntegerField(blank=True, null=True)
    car_mods = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    total_races = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def win_rate(self):
        if self.total_races == 0:
            return 0
        return (self.wins / self.total_races) * 100


class Track(models.Model):
    """Racing tracks"""
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    track_type = models.CharField(max_length=50, choices=[
        ('drag', 'Drag Strip'),
        ('road', 'Road Course'),
        ('oval', 'Oval Track'),
    ])
    surface_type = models.CharField(max_length=50, choices=[
        ('asphalt', 'Asphalt'),
        ('concrete', 'Concrete'),
        ('dirt', 'Dirt'),
    ])
    length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # in miles
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    """Racing events"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    event_type = models.CharField(max_length=50, choices=[
        ('race', 'Race Event'),
        ('meet', 'Car Meet'),
        ('show', 'Car Show'),
        ('test', 'Test & Tune'),
    ])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_participants = models.IntegerField(blank=True, null=True)
    entry_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_public = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.start_date > timezone.now()

    @property
    def is_ongoing(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date


class Callout(models.Model):
    """Race callouts between users"""
    challenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_callouts')
    challenged = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_callouts')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='callouts', blank=True, null=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='callouts', blank=True, null=True)
    location_type = models.CharField(max_length=20, choices=[
        ('track', 'Track'),
        ('street', 'Street'),
    ])
    street_location = models.CharField(max_length=200, blank=True)  # For street races
    race_type = models.CharField(max_length=50, choices=[
        ('quarter_mile', 'Quarter Mile'),
        ('eighth_mile', 'Eighth Mile'),
        ('roll_race', 'Roll Race'),
        ('dig_race', 'Dig Race'),
    ])
    wager_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    scheduled_date = models.DateTimeField(blank=True, null=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='won_races')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.challenger.username} vs {self.challenged.username}"

    class Meta:
        ordering = ['-created_at']


class RaceResult(models.Model):
    """Results of completed races"""
    callout = models.OneToOneField(Callout, on_delete=models.CASCADE, related_name='result')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='race_wins')
    loser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='race_losses')
    winner_time = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    loser_time = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    winner_speed = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    loser_speed = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.winner.username} defeated {self.loser.username}"


class Marketplace(models.Model):
    """Marketplace for buying/selling/trading"""
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marketplace_items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('car', 'Car'),
        ('parts', 'Parts'),
        ('wheels', 'Wheels & Tires'),
        ('electronics', 'Electronics'),
        ('tools', 'Tools'),
        ('other', 'Other'),
    ])
    condition = models.CharField(max_length=20, choices=[
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_negotiable = models.BooleanField(default=True)
    trade_offered = models.BooleanField(default=False)
    trade_description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class MarketplaceImage(models.Model):
    """Images for marketplace items"""
    marketplace_item = models.ForeignKey(Marketplace, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='marketplace_images/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.marketplace_item.title}"


class EventParticipant(models.Model):
    """Participants in events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_participations')
    car_info = models.TextField(blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

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