"""
API Serializers for CalloutRacing Application

This module contains serializers for all API endpoints:
- User authentication and profile
- Racing models (Callout, Track, RaceResult)
- Marketplace models
- Social features
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import User
from core.models.auth import UserProfile
from core.models.racing import Callout, Track, RaceResult, Event, EventParticipant
from core.models.cars import CarProfile, CarImage, BuildLog, PerformanceData, BuildMilestone
from core.models.marketplace import (
    Marketplace, MarketplaceImage, MarketplaceOrder, MarketplaceReview,
    ListingCategory, MarketplaceListing, ListingImage, CarListing,
    Review, Rating, PaymentTransaction, Order, OrderItem, ShippingAddress
)
from core.models.social import (
    Friendship, Message, UserPost, PostComment, RacingCrew, CrewMembership, Notification
)
from core.models.locations import (
    HotSpot, LocationBroadcast, OpenChallenge, ChallengeResponse
)
from core.models.payments import UserWallet, Bet, BettingPool

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer for public information."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'email_verified']
        read_only_fields = ['id', 'date_joined', 'email_verified']


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']


class RegisterSerializer(serializers.ModelSerializer):
    """User registration serializer."""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """User login serializer."""
    username = serializers.CharField()
    password = serializers.CharField()


class PasswordResetRequestSerializer(serializers.Serializer):
    """Password reset request serializer."""
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Password reset confirmation serializer."""
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs


class OTPVerifySerializer(serializers.Serializer):
    """OTP verification serializer."""
    otp_code = serializers.CharField(max_length=6, min_length=6)


class OTPEnableSerializer(serializers.Serializer):
    """OTP enable/disable serializer."""
    enable = serializers.BooleanField()


# Racing Serializers

class TrackSerializer(serializers.ModelSerializer):
    """Track serializer."""
    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CalloutSerializer(serializers.ModelSerializer):
    """Basic callout serializer for list views."""
    challenger = UserSerializer(read_only=True)
    challenged = UserSerializer(read_only=True)
    track = TrackSerializer(read_only=True)
    winner = UserSerializer(read_only=True)
    location_display = serializers.CharField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Callout
        fields = [
            'id', 'challenger', 'challenged', 'location_type', 'track', 
            'street_location', 'city', 'state', 'race_type', 'wager_amount',
            'message', 'experience_level', 'min_horsepower', 'max_horsepower',
            'tire_requirement', 'rules', 'is_private', 'is_invite_only',
            'status', 'scheduled_date', 'winner', 'location_display',
            'is_expired', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'challenger', 'created_at', 'updated_at']


class CalloutCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating callouts."""
    challenged_username = serializers.CharField(write_only=True)
    
    class Meta:
        model = Callout
        fields = [
            'challenged_username', 'location_type', 'track', 'street_location',
            'city', 'state', 'race_type', 'wager_amount', 'message',
            'experience_level', 'min_horsepower', 'max_horsepower',
            'tire_requirement', 'rules', 'is_private', 'is_invite_only',
            'scheduled_date'
        ]
    
    def validate(self, attrs):
        # Validate challenged user exists
        challenged_username = attrs.get('challenged_username')
        try:
            challenged_user = User.objects.get(username=challenged_username)
            attrs['challenged'] = challenged_user
        except User.DoesNotExist:
            raise serializers.ValidationError("Challenged user not found")
        
        # Validate location requirements
        location_type = attrs.get('location_type')
        if location_type == 'track':
            if not attrs.get('track'):
                raise serializers.ValidationError("Track is required when location_type is 'track'")
        elif location_type == 'street':
            if not attrs.get('street_location') or not attrs.get('city') or not attrs.get('state'):
                raise serializers.ValidationError("Street location, city, and state are required when location_type is 'street'")
        
        # Validate scheduled date is in the future
        scheduled_date = attrs.get('scheduled_date')
        if scheduled_date and scheduled_date <= timezone.now():
            raise serializers.ValidationError("Scheduled date must be in the future")
        
        # Validate horsepower range
        min_hp = attrs.get('min_horsepower')
        max_hp = attrs.get('max_horsepower')
        if min_hp and max_hp and min_hp > max_hp:
            raise serializers.ValidationError("Minimum horsepower cannot be greater than maximum horsepower")
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('challenged_username')
        return super().create(validated_data)


class CalloutDetailSerializer(CalloutSerializer):
    """Detailed callout serializer with race result."""
    race_result = serializers.SerializerMethodField()
    
    class Meta(CalloutSerializer.Meta):
        fields = CalloutSerializer.Meta.fields + ['race_result']
    
    def get_race_result(self, obj):
        if hasattr(obj, 'race_result') and obj.race_result:
            return RaceResultSerializer(obj.race_result).data
        return None


class RaceResultSerializer(serializers.ModelSerializer):
    """Race result serializer."""
    callout = serializers.PrimaryKeyRelatedField(queryset=Callout.objects.all(), write_only=True)
    callout_detail = CalloutSerializer(source='callout', read_only=True)
    verified_by = UserSerializer(read_only=True)
    winner = serializers.SerializerMethodField()
    
    class Meta:
        model = RaceResult
        fields = [
            'id', 'callout', 'callout_detail', 'challenger_time', 'challenged_time',
            'challenger_speed', 'challenged_speed', 'challenger_reaction',
            'challenged_reaction', 'weather_conditions', 'track_conditions',
            'notes', 'is_verified', 'verified_by', 'winner', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'callout_detail', 'is_verified', 'verified_by', 'created_at', 'updated_at']
    
    def get_winner(self, obj):
        winner = obj.winner
        if winner:
            return UserSerializer(winner).data
        return None
    
    def validate(self, attrs):
        # Validate that at least one time is provided
        challenger_time = attrs.get('challenger_time')
        challenged_time = attrs.get('challenged_time')
        
        if not challenger_time and not challenged_time:
            raise serializers.ValidationError("At least one race time must be provided")
        
        # Validate times are positive
        if challenger_time and challenger_time <= 0:
            raise serializers.ValidationError("Challenger time must be positive")
        if challenged_time and challenged_time <= 0:
            raise serializers.ValidationError("Challenged time must be positive")
        
        # Validate speeds are positive
        challenger_speed = attrs.get('challenger_speed')
        challenged_speed = attrs.get('challenged_speed')
        if challenger_speed and challenger_speed <= 0:
            raise serializers.ValidationError("Challenger speed must be positive")
        if challenged_speed and challenged_speed <= 0:
            raise serializers.ValidationError("Challenged speed must be positive")
        
        return attrs


# Car Serializers

class CarProfileSerializer(serializers.ModelSerializer):
    """Car profile serializer."""
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = CarProfile
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']


# Marketplace Serializers

class MarketplaceSerializer(serializers.ModelSerializer):
    """Marketplace serializer."""
    seller = UserSerializer(read_only=True)
    car = CarProfileSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Marketplace
        fields = '__all__'
        read_only_fields = ['seller', 'created_at', 'updated_at']
    
    def get_images(self, obj):
        return MarketplaceImageSerializer(obj.images.all(), many=True).data
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / reviews.count()
        return 0


class MarketplaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketplace
        fields = ['title', 'description', 'category', 'brand', 'model', 'year',
                 'condition', 'price', 'location', 'contact_info']


class MarketplaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceImage
        fields = '__all__'


class MarketplaceOrderSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    listing = MarketplaceSerializer(read_only=True)
    
    class Meta:
        model = MarketplaceOrder
        fields = '__all__'


class MarketplaceReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    listing = MarketplaceSerializer(read_only=True)
    
    class Meta:
        model = MarketplaceReview
        fields = '__all__'


# Social Serializers

class FriendshipSerializer(serializers.ModelSerializer):
    """Friendship serializer."""
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    
    class Meta:
        model = Friendship
        fields = '__all__'
        read_only_fields = ['from_user', 'created_at']


class FriendshipCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating friend requests."""
    to_username = serializers.CharField(write_only=True)
    
    class Meta:
        model = Friendship
        fields = ['to_username']
    
    def validate(self, attrs):
        to_username = attrs.get('to_username')
        try:
            to_user = User.objects.get(username=to_username)
            attrs['to_user'] = to_user
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        
        # Check if friend request already exists
        from_user = self.context['request'].user
        if Friendship.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise serializers.ValidationError("Friend request already sent")
        if Friendship.objects.filter(from_user=to_user, to_user=from_user).exists():
            raise serializers.ValidationError("Friend request already received from this user")
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('to_username')
        validated_data['from_user'] = self.context['request'].user
        return super().create(validated_data)


