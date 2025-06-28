from django.contrib import admin
from .models import (
    UserProfile, Track, Event, Callout, RaceResult, 
    Marketplace, MarketplaceImage, EventParticipant,
    Friendship, Message, CarProfile, CarModification, 
    CarImage, UserPost, PostComment,
    Subscription, Payment, UserWallet, MarketplaceOrder, 
    MarketplaceReview, Bet, BettingPool, Notification, ContactSubmission,
    # Advanced racing features
    HotSpot, RacingCrew, CrewMembership, LocationBroadcast,
    ReputationRating, OpenChallenge, ChallengeResponse,
    # Build showcase models
    BuildLog, BuildMilestone, BuildMedia, CarTour, PerformanceData,
    BuildWishlist, WishlistSuggestion, BuildRating, BuildComment,
    BuildBadge, BuildBadgeAward
)
from django.utils import timezone


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


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription_type', 'status', 'start_date', 'end_date']
    list_filter = ['subscription_type', 'status']
    search_fields = ['user__username']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_type', 'amount', 'status', 'created_at']
    list_filter = ['payment_type', 'status', 'created_at']
    search_fields = ['user__username']


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username']


@admin.register(MarketplaceOrder)
class MarketplaceOrderAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'seller', 'item', 'quantity', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['buyer__username', 'seller__username', 'item__title']


@admin.register(MarketplaceReview)
class MarketplaceReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'order', 'rating', 'title', 'created_at']
    list_filter = ['rating', 'is_verified_purchase', 'created_at']
    search_fields = ['reviewer__username', 'title']


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ['bettor', 'bet_type', 'bet_amount', 'odds', 'status', 'created_at']
    list_filter = ['bet_type', 'status', 'created_at']
    search_fields = ['bettor__username']


@admin.register(BettingPool)
class BettingPoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_pool', 'is_active', 'is_settled', 'created_at']
    list_filter = ['is_active', 'is_settled', 'created_at']
    search_fields = ['name']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title']


@admin.register(HotSpot)
class HotSpotAdmin(admin.ModelAdmin):
    list_display = ['name', 'spot_type', 'city', 'state', 'is_verified', 'is_active', 'total_races']
    list_filter = ['spot_type', 'is_verified', 'is_active', 'state']
    search_fields = ['name', 'description', 'address', 'city']
    ordering = ['name']


@admin.register(RacingCrew)
class RacingCrewAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'member_count', 'is_public', 'is_verified', 'created_by']
    list_filter = ['is_public', 'is_verified', 'founded_date']
    search_fields = ['name', 'description', 'location']
    ordering = ['name']


@admin.register(CrewMembership)
class CrewMembershipAdmin(admin.ModelAdmin):
    list_display = ['crew', 'user', 'role', 'status', 'joined_date']
    list_filter = ['role', 'status', 'joined_date']
    search_fields = ['crew__name', 'user__username']
    ordering = ['joined_date']


@admin.register(LocationBroadcast)
class LocationBroadcastAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'is_active', 'expires_at', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'location', 'message']
    ordering = ['-created_at']


@admin.register(ReputationRating)
class ReputationRatingAdmin(admin.ModelAdmin):
    list_display = ['rater', 'rated_user', 'overall', 'created_at']
    list_filter = ['overall', 'created_at']
    search_fields = ['rater__username', 'rated_user__username', 'comment']
    ordering = ['-created_at']


@admin.register(OpenChallenge)
class OpenChallengeAdmin(admin.ModelAdmin):
    list_display = ['challenger', 'title', 'race_type', 'wager_amount', 'is_active', 'expires_at']
    list_filter = ['race_type', 'is_active', 'created_at']
    search_fields = ['challenger__username', 'title', 'description', 'location']
    ordering = ['-created_at']


@admin.register(ChallengeResponse)
class ChallengeResponseAdmin(admin.ModelAdmin):
    list_display = ['challenge', 'respondent', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['challenge__title', 'respondent__username', 'message']
    ordering = ['created_at']


@admin.register(BuildLog)
class BuildLogAdmin(admin.ModelAdmin):
    list_display = ['car', 'title', 'is_complete', 'start_date', 'completion_date', 'total_cost']
    list_filter = ['is_complete', 'start_date', 'completion_date']
    search_fields = ['car__name', 'title', 'description']
    date_hierarchy = 'start_date'


@admin.register(BuildMilestone)
class BuildMilestoneAdmin(admin.ModelAdmin):
    list_display = ['build_log', 'title', 'category', 'is_complete', 'start_date', 'completion_date']
    list_filter = ['category', 'is_complete', 'start_date', 'completion_date']
    search_fields = ['build_log__title', 'title', 'description']


@admin.register(BuildMedia)
class BuildMediaAdmin(admin.ModelAdmin):
    list_display = ['build_log', 'media_type', 'title', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['build_log__title', 'title', 'description']


@admin.register(CarTour)
class CarTourAdmin(admin.ModelAdmin):
    list_display = ['car', 'tour_type', 'title', 'is_public', 'created_at']
    list_filter = ['tour_type', 'is_public', 'created_at']
    search_fields = ['car__name', 'title', 'description']


@admin.register(PerformanceData)
class PerformanceDataAdmin(admin.ModelAdmin):
    list_display = ['car', 'test_type', 'test_date', 'horsepower', 'quarter_mile_time']
    list_filter = ['test_type', 'test_date']
    search_fields = ['car__name', 'title', 'notes']


@admin.register(BuildWishlist)
class BuildWishlistAdmin(admin.ModelAdmin):
    list_display = ['build_log', 'title', 'priority', 'estimated_cost', 'is_public']
    list_filter = ['priority', 'is_public', 'created_at']
    search_fields = ['build_log__title', 'title', 'description']


@admin.register(WishlistSuggestion)
class WishlistSuggestionAdmin(admin.ModelAdmin):
    list_display = ['wishlist_item', 'user', 'suggestion', 'created_at']
    list_filter = ['created_at']
    search_fields = ['wishlist_item__title', 'user__username', 'suggestion']


@admin.register(BuildRating)
class BuildRatingAdmin(admin.ModelAdmin):
    list_display = ['build_log', 'rater', 'overall', 'created_at']
    list_filter = ['overall', 'created_at']
    search_fields = ['build_log__title', 'rater__username', 'comment']


@admin.register(BuildComment)
class BuildCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'content']


@admin.register(BuildBadge)
class BuildBadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'is_active']
    list_filter = ['badge_type', 'is_active']
    search_fields = ['name', 'description']


@admin.register(BuildBadgeAward)
class BuildBadgeAwardAdmin(admin.ModelAdmin):
    list_display = ['build_log', 'badge', 'awarded_by', 'awarded_at']
    list_filter = ['badge', 'awarded_at']
    search_fields = ['build_log__title', 'badge__name', 'awarded_by__username']


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """Admin interface for contact form submissions."""
    list_display = ['name', 'email', 'subject', 'is_reviewed', 'is_responded', 'created_at']
    list_filter = ['is_reviewed', 'is_responded', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('is_reviewed', 'is_responded', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'reviewed_at', 'responded_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and 'is_reviewed' in form.changed_data and obj.is_reviewed:
            obj.reviewed_at = timezone.now()
        if change and 'is_responded' in form.changed_data and obj.is_responded:
            obj.responded_at = timezone.now()
        super().save_model(request, obj, form, change) 