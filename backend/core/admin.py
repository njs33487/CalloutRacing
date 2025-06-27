from django.contrib import admin
from .models import (
    UserProfile, Track, Event, Callout, RaceResult, 
    Marketplace, MarketplaceImage, EventParticipant,
    Friendship, Message, CarProfile, CarModification, 
    CarImage, UserPost, PostComment
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'car_make', 'car_model', 'wins', 'losses', 'win_rate']
    list_filter = ['location', 'car_make']
    search_fields = ['user__username', 'user__email', 'location']


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'track_type', 'surface_type', 'is_active']
    list_filter = ['track_type', 'surface_type', 'is_active']
    search_fields = ['name', 'location']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'track', 'organizer', 'event_type', 'start_date', 'is_active']
    list_filter = ['event_type', 'is_public', 'is_active', 'start_date']
    search_fields = ['title', 'description', 'track__name']
    date_hierarchy = 'start_date'


@admin.register(Callout)
class CalloutAdmin(admin.ModelAdmin):
    list_display = ['challenger', 'challenged', 'location_type', 'race_type', 'status', 'created_at']
    list_filter = ['status', 'location_type', 'race_type', 'created_at']
    search_fields = ['challenger__username', 'challenged__username', 'message']
    date_hierarchy = 'created_at'


@admin.register(RaceResult)
class RaceResultAdmin(admin.ModelAdmin):
    list_display = ['winner', 'loser', 'winner_time', 'completed_at']
    list_filter = ['completed_at']
    search_fields = ['winner__username', 'loser__username']


@admin.register(Marketplace)
class MarketplaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'category', 'price', 'condition', 'is_active']
    list_filter = ['category', 'condition', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'seller__username']
    date_hierarchy = 'created_at'


@admin.register(MarketplaceImage)
class MarketplaceImageAdmin(admin.ModelAdmin):
    list_display = ['marketplace_item', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'registration_date']
    list_filter = ['registration_date']
    search_fields = ['event__title', 'user__username']


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['sender__username', 'receiver__username']
    date_hierarchy = 'created_at'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'content']
    date_hierarchy = 'created_at'


@admin.register(CarProfile)
class CarProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'make', 'model', 'year', 'is_primary', 'is_active']
    list_filter = ['make', 'model', 'year', 'fuel_type', 'drivetrain', 'is_primary', 'is_active']
    search_fields = ['user__username', 'name', 'make', 'model', 'description']
    date_hierarchy = 'created_at'


@admin.register(CarModification)
class CarModificationAdmin(admin.ModelAdmin):
    list_display = ['car', 'category', 'name', 'brand', 'is_installed', 'installed_date']
    list_filter = ['category', 'brand', 'is_installed', 'installed_date']
    search_fields = ['car__name', 'name', 'brand', 'description']


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ['car', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']


@admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'like_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'content']
    date_hierarchy = 'created_at'


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__content', 'user__username', 'content']
    date_hierarchy = 'created_at' 