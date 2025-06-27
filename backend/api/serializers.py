from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import (
    UserProfile, Track, Event, Callout, RaceResult, 
    Marketplace, MarketplaceImage, EventParticipant
)


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