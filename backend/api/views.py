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
    CarImage, UserPost, PostComment
)
from .serializers import (
    UserSerializer, UserProfileSerializer, TrackSerializer, EventSerializer,
    CalloutSerializer, CalloutDetailSerializer, RaceResultSerializer,
    MarketplaceSerializer, MarketplaceDetailSerializer, EventParticipantSerializer,
    EventDetailSerializer, FriendshipSerializer, MessageSerializer,
    CarProfileSerializer, CarModificationSerializer, CarImageSerializer,
    UserPostSerializer, PostCommentSerializer, UserProfileDetailSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'car_make', 'car_model']
    search_fields = ['user__username', 'bio', 'location']
    ordering_fields = ['wins', 'losses', 'total_races', 'created_at']

    def get_queryset(self):
        if self.action == 'list':
            return UserProfile.objects.select_related('user')
        return UserProfile.objects.all()

    @action(detail=True, methods=['post'])
    def update_stats(self, request, pk=None):
        profile = self.get_object()
        # Logic to update race statistics
        return Response({'message': 'Stats updated'})


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.filter(is_active=True)
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['track_type', 'surface_type']
    search_fields = ['name', 'location', 'description']


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event_type', 'track', 'organizer', 'is_public']
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'end_date', 'created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        return EventSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'])
    def join_event(self, request, pk=None):
        event = self.get_object()
        user = request.user
        
        if EventParticipant.objects.filter(event=event, user=user).exists():
            return Response({'error': 'Already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        EventParticipant.objects.create(event=event, user=user)
        return Response({'message': 'Successfully joined event'})

    @action(detail=True, methods=['post'])
    def leave_event(self, request, pk=None):
        event = self.get_object()
        user = request.user
        
        try:
            participant = EventParticipant.objects.get(event=event, user=user)
            participant.delete()
            return Response({'message': 'Successfully left event'})
        except EventParticipant.DoesNotExist:
            return Response({'error': 'Not registered for this event'}, status=status.HTTP_400_BAD_REQUEST)


class CalloutViewSet(viewsets.ModelViewSet):
    queryset = Callout.objects.all()
    serializer_class = CalloutSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'location_type', 'race_type', 'challenger', 'challenged']
    search_fields = ['message']
    ordering_fields = ['created_at', 'scheduled_date']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CalloutDetailSerializer
        return CalloutSerializer

    def get_queryset(self):
        user = self.request.user
        return Callout.objects.filter(
            models.Q(challenger=user) | models.Q(challenged=user)
        )

    def perform_create(self, serializer):
        serializer.save(challenger=self.request.user)

    @action(detail=True, methods=['post'])
    def accept_callout(self, request, pk=None):
        callout = self.get_object()
        if callout.challenged != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        callout.status = 'accepted'
        callout.save()
        return Response({'message': 'Callout accepted'})

    @action(detail=True, methods=['post'])
    def decline_callout(self, request, pk=None):
        callout = self.get_object()
        if callout.challenged != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        callout.status = 'declined'
        callout.save()
        return Response({'message': 'Callout declined'})

    @action(detail=True, methods=['post'])
    def complete_race(self, request, pk=None):
        callout = self.get_object()
        if callout.status != 'accepted':
            return Response({'error': 'Callout must be accepted first'}, status=status.HTTP_400_BAD_REQUEST)
        
        winner_id = request.data.get('winner_id')
        if not winner_id:
            return Response({'error': 'Winner ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            winner = User.objects.get(id=winner_id)
            if winner not in [callout.challenger, callout.challenged]:
                return Response({'error': 'Invalid winner'}, status=status.HTTP_400_BAD_REQUEST)
            
            callout.status = 'completed'
            callout.winner = winner
            callout.save()
            
            # Update user profiles
            loser = callout.challenged if winner == callout.challenger else callout.challenger
            
            winner_profile = winner.profile
            winner_profile.wins += 1
            winner_profile.total_races += 1
            winner_profile.save()
            
            loser_profile = loser.profile
            loser_profile.losses += 1
            loser_profile.total_races += 1
            loser_profile.save()
            
            return Response({'message': 'Race completed'})
        except User.DoesNotExist:
            return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)


class RaceResultViewSet(viewsets.ModelViewSet):
    queryset = RaceResult.objects.all()
    serializer_class = RaceResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['winner', 'loser']
    ordering_fields = ['completed_at']


class MarketplaceViewSet(viewsets.ModelViewSet):
    queryset = Marketplace.objects.filter(is_active=True)
    serializer_class = MarketplaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'condition', 'seller', 'trade_offered']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'views']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MarketplaceDetailSerializer
        return MarketplaceSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_listings(self, request):
        queryset = self.queryset.filter(seller=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EventParticipantViewSet(viewsets.ModelViewSet):
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'user', 'is_confirmed']


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def contact_form(request):
    """
    Handle contact form submissions and send email notifications
    """
    try:
        name = request.data.get('name')
        email = request.data.get('email')
        subject = request.data.get('subject')
        message = request.data.get('message')
        
        if not all([name, email, subject, message]):
            return Response({
                'error': 'All fields are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Email content
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
            fail_silently=False,
        )
        
        # Send confirmation email to user
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
        
        send_mail(
            subject=confirmation_subject,
            message=confirmation_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        
        return Response({
            'message': 'Thank you for your message! We\'ll get back to you soon.'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'There was an error sending your message. Please try again.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    User login endpoint - supports email usernames
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Try to authenticate with the provided username
    user = authenticate(username=username, password=password)
    
    if user:
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
    User registration endpoint - allows emails to be used as usernames
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
    
    # Check if username is an email
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
        return UserProfile.objects.select_related('user').prefetch_related('cars', 'posts') 