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
from django.db import models  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from django.core.validators import MinValueValidator, MaxValueValidator  # type: ignore
from django.utils import timezone  # type: ignore


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
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']


class Callout(models.Model):
    """Race callout model."""
    challenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_callouts')
    challenged = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_callouts')
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
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='won_races')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='callouts', blank=True, null=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='callouts', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.challenger.username} vs {self.challenged.username}"

    class Meta:
        ordering = ['-created_at']


class RaceResult(models.Model):
    """Race result model."""
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='race_wins')
    loser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='race_losses')
    winner_time = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, help_text="Winner's time")
    loser_time = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, help_text="Loser's time")
    winner_speed = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, help_text="Winner's speed")
    loser_speed = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, help_text="Loser's speed")
    completed_at = models.DateTimeField(auto_now_add=True, help_text="When race was completed")

    def __str__(self):
        return f"{self.winner.username} defeated {self.loser.username}"

    class Meta:
        ordering = ['-completed_at']


class Marketplace(models.Model):
    """Marketplace listing model."""
    title = models.CharField(max_length=200, help_text="Listing title")
    description = models.TextField(help_text="Listing description")
    category = models.CharField(max_length=50, choices=[
        ('car', 'Car'),
        ('parts', 'Parts'),
        ('wheels', 'Wheels & Tires'),
        ('electronics', 'Electronics'),
        ('tools', 'Tools'),
        ('other', 'Other'),
    ], help_text="Listing category")
    condition = models.CharField(max_length=20, choices=[
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ], help_text="Item condition")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Item price")
    is_negotiable = models.BooleanField(default=True, help_text="Whether price is negotiable")
    trade_offered = models.BooleanField(default=False, help_text="Whether trade is offered")
    trade_description = models.TextField(blank=True, help_text="Trade description")
    location = models.CharField(max_length=200, help_text="Item location")
    contact_phone = models.CharField(max_length=20, blank=True, help_text="Contact phone")
    contact_email = models.EmailField(blank=True, help_text="Contact email")
    is_active = models.BooleanField(default=True, help_text="Whether listing is active")
    views = models.IntegerField(default=0, help_text="Number of views")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marketplace_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class MarketplaceImage(models.Model):
    """Marketplace image model."""
    marketplace_item = models.ForeignKey(Marketplace, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='marketplace_images/', help_text="Item image")
    caption = models.CharField(max_length=200, blank=True, help_text="Image caption")
    is_primary = models.BooleanField(default=False, help_text="Whether this is the primary image")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.marketplace_item.title}"

    class Meta:
        ordering = ['-is_primary', '-created_at']


