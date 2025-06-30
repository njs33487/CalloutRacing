"""
Social Models for CalloutRacing Application

This module contains models related to social features:
- Friendship: Friend relationships between users
- Follow: Follow relationships between users
- Message: Direct messages between users
- UserPost: User posts and content
- PostComment: Comments on posts
- Notification: User notifications
- ReputationRating: User reputation and ratings
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Follow(models.Model):
    """Follow relationship between users."""
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='following',
        help_text='User who is following'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='followers',
        help_text='User being followed'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
    def save(self, *args, **kwargs):
        # Prevent self-following
        if self.follower == self.following:
            raise ValueError("Users cannot follow themselves")
        super().save(*args, **kwargs)


class Block(models.Model):
    """Block relationship between users."""
    blocker = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='blocking',
        help_text='User who is blocking'
    )
    blocked = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='blocked_by',
        help_text='User being blocked'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, help_text='Reason for blocking')
    
    class Meta:
        unique_together = ('blocker', 'blocked')
        ordering = ['-created_at']
        verbose_name = "Block"
        verbose_name_plural = "Blocks"
    
    def __str__(self):
        return f"{self.blocker.username} blocks {self.blocked.username}"
    
    def save(self, *args, **kwargs):
        # Prevent self-blocking
        if self.blocker == self.blocked:
            raise ValueError("Users cannot block themselves")
        super().save(*args, **kwargs)


class Friendship(models.Model):
    """Friendship relationship between users."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_friend_requests',
        help_text='User who sent the friend request',
        null=True,  # Make nullable for migration
        blank=True
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_friend_requests',
        help_text='User who received the friend request',
        null=True,  # Make nullable for migration
        blank=True
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        help_text='Status of the friendship'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('sender', 'receiver')
        ordering = ['-created_at']
        verbose_name = "Friendship"
        verbose_name_plural = "Friendships"
    
    def __str__(self):
        if self.sender and self.receiver:
            return f"{self.sender.username} -> {self.receiver.username} ({self.status})"
        return f"Friendship {self.id} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Prevent self-friending
        if self.sender and self.receiver and self.sender == self.receiver:
            raise ValueError("Users cannot friend themselves")
        super().save(*args, **kwargs)


class Message(models.Model):
    """Direct message between users."""
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_messages',
        help_text='User who sent the message',
        null=True,  # Make nullable for migration
        blank=True
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_messages',
        help_text='User who received the message',
        null=True,  # Make nullable for migration
        blank=True
    )
    content = models.TextField(help_text='Message content')
    is_read = models.BooleanField(default=False, help_text='Whether message has been read')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"
    
    def __str__(self):
        if self.sender and self.recipient:
            return f"{self.sender.username} -> {self.recipient.username}: {self.content[:50]}"
        return f"Message {self.id}: {self.content[:50]}"


class UserPost(models.Model):
    """User post/content."""
    POST_TYPES = [
        ('text', 'Text Post'),
        ('image', 'Image Post'),
        ('video', 'Video Post'),
        ('race_result', 'Race Result'),
        ('car_update', 'Car Update'),
    ]
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posts',
        help_text='User who created the post',
        null=True,  # Make nullable for migration
        blank=True
    )
    content = models.TextField(help_text='Post content')
    post_type = models.CharField(
        max_length=20, 
        choices=POST_TYPES, 
        default='text',
        help_text='Type of post'
    )
    image = models.ImageField(
        upload_to='posts/images/', 
        blank=True, 
        null=True,
        help_text='Post image'
    )
    video = models.FileField(
        upload_to='posts/videos/', 
        blank=True, 
        null=True,
        help_text='Post video'
    )
    likes_count = models.IntegerField(default=0, help_text='Number of likes')
    comments_count = models.IntegerField(default=0, help_text='Number of comments')
    is_public = models.BooleanField(default=True, help_text='Whether post is public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "User Post"
        verbose_name_plural = "User Posts"
    
    def __str__(self):
        if self.author:
            return f"{self.author.username}: {self.content[:50]}"
        return f"Post {self.id}: {self.content[:50]}"


class PostComment(models.Model):
    """Comment on a user post."""
    post = models.ForeignKey(
        UserPost, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text='Post being commented on'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text='User who wrote the comment',
        null=True,  # Make nullable for migration
        blank=True
    )
    content = models.TextField(help_text='Comment content')
    likes_count = models.IntegerField(default=0, help_text='Number of likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Post Comment"
        verbose_name_plural = "Post Comments"
    
    def __str__(self):
        if self.author:
            return f"{self.author.username} on {self.post}: {self.content[:50]}"
        return f"Comment on {self.post}: {self.content[:50]}"


class Notification(models.Model):
    """User notification."""
    NOTIFICATION_TYPES = [
        ('follow', 'New Follower'),
        ('friend_request', 'Friend Request'),
        ('message', 'New Message'),
        ('like', 'Post Liked'),
        ('comment', 'Post Commented'),
        ('callout', 'New Callout'),
        ('race_result', 'Race Result'),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        help_text='User receiving the notification',
        null=True,  # Make nullable for migration
        blank=True
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_notifications',
        blank=True, 
        null=True,
        help_text='User who triggered the notification'
    )
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES,
        help_text='Type of notification'
    )
    title = models.CharField(max_length=200, help_text='Notification title')
    message = models.TextField(help_text='Notification message')
    is_read = models.BooleanField(default=False, help_text='Whether notification has been read')
    related_object_id = models.IntegerField(
        blank=True, 
        null=True,
        help_text='ID of related object (post, message, etc.)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
    
    def __str__(self):
        if self.recipient:
            return f"{self.recipient.username}: {self.title}"
        return f"Notification {self.id}: {self.title}"


class ReputationRating(models.Model):
    """User reputation rating."""
    rater = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='given_ratings',
        help_text='User giving the rating',
        null=True,  # Make nullable for migration
        blank=True
    )
    rated_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_ratings',
        help_text='User being rated',
        null=True,  # Make nullable for migration
        blank=True
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5',
        null=True,  # Make nullable for migration
        blank=True
    )
    comment = models.TextField(blank=True, help_text='Rating comment')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('rater', 'rated_user')
        ordering = ['-created_at']
        verbose_name = "Reputation Rating"
        verbose_name_plural = "Reputation Ratings"
    
    def __str__(self):
        if self.rater and self.rated_user:
            return f"{self.rater.username} rates {self.rated_user.username}: {self.rating}/5"
        return f"Rating {self.id}: {self.rating}/5"
    
    def save(self, *args, **kwargs):
        # Prevent self-rating
        if self.rater and self.rated_user and self.rater == self.rated_user:
            raise ValueError("Users cannot rate themselves")
        super().save(*args, **kwargs)


# Additional models for advanced social features

class RacingCrew(models.Model):
    """Racing crew model for social features."""
    CREW_TYPES = [
        ('drag_racing', 'Drag Racing'),
        ('street_racing', 'Street Racing'),
        ('track_racing', 'Track Racing'),
        ('car_club', 'Car Club'),
        ('modification', 'Modification Crew'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200, help_text='Crew name')
    description = models.TextField(help_text='Crew description')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_crews',
        help_text='Crew owner'
    )
    crew_type = models.CharField(
        max_length=20,
        choices=CREW_TYPES,
        default='car_club',
        help_text='Type of crew'
    )
    location = models.CharField(max_length=200, help_text='Crew location')
    is_public = models.BooleanField(default=True, help_text='Whether crew is public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Racing Crew"
        verbose_name_plural = "Racing Crews"
    
    def __str__(self):
        return self.name


class CrewMembership(models.Model):
    """Crew membership model."""
    ROLES = [
        ('member', 'Member'),
        ('officer', 'Officer'),
        ('leader', 'Leader'),
        ('founder', 'Founder'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    crew = models.ForeignKey(
        RacingCrew,
        on_delete=models.CASCADE,
        related_name='memberships',
        help_text='Crew being joined'
    )
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='crew_memberships',
        help_text='Crew member'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default='member',
        help_text='Member role'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='Membership status'
    )
    joined_at = models.DateTimeField(auto_now_add=True, help_text='When member joined')
    
    class Meta:
        unique_together = ('crew', 'member')
        ordering = ['joined_at']
        verbose_name = "Crew Membership"
        verbose_name_plural = "Crew Memberships"
    
    def __str__(self):
        return f"{self.member.username} - {self.crew.name} ({self.role})" 