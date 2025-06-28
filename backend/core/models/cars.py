"""
Car Models

This module contains models related to cars and build logs:
- CarProfile: Car profiles and specifications
- CarModification: Car modifications and parts
- CarImage: Car images
- BuildLog: Car build logs and projects
- BuildMilestone: Build milestones and progress
- BuildMedia: Media files for builds
- CarTour: Car tours and videos
- PerformanceData: Performance testing data
- BuildWishlist: Build wishlist items
- WishlistSuggestion: Suggestions for wishlist items
- BuildRating: Ratings for builds
- BuildComment: Comments on builds
- BuildBadge: Achievement badges
- BuildBadgeAward: Badge awards
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class CarProfile(models.Model):
    """Car profile model."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cars')
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
        return f"{self.name} on {self.car}"

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
        return f"Image of {self.car}"

    class Meta:
        ordering = ['-is_primary', '-created_at']


class BuildLog(models.Model):
    """Build log model."""
    car = models.ForeignKey(CarProfile, on_delete=models.CASCADE, related_name='build_logs')
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
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_builds', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.car}"

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def progress_percentage(self):
        if not self.milestones.exists():
            return 0
        completed = self.milestones.filter(is_complete=True).count()
        total = self.milestones.count()
        return (completed / total) * 100 if total > 0 else 0

    class Meta:
        ordering = ['-updated_at']


class BuildMilestone(models.Model):
    """Build milestone model."""
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
        return f"{self.title} - {self.build_log.title}"

    class Meta:
        ordering = ['start_date']


class BuildMedia(models.Model):
    """Build media model."""
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
        return f"{self.media_type} - {self.title or self.file.name}"

    class Meta:
        ordering = ['-created_at']


class CarTour(models.Model):
    """Car tour model."""
    car = models.ForeignKey(CarProfile, on_delete=models.CASCADE, related_name='tours')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tour_type = models.CharField(max_length=20)
    primary_media = models.FileField(upload_to='car_tours/')
    thumbnail = models.ImageField(upload_to='tour_thumbnails/', blank=True, null=True)
    is_public = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_tours', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.car}"

    @property
    def like_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']


class PerformanceData(models.Model):
    """Performance data model."""
    car = models.ForeignKey(CarProfile, on_delete=models.CASCADE, related_name='performance_data')
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
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='verified_performance_data')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.car}"

    class Meta:
        ordering = ['-test_date']


class BuildWishlist(models.Model):
    """Build wishlist model."""
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
        return f"{self.title} - {self.build_log.title}"

    class Meta:
        ordering = ['priority', '-created_at']


class WishlistSuggestion(models.Model):
    """Wishlist suggestion model."""
    wishlist_item = models.ForeignKey(BuildWishlist, on_delete=models.CASCADE, related_name='suggestions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist_suggestions_given')
    suggestion = models.TextField()
    alternative_part = models.CharField(max_length=200, blank=True)
    price_info = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=200, blank=True)
    is_helpful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion for {self.wishlist_item.title}"

    class Meta:
        ordering = ['-created_at']


class BuildRating(models.Model):
    """Build rating model."""
    build_log = models.ForeignKey(BuildLog, on_delete=models.CASCADE, related_name='ratings')
    rater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='build_ratings_given')
    creativity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    execution = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    documentation = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    performance = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    overall = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rating for {self.build_log.title}"

    class Meta:
        unique_together = ['build_log', 'rater']
        ordering = ['-created_at']


class BuildComment(models.Model):
    """Build comment model."""
    build_log = models.ForeignKey(BuildLog, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    milestone = models.ForeignKey(BuildMilestone, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    tour = models.ForeignKey(CarTour, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='build_comments')
    content = models.TextField()
    comment_type = models.CharField(max_length=20, default='general')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    is_approved = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_build_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username}"

    def get_content_object(self):
        """Get the object this comment is attached to."""
        if self.build_log:
            return self.build_log
        elif self.milestone:
            return self.milestone
        elif self.tour:
            return self.tour
        return None

    @property
    def like_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['created_at']


class BuildBadge(models.Model):
    """Build badge model."""
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
    """Build badge award model."""
    build_log = models.ForeignKey(BuildLog, on_delete=models.CASCADE, related_name='badge_awards')
    badge = models.ForeignKey(BuildBadge, on_delete=models.CASCADE, related_name='awards')
    awarded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges_awarded')
    awarded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.badge.name} awarded to {self.build_log.title}"

    class Meta:
        unique_together = ['build_log', 'badge']
        ordering = ['-awarded_at'] 