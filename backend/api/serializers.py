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

from core.models.auth import User, UserProfile
from core.models.racing import Callout, Track, RaceResult
from core.models.cars import CarProfile
from core.models.marketplace import Marketplace
from core.models.social import Friendship

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer for public information."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'is_verified']
        read_only_fields = ['id', 'date_joined', 'is_verified']


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
    callout = CalloutSerializer(read_only=True)
    verified_by = UserSerializer(read_only=True)
    winner = serializers.SerializerMethodField()
    
    class Meta:
        model = RaceResult
        fields = [
            'id', 'callout', 'challenger_time', 'challenged_time',
            'challenger_speed', 'challenged_speed', 'challenger_reaction',
            'challenged_reaction', 'weather_conditions', 'track_conditions',
            'notes', 'is_verified', 'verified_by', 'winner', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'callout', 'is_verified', 'verified_by', 'created_at', 'updated_at']
    
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
    
    class Meta:
        model = Marketplace
        fields = '__all__'
        read_only_fields = ['seller', 'created_at', 'updated_at']


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