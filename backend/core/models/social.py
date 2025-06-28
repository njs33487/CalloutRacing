"""
Social Models

This module contains models related to social features:
- Friendship: Friend relationships between users
- Message: Direct messages between users
- UserPost: User posts and content
- PostComment: Comments on posts
- Notification: User notifications
- ReputationRating: User reputation and ratings
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Friendship(models.Model):
    """Friendship model."""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendship_requests_sent')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendship_requests_received')
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
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(help_text="Message content")
    is_read = models.BooleanField(default=False, help_text="Whether message has been read")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

    class Meta:
        ordering = ['created_at']


class UserPost(models.Model):
    """User post model."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(help_text="Post content")
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, help_text="Post image")
    car = models.ForeignKey('CarProfile', on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField(help_text="Comment content")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"

    class Meta:
        ordering = ['created_at']


class Notification(models.Model):
    """Notification model."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
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
        return f"Notification for {self.user.username}: {self.title}"

    class Meta:
        ordering = ['-created_at']


class ReputationRating(models.Model):
    """Reputation rating model."""
    rater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings_given')
    rated_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings_received')
    callout = models.ForeignKey('Callout', on_delete=models.CASCADE, related_name='ratings', blank=True, null=True)
    punctuality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Punctuality rating (1-5)")
    rule_adherence = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Rule adherence rating (1-5)")
    sportsmanship = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Sportsmanship rating (1-5)")
    overall = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Overall rating (1-5)")
    comment = models.TextField(blank=True, help_text="Optional comment about the experience")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating from {self.rater.username} to {self.rated_user.username}"

    class Meta:
        unique_together = ['rater', 'rated_user', 'callout']
        ordering = ['-created_at'] 