# Event Serializers
class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    track = TrackSerializer(read_only=True)
    participants_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = '__all__'
    
    def get_participants_count(self, obj):
        return obj.participants.count()


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_type', 'start_date', 'end_date', 
                 'max_participants', 'entry_fee', 'is_public', 'track']


class EventParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    
    class Meta:
        model = EventParticipant
        fields = '__all__'


# HotSpot Serializers
class HotSpotSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    distance = serializers.SerializerMethodField()
    
    class Meta:
        model = HotSpot
        fields = '__all__'
    
    def get_distance(self, obj):
        # This will be populated by the ViewSet when using location-based queries
        return getattr(obj, 'distance', None)


class HotSpotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSpot
        fields = ['name', 'description', 'address', 'city', 'state', 'zip_code',
                 'latitude', 'longitude', 'category', 'is_verified']


# Social Feature Serializers

class MessageSerializer(serializers.ModelSerializer):
    """Message serializer for direct messaging."""
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']


class UserPostSerializer(serializers.ModelSerializer):
    """User post serializer for social content."""
    author = UserSerializer(read_only=True)
    car = CarProfileSerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = UserPost
        fields = [
            'id', 'author', 'content', 'post_type', 'image', 'video', 
            'car', 'likes_count', 'comments_count', 'is_public', 
            'is_liked', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'likes_count', 'comments_count', 'created_at', 'updated_at']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


class PostCommentSerializer(serializers.ModelSerializer):
    """Post comment serializer."""
    author = UserSerializer(read_only=True)
    post = UserPostSerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = PostComment
        fields = ['id', 'author', 'post', 'content', 'likes_count', 'time_ago', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']
    
    def get_time_ago(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours}h ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes}m ago"
        else:
            return "Just now"


class FeedItemSerializer(serializers.ModelSerializer):
    """Feed item serializer for live feed."""
    author = UserSerializer(read_only=True)
    comments = PostCommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = UserPost
        fields = [
            'id', 'author', 'content', 'post_type', 'image', 'video',
            'likes_count', 'comments_count', 'is_liked', 'time_ago',
            'comments', 'created_at'
        ]
        read_only_fields = ['id', 'author', 'likes_count', 'comments_count', 'created_at']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False
    
    def get_time_ago(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours}h ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes}m ago"
        else:
            return "Just now"


class RacingCrewSerializer(serializers.ModelSerializer):
    """Racing crew serializer."""
    owner = UserSerializer(read_only=True)
    members_count = serializers.SerializerMethodField()
    
    class Meta:
        model = RacingCrew
        fields = ['id', 'name', 'description', 'owner', 'crew_type', 'location',
                 'members_count', 'is_public', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'members_count', 'created_at', 'updated_at']
    
    def get_members_count(self, obj):
        return getattr(obj, 'members_count', 0)