class EventParticipant(models.Model):
    """Event participant model."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_participations')
    registration_date = models.DateTimeField(auto_now_add=True, help_text="When user registered")
    is_confirmed = models.BooleanField(default=False, help_text="Whether participation is confirmed")

    def __str__(self):
        return f"{self.user.username} in {self.event.title}"

    class Meta:
        unique_together = ['event', 'user']
        ordering = ['registration_date']


class Friendship(models.Model):
    """Friendship model."""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_received')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('blocked', 'Blocked'),
    ], default='pending', help_text="Friendship status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"

    class Meta:
        unique_together = ['sender', 'receiver']
        ordering = ['-created_at']


class Message(models.Model):
    """Message model."""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(help_text="Message content")
    is_read = models.BooleanField(default=False, help_text="Whether message has been read")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}"

    class Meta:
        ordering = ['created_at']


class CarProfile(models.Model):
    """Car profile model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField(max_length=100, help_text="Car name")
    make = models.CharField(max_length=50, help_text="Car make")
    model = models.CharField(max_length=50, help_text="Car model")
    year = models.IntegerField(help_text="Car year")
    trim = models.CharField(max_length=100, blank=True, help_text="Car trim")
    color = models.CharField(max_length=50, blank=True, help_text="Car color")
    vin = models.CharField(max_length=17, blank=True, help_text="Vehicle identification number")
    engine_size = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Engine size in liters")
    engine_type = models.CharField(max_length=50, blank=True, help_text="Engine type")
    fuel_type = models.CharField(max_length=20, choices=[
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ], default='gasoline', help_text="Fuel type")
    horsepower = models.IntegerField(blank=True, null=True, help_text="Horsepower")
    torque = models.IntegerField(blank=True, null=True, help_text="Torque")
    weight = models.IntegerField(blank=True, null=True, help_text="Weight in pounds")
    transmission = models.CharField(max_length=50, blank=True, help_text="Transmission type")
    drivetrain = models.CharField(max_length=20, choices=[
        ('fwd', 'Front-Wheel Drive'),
        ('rwd', 'Rear-Wheel Drive'),
        ('awd', 'All-Wheel Drive'),
        ('4wd', 'Four-Wheel Drive'),
    ], blank=True, help_text="Drivetrain type")
    best_quarter_mile = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, help_text="Best quarter mile time")
    best_eighth_mile = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, help_text="Best eighth mile time")
    best_trap_speed = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, help_text="Best trap speed")
    description = models.TextField(blank=True, help_text="Car description")
    is_primary = models.BooleanField(default=False, help_text="Whether this is the primary car")
    is_active = models.BooleanField(default=True, help_text="Whether car profile is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.user.username}"

    class Meta:
        ordering = ['-is_primary', '-created_at']


class CarModification(models.Model):
    """Car modification model."""
    car = models.ForeignKey(CarProfile, on_delete=models.CASCADE, related_name='modifications')
    category = models.CharField(max_length=20, choices=[
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
    ], help_text="Modification category")
    name = models.CharField(max_length=200, help_text="Modification name")
    brand = models.CharField(max_length=100, blank=True, help_text="Brand name")
    part_number = models.CharField(max_length=100, blank=True, help_text="Part number")
    description = models.TextField(blank=True, help_text="Modification description")
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="Modification cost")
    installed_date = models.DateField(blank=True, null=True, help_text="Installation date")
    is_installed = models.BooleanField(default=True, help_text="Whether modification is installed")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car} - {self.name}"

    class Meta:
        ordering = ['-installed_date', '-created_at']


class CarImage(models.Model):
    """Car image model."""
    car = models.ForeignKey(CarProfile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/', help_text="Car image")
    caption = models.CharField(max_length=200, blank=True, help_text="Image caption")
    is_primary = models.BooleanField(default=False, help_text="Whether this is the primary image")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car}"

    class Meta:
        ordering = ['-is_primary', '-created_at']


