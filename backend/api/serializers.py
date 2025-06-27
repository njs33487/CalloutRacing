"""
Django REST Framework Serializers for CalloutRacing Application

This module contains all the serializers for the CalloutRacing application, including:
- User and profile serializers
- Event and callout serializers
- Marketplace serializers
- Social feature serializers
- Car profile serializers

Serializers handle the conversion between Django model instances and JSON data,
including nested relationships and computed fields.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import (
    UserProfile, Track, Event, Callout, RaceResult, 
    Marketplace, MarketplaceImage, EventParticipant,
    Friendship, Message, CarProfile, CarModification, 
    CarImage, UserPost, PostComment, Subscription, Payment,
    UserWallet, MarketplaceOrder, MarketplaceReview, Bet, BettingPool,
    Notification
)
from django.db import models


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Django User model.
    
    Provides basic user information including ID, username, email,
    name, and registration date. Used as nested serializer in other views.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model.
    
    Includes nested user data and computed win_rate field.
    Used for basic profile information display.
    """
    user = UserSerializer(read_only=True)
    win_rate = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    """
    Serializer for Track model.
    
    Provides complete track information including name, location,
    type, surface, and specifications.
    """
    class Meta:
        model = Track
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model.
    
    Includes nested track and organizer data, plus computed
    participant count for event listings.
    """
    track = TrackSerializer(read_only=True)
    organizer = UserSerializer(read_only=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_participant_count(self, obj):
        """
        Get the number of participants for an event.
        
        Args:
            obj: Event instance
            
        Returns:
            int: Number of participants
        """
        return obj.participants.count()


class CalloutSerializer(serializers.ModelSerializer):
    """
    Serializer for Callout model.
    
    Includes nested data for challenger, challenged, event, and track.
    Protects challenger and timestamp fields from modification.
    """
    challenger = UserSerializer(read_only=True)
    challenged = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    track = TrackSerializer(read_only=True)

    class Meta:
        model = Callout
        fields = '__all__'
        read_only_fields = ['challenger', 'created_at', 'updated_at']


class RaceResultSerializer(serializers.ModelSerializer):
    """
    Serializer for RaceResult model.
    
    Includes nested data for callout, winner, and loser.
    Used for displaying race results and statistics.
    """
    callout = CalloutSerializer(read_only=True)
    winner = UserSerializer(read_only=True)
    loser = UserSerializer(read_only=True)

    class Meta:
        model = RaceResult
        fields = '__all__'


class MarketplaceImageSerializer(serializers.ModelSerializer):
    """
    Serializer for MarketplaceImage model.
    
    Handles image uploads and metadata for marketplace items.
    """
    class Meta:
        model = MarketplaceImage
        fields = '__all__'


class MarketplaceSerializer(serializers.ModelSerializer):
    """
    Serializer for Marketplace model.
    
    Includes nested seller data, images, and computed primary image.
    Protects seller and metric fields from modification.
    """
    seller = UserSerializer(read_only=True)
    images = MarketplaceImageSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Marketplace
        fields = '__all__'
        read_only_fields = ['seller', 'views', 'created_at', 'updated_at']

    def get_primary_image(self, obj):
        """
        Get the primary image for a marketplace item.
        
        Args:
            obj: Marketplace instance
            
        Returns:
            dict: Primary image data or None
        """
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return MarketplaceImageSerializer(primary_image).data
        return None


class EventParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer for EventParticipant model.
    
    Includes nested event and user data.
    Protects user and registration date from modification.
    """
    event = EventSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = EventParticipant
        fields = '__all__'
        read_only_fields = ['user', 'registration_date']


# Nested serializers for detailed views
class CalloutDetailSerializer(CalloutSerializer):
    """
    Detailed serializer for Callout model.
    
    Extends CalloutSerializer to include race result data
    for comprehensive callout information.
    """
    result = RaceResultSerializer(read_only=True)


class EventDetailSerializer(EventSerializer):
    """
    Detailed serializer for Event model.
    
    Extends EventSerializer to include participants and callouts
    for comprehensive event information.
    """
    participants = EventParticipantSerializer(many=True, read_only=True)
    callouts = CalloutSerializer(many=True, read_only=True)