class CrewMembershipSerializer(serializers.ModelSerializer):
    """Crew membership serializer."""
    crew = RacingCrewSerializer(read_only=True)
    member = UserSerializer(read_only=True)
    
    class Meta:
        model = CrewMembership
        fields = ['id', 'crew', 'member', 'role', 'status', 'joined_at']
        read_only_fields = ['id', 'joined_at']


# Marketplace Feature Serializers

class MarketplaceListingSerializer(serializers.ModelSerializer):
    """Marketplace listing serializer."""
    seller = UserSerializer(read_only=True)
    category = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = MarketplaceListing
        fields = ['id', 'seller', 'title', 'description', 'category', 'price',
                 'condition', 'location', 'is_negotiable', 'images', 'created_at', 'updated_at']
        read_only_fields = ['id', 'seller', 'created_at', 'updated_at']
    
    def get_category(self, obj):
        if hasattr(obj, 'category') and obj.category:
            return obj.category.name
        return None
    
    def get_images(self, obj):
        if hasattr(obj, 'images'):
            return [img.image.url for img in obj.images.all()]
        return []


class CarListingSerializer(serializers.ModelSerializer):
    """Car listing serializer."""
    seller = UserSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = CarListing
        fields = ['id', 'seller', 'title', 'description', 'make', 'model', 'year',
                 'price', 'mileage', 'condition', 'location', 'is_negotiable',
                 'images', 'created_at', 'updated_at']
        read_only_fields = ['id', 'seller', 'created_at', 'updated_at']
    
    def get_images(self, obj):
        if hasattr(obj, 'images'):
            return [img.image.url for img in obj.images.all()]
        return []


class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer."""
    reviewer = UserSerializer(read_only=True)
    listing = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'listing', 'rating', 'title', 'content',
                 'is_verified_purchase', 'created_at']
        read_only_fields = ['id', 'reviewer', 'is_verified_purchase', 'created_at']
    
    def get_listing(self, obj):
        if hasattr(obj, 'listing') and obj.listing:
            return {
                'id': obj.listing.id,
                'title': obj.listing.title
            }
        return None


class RatingSerializer(serializers.ModelSerializer):
    """Rating serializer."""
    rater = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    
    class Meta:
        model = Rating
        fields = ['id', 'rater', 'seller', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'rater', 'created_at']


class PaymentTransactionSerializer(serializers.ModelSerializer):
    """Payment transaction serializer."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = PaymentTransaction
        fields = ['id', 'user', 'amount', 'transaction_type', 'status',
                 'payment_method', 'reference', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class UserWalletSerializer(serializers.ModelSerializer):
    """User wallet serializer."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserWallet
        fields = ['id', 'user', 'balance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer."""
    buyer = UserSerializer(read_only=True)
    items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'buyer', 'total_amount', 'status', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'buyer', 'created_at', 'updated_at']
    
    def get_items(self, obj):
        if hasattr(obj, 'items'):
            return [{'id': item.id, 'listing_title': item.listing.title, 'quantity': item.quantity} 
                   for item in obj.items.all()]
        return []


# Advanced Feature Serializers

class LocationBroadcastSerializer(serializers.ModelSerializer):
    """Location broadcast serializer."""
    user = UserSerializer(read_only=True)
    responses = serializers.SerializerMethodField()
    
    class Meta:
        model = LocationBroadcast
        fields = ['id', 'user', 'latitude', 'longitude', 'message', 'duration_minutes',
                 'expires_at', 'responses', 'created_at']
        read_only_fields = ['id', 'user', 'expires_at', 'created_at']
    
    def get_responses(self, obj):
        if hasattr(obj, 'responses'):
            return [{'user': response.user.username, 'message': response.message} 
                   for response in obj.responses.all()]
        return []