class UserPost(models.Model):
    """User post model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(help_text="Post content")
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, help_text="Post image")
    car = models.ForeignKey(CarProfile, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.user.username}"

    @property
    def like_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']


class PostComment(models.Model):
    """Post comment model."""
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField(help_text="Comment content")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"

    class Meta:
        ordering = ['created_at']


class Subscription(models.Model):
    """Subscription model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscription_type = models.CharField(max_length=20, choices=[
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('pro', 'Pro'),
    ], help_text="Subscription type")
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ], default='active', help_text="Subscription status")
    start_date = models.DateTimeField(auto_now_add=True, help_text="Subscription start date")
    end_date = models.DateTimeField(blank=True, null=True, help_text="Subscription end date")
    next_billing_date = models.DateTimeField(blank=True, null=True, help_text="Next billing date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type}"

    class Meta:
        ordering = ['-created_at']


class Payment(models.Model):
    """Payment model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=[
        ('subscription', 'Subscription'),
        ('marketplace', 'Marketplace'),
        ('betting', 'Betting'),
        ('other', 'Other'),
    ], help_text="Payment type")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Payment amount")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ], default='pending', help_text="Payment status")
    payment_provider = models.CharField(max_length=50, blank=True, help_text="Payment provider")
    transaction_id = models.CharField(max_length=100, blank=True, help_text="Transaction ID")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.status})"

    class Meta:
        ordering = ['-created_at']


class UserWallet(models.Model):
    """User wallet model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Wallet balance")
    is_active = models.BooleanField(default=True, help_text="Whether wallet is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s wallet"

    class Meta:
        ordering = ['-updated_at']


class MarketplaceOrder(models.Model):
    """Marketplace order model."""
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    item = models.ForeignKey(Marketplace, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField(default=1, help_text="Order quantity")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total order amount")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='pending', help_text="Order status")
    shipping_address = models.TextField(blank=True, help_text="Shipping address")
    tracking_number = models.CharField(max_length=100, blank=True, help_text="Tracking number")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.buyer.username} -> {self.seller.username}"

    class Meta:
        ordering = ['-created_at']


class MarketplaceReview(models.Model):
    """Marketplace review model."""
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marketplace_reviews')
    order = models.OneToOneField(MarketplaceOrder, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Review rating")
    title = models.CharField(max_length=200, help_text="Review title")
    comment = models.TextField(help_text="Review comment")
    is_verified_purchase = models.BooleanField(default=True, help_text="Whether this is a verified purchase")
    helpful_votes = models.IntegerField(default=0, help_text="Number of helpful votes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.order}"

    class Meta:
        ordering = ['-created_at']


class Bet(models.Model):
    """Bet model."""
    bettor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bets')
    bet_type = models.CharField(max_length=20, choices=[
        ('callout', 'Callout'),
        ('event', 'Event'),
        ('other', 'Other'),
    ], help_text="Bet type")
    bet_amount = models.DecimalField(max_digits=8, decimal_places=2, help_text="Bet amount")
    odds = models.DecimalField(max_digits=5, decimal_places=2, help_text="Betting odds")
    potential_payout = models.DecimalField(max_digits=8, decimal_places=2, help_text="Potential payout")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('cancelled', 'Cancelled'),
    ], default='pending', help_text="Bet status")
    callout = models.ForeignKey(Callout, on_delete=models.CASCADE, related_name='bets', blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bets', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bettor.username} - {self.bet_amount} ({self.status})"

    class Meta:
        ordering = ['-created_at']


class BettingPool(models.Model):
    """Betting pool model."""
    name = models.CharField(max_length=200, help_text="Pool name")
    description = models.TextField(blank=True, help_text="Pool description")
    total_pool = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Total pool amount")
    is_active = models.BooleanField(default=True, help_text="Whether pool is active")
    is_settled = models.BooleanField(default=False, help_text="Whether pool is settled")
    callout = models.ForeignKey(Callout, on_delete=models.CASCADE, related_name='betting_pools', blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='betting_pools', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Notification(models.Model):
    """Notification model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=[
        ('callout', 'Callout'),
        ('friend_request', 'Friend Request'),
        ('message', 'Message'),
        ('event', 'Event'),
        ('marketplace', 'Marketplace'),
        ('other', 'Other'),
    ], help_text="Notification type")
    title = models.CharField(max_length=200, help_text="Notification title")
    message = models.TextField(help_text="Notification message")
    is_read = models.BooleanField(default=False, help_text="Whether notification is read")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        ordering = ['-created_at']


# --- Advanced Racing Features Models ---

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_hotspots')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class RacingCrew(models.Model):
    """Racing crew model."""
    name = models.CharField(max_length=200, help_text="Crew name")
    description = models.TextField(help_text="Crew description")
    logo = models.ImageField(upload_to='crew_logos/', blank=True, null=True, help_text="Crew logo")
    location = models.CharField(max_length=200, help_text="Crew location")
    founded_date = models.DateField(blank=True, null=True, help_text="When the crew was founded")
    is_public = models.BooleanField(default=True, help_text="Whether crew is public")
    is_verified = models.BooleanField(default=False, help_text="Whether crew is verified")
    member_count = models.IntegerField(default=0, help_text="Number of members")
    max_members = models.IntegerField(blank=True, null=True, help_text="Maximum number of members")
    requirements = models.TextField(blank=True, help_text="Requirements to join")
    rules = models.TextField(blank=True, help_text="Crew rules")
    website = models.URLField(blank=True, help_text="Crew website")
    social_media = models.JSONField(default=dict, blank=True, help_text="Social media links")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_crews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CrewMembership(models.Model):
    """Crew membership model."""
    crew = models.ForeignKey(RacingCrew, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crew_memberships')
    role = models.CharField(max_length=50, choices=[
        ('member', 'Member'),
        ('officer', 'Officer'),
        ('leader', 'Leader'),
        ('founder', 'Founder'),
    ], default='member', help_text="Member role")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('banned', 'Banned'),
    ], default='pending', help_text="Membership status")
    joined_date = models.DateTimeField(auto_now_add=True, help_text="When member joined")
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='crew_invitations_sent')
    notes = models.TextField(blank=True, help_text="Admin notes")

    def __str__(self):
        return f"{self.user.username} in {self.crew.name}"

    class Meta:
        unique_together = ['crew', 'user']
        ordering = ['joined_date']


class LocationBroadcast(models.Model):
    """Location broadcast model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='location_broadcasts')
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


class ReputationRating(models.Model):
    """Reputation rating model."""
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received')
    callout = models.ForeignKey(Callout, on_delete=models.CASCADE, related_name='ratings', blank=True, null=True)
    punctuality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Punctuality rating (1-5)")
    rule_adherence = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Rule adherence rating (1-5)")
    sportsmanship = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Sportsmanship rating (1-5)")
    overall = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Overall rating (1-5)")
    comment = models.TextField(blank=True, help_text="Optional comment about the experience")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rater.username} rated {self.rated_user.username}"

    class Meta:
        unique_together = ['rater', 'rated_user', 'callout']
        ordering = ['-created_at']


class OpenChallenge(models.Model):
    """Open challenge model."""
    challenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='open_challenges_created')
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
        return f"{self.challenger.username} - {self.title}"

    class Meta:
        ordering = ['-created_at']


class ChallengeResponse(models.Model):
    """Challenge response model."""
    challenge = models.ForeignKey(OpenChallenge, on_delete=models.CASCADE, related_name='responses')
    respondent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_responses')
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
        return f"{self.respondent.username} responded to {self.challenge.title}"

    class Meta:
        unique_together = ['challenge', 'respondent']
        ordering = ['created_at']


# --- End Advanced Racing Features Models ---

# --- Build Showcase Models ---

class BuildLog(models.Model):
    car = models.ForeignKey('CarProfile', on_delete=models.CASCADE, related_name='build_logs')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)
    start_date = models.DateField()
    completion_date = models.DateField(blank=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    target_horsepower = models.IntegerField(blank=True, null=True)
    target_quarter_mile = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    is_public = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    allow_ratings = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_builds', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.car} - {self.title}"
    
    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def progress_percentage(self):
        milestones = self.milestones.all()
        if not milestones:
            return 0
        completed = milestones.filter(is_complete=True).count()
        return (completed / milestones.count()) * 100
    
    class Meta:
        ordering = ['-updated_at']


class BuildMilestone(models.Model):
    build_log = models.ForeignKey(BuildLog, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50)
    is_complete = models.BooleanField(default=False)
    start_date = models.DateField()
    completion_date = models.DateField(blank=True, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    hours_spent = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    horsepower_gain = models.IntegerField(blank=True, null=True)
    torque_gain = models.IntegerField(blank=True, null=True)
    weight_change = models.IntegerField(blank=True, null=True)
    parts_used = models.TextField(blank=True)
    part_numbers = models.TextField(blank=True)
    difficulty_level = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.build_log.title} - {self.title}"
    
    class Meta:
        ordering = ['start_date']


class BuildMedia(models.Model):
    MEDIA_TYPES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
    ]
    build_log = models.ForeignKey(BuildLog, on_delete=models.CASCADE, related_name='media', blank=True, null=True)
    milestone = models.ForeignKey(BuildMilestone, on_delete=models.CASCADE, related_name='media', blank=True, null=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='build_media/')
    thumbnail = models.ImageField(upload_to='build_thumbnails/', blank=True, null=True)
    title = models.CharField(max_length=200, blank=True)
    caption = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)
    file_size = models.IntegerField(blank=True, null=True)
    duration = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_media_type_display()} - {self.title or self.file.name}"
    
    class Meta:
        ordering = ['-created_at']