class MarketplaceDetailSerializer(MarketplaceSerializer):
    """
    Detailed serializer for Marketplace model.
    
    Currently identical to MarketplaceSerializer but can be extended
    for additional detailed marketplace information.
    """
    pass


# Social feature serializers
class FriendshipSerializer(serializers.ModelSerializer):
    """
    Serializer for Friendship model.
    
    Includes nested sender and receiver data.
    Protects sender and timestamp fields from modification.
    """
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = '__all__'
        read_only_fields = ['sender', 'created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    
    Includes nested sender and receiver data.
    Protects sender and timestamp fields from modification.
    """
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'created_at']


class CarModificationSerializer(serializers.ModelSerializer):
    """
    Serializer for CarModification model.
    
    Handles car modification data including category, brand,
    cost, and installation information.
    """
    class Meta:
        model = CarModification
        fields = '__all__'


class CarImageSerializer(serializers.ModelSerializer):
    """
    Serializer for CarImage model.
    
    Handles car image uploads and metadata.
    """
    class Meta:
        model = CarImage
        fields = '__all__'


class CarProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for CarProfile model.
    
    Includes nested user data, modifications, images, and computed primary image.
    Protects user and timestamp fields from modification.
    """
    user = UserSerializer(read_only=True)
    modifications = CarModificationSerializer(many=True, read_only=True)
    images = CarImageSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = CarProfile
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_primary_image(self, obj):
        """
        Get the primary image for a car profile.
        
        Args:
            obj: CarProfile instance
            
        Returns:
            dict: Primary image data or None
        """
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return CarImageSerializer(primary_image).data
        return None


class PostCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for PostComment model.
    
    Includes nested user data.
    Protects user and timestamp fields from modification.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class UserPostSerializer(serializers.ModelSerializer):
    """
    Serializer for UserPost model.
    
    Includes nested user, car, and comments data.
    Provides computed like_count and is_liked fields.
    Protects user, likes, and timestamp fields from modification.
    """
    user = UserSerializer(read_only=True)
    car = CarProfileSerializer(read_only=True)
    comments = PostCommentSerializer(many=True, read_only=True)
    like_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = UserPost
        fields = '__all__'
        read_only_fields = ['user', 'likes', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        """
        Check if the current user has liked this post.
        
        Args:
            obj: UserPost instance
            
        Returns:
            bool: True if current user has liked the post
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


class UserProfileDetailSerializer(UserProfileSerializer):
    """
    Enhanced user profile serializer with social features.
    
    Extends UserProfileSerializer to include cars, posts, and
    friendship information for comprehensive profile views.
    """
    cars = CarProfileSerializer(many=True, read_only=True)
    posts = UserPostSerializer(many=True, read_only=True)
    friends_count = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()
    friendship_status = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_friends_count(self, obj):
        """
        Get the number of friends for a user.
        
        Args:
            obj: UserProfile instance
            
        Returns:
            int: Number of accepted friends
        """
        return Friendship.objects.filter(
            models.Q(sender=obj.user) | models.Q(receiver=obj.user),
            status='accepted'
        ).count()

    def get_is_friend(self, obj):
        """
        Check if the current user is friends with the profile user.
        
        Args:
            obj: UserProfile instance
            
        Returns:
            bool: True if users are friends
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        
        return Friendship.objects.filter(
            models.Q(sender=request.user, receiver=obj.user) |
            models.Q(sender=obj.user, receiver=request.user),
            status='accepted'
        ).exists()

    def get_friendship_status(self, obj):
        """
        Get the friendship status between the current user and profile user.
        
        Args:
            obj: UserProfile instance
            
        Returns:
            str: Friendship status or None
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if request.user == obj.user:
                return 'self'
            
            friendship = Friendship.objects.filter(
                models.Q(sender=request.user, receiver=obj.user) |
                models.Q(sender=obj.user, receiver=request.user)
            ).first()
            
            if friendship:
                return friendship.status
        return None


# ============================================================================
# PAYMENT & SUBSCRIPTION SERIALIZERS
# ============================================================================

class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for Subscription model.
    
    Includes nested user data and computed is_active field.
    Protects user and timestamp fields from modification.
    """
    user = UserSerializer(read_only=True)
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment model.
    
    Includes nested user data and related object information.
    Protects user and timestamp fields from modification.
    """
    user = UserSerializer(read_only=True)
    subscription = SubscriptionSerializer(read_only=True)
    marketplace_item = MarketplaceSerializer(read_only=True)
    callout = CalloutSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class UserWalletSerializer(serializers.ModelSerializer):
    """
    Serializer for UserWallet model.
    
    Includes nested user data and computed can_afford method.
    Protects user and timestamp fields from modification.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserWallet
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


# ============================================================================
# ENHANCED MARKETPLACE SERIALIZERS
# ============================================================================

class MarketplaceOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for MarketplaceOrder model.
    
    Includes nested buyer, seller, item, and payment data.
    Protects buyer and timestamp fields from modification.
    """
    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    item = MarketplaceSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = MarketplaceOrder
        fields = '__all__'
        read_only_fields = ['buyer', 'created_at', 'updated_at']


class MarketplaceReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for MarketplaceReview model.
    
    Includes nested order and reviewer data.
    Protects reviewer and timestamp fields from modification.
    """
    order = MarketplaceOrderSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)

    class Meta:
        model = MarketplaceReview
        fields = '__all__'
        read_only_fields = ['reviewer', 'created_at', 'updated_at']


# ============================================================================
# BETTING SERIALIZERS
# ============================================================================

class BetSerializer(serializers.ModelSerializer):
    """
    Serializer for Bet model.
    
    Includes nested bettor, callout, event, and payment data.
    Protects bettor and timestamp fields from modification.
    """
    bettor = UserSerializer(read_only=True)
    callout = CalloutSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    selected_winner = UserSerializer(read_only=True)
    actual_winner = UserSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Bet
        fields = '__all__'
        read_only_fields = ['bettor', 'created_at', 'updated_at']


class BettingPoolSerializer(serializers.ModelSerializer):
    """
    Serializer for BettingPool model.
    
    Includes nested callout and event data, plus computed bet count.
    """
    callout = CalloutSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    bet_count = serializers.SerializerMethodField()

    class Meta:
        model = BettingPool
        fields = '__all__'

    def get_bet_count(self, obj):
        """
        Get the number of bets in the pool.
        
        Args:
            obj: BettingPool instance
            
        Returns:
            int: Number of bets
        """
        return obj.bets.count()


# ============================================================================
# NOTIFICATION SERIALIZERS
# ============================================================================

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    
    Includes nested user and related object data.
    Protects user and timestamp fields from modification.
    """
    user = UserSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)
    bet = BetSerializer(read_only=True)
    marketplace_order = MarketplaceOrderSerializer(read_only=True)
    callout = CalloutSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


# ============================================================================
# SPECIALIZED SERIALIZERS FOR FRONTEND
# ============================================================================

class WalletTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for wallet transactions (deposits/withdrawals).
    
    Simplified serializer for wallet transaction history.
    """
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'payment_type', 'payment_type_display', 'amount', 'currency', 
                 'status', 'status_display', 'description', 'created_at']


class BettingHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for user betting history.
    
    Simplified serializer for displaying user's betting history.
    """
    bet_type_display = serializers.CharField(source='get_bet_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    selected_winner_name = serializers.CharField(source='selected_winner.username', read_only=True)
    actual_winner_name = serializers.CharField(source='actual_winner.username', read_only=True)

    class Meta:
        model = Bet
        fields = ['id', 'bet_type', 'bet_type_display', 'bet_amount', 'odds', 
                 'potential_payout', 'selected_winner_name', 'status', 'status_display',
                 'actual_winner_name', 'payout_amount', 'created_at', 'settled_at']


class SubscriptionPlanSerializer(serializers.Serializer):
    """
    Serializer for subscription plan information.
    
    Used for displaying available subscription plans and their features.
    """
    plan_type = serializers.CharField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    currency = serializers.CharField()
    features = serializers.ListField(child=serializers.CharField())
    is_popular = serializers.BooleanField(default=False)
    is_current = serializers.BooleanField(default=False) 