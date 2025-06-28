"""
Django REST Framework API Views for CalloutRacing Application

This module contains all the API views for the CalloutRacing application, including:
- User management and authentication
- Racing events and callouts
- Marketplace functionality
- Social features (friends, messages, posts)
- Car profiles and modifications

All views use Django REST Framework ViewSets for consistent API patterns.
"""

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from rest_framework.authtoken.models import Token
from core.models import (
    UserProfile, Track, Event, Callout, RaceResult, 
    Marketplace, MarketplaceImage, EventParticipant,
    Friendship, Message, CarProfile, CarModification, 
    CarImage, UserPost, PostComment, Subscription, Payment, UserWallet,
    MarketplaceOrder, MarketplaceReview, Bet, BettingPool, Notification,
    ContactSubmission, HotSpot, RacingCrew, CrewMembership, LocationBroadcast,
    ReputationRating, OpenChallenge, ChallengeResponse
)
from .serializers import (
    UserSerializer, UserProfileSerializer, TrackSerializer, EventSerializer,
    CalloutSerializer, CalloutDetailSerializer, RaceResultSerializer,
    MarketplaceSerializer, MarketplaceDetailSerializer, EventParticipantSerializer,
    EventDetailSerializer, FriendshipSerializer, MessageSerializer,
    CarProfileSerializer, CarModificationSerializer, CarImageSerializer,
    UserPostSerializer, PostCommentSerializer, UserProfileDetailSerializer,
    SubscriptionSerializer, PaymentSerializer, UserWalletSerializer,
    MarketplaceOrderSerializer, MarketplaceReviewSerializer, BetSerializer,
    BettingPoolSerializer, NotificationSerializer, SubscriptionPlanSerializer,
    HotSpotSerializer, RacingCrewSerializer, CrewMembershipSerializer,
    LocationBroadcastSerializer, ReputationRatingSerializer, OpenChallengeSerializer,
    ChallengeResponseSerializer
)
from django.utils import timezone
from datetime import timedelta
import math


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for User model.
    
    Provides search functionality for users by username, first_name, and last_name.
    Only authenticated users can access this endpoint.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserProfile model.
    
    Handles CRUD operations for user profiles with filtering, searching, and ordering.
    Includes custom actions for updating race statistics and profile images.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'car_make', 'car_model']
    search_fields = ['user__username', 'bio', 'location']
    ordering_fields = ['wins', 'losses', 'total_races', 'created_at']

    def get_queryset(self):
        """Users can only see their own profile or public profiles."""
        user = self.request.user
        if self.action == 'list':
            # For list view, show all profiles (could be filtered by privacy settings later)
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=user)

    def perform_create(self, serializer):
        """Set the user when creating a profile."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def update_stats(self, request, pk=None):
        """Update race statistics for a profile."""
        profile = self.get_object()
        
        # Ensure user can only update their own stats
        if profile.user != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        wins = request.data.get('wins', profile.wins)
        losses = request.data.get('losses', profile.losses)
        total_races = request.data.get('total_races', profile.total_races)
        
        profile.wins = wins
        profile.losses = losses
        profile.total_races = total_races
        profile.save()
        
        return Response({
            'wins': profile.wins,
            'losses': profile.losses,
            'total_races': profile.total_races,
            'win_rate': profile.win_rate
        })

    @action(detail=True, methods=['post'])
    def upload_profile_picture(self, request, pk=None):
        """Upload a profile picture."""
        profile = self.get_object()
        
        # Ensure user can only update their own profile
        if profile.user != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES['image']
        
        # Validate file type
        if not image_file.content_type.startswith('image/'):
            return Response({'error': 'File must be an image'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate file size (max 5MB)
        if image_file.size > 5 * 1024 * 1024:
            return Response({'error': 'Image file too large (max 5MB)'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the image
        profile.profile_picture = image_file
        profile.save()
        
        return Response({
            'profile_picture': profile.profile_picture.url if profile.profile_picture else None
        })

    @action(detail=True, methods=['post'])
    def upload_cover_photo(self, request, pk=None):
        """Upload a cover photo."""
        profile = self.get_object()
        
        # Ensure user can only update their own profile
        if profile.user != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES['image']
        
        # Validate file type
        if not image_file.content_type.startswith('image/'):
            return Response({'error': 'File must be an image'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate file size (max 10MB for cover photos)
        if image_file.size > 10 * 1024 * 1024:
            return Response({'error': 'Image file too large (max 10MB)'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the image
        profile.cover_photo = image_file
        profile.save()
        
        return Response({
            'cover_photo': profile.cover_photo.url if profile.cover_photo else None
        })

    @action(detail=True, methods=['delete'])
    def remove_profile_picture(self, request, pk=None):
        """Remove profile picture."""
        profile = self.get_object()
        
        # Ensure user can only update their own profile
        if profile.user != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if profile.profile_picture:
            profile.profile_picture.delete(save=False)
            profile.profile_picture = None
            profile.save()
        
        return Response({'message': 'Profile picture removed'})

    @action(detail=True, methods=['delete'])
    def remove_cover_photo(self, request, pk=None):
        """Remove cover photo."""
        profile = self.get_object()
        
        # Ensure user can only update their own profile
        if profile.user != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if profile.cover_photo:
            profile.cover_photo.delete(save=False)
            profile.cover_photo = None
            profile.save()
        
        return Response({'message': 'Cover photo removed'})


class TrackViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Track model.
    
    Handles CRUD operations for racing tracks with filtering and search capabilities.
    Only active tracks are returned by default.
    """
    queryset = Track.objects.filter(is_active=True)
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['track_type', 'surface_type']
    search_fields = ['name', 'location', 'description']


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Event model.
    
    Handles CRUD operations for racing events with custom actions for joining/leaving events.
    Only active events are returned by default.
    """
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event_type', 'track', 'organizer', 'is_public']
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'end_date', 'created_at']

    def get_serializer_class(self):
        """
        Use detailed serializer for retrieve actions to include related data.
        """
        if self.action == 'retrieve':
            return EventDetailSerializer
        return EventSerializer

    def perform_create(self, serializer):
        """
        Automatically set the current user as the event organizer.
        """
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'])
    def join_event(self, request, pk=None):
        """
        Custom action to allow users to join an event.
        
        Args:
            request: HTTP request object
            pk: Primary key of the event
            
        Returns:
            Response with success/error message
        """
        event = self.get_object()
        user = request.user
        
        # Check if user is already registered
        if EventParticipant.objects.filter(event=event, user=user).exists():
            return Response({'error': 'Already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create new participant record
        EventParticipant.objects.create(event=event, user=user)
        return Response({'message': 'Successfully joined event'})

    @action(detail=True, methods=['post'])
    def leave_event(self, request, pk=None):
        """
        Custom action to allow users to leave an event.
        
        Args:
            request: HTTP request object
            pk: Primary key of the event
            
        Returns:
            Response with success/error message
        """
        event = self.get_object()
        user = request.user
        
        try:
            participant = EventParticipant.objects.get(event=event, user=user)
            participant.delete()
            return Response({'message': 'Successfully left event'})
        except EventParticipant.DoesNotExist:
            return Response({'error': 'Not registered for this event'}, status=status.HTTP_400_BAD_REQUEST)


class CalloutViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Callout model.
    
    Provides CRUD operations for race callouts between users.
    """
    queryset = Callout.objects.all()
    serializer_class = CalloutSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter callouts based on user participation and privacy."""
        user = self.request.user
        
        # Get callouts where user is challenger, challenged, or in a crew
        queryset = Callout.objects.filter(
            models.Q(challenger=user) |
            models.Q(challenged=user) |
            models.Q(crew__members=user) |
            models.Q(is_private=False)
        ).distinct()
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by location type
        location_type = self.request.query_params.get('location_type', None)
        if location_type:
            queryset = queryset.filter(location_type=location_type)
        
        # Filter by race type
        race_type = self.request.query_params.get('race_type', None)
        if race_type:
            queryset = queryset.filter(race_type=race_type)
        
        # Filter by experience level
        experience_level = self.request.query_params.get('experience_level', None)
        if experience_level:
            queryset = queryset.filter(experience_level=experience_level)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set the challenger when creating a callout."""
        serializer.save(challenger=self.request.user)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a callout."""
        callout = self.get_object()
        
        if callout.challenged != request.user:
            return Response({'error': 'Not authorized'}, status=403)
        
        if callout.status != 'pending':
            return Response({'error': 'Callout already processed'}, status=400)
        
        callout.status = 'accepted'
        callout.save()
        
        return Response({'status': 'Callout accepted'})
    
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        """Decline a callout."""
        callout = self.get_object()
        
        if callout.challenged != request.user:
            return Response({'error': 'Not authorized'}, status=403)
        
        if callout.status != 'pending':
            return Response({'error': 'Callout already processed'}, status=400)
        
        callout.status = 'declined'
        callout.save()
        
        return Response({'status': 'Callout declined'})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a callout as completed with winner."""
        callout = self.get_object()
        winner_id = request.data.get('winner_id')
        
        if not winner_id:
            return Response({'error': 'winner_id required'}, status=400)
        
        if callout.challenger != request.user and callout.challenged != request.user:
            return Response({'error': 'Not authorized'}, status=403)
        
        if callout.status != 'accepted':
            return Response({'error': 'Callout must be accepted first'}, status=400)
        
        try:
            winner = User.objects.get(id=winner_id)
            if winner not in [callout.challenger, callout.challenged]:
                return Response({'error': 'Winner must be a participant'}, status=400)
        except User.DoesNotExist:
            return Response({'error': 'Winner not found'}, status=404)
        
        callout.status = 'completed'
        callout.winner = winner
        callout.save()
        
        # Update user stats
        winner_profile = winner.profile
        loser_profile = (callout.challenged if winner == callout.challenger else callout.challenger).profile
        
        winner_profile.wins += 1
        winner_profile.total_races += 1
        winner_profile.save()
        
        loser_profile.losses += 1
        loser_profile.total_races += 1
        loser_profile.save()
        
        return Response({'status': 'Callout completed'})


class RaceResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RaceResult model.
    
    Handles CRUD operations for race results with filtering and ordering capabilities.
    """
    queryset = RaceResult.objects.all()
    serializer_class = RaceResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['winner', 'loser']
    ordering_fields = ['completed_at']


class MarketplaceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Marketplace model.
    
    Handles CRUD operations for marketplace listings with filtering, searching,
    and ordering. Includes view tracking and custom actions for user's own listings.
    """
    queryset = Marketplace.objects.filter(is_active=True)
    serializer_class = MarketplaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'condition', 'seller', 'trade_offered']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'views']

    def get_serializer_class(self):
        """
        Use detailed serializer for retrieve actions to include related data.
        """
        if self.action == 'retrieve':
            return MarketplaceDetailSerializer
        return MarketplaceSerializer

    def perform_create(self, serializer):
        """
        Automatically set the current user as the seller.
        """
        serializer.save(seller=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to increment view count when a listing is viewed.
        """
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_listings(self, request):
        """
        Custom action to get current user's marketplace listings.
        
        Returns:
            List of marketplace items created by the current user
        """
        queryset = self.queryset.filter(seller=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EventParticipantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for EventParticipant model.
    
    Handles CRUD operations for event participants with filtering capabilities.
    """
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'user', 'is_confirmed']


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def contact_form(request):
    """
    Handle contact form submissions and send email notifications.
    
    This endpoint allows anyone to submit a contact form. It sends an email
    to the admin and a confirmation email to the user.
    
    Args:
        request: HTTP request object containing name, email, subject, and message
        
    Returns:
        Response with success/error message
    """
    try:
        name = request.data.get('name')
        email = request.data.get('email')
        subject = request.data.get('subject')
        message = request.data.get('message')
        
        # Validate required fields
        if not all([name, email, subject, message]):
            return Response({
                'error': 'All fields are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if email is configured
        email_configured = (
            settings.EMAIL_HOST_USER and 
            settings.EMAIL_HOST_PASSWORD and 
            settings.DEFAULT_FROM_EMAIL
        )
        
        if email_configured:
            try:
                # Prepare email content for admin notification
                email_subject = f"CalloutRacing Contact: {subject}"
                email_body = f"""
New contact form submission from CalloutRacing:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This message was sent from the CalloutRacing contact form.
                """
                
                # Send email to admin
                send_mail(
                    subject=email_subject,
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['digibin@digitalbinarysolutionsllc.com'],
                    fail_silently=True,  # Don't fail if email sending fails
                )
                
                # Prepare confirmation email for user
                confirmation_subject = "Thank you for contacting CalloutRacing"
                confirmation_body = f"""
Dear {name},

Thank you for reaching out to CalloutRacing! We have received your message and will get back to you within 24 hours.

Your message:
Subject: {subject}
Message: {message}

Best regards,
The CalloutRacing Team
                """
                
                # Send confirmation email to user
                send_mail(
                    subject=confirmation_subject,
                    message=confirmation_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,  # Don't fail if email sending fails
                )
                
            except Exception as email_error:
                # Log email error but don't fail the request
                print(f"Email sending failed: {email_error}")
        
        # Store contact form submission in database for admin review
        try:
            ContactSubmission.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
        except Exception as db_error:
            # Log database error but don't fail the request
            print(f"Database storage failed: {db_error}")
        
        return Response({
            'message': 'Thank you for your message! We\'ll get back to you soon.'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Contact form error: {e}")
        return Response({
            'error': 'There was an error sending your message. Please try again.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    User login endpoint - supports email usernames.
    
    Authenticates users and returns a token for API access.
    
    Args:
        request: HTTP request object containing username and password
        
    Returns:
        Response with authentication token and user data
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Validate required fields
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Try to authenticate with the provided username
    user = authenticate(username=username, password=password)
    
    if user:
        # Get or create authentication token
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })
    else:
        return Response({
            'error': 'Invalid username or password'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """
    User registration endpoint - allows emails to be used as usernames.
    
    Creates new user accounts with validation for unique usernames and emails.
    
    Args:
        request: HTTP request object containing user registration data
        
    Returns:
        Response with authentication token and user data
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    
    # Validate required fields
    if not all([username, email, password]):
        return Response({
            'error': 'Username, email, and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if username is an email format
    import re
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    is_email_username = email_pattern.match(username) is not None
    
    # If username is an email, ensure it matches the email field
    if is_email_username and username != email:
        return Response({
            'error': 'If using email as username, it must match the email field'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user already exists (by username or email)
    if User.objects.filter(username=username).exists():
        return Response({
            'username': ['A user with this username already exists.']
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if email is already used by another user
    if User.objects.filter(email=email).exists():
        return Response({
            'email': ['A user with this email already exists.']
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Create user
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        # Generate token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': 'Registration failed. Please try again.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    User logout endpoint
    """
    try:
        # Delete the token
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'})
    except:
        return Response({'message': 'Successfully logged out'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """
    Get current user profile
    """
    try:
        profile = request.user.profile
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            },
            'profile': {
                'bio': profile.bio,
                'location': profile.location,
                'car_make': profile.car_make,
                'car_model': profile.car_model,
                'car_year': profile.car_year,
                'wins': profile.wins,
                'losses': profile.losses,
                'total_races': profile.total_races,
            }
        })
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'Profile not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def stats_view(request):
    """Get basic stats for the platform"""
    stats = {
        'total_users': User.objects.count(),
        'total_tracks': Track.objects.filter(is_active=True).count(),
        'total_events': Event.objects.filter(is_active=True).count(),
        'total_callouts': Callout.objects.count(),
        'total_marketplace_items': Marketplace.objects.filter(is_active=True).count(),
    }
    return Response(stats)


# New social feature viewsets
class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user)
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'])
    def accept_friend_request(self, request, pk=None):
        friendship = self.get_object()
        if friendship.receiver != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        friendship.status = 'accepted'
        friendship.save()
        return Response({'message': 'Friend request accepted'})

    @action(detail=True, methods=['post'])
    def decline_friend_request(self, request, pk=None):
        friendship = self.get_object()
        if friendship.receiver != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        friendship.status = 'declined'
        friendship.save()
        return Response({'message': 'Friend request declined'})

    @action(detail=True, methods=['post'])
    def block_user(self, request, pk=None):
        friendship = self.get_object()
        if friendship.receiver != request.user and friendship.sender != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        friendship.status = 'blocked'
        friendship.save()
        return Response({'message': 'User blocked'})

    @action(detail=False, methods=['get'])
    def my_friends(self, request):
        """Get list of accepted friends"""
        user = request.user
        friends = Friendship.objects.filter(
            (models.Q(sender=user) | models.Q(receiver=user)),
            status='accepted'
        )
        serializer = self.get_serializer(friends, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending_requests(self, request):
        """Get pending friend requests received"""
        user = request.user
        pending = Friendship.objects.filter(receiver=user, status='pending')
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def friends(self, request):
        """Get list of accepted friends with user details"""
        user = request.user
        friendships = Friendship.objects.filter(
            (models.Q(sender=user) | models.Q(receiver=user)),
            status='accepted'
        ).select_related('sender__profile', 'receiver__profile')
        
        friends = []
        for friendship in friendships:
            if friendship.sender == user:
                friends.append(friendship.receiver)
            else:
                friends.append(friendship.sender)
        
        from .serializers import UserSerializer
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sent_requests(self, request):
        """Get sent friend requests"""
        user = request.user
        sent = Friendship.objects.filter(sender=user, status='pending').select_related('receiver__profile')
        serializer = self.get_serializer(sent, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def send_request(self, request):
        """Send a friend request"""
        receiver_id = request.data.get('receiver')
        if not receiver_id:
            return Response({'error': 'receiver ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if receiver == request.user:
            return Response({'error': 'Cannot send friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if friendship already exists
        existing_friendship = Friendship.objects.filter(
            (models.Q(sender=request.user, receiver=receiver) |
             models.Q(sender=receiver, receiver=request.user))
        ).first()
        
        if existing_friendship:
            if existing_friendship.status == 'accepted':
                return Response({'error': 'Already friends'}, status=status.HTTP_400_BAD_REQUEST)
            elif existing_friendship.status == 'pending':
                return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
            elif existing_friendship.status == 'blocked':
                return Response({'error': 'Cannot send request to blocked user'}, status=status.HTTP_400_BAD_REQUEST)
        
        friendship = Friendship.objects.create(
            sender=request.user,
            receiver=receiver,
            status='pending'
        )
        serializer = self.get_serializer(friendship)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a friend request"""
        friendship = self.get_object()
        if friendship.receiver != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if friendship.status != 'pending':
            return Response({'error': 'Request is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        
        friendship.status = 'accepted'
        friendship.save()
        return Response({'message': 'Friend request accepted'})

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        """Decline a friend request"""
        friendship = self.get_object()
        if friendship.receiver != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if friendship.status != 'pending':
            return Response({'error': 'Request is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        
        friendship.status = 'declined'
        friendship.save()
        return Response({'message': 'Friend request declined'})

    @action(detail=False, methods=['delete'])
    def remove_friend(self, request, user_id=None):
        """Remove a friend"""
        try:
            friend = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        friendship = Friendship.objects.filter(
            (models.Q(sender=request.user, receiver=friend) |
             models.Q(sender=friend, receiver=request.user)),
            status='accepted'
        ).first()
        
        if not friendship:
            return Response({'error': 'Not friends with this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        friendship.delete()
        return Response({'message': 'Friend removed'})


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['receiver', 'is_read']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user)
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        if message.receiver != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        message.is_read = True
        message.save()
        return Response({'message': 'Message marked as read'})

    @action(detail=False, methods=['get'])
    def conversation(self, request):
        """Get conversation with a specific user"""
        other_user_id = request.query_params.get('user_id')
        if not other_user_id:
            return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            other_user = User.objects.get(id=other_user_id)
            messages = Message.objects.filter(
                (models.Q(sender=request.user, receiver=other_user) |
                 models.Q(sender=other_user, receiver=request.user))
            ).order_by('created_at')
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread messages"""
        count = Message.objects.filter(receiver=request.user, is_read=False).count()
        return Response({'unread_count': count})


class CarProfileViewSet(viewsets.ModelViewSet):
    queryset = CarProfile.objects.filter(is_active=True)
    serializer_class = CarProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['make', 'model', 'year', 'fuel_type', 'drivetrain']
    search_fields = ['name', 'make', 'model', 'description']
    ordering_fields = ['created_at', 'horsepower', 'best_quarter_mile']

    def get_queryset(self):
        if self.action == 'list':
            return CarProfile.objects.filter(is_active=True).select_related('user')
        return CarProfile.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_cars(self, request):
        """Get current user's cars"""
        cars = CarProfile.objects.filter(user=request.user, is_active=True)
        serializer = self.get_serializer(cars, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_primary(self, request, pk=None):
        """Set a car as primary"""
        car = self.get_object()
        if car.user != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        # Remove primary from other cars
        CarProfile.objects.filter(user=request.user).update(is_primary=False)
        # Set this car as primary
        car.is_primary = True
        car.save()
        return Response({'message': 'Car set as primary'})


class CarModificationViewSet(viewsets.ModelViewSet):
    queryset = CarModification.objects.all()
    serializer_class = CarModificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'car', 'is_installed']
    search_fields = ['name', 'brand', 'description']

    def perform_create(self, serializer):
        car_id = self.request.data.get('car_id')
        if car_id:
            try:
                car = CarProfile.objects.get(id=car_id, user=self.request.user)
                serializer.save(car=car)
            except CarProfile.DoesNotExist:
                return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)


class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['car', 'is_primary']

    def perform_create(self, serializer):
        car_id = self.request.data.get('car_id')
        if car_id:
            try:
                car = CarProfile.objects.get(id=car_id, user=self.request.user)
                serializer.save(car=car)
            except CarProfile.DoesNotExist:
                return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)


class UserPostViewSet(viewsets.ModelViewSet):
    queryset = UserPost.objects.all()
    serializer_class = UserPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'car']
    ordering_fields = ['created_at', 'like_count']

    def get_queryset(self):
        if self.action == 'list':
            return UserPost.objects.select_related('user', 'car').prefetch_related('likes')
        return UserPost.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like_post(self, request, pk=None):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({'message': 'Post unliked'})
        else:
            post.likes.add(request.user)
            return Response({'message': 'Post liked'})

    @action(detail=False, methods=['get'])
    def feed(self, request):
        """Get posts from friends and followed users"""
        user = request.user
        
        # Get friends
        friends = Friendship.objects.filter(
            (models.Q(sender=user) | models.Q(receiver=user)),
            status='accepted'
        )
        friend_ids = []
        for friendship in friends:
            if friendship.sender == user:
                friend_ids.append(friendship.receiver.id)
            else:
                friend_ids.append(friendship.sender.id)
        
        # Get posts from friends and self
        friend_ids.append(user.id)
        posts = UserPost.objects.filter(user__id__in=friend_ids).select_related('user', 'car').prefetch_related('likes')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post', 'user']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Enhanced user profile viewset
class UserProfileDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location', 'car_make', 'car_model']
    search_fields = ['user__username', 'bio', 'location']

    def get_queryset(self):
        """
        Optimize queryset for detail view by using select_related and prefetch_related.
        """
        return UserProfile.objects.select_related('user').prefetch_related(
            'cars', 'cars__modifications', 'cars__images', 'posts', 'posts__comments'
        )


# ============================================================================
# PAYMENT & SUBSCRIPTION VIEWSETS
# ============================================================================

class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Subscription model.
    
    Handles CRUD operations for user subscriptions with custom actions
    for managing subscription status and billing.
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['subscription_type', 'status']
    ordering_fields = ['created_at', 'next_billing_date']

    def get_queryset(self):
        """Only show user's own subscriptions."""
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically set the current user."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel_subscription(self, request, pk=None):
        """Cancel a subscription."""
        subscription = self.get_object()
        subscription.status = 'cancelled'
        subscription.save()
        return Response({'message': 'Subscription cancelled successfully'})

    @action(detail=True, methods=['post'])
    def reactivate_subscription(self, request, pk=None):
        """Reactivate a cancelled subscription."""
        subscription = self.get_object()
        subscription.status = 'active'
        subscription.save()
        return Response({'message': 'Subscription reactivated successfully'})


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Payment model.
    
    Handles CRUD operations for payment transactions with custom actions
    for payment processing and refunds.
    """
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['payment_type', 'status', 'payment_provider']
    ordering_fields = ['created_at', 'amount']

    def get_queryset(self):
        """Only show user's own payments."""
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically set the current user."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        """Process a pending payment."""
        payment = self.get_object()
        # TODO: Integrate with payment provider (Stripe, PayPal, etc.)
        payment.status = 'completed'
        payment.save()
        return Response({'message': 'Payment processed successfully'})

    @action(detail=True, methods=['post'])
    def refund_payment(self, request, pk=None):
        """Refund a completed payment."""
        payment = self.get_object()
        # TODO: Process refund through payment provider
        payment.status = 'refunded'
        payment.save()
        return Response({'message': 'Payment refunded successfully'})


class UserWalletViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserWallet model.
    
    Handles wallet operations including deposits, withdrawals,
    and balance management.
    """
    serializer_class = UserWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Only show user's own wallet."""
        return UserWallet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically set the current user."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_funds(self, request, pk=None):
        """Add funds to wallet."""
        wallet = self.get_object()
        amount = request.data.get('amount')
        description = request.data.get('description', 'Deposit')
        
        if not amount or float(amount) <= 0:
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)
        
        wallet.add_funds(float(amount), description)
        return Response({'message': f'${amount} added to wallet', 'new_balance': wallet.balance})

    @action(detail=True, methods=['post'])
    def withdraw_funds(self, request, pk=None):
        """Withdraw funds from wallet."""
        wallet = self.get_object()
        amount = request.data.get('amount')
        description = request.data.get('description', 'Withdrawal')
        
        if not amount or float(amount) <= 0:
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)
        
        if wallet.deduct_funds(float(amount), description):
            return Response({'message': f'${amount} withdrawn from wallet', 'new_balance': wallet.balance})
        else:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def transaction_history(self, request, pk=None):
        """Get wallet transaction history."""
        wallet = self.get_object()
        transactions = Payment.objects.filter(user=wallet.user).order_by('-created_at')
        serializer = WalletTransactionSerializer(transactions, many=True)
        return Response(serializer.data)


# ============================================================================
# ENHANCED MARKETPLACE VIEWSETS
# ============================================================================

class MarketplaceOrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for MarketplaceOrder model.
    
    Handles CRUD operations for marketplace orders with custom actions
    for order management and tracking.
    """
    serializer_class = MarketplaceOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'seller', 'buyer']
    ordering_fields = ['created_at', 'total_amount']

    def get_queryset(self):
        """Show orders where user is buyer or seller."""
        return MarketplaceOrder.objects.filter(
            models.Q(buyer=self.request.user) | models.Q(seller=self.request.user)
        )

    def perform_create(self, serializer):
        """Automatically set the current user as buyer."""
        serializer.save(buyer=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        """Mark order as paid."""
        order = self.get_object()
        if order.seller != self.request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        order.status = 'paid'
        order.paid_at = timezone.now()
        order.save()
        return Response({'message': 'Order marked as paid'})

    @action(detail=True, methods=['post'])
    def ship_order(self, request, pk=None):
        """Mark order as shipped."""
        order = self.get_object()
        if order.seller != self.request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        tracking_number = request.data.get('tracking_number')
        order.status = 'shipped'
        order.tracking_number = tracking_number
        order.shipped_at = timezone.now()
        order.save()
        return Response({'message': 'Order marked as shipped'})

    @action(detail=True, methods=['post'])
    def mark_as_delivered(self, request, pk=None):
        """Mark order as delivered."""
        order = self.get_object()
        if order.buyer != self.request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        order.status = 'delivered'
        order.delivered_at = timezone.now()
        order.save()
        return Response({'message': 'Order marked as delivered'})

    @action(detail=False, methods=['get'])
    def my_purchases(self, request):
        """Get user's purchase history."""
        purchases = MarketplaceOrder.objects.filter(buyer=request.user).order_by('-created_at')
        serializer = self.get_serializer(purchases, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_sales(self, request):
        """Get user's sales history."""
        sales = MarketplaceOrder.objects.filter(seller=request.user).order_by('-created_at')
        serializer = self.get_serializer(sales, many=True)
        return Response(serializer.data)


class MarketplaceReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for MarketplaceReview model.
    
    Handles CRUD operations for marketplace reviews with custom actions
    for review management.
    """
    serializer_class = MarketplaceReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rating', 'is_verified_purchase']
    ordering_fields = ['created_at', 'rating', 'helpful_votes']

    def get_queryset(self):
        """Show reviews where user is reviewer or seller."""
        return MarketplaceReview.objects.filter(
            models.Q(reviewer=self.request.user) | 
            models.Q(order__seller=self.request.user)
        )

    def perform_create(self, serializer):
        """Automatically set the current user as reviewer."""
        serializer.save(reviewer=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_helpful(self, request, pk=None):
        """Mark review as helpful."""
        review = self.get_object()
        review.helpful_votes += 1
        review.save()
        return Response({'message': 'Review marked as helpful'})


# ============================================================================
# BETTING VIEWSETS
# ============================================================================

class BetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Bet model.
    
    Handles CRUD operations for bets with custom actions
    for bet management and settlement.
    """
    serializer_class = BetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['bet_type', 'status', 'callout', 'event']
    ordering_fields = ['created_at', 'bet_amount', 'potential_payout']

    def get_queryset(self):
        """Only show user's own bets."""
        return Bet.objects.filter(bettor=self.request.user)

    def perform_create(self, serializer):
        """Automatically set the current user as bettor."""
        serializer.save(bettor=self.request.user)

    @action(detail=True, methods=['post'])
    def place_bet(self, request, pk=None):
        """Place a bet on a race."""
        bet = self.get_object()
        
        # Check if user has sufficient funds
        wallet = UserWallet.objects.get_or_create(user=request.user)[0]
        if not wallet.can_afford(bet.bet_amount):
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Deduct funds and activate bet
        wallet.deduct_funds(bet.bet_amount, f"Bet on {bet.selected_winner.username}")
        bet.status = 'active'
        bet.save()
        
        return Response({'message': 'Bet placed successfully'})

    @action(detail=True, methods=['post'])
    def cancel_bet(self, request, pk=None):
        """Cancel a pending bet."""
        bet = self.get_object()
        if bet.status != 'pending':
            return Response({'error': 'Cannot cancel active bet'}, status=status.HTTP_400_BAD_REQUEST)
        
        bet.status = 'cancelled'
        bet.save()
        return Response({'message': 'Bet cancelled successfully'})

    @action(detail=False, methods=['get'])
    def betting_history(self, request):
        """Get user's betting history."""
        bets = Bet.objects.filter(bettor=request.user).order_by('-created_at')
        serializer = BettingHistorySerializer(bets, many=True)
        return Response(serializer.data)


class BettingPoolViewSet(viewsets.ModelViewSet):
    """
    ViewSet for BettingPool model.
    
    Handles CRUD operations for betting pools with custom actions
    for pool management and odds calculation.
    """
    serializer_class = BettingPoolSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_settled', 'callout', 'event']
    ordering_fields = ['created_at', 'total_pool']

    def get_queryset(self):
        """Show active betting pools."""
        return BettingPool.objects.filter(is_active=True)

    @action(detail=True, methods=['get'])
    def odds(self, request, pk=None):
        """Get current odds for all participants."""
        pool = self.get_object()
        odds_data = {}
        
        # Calculate odds for each participant
        if pool.callout:
            participants = [pool.callout.challenger, pool.callout.challenged]
        elif pool.event:
            participants = [participant.user for participant in pool.event.participants.all()]
        else:
            return Response({'error': 'No participants found'}, status=status.HTTP_400_BAD_REQUEST)
        
        for participant in participants:
            odds_data[participant.username] = pool.calculate_odds(participant)
        
        return Response(odds_data)

    @action(detail=True, methods=['post'])
    def close_pool(self, request, pk=None):
        """Close betting pool before race starts."""
        pool = self.get_object()
        pool.close_pool()
        return Response({'message': 'Betting pool closed'})

    @action(detail=True, methods=['post'])
    def settle_pool(self, request, pk=None):
        """Settle betting pool after race completion."""
        pool = self.get_object()
        winner_id = request.data.get('winner_id')
        
        if not winner_id:
            return Response({'error': 'Winner ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            winner = User.objects.get(id=winner_id)
            pool.settle_pool(winner)
            return Response({'message': 'Betting pool settled'})
        except User.DoesNotExist:
            return Response({'error': 'Winner not found'}, status=status.HTTP_400_BAD_REQUEST)


# ============================================================================
# NOTIFICATION VIEWSET
# ============================================================================

class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Notification model.
    
    Handles CRUD operations for user notifications with custom actions
    for notification management.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'is_read']
    ordering_fields = ['created_at']

    def get_queryset(self):
        """Only show user's own notifications."""
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically set the current user."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark notification as read."""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read."""
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message': 'All notifications marked as read'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications."""
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})


# ============================================================================
# SUBSCRIPTION PLANS API
# ============================================================================

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def subscription_plans(request):
    """
    Get available subscription plans.
    
    Returns a list of available subscription plans with pricing and features.
    """
    plans = [
        {
            'plan_type': 'basic',
            'name': 'Basic Plan',
            'price': 9.99,
            'currency': 'USD',
            'features': [
                'Basic race tracking',
                'Limited marketplace access',
                'Standard support'
            ],
            'is_popular': False,
            'is_current': False
        },
        {
            'plan_type': 'premium',
            'name': 'Premium Plan',
            'price': 19.99,
            'currency': 'USD',
            'features': [
                'Advanced race analytics',
                'Full marketplace access',
                'Priority support',
                'Custom car profiles',
                'Betting features'
            ],
            'is_popular': True,
            'is_current': False
        },
        {
            'plan_type': 'pro',
            'name': 'Pro Plan',
            'price': 39.99,
            'currency': 'USD',
            'features': [
                'All Premium features',
                'Event organization',
                'Advanced betting pools',
                'API access',
                'Dedicated support'
            ],
            'is_popular': False,
            'is_current': False
        }
    ]
    
    # Check user's current subscription
    current_subscription = Subscription.objects.filter(
        user=request.user, 
        status='active'
    ).first()
    
    if current_subscription:
        for plan in plans:
            if plan['plan_type'] == current_subscription.subscription_type:
                plan['is_current'] = True
                break
    
    serializer = SubscriptionPlanSerializer(plans, many=True)
    return Response(serializer.data)


# Add these new viewsets after the existing viewsets

class HotSpotViewSet(viewsets.ModelViewSet):
    """
    API endpoint for HotSpot model.
    
    Provides CRUD operations for racing hot spots including tracks,
    street meet points, and popular racing locations.
    """
    queryset = HotSpot.objects.all()
    serializer_class = HotSpotSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter hot spots based on query parameters."""
        queryset = HotSpot.objects.filter(is_active=True)
        
        # Filter by spot type
        spot_type = self.request.query_params.get('spot_type', None)
        if spot_type:
            queryset = queryset.filter(spot_type=spot_type)
        
        # Filter by location (city/state)
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        state = self.request.query_params.get('state', None)
        if state:
            queryset = queryset.filter(state__icontains=state)
        
        # Filter by verification status
        is_verified = self.request.query_params.get('is_verified', None)
        if is_verified is not None:
            queryset = queryset.filter(is_verified=is_verified.lower() == 'true')
        
        return queryset.order_by('-is_verified', '-total_races', 'name')
    
    def perform_create(self, serializer):
        """Set the creator when creating a new hot spot."""
        serializer.save(created_by=self.request.user)


class RacingCrewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for RacingCrew model.
    
    Provides CRUD operations for racing crews and car clubs.
    """
    queryset = RacingCrew.objects.all()
    serializer_class = RacingCrewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter crews based on user membership and privacy settings."""
        user = self.request.user
        
        # Get crews the user owns, admins, or is a member of
        user_crews = RacingCrew.objects.filter(
            models.Q(owner=user) |
            models.Q(admins=user) |
            models.Q(members=user)
        )
        
        # Get public crews
        public_crews = RacingCrew.objects.filter(is_private=False)
        
        # Combine and remove duplicates
        queryset = (user_crews | public_crews).distinct()
        
        # Filter by crew type
        crew_type = self.request.query_params.get('crew_type', None)
        if crew_type:
            queryset = queryset.filter(crew_type=crew_type)
        
        return queryset.order_by('-member_count', 'name')
    
    def perform_create(self, serializer):
        """Set the owner when creating a new crew."""
        crew = serializer.save(owner=self.request.user)
        # Add creator as admin and member
        crew.admins.add(self.request.user)
        crew.members.add(self.request.user)
        crew.member_count = crew.members.count()
        crew.save()


class CrewMembershipViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CrewMembership model.
    
    Manages crew memberships and invitations.
    """
    queryset = CrewMembership.objects.all()
    serializer_class = CrewMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter memberships based on user's crews."""
        user = self.request.user
        
        # Get memberships for crews the user owns or admins
        return CrewMembership.objects.filter(
            models.Q(crew__owner=user) |
            models.Q(crew__admins=user)
        ).order_by('-joined_at')
    
    @action(detail=True, methods=['post'])
    def accept_invitation(self, request, pk=None):
        """Accept a crew invitation."""
        membership = self.get_object()
        
        if membership.user != request.user:
            return Response({'error': 'Not authorized'}, status=403)
        
        if membership.status != 'pending':
            return Response({'error': 'Invitation already processed'}, status=400)
        
        membership.status = 'active'
        membership.save()
        
        # Add user to crew members
        crew = membership.crew
        crew.members.add(request.user)
        crew.member_count = crew.members.count()
        crew.save()
        
        return Response({'status': 'Invitation accepted'})
    
    @action(detail=True, methods=['post'])
    def decline_invitation(self, request, pk=None):
        """Decline a crew invitation."""
        membership = self.get_object()
        
        if membership.user != request.user:
            return Response({'error': 'Not authorized'}, status=403)
        
        if membership.status != 'pending':
            return Response({'error': 'Invitation already processed'}, status=400)
        
        membership.status = 'declined'
        membership.save()
        
        return Response({'status': 'Invitation declined'})


class LocationBroadcastViewSet(viewsets.ModelViewSet):
    """
    API endpoint for LocationBroadcast model.
    
    Manages real-time location broadcasting for "I'm Here, Who's There?" feature.
    """
    queryset = LocationBroadcast.objects.all()
    serializer_class = LocationBroadcastSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter broadcasts based on location and activity."""
        queryset = LocationBroadcast.objects.filter(is_active=True)
        
        # Filter by hot spot
        hot_spot_id = self.request.query_params.get('hot_spot', None)
        if hot_spot_id:
            queryset = queryset.filter(hot_spot_id=hot_spot_id)
        
        # Filter by location radius (basic implementation)
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)
        radius = self.request.query_params.get('radius', 10)  # Default 10 miles
        
        if lat and lng:
            # Simple distance filtering (can be enhanced with proper geospatial queries)
            lat, lng = float(lat), float(lng)
            radius = float(radius)
            
            # Basic bounding box filter (approximate)
            lat_range = radius / 69  # Rough miles to degrees conversion
            lng_range = radius / (69 * math.cos(math.radians(lat)))
            
            queryset = queryset.filter(
                latitude__range=(lat - lat_range, lat + lat_range),
                longitude__range=(lng - lng_range, lng + lng_range)
            )
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set the user and expiration when creating a broadcast."""
        # Set expiration to 2 hours from now
        expires_at = timezone.now() + timedelta(hours=2)
        serializer.save(user=self.request.user, expires_at=expires_at)
    
    @action(detail=False, methods=['post'])
    def deactivate_all(self, request):
        """Deactivate all active broadcasts for the current user."""
        LocationBroadcast.objects.filter(
            user=request.user,
            is_active=True
        ).update(is_active=False)
        
        return Response({'status': 'All broadcasts deactivated'})


class ReputationRatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ReputationRating model.
    
    Manages sportsmanship and reputation ratings between users.
    """
    queryset = ReputationRating.objects.all()
    serializer_class = ReputationRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter ratings based on user relationships."""
        user = self.request.user
        
        # Get ratings given by or received by the user
        return ReputationRating.objects.filter(
            models.Q(rater=user) | models.Q(rated_user=user)
        ).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set the rater when creating a rating."""
        serializer.save(rater=self.request.user)
    
    @action(detail=False, methods=['get'])
    def user_stats(self, request):
        """Get reputation statistics for a user."""
        user_id = request.query_params.get('user_id', None)
        if not user_id:
            return Response({'error': 'user_id required'}, status=400)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        
        ratings = ReputationRating.objects.filter(rated_user=user)
        
        if not ratings.exists():
            return Response({
                'user_id': user.id,
                'username': user.username,
                'average_ratings': {
                    'punctuality': 0,
                    'rule_adherence': 0,
                    'sportsmanship': 0,
                    'overall': 0
                },
                'total_ratings': 0
            })
        
        stats = {
            'user_id': user.id,
            'username': user.username,
            'average_ratings': {
                'punctuality': ratings.aggregate(avg=models.Avg('punctuality'))['punctuality__avg'],
                'rule_adherence': ratings.aggregate(avg=models.Avg('rule_adherence'))['rule_adherence__avg'],
                'sportsmanship': ratings.aggregate(avg=models.Avg('sportsmanship'))['sportsmanship__avg'],
                'overall': ratings.aggregate(avg=models.Avg('overall'))['overall__avg']
            },
            'total_ratings': ratings.count()
        }
        
        return Response(stats)


class OpenChallengeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for OpenChallenge model.
    
    Manages public open challenges for racing.
    """
    queryset = OpenChallenge.objects.all()
    serializer_class = OpenChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter challenges based on various criteria."""
        queryset = OpenChallenge.objects.filter(is_active=True)
        
        # Filter by challenge type
        challenge_type = self.request.query_params.get('challenge_type', None)
        if challenge_type:
            queryset = queryset.filter(challenge_type=challenge_type)
        
        # Filter by location
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Filter by horsepower requirements
        min_hp = self.request.query_params.get('min_horsepower', None)
        if min_hp:
            queryset = queryset.filter(min_horsepower__lte=min_hp)
        
        max_hp = self.request.query_params.get('max_horsepower', None)
        if max_hp:
            queryset = queryset.filter(max_horsepower__gte=max_hp)
        
        # Filter by scheduled date
        scheduled_after = self.request.query_params.get('scheduled_after', None)
        if scheduled_after:
            queryset = queryset.filter(scheduled_date__gte=scheduled_after)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set the challenger when creating a new challenge."""
        serializer.save(challenger=self.request.user)
    
    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        """Respond to an open challenge."""
        challenge = self.get_object()
        status = request.data.get('status', 'interested')
        message = request.data.get('message', '')
        
        # Check if user already responded
        existing_response = ChallengeResponse.objects.filter(
            challenge=challenge,
            responder=request.user
        ).first()
        
        if existing_response:
            existing_response.status = status
            existing_response.message = message
            existing_response.save()
            return Response({'status': 'Response updated'})
        
        # Create new response
        ChallengeResponse.objects.create(
            challenge=challenge,
            responder=request.user,
            status=status,
            message=message
        )
        
        return Response({'status': 'Response submitted'})
    
    @action(detail=True, methods=['get'])
    def responses(self, request, pk=None):
        """Get all responses for a challenge."""
        challenge = self.get_object()
        responses = ChallengeResponse.objects.filter(challenge=challenge)
        serializer = ChallengeResponseSerializer(responses, many=True)
        return Response(serializer.data)


class ChallengeResponseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ChallengeResponse model.
    
    Manages responses to open challenges.
    """
    queryset = ChallengeResponse.objects.all()
    serializer_class = ChallengeResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter responses based on user's challenges and responses."""
        user = self.request.user
        
        # Get responses to challenges created by the user
        # and responses made by the user
        return ChallengeResponse.objects.filter(
            models.Q(challenge__challenger=user) | models.Q(responder=user)
        ).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set the responder when creating a response."""
        serializer.save(responder=self.request.user) 