class CarTour(models.Model):
    car = models.ForeignKey('CarProfile', on_delete=models.CASCADE, related_name='tours')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tour_type = models.CharField(max_length=20)
    primary_media = models.FileField(upload_to='car_tours/')
    thumbnail = models.ImageField(upload_to='tour_thumbnails/', blank=True, null=True)
    is_public = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_tours', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.car} - {self.title}"
    
    @property
    def like_count(self):
        return self.likes.count()
    
    class Meta:
        ordering = ['-created_at']


class PerformanceData(models.Model):
    car = models.ForeignKey('CarProfile', on_delete=models.CASCADE, related_name='performance_data')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    test_type = models.CharField(max_length=20)
    test_date = models.DateField()
    track = models.CharField(max_length=200, blank=True)
    weather_conditions = models.CharField(max_length=200, blank=True)
    horsepower = models.IntegerField(blank=True, null=True)
    torque = models.IntegerField(blank=True, null=True)
    rpm_hp_peak = models.IntegerField(blank=True, null=True)
    rpm_torque_peak = models.IntegerField(blank=True, null=True)
    quarter_mile_time = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    quarter_mile_speed = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    sixty_foot_time = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
    three_thirty_time = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    eighth_mile_time = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    eighth_mile_speed = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    fuel_type = models.CharField(max_length=50, blank=True)
    tire_type = models.CharField(max_length=100, blank=True)
    dyno_sheet = models.ImageField(upload_to='dyno_sheets/', blank=True, null=True)
    time_slip = models.ImageField(upload_to='time_slips/', blank=True, null=True)
    video = models.FileField(upload_to='performance_videos/', blank=True, null=True)
    notes = models.TextField(blank=True)
    modifications = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='verified_performance_data')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.car} - {self.title} ({self.test_type})"
    
    class Meta:
        ordering = ['-test_date']


