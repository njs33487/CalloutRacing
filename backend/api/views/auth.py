"""
Authentication and User Management Views

This module contains views for user authentication and profile management:
- UserViewSet: User search and management
- UserProfileViewSet: User profile CRUD operations
- UserProfileDetailViewSet: Detailed user profile views
- Authentication views: login, register, logout
- Email verification views
"""

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta
import uuid

from core.models.auth import User, UserProfile
from core.email_service import send_email_verification, send_welcome_email
from ..serializers import (
    UserSerializer, UserProfileSerializer, UserProfileDetailSerializer
)


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


class UserProfileDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """Detailed user profile viewset for public profile viewing."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location', 'car_make', 'car_model']
    search_fields = ['user__username', 'bio', 'location']

    def get_queryset(self):
        """Show all public profiles for detailed viewing."""
        return UserProfile.objects.all()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """User login endpoint."""
    # Add debugging
    print(f"Login request data: {request.data}")
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    print(f"Login attempt - username: {username}")
    
    if not username or not password:
        print("Missing username or password")
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    print(f"Authentication result - user: {user}")
    
    if user is None:
        print("Authentication failed - invalid credentials")
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check if email is verified
    print(f"Email verified: {user.email_verified}")
    # Temporarily bypass email verification for development
    # if not user.email_verified:
    #     print("Email not verified - blocking login")
    #     return Response({
    #         'error': 'Please verify your email before logging in',
    #         'email_verification_required': True
    #     }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Create or get token
    token, created = Token.objects.get_or_create(user=user)
    print(f"Login successful - user: {user.username}, token created: {created}")
    
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email_verified': user.email_verified
        }
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def check_user_exists(request):
    """Check if a username or email already exists."""
    username = request.data.get('username', '').strip()
    email = request.data.get('email', '').strip()
    
    if not username and not email:
        return Response({
            'error': 'Username or email is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    exists = False
    field = None
    
    if username:
        if User.objects.filter(username=username).exists():
            exists = True
            field = 'username'
    
    if email and not exists:
        if User.objects.filter(email=email).exists():
            exists = True
            field = 'email'
    
    return Response({
        'exists': exists,
        'field': field,
        'message': f'{field.capitalize()} already exists' if exists and field else f'{field.capitalize()} is available' if field else 'Available'
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """User registration endpoint with robust error logging."""
    # Add debugging
    print(f"Register request data: {request.data}")
    
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')

    print(f"Extracted data - username: {username}, email: {email}, first_name: {first_name}, last_name: {last_name}")

    if not username or not email or not password:
        print("Missing required fields")
        return Response({
            'error': 'Username, email, and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Check for existing users and provide detailed feedback
    existing_errors = {}
    
    # Check if username already exists
    if User.objects.filter(username=username).exists():
        print(f"Username {username} already exists")
        existing_errors['username'] = f'The username "{username}" is already taken. Please choose a different username.'
    
    # Check if email already exists
    if User.objects.filter(email=email).exists():
        print(f"Email {email} already exists")
        existing_errors['email'] = f'The email "{email}" is already registered. Please use a different email or try logging in.'
    
    # If there are existing user errors, return them
    if existing_errors:
        return Response({
            'error': 'User already exists',
            'details': existing_errors,
            'suggestion': 'If you already have an account, please try logging in instead.'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email_verified=False
        )
        # Generate verification token
        user.email_verification_token = uuid.uuid4()
        user.email_verification_expires_at = timezone.now() + timedelta(hours=24)
        user.save()
        print(f"User created successfully: {user.username}")
    except Exception as e:
        print(f"Failed to create user: {str(e)}")
        return Response({
            'error': f'Failed to create user: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    email_sent = True
    warning = None
    # Send verification email
    try:
        send_email_verification(user)
        user.email_verification_sent_at = timezone.now()
        user.save()
    except Exception as e:
        print(f"Failed to send verification email: {e}")
        email_sent = False
        warning = f"Failed to send verification email: {str(e)}. Please contact support if you do not receive an email."

    # Send welcome email
    try:
        send_welcome_email(user)
    except Exception as e:
        print(f"Failed to send welcome email: {e}")
        if not warning:
            warning = f"Failed to send welcome email: {str(e)}. Please contact support if you do not receive an email."

    if email_sent:
        message = "Account created successfully. A verification email has been sent to your address. Please check your inbox."
    else:
        message = "Account created successfully, but there was a problem sending the verification email. Please contact support if you do not receive an email."

    response = {
        'message': message,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email_verified': user.email_verified
        }
    }
    if warning:
        response['warning'] = warning

    return Response(response, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """User logout endpoint."""
    try:
        # Delete the user's token
        request.user.auth_token.delete()
    except:
        pass
    
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """Get current user's profile."""
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = None
    
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email_verified': user.email_verified
        },
        'profile': UserProfileSerializer(profile).data if profile else None
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def verify_email(request, token):
    """Verify user email with token."""
    try:
        user = User.objects.get(email_verification_token=token)
        
        # Check if token is expired
        if user.email_verification_expires_at and user.email_verification_expires_at < timezone.now():
            return Response({
                'error': 'Verification token has expired. Please request a new one.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark email as verified
        user.email_verified = True
        user.email_verification_token = None
        user.email_verification_expires_at = None
        user.save()
        
        return Response({
            'message': 'Email verified successfully. You can now log in.'
        })
        
    except User.DoesNotExist:
        return Response({
            'error': 'Invalid verification token'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def resend_verification_email(request):
    """Resend email verification."""
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        
        if user.email_verified:
            return Response({
                'error': 'Email is already verified'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate new verification token
        user.email_verification_token = uuid.uuid4()
        user.email_verification_expires_at = timezone.now() + timedelta(hours=24)
        user.save()
        
        # Send verification email
        try:
            send_email_verification(user)
            user.email_verification_sent_at = timezone.now()
            user.save()
            
            return Response({
                'message': 'Verification email sent successfully'
            })
            
        except Exception as e:
            return Response({
                'error': 'Failed to send verification email'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except User.DoesNotExist:
        return Response({
            'error': 'User with this email does not exist'
        }, status=status.HTTP_400_BAD_REQUEST) 