class OpenChallengeSerializer(serializers.ModelSerializer):
    """Open challenge serializer."""
    challenger = UserSerializer(read_only=True)
    track = TrackSerializer(read_only=True)
    responses_count = serializers.SerializerMethodField()
    
    class Meta:
        model = OpenChallenge
        fields = ['id', 'challenger', 'title', 'description', 'track', 'challenge_type',
                 'stakes', 'expires_at', 'status', 'responses_count', 'created_at']
        read_only_fields = ['id', 'challenger', 'responses_count', 'created_at']
    
    def get_responses_count(self, obj):
        return getattr(obj, 'responses_count', 0)


class ChallengeResponseSerializer(serializers.ModelSerializer):
    """Challenge response serializer."""
    challenge = OpenChallengeSerializer(read_only=True)
    responder = UserSerializer(read_only=True)
    
    class Meta:
        model = ChallengeResponse
        fields = ['id', 'challenge', 'responder', 'message', 'status', 'created_at']
        read_only_fields = ['id', 'responder', 'created_at']


class BetSerializer(serializers.ModelSerializer):
    """Bet serializer."""
    bettor = UserSerializer(read_only=True)
    pool = serializers.SerializerMethodField()
    
    class Meta:
        model = Bet
        fields = ['id', 'bettor', 'pool', 'predicted_winner', 'amount', 'created_at']
        read_only_fields = ['id', 'bettor', 'created_at']
    
    def get_pool(self, obj):
        if hasattr(obj, 'pool') and obj.pool:
            return {
                'id': obj.pool.id,
                'title': obj.pool.title
            }
        return None


class BettingPoolSerializer(serializers.ModelSerializer):
    """Betting pool serializer."""
    created_by = UserSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    total_bets = serializers.SerializerMethodField()
    
    class Meta:
        model = BettingPool
        fields = ['id', 'created_by', 'title', 'description', 'participants',
                 'total_pot', 'entry_fee', 'race_date', 'winner', 'total_bets', 'created_at']
        read_only_fields = ['id', 'created_by', 'total_bets', 'created_at']
    
    def get_total_bets(self, obj):
        return getattr(obj, 'total_bets', 0)


class BuildLogSerializer(serializers.ModelSerializer):
    """Build log serializer."""
    owner = UserSerializer(read_only=True)
    car = CarProfileSerializer(read_only=True)
    entries_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BuildLog
        fields = ['id', 'owner', 'car', 'title', 'description', 'entries_count',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'entries_count', 'created_at', 'updated_at']
    
    def get_entries_count(self, obj):
        return getattr(obj, 'entries_count', 0)


class BuildLogEntrySerializer(serializers.ModelSerializer):
    """Build log entry serializer."""
    build_log = BuildLogSerializer(read_only=True)
    
    class Meta:
        model = BuildMilestone
        fields = ['id', 'build_log', 'title', 'content', 'modifications', 'cost',
                 'hours_spent', 'images', 'created_at']
        read_only_fields = ['id', 'created_at']


class PerformanceDataSerializer(serializers.ModelSerializer):
    """Performance data serializer."""
    car = CarProfileSerializer(read_only=True)
    track = TrackSerializer(read_only=True)
    verified_by = UserSerializer(read_only=True)
    
    class Meta:
        model = PerformanceData
        fields = ['id', 'car', 'track', 'performance_type', 'time_seconds', 'speed_mph',
                 'reaction_time', 'sixty_foot_time', 'horsepower', 'torque',
                 'rpm_peak_hp', 'rpm_peak_torque', 'dyno_type', 'weather_conditions',
                 'track_conditions', 'date', 'notes', 'is_verified', 'verified_by', 'created_at']
        read_only_fields = ['id', 'is_verified', 'verified_by', 'created_at']


# Social Feed Serializers

class NotificationSerializer(serializers.ModelSerializer):
    """Notification serializer for social feed."""
    sender = UserSerializer(read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'sender', 'notification_type', 'title', 'message',
            'is_read', 'related_object_id', 'time_ago', 'created_at'
        ]
        read_only_fields = ['id', 'sender', 'created_at']
    
    def get_time_ago(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours}h ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes}m ago"
        else:
            return "Just now" 