class BuildWishlist(models.Model):
    build_log = models.ForeignKey(BuildLog, on_delete=models.CASCADE, related_name='wishlist_items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=100, blank=True)
    part_number = models.CharField(max_length=100, blank=True)
    estimated_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    priority = models.CharField(max_length=20, default='medium')
    is_public = models.BooleanField(default=True)
    is_acquired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.build_log.title} - {self.title}"
    
    class Meta:
        ordering = ['priority', '-created_at']


class WishlistSuggestion(models.Model):
    wishlist_item = models.ForeignKey(BuildWishlist, on_delete=models.CASCADE, related_name='suggestions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_suggestions_given')
    suggestion = models.TextField()
    alternative_part = models.CharField(max_length=200, blank=True)
    price_info = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=200, blank=True)
    is_helpful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Suggestion for {self.wishlist_item.title} by {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']


class BuildRating(models.Model):
    build_log = models.ForeignKey(BuildLog, on_delete=models.CASCADE, related_name='ratings')
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='build_ratings_given')
    creativity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    execution = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    documentation = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    performance = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    overall = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Rating for {self.build_log.title} by {self.rater.username}"
    
    class Meta:
        unique_together = ['build_log', 'rater']
        ordering = ['-created_at']


class BuildComment(models.Model):
    build_log = models.ForeignKey(BuildLog, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    milestone = models.ForeignKey(BuildMilestone, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    tour = models.ForeignKey(CarTour, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='build_comments')
    content = models.TextField()
    comment_type = models.CharField(max_length=20, default='general')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    is_approved = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_build_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.get_content_object()}"
    
    def get_content_object(self):
        if self.build_log:
            return self.build_log.title
        elif self.milestone:
            return self.milestone.title
        elif self.tour:
            return self.tour.title
        return "Unknown"
    
    @property
    def like_count(self):
        return self.likes.count()
    
    class Meta:
        ordering = ['created_at']


class BuildBadge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badge_icons/')
    criteria = models.TextField()
    badge_type = models.CharField(max_length=20)
    is_automatic = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class BuildBadgeAward(models.Model):
    build_log = models.ForeignKey(BuildLog, on_delete=models.CASCADE, related_name='badge_awards')
    badge = models.ForeignKey(BuildBadge, on_delete=models.CASCADE, related_name='awards')
    awarded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges_awarded')
    awarded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.badge.name} awarded to {self.build_log.title}"
    
    class Meta:
        unique_together = ['build_log', 'badge']
        ordering = ['-awarded_at']


# --- End Build Showcase Models ---

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100, help_text="Contact person's name")
    email = models.EmailField(help_text="Contact person's email")
    subject = models.CharField(max_length=200, help_text="Subject of the inquiry")
    message = models.TextField(help_text="Contact message content")
    is_reviewed = models.BooleanField(default=False, help_text="Whether admin has reviewed this submission")
    is_responded = models.BooleanField(default=False, help_text="Whether admin has responded to this submission")
    admin_notes = models.TextField(blank=True, help_text="Admin notes about this submission")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the submission was received")
    reviewed_at = models.DateTimeField(blank=True, null=True, help_text="When admin reviewed this submission")
    responded_at = models.DateTimeField(blank=True, null=True, help_text="When admin responded to this submission")
    
    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at'] 