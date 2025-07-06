"""
Django Admin Configuration for CalloutRacing Application

This module configures the Django admin interface for all models.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models.auth import UserProfile
from .models.racing import Track, Callout, RaceResult, Event, EventParticipant
from .models.social import (
    Follow, Block, Friendship, Message, UserPost, PostComment, 
    Notification, ReputationRating
)
from .models.cars import CarProfile
from .models.marketplace import Marketplace
from .models.payments import Subscription, Payment, UserWallet
from .models.locations import HotSpot


# User model is now Django's built-in User model, no need to register it here
# Django automatically registers the built-in User model with UserAdmin


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'car_make', 'car_model', 'wins', 'losses', 'total_races']
    list_filter = ['location', 'car_make', 'car_model']
    search_fields = ['user__username', 'bio', 'location']
    readonly_fields = ['user', 'created_at', 'updated_at']


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'track_type', 'surface_type', 'is_active']
    list_filter = ['track_type', 'surface_type', 'is_active']
    search_fields = ['name', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Callout)
class CalloutAdmin(admin.ModelAdmin):
    list_display = ['challenger', 'challenged', 'race_type', 'status', 'created_at']
    list_filter = ['status', 'race_type', 'location_type', 'experience_level']
    search_fields = ['challenger__username', 'challenged__username', 'message']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(RaceResult)
class RaceResultAdmin(admin.ModelAdmin):
    list_display = ['callout', 'challenger_time', 'challenged_time', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['callout__challenger__username', 'callout__challenged__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']
    readonly_fields = ['created_at']


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['blocker', 'blocked', 'reason', 'created_at']
    list_filter = ['created_at']
    search_fields = ['blocker__username', 'blocked__username', 'reason']
    readonly_fields = ['created_at']


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['sender__username', 'receiver__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'recipient__username', 'content']
    readonly_fields = ['created_at']


@admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin):
    list_display = ['author', 'post_type', 'likes_count', 'comments_count', 'is_public', 'created_at']
    list_filter = ['post_type', 'is_public', 'created_at']
    search_fields = ['author__username', 'content']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'likes_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author__username', 'content', 'post__content']
    readonly_fields = ['created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'sender', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__username', 'sender__username', 'title', 'message']
    readonly_fields = ['created_at']


@admin.register(ReputationRating)
class ReputationRatingAdmin(admin.ModelAdmin):
    list_display = ['rater', 'rated_user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['rater__username', 'rated_user__username', 'comment']
    readonly_fields = ['created_at']


@admin.register(CarProfile)
class CarProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'make', 'model', 'year', 'is_primary']
    list_filter = ['make', 'model', 'year', 'is_primary']
    search_fields = ['user__username', 'make', 'model']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Marketplace)
class MarketplaceAdmin(admin.ModelAdmin):
    list_display = ['seller', 'title', 'price', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['seller__username', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'stripe_subscription_id', 'current_period_start', 'current_period_end']
    list_filter = ['status', 'cancel_at_period_end', 'created_at']
    search_fields = ['user__username', 'user__email', 'stripe_subscription_id']
    readonly_fields = ['stripe_subscription_id', 'stripe_customer_id', 'stripe_price_id']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'payment_type', 'created_at']
    list_filter = ['status', 'payment_type', 'created_at']
    search_fields = ['user__username', 'transaction_id']
    readonly_fields = ['created_at']


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'stripe_account_id', 'is_onboarded']
    list_filter = ['is_onboarded', 'created_at']
    search_fields = ['user__username', 'user__email', 'stripe_account_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(HotSpot)
class HotSpotAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'is_verified', 'created_by', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['name', 'city', 'state', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'organizer', 'start_date', 'end_date', 'is_active', 'is_public']
    list_filter = ['event_type', 'is_active', 'is_public', 'start_date']
    search_fields = ['title', 'description', 'organizer__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'is_confirmed', 'registration_date']
    list_filter = ['is_confirmed', 'registration_date']
    search_fields = ['event__title', 'user__username']
    readonly_fields = ['registration_date'] 