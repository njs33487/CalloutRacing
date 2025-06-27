from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import (
    UserProfile, Track, Event, Callout, RaceResult, 
    Marketplace, MarketplaceImage, EventParticipant,
    Friendship, Message, CarProfile, CarModification, 
    CarImage, UserPost, PostComment
)
from django.db import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    win_rate = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    organizer = UserSerializer(read_only=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_participant_count(self, obj):
        return obj.participants.count()


class CalloutSerializer(serializers.ModelSerializer):
    challenger = UserSerializer(read_only=True)
    challenged = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    track = TrackSerializer(read_only=True)

    class Meta:
        model = Callout
        fields = '__all__'
        read_only_fields = ['challenger', 'created_at', 'updated_at']


class RaceResultSerializer(serializers.ModelSerializer):
    callout = CalloutSerializer(read_only=True)
    winner = UserSerializer(read_only=True)
    loser = UserSerializer(read_only=True)

    class Meta:
        model = RaceResult
        fields = '__all__'


class MarketplaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceImage
        fields = '__all__'


class MarketplaceSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    images = MarketplaceImageSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Marketplace
        fields = '__all__'
        read_only_fields = ['seller', 'views', 'created_at', 'updated_at']

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return MarketplaceImageSerializer(primary_image).data
        return None


class EventParticipantSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = EventParticipant
        fields = '__all__'
        read_only_fields = ['user', 'registration_date']


# Nested serializers for detailed views
class CalloutDetailSerializer(CalloutSerializer):
    result = RaceResultSerializer(read_only=True)


class EventDetailSerializer(EventSerializer):
    participants = EventParticipantSerializer(many=True, read_only=True)
    callouts = CalloutSerializer(many=True, read_only=True)


class MarketplaceDetailSerializer(MarketplaceSerializer):
    pass


# New serializers for social features
class FriendshipSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = '__all__'
        read_only_fields = ['sender', 'created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'created_at']


class CarModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModification
        fields = '__all__'


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = '__all__'


class CarProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    modifications = CarModificationSerializer(many=True, read_only=True)
    images = CarImageSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = CarProfile
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return CarImageSerializer(primary_image).data
        return None


class PostCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class UserPostSerializer(serializers.ModelSerializer):
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
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


# Enhanced user profile serializer with social features
class UserProfileDetailSerializer(UserProfileSerializer):
    cars = CarProfileSerializer(many=True, read_only=True)
    posts = UserPostSerializer(many=True, read_only=True)
    friends_count = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()
    friendship_status = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_friends_count(self, obj):
        return Friendship.objects.filter(
            sender=obj.user, status='accepted'
        ).count() + Friendship.objects.filter(
            receiver=obj.user, status='accepted'
        ).count()

    def get_is_friend(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Friendship.objects.filter(
                (models.Q(sender=request.user, receiver=obj.user) |
                 models.Q(sender=obj.user, receiver=request.user)),
                status='accepted'
            ).exists()
        return False

    def get_friendship_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            friendship = Friendship.objects.filter(
                (models.Q(sender=request.user, receiver=obj.user) |
                 models.Q(sender=obj.user, receiver=request.user))
            ).first()
            if friendship:
                return friendship.status
        return None 