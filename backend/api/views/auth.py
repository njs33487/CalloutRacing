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
# Removed Token import since we're not using authtoken anymore
from django.utils import timezone
from datetime import timedelta
import uuid
from django.core.management import call_command
from django.http import JsonResponse
import pyotp
import qrcode
import base64
import io
import secrets
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from core.models.auth import User
from core.models.auth import UserProfile
from core.models.social import Follow, Block
from core.email_service import (
    send_email_verification, send_welcome_email, 
    verify_email_token, resend_verification_email,
    send_password_reset_email, verify_password_reset_token, reset_password_with_token
)

from ..serializers import (
    UserSerializer, UserProfileSerializer
)

from core.otp_service import OTPService
import re


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

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Get current user's profile."""
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='username/(?P<username>[^/.]+)', permission_classes=[permissions.AllowAny])
    def by_username(self, request, username=None):
        """Get profile by username (public access)."""
        try:
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='username/(?P<username>[^/.]+)/edit', permission_classes=[permissions.IsAuthenticated])
    def edit_by_username(self, request, username=None):
        """Get profile for editing (only if owner)."""
        try:
            user = User.objects.get(username=username)
            if user != request.user:
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            
            profile = UserProfile.objects.get(user=user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk=None):
        """Follow a user."""
        profile = self.get_object()
        if profile.user == request.user:
            return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already following
        if Follow.objects.filter(follower=request.user, following=profile.user).exists():
            return Response({'error': 'Already following this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if blocked
        if Block.objects.filter(blocker=request.user, blocked=profile.user).exists():
            return Response({'error': 'Cannot follow blocked user'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Block.objects.filter(blocker=profile.user, blocked=request.user).exists():
            return Response({'error': 'Cannot follow user who has blocked you'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create follow relationship
        Follow.objects.create(follower=request.user, following=profile.user)
        
        # Create notification
        from core.models.social import Notification
        Notification.objects.create(
            recipient=profile.user,
            sender=request.user,
            notification_type='follow',
            title='New Follower',
            message=f'{request.user.username} started following you'
        )
        
        return Response({
            'message': f'Successfully followed {profile.user.username}',
            'following': True
        })

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unfollow(self, request, pk=None):
        """Unfollow a user."""
        profile = self.get_object()
        if profile.user == request.user:
            return Response({'error': 'Cannot unfollow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if following
        follow_obj = Follow.objects.filter(follower=request.user, following=profile.user).first()
        if not follow_obj:
            return Response({'error': 'Not following this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove follow relationship
        follow_obj.delete()
        
        return Response({
            'message': f'Successfully unfollowed {profile.user.username}',
            'following': False
        })

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def block(self, request, pk=None):
        """Block a user."""
        profile = self.get_object()
        if profile.user == request.user:
            return Response({'error': 'Cannot block yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already blocked
        if Block.objects.filter(blocker=request.user, blocked=profile.user).exists():
            return Response({'error': 'Already blocking this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove any existing follow relationships
        Follow.objects.filter(follower=request.user, following=profile.user).delete()
        Follow.objects.filter(follower=profile.user, following=request.user).delete()
        
        # Create block relationship
        reason = request.data.get('reason', '')
        Block.objects.create(blocker=request.user, blocked=profile.user, reason=reason)
        
        return Response({
            'message': f'Successfully blocked {profile.user.username}',
            'blocked': True
        })

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unblock(self, request, pk=None):
        """Unblock a user."""
        profile = self.get_object()
        if profile.user == request.user:
            return Response({'error': 'Cannot unblock yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if blocking
        block_obj = Block.objects.filter(blocker=request.user, blocked=profile.user).first()
        if not block_obj:
            return Response({'error': 'Not blocking this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove block relationship
        block_obj.delete()
        
        return Response({
            'message': f'Successfully unblocked {profile.user.username}',
            'blocked': False
        })

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def followers(self, request, pk=None):
        """Get list of followers for a profile."""
        profile = self.get_object()
        followers = Follow.objects.filter(following=profile.user).select_related('follower')
        
        data = []
        for follow in followers:
            data.append({
                'id': follow.follower.id,
                'username': follow.follower.username,
                'followed_at': follow.created_at
            })
        
        return Response({'followers': data})

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def following(self, request, pk=None):
        """Get list of users that this profile is following."""
        profile = self.get_object()
        following = Follow.objects.filter(follower=profile.user).select_related('following')
        
        data = []
        for follow in following:
            data.append({
                'id': follow.following.id,
                'username': follow.following.username,
                'followed_at': follow.created_at
            })
        
        return Response({'following': data})

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def is_following(self, request, pk=None):
        """Check if current user is following this profile."""
        profile = self.get_object()
        is_following = Follow.objects.filter(
            follower=request.user, 
            following=profile.user
        ).exists()
        
        return Response({'is_following': is_following})

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def is_blocked(self, request, pk=None):
        """Check if current user is blocked by this profile."""
        profile = self.get_object()
        is_blocked = Block.objects.filter(
            blocker=profile.user, 
            blocked=request.user
        ).exists()
        
        return Response({'is_blocked': is_blocked})

    @action(detail=True, methods=['post'])
    def update_stats(self, request, pk=None):
        """Update race statistics for a profile."""
        profile = self.get_object()
        
        # Ensure user can only update their own stats
        if profile.user != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        wins = int(request.data.get('wins', profile.wins))
        losses = int(request.data.get('losses', profile.losses))
        total_races = int(request.data.get('total_races', profile.total_races))
        
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


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """User login endpoint."""
    # Add debugging
    print(f"Login request data: {request.data}")
    print(f"Request user: {request.user}")
    print(f"Request user is authenticated: {request.user.is_authenticated}")
    print(f"Request method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    print(f"CSRF Token in header: {request.headers.get('X-CSRFToken', 'NOT_FOUND')}")
    print(f"CSRF Token in cookies: {request.COOKIES.get('csrftoken', 'NOT_FOUND')}")
    print(f"Session ID in cookies: {request.COOKIES.get('sessionid', 'NOT_FOUND')}")
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    print(f"Login attempt - username: {username}")
    
    # If user is already authenticated, return success
    if request.user.is_authenticated:
        print("User is already authenticated, returning current user data")
        try:
            profile = request.user.profile
            email_verified = profile.email_verified
        except UserProfile.DoesNotExist:
            email_verified = False
        
        response_data = {
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email_verified': email_verified
            }
        }
        print(f"Response data for already authenticated user: {response_data}")
        return Response(response_data)
    
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
    try:
        profile = user.profile
        if not profile.email_verified:
            return Response({
                'error': 'Please verify your email address before logging in. Check your email for a verification link.',
                'email_verification_required': True
            }, status=status.HTTP_401_UNAUTHORIZED)
    except UserProfile.DoesNotExist:
        # If no profile exists, allow login (backward compatibility)
        pass
    
    # Create session - this is crucial for session authentication
    from django.contrib.auth import login
    login(request, user)
    
    # Get email verification status
    try:
        profile = user.profile
        email_verified = profile.email_verified
    except UserProfile.DoesNotExist:
        email_verified = False
    
    response_data = {
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email_verified': email_verified
        }
    }
    print(f"Response data: {response_data}")
    
    return Response(response_data)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def check_user_exists(request):
    """Check if a username or email already exists."""
    # Add debugging
    print(f"Check user exists request data: {request.data}")
    print(f"Request method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    print(f"CSRF Token in header: {request.headers.get('X-CSRFToken', 'NOT_FOUND')}")
    print(f"CSRF Token in cookies: {request.COOKIES.get('csrftoken', 'NOT_FOUND')}")
    print(f"Session ID in cookies: {request.COOKIES.get('sessionid', 'NOT_FOUND')}")
    
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


@csrf_exempt
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
        # Create user with basic fields only
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        print(f"User created successfully: {user.username}")
    except Exception as e:
        print(f"Failed to create user: {str(e)}")
        return Response({
            'error': 'Failed to create user'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Create user profile
    try:
        UserProfile.objects.get_or_create(user=user)
        print(f"User profile created successfully for {user.username}")
    except Exception as e:
        print(f"Failed to create user profile: {str(e)}")
        # Continue anyway as profile is not critical for registration

    # Send email verification
    email_sent = True
    warning = None
    try:
        send_email_verification(user)
        print(f"Email verification sent to {user.email}")
    except Exception as e:
        print(f"Failed to send verification email: {e}")
        email_sent = False
        warning = f"Failed to send verification email: {str(e)}. Please contact support if you do not receive an email."

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
            'last_name': user.last_name
        }
    }
    if warning:
        response['warning'] = warning

    return Response(response, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """User logout endpoint."""
    # With session authentication, we don't need to delete tokens
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """Get current user's profile."""
    user = request.user
    print(f"User profile request - user: {user.username}, authenticated: {request.user.is_authenticated}")
    # Get user profile for email verification status
    try:
        profile = user.profile
        email_verified = profile.email_verified
    except UserProfile.DoesNotExist:
        email_verified = False
    
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email_verified': email_verified
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def setup_otp(request):
    """Setup OTP for user account."""
    user = request.user
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if profile.otp_enabled:
        return Response({
            'error': 'OTP is already enabled for this account'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate TOTP secret
    secret = pyotp.random_base32()
    profile.otp_secret = secret
    profile.save()
    
    # Generate QR code
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(
        name=user.email,
        issuer_name="CalloutRacing"
    )
    
    # Create QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # Generate backup codes
    backup_codes = [secrets.token_hex(4).upper() for _ in range(10)]
    profile.otp_backup_codes = backup_codes
    profile.save()
    
    return Response({
        'secret': secret,
        'qr_code': f"data:image/png;base64,{qr_code_base64}",
        'backup_codes': backup_codes,
        'message': 'Scan the QR code with your authenticator app and enter the code to verify setup.'
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_otp_setup(request):
    """Verify OTP setup with a code."""
    user = request.user
    code = request.data.get('code')
    
    if not code:
        return Response({
            'error': 'OTP code is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Get user profile
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'User profile not found'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not profile.otp_secret:
        return Response({
            'error': 'OTP setup not initiated'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify the code
    totp = pyotp.TOTP(profile.otp_secret)
    if totp.verify(code):
        profile.otp_enabled = True
        profile.save()
        
        return Response({
            'message': 'OTP setup completed successfully'
        })
    else:
        return Response({
            'error': 'Invalid OTP code'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def disable_otp(request):
    """Disable OTP for user account."""
    user = request.user
    code = request.data.get('code')
    
    # Get user profile
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'User profile not found'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not profile.otp_enabled:
        return Response({
            'error': 'OTP is not enabled for this account'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not code:
        return Response({
            'error': 'OTP code is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify the code
    totp = pyotp.TOTP(profile.otp_secret)
    if totp.verify(code):
        profile.otp_enabled = False
        profile.otp_secret = None
        profile.otp_backup_codes = []
        profile.save()
        
        return Response({
            'message': 'OTP disabled successfully'
        })
    else:
        return Response({
            'error': 'Invalid OTP code'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_otp_login(request):
    """Verify OTP code during login."""
    username = request.data.get('username')
    code = request.data.get('code')
    
    if not username or not code:
        return Response({
            'error': 'Username and OTP code are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username=username)
        profile = user.profile
        
        if not profile.otp_enabled:
            return Response({
                'error': 'OTP is not enabled for this account'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if it's a backup code
        if code in profile.otp_backup_codes:
            # Remove used backup code
            profile.otp_backup_codes.remove(code)
            profile.save()
            is_backup_code = True
        else:
            # Verify TOTP code
            totp = pyotp.TOTP(profile.otp_secret)
            if not totp.verify(code):
                return Response({
                    'error': 'Invalid OTP code'
                }, status=status.HTTP_400_BAD_REQUEST)
            is_backup_code = False
        
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
                'email_verified': profile.email_verified
            },
            'is_backup_code': is_backup_code
        })
        
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_backup_codes(request):
    """Generate new backup codes for OTP."""
    user = request.user
    
    # Get user profile
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'User profile not found'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not profile.otp_enabled:
        return Response({
            'error': 'OTP is not enabled for this account'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate new backup codes
    backup_codes = [secrets.token_hex(4).upper() for _ in range(10)]
    profile.otp_backup_codes = backup_codes
    profile.save()
    
    return Response({
        'backup_codes': backup_codes,
        'message': 'New backup codes generated successfully'
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def run_migrations(request):
    """Temporary endpoint to run migrations (for development only)."""
    try:
        call_command('migrate')
        return Response({
            'message': 'Migrations applied successfully'
        })
    except Exception as e:
        return Response({
            'error': 'Migration failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def test_auth(request):
    """Test endpoint to verify authentication is working."""
    print(f"Test auth request - user: {request.user.username}, authenticated: {request.user.is_authenticated}")
    return Response({
        'message': 'Authentication working',
        'user': request.user.username,
        'authenticated': request.user.is_authenticated
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):
    return Response({'message': 'CSRF cookie set'})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def verify_email(request, token):
    """Verify user email with token."""
    success, user, message = verify_email_token(token)
    
    if success:
        return Response({
            'message': message,
            'verified': True
        })
    else:
        return Response({
            'error': message,
            'verified': False
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def resend_verification_email_view(request):
    """Resend email verification."""
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    success, message = resend_verification_email(email)
    
    if success:
        return Response({
            'message': message
        })
    else:
        return Response({
            'error': message
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def request_password_reset(request):
    """Request password reset email."""
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        success = send_password_reset_email(user)
        
        if success:
            return Response({
                'message': 'Password reset email sent successfully'
            })
        else:
            return Response({
                'error': 'Failed to send password reset email'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except User.DoesNotExist:
        # Don't reveal if email exists or not for security
        return Response({
            'message': 'If an account with this email exists, a password reset email has been sent.'
        })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reset_password(request):
    """Reset password with token."""
    token = request.data.get('token')
    new_password = request.data.get('new_password')
    
    if not token or not new_password:
        return Response({'error': 'Token and new password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    success, message = reset_password_with_token(token, new_password)
    
    if success:
        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)


# OTP Authentication Views

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_otp(request):
    """Send OTP to phone number or email with enhanced security."""
    identifier = request.data.get('identifier')  # phone or email
    otp_type = request.data.get('type')  # 'phone' or 'email'
    purpose = request.data.get('purpose', 'login')  # 'login', 'signup', etc.
    
    if not identifier or not otp_type:
        return Response({
            'error': 'Identifier and type are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if otp_type not in ['phone', 'email']:
        return Response({
            'error': 'Type must be either "phone" or "email"'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate phone number format
    if otp_type == 'phone':
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not phone_pattern.match(identifier):
            return Response({
                'error': 'Invalid phone number format. Please enter a valid phone number.'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate email format
    if otp_type == 'email':
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(identifier):
            return Response({
                'error': 'Invalid email format. Please enter a valid email address.'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user exists with this identifier
    if otp_type == 'phone':
        try:
            user = User.objects.get(phone_number=identifier)
        except User.DoesNotExist:
            return Response({
                'error': 'No account found with this phone number. Please check the number or sign up.'
            }, status=status.HTTP_404_NOT_FOUND)
    else:  # email
        try:
            user = User.objects.get(email=identifier)
        except User.DoesNotExist:
            return Response({
                'error': 'No account found with this email address. Please check the email or sign up.'
            }, status=status.HTTP_404_NOT_FOUND)
    
    # Send OTP with enhanced security
    success, result = OTPService.send_otp(user, identifier, otp_type, purpose)
    
    if not success:
        return Response({
            'error': result  # result contains the error message
        }, status=status.HTTP_429_TOO_MANY_REQUESTS if 'rate limit' in result.lower() else status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Get rate limiting info for user feedback
    remaining_attempts = OTPService.get_remaining_attempts(identifier)
    resend_cooldown = OTPService.get_resend_cooldown_remaining(identifier)
    
    masked_identifier = OTPService._mask_identifier(identifier)
    
    return Response({
        'message': f'Verification code sent to {masked_identifier}',
        'type': otp_type,
        'purpose': purpose,
        'remaining_attempts': remaining_attempts,
        'resend_cooldown_seconds': resend_cooldown,
        'expires_in_minutes': 10
    }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_otp(request):
    """Verify OTP and authenticate user with enhanced security."""
    identifier = request.data.get('identifier')
    otp_code = request.data.get('otp_code')
    otp_type = request.data.get('type')
    purpose = request.data.get('purpose', 'login')
    
    if not identifier or not otp_code or not otp_type:
        return Response({
            'error': 'Identifier, OTP code, and type are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if otp_type not in ['phone', 'email']:
        return Response({
            'error': 'Type must be either "phone" or "email"'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate OTP code format
    if not otp_code.isdigit() or len(otp_code) != 6:
        return Response({
            'error': 'Invalid OTP code format. Please enter the 6-digit code.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Find user by identifier
    if otp_type == 'phone':
        try:
            user = User.objects.get(phone_number=identifier)
        except User.DoesNotExist:
            return Response({
                'error': 'No account found with this phone number.'
            }, status=status.HTTP_404_NOT_FOUND)
    else:  # email
        try:
            user = User.objects.get(email=identifier)
        except User.DoesNotExist:
            return Response({
                'error': 'No account found with this email address.'
            }, status=status.HTTP_404_NOT_FOUND)
    
    # Verify OTP with enhanced security
    success, message = OTPService.verify_otp(user, identifier, otp_code, otp_type, purpose)
    
    if not success:
        return Response({
            'error': message
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Mark phone as verified if it's a phone OTP
    if otp_type == 'phone' and not user.phone_verified:
        user.phone_verified = True
        user.save()
    
    # Log in the user
    from django.contrib.auth import login
    login(request, user)
    
    # Get user profile
    try:
        profile = UserProfile.objects.get(user=user)
        profile_data = UserProfileSerializer(profile).data
    except UserProfile.DoesNotExist:
        profile_data = None
    
    masked_identifier = OTPService._mask_identifier(identifier)
    
    return Response({
        'message': f'Successfully verified {otp_type} OTP',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'phone_verified': user.phone_verified,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_authenticated': True
        },
        'profile': profile_data,
        'verified_identifier': masked_identifier
    }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def phone_login(request):
    """Login with phone number and OTP with enhanced security."""
    phone_number = request.data.get('phone_number')
    
    if not phone_number:
        return Response({
            'error': 'Phone number is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate phone number format
    phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
    if not phone_pattern.match(phone_number):
        return Response({
            'error': 'Invalid phone number format. Please enter a valid phone number.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user exists
    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return Response({
            'error': 'No account found with this phone number. Please check the number or sign up.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Send OTP with enhanced security
    success, result = OTPService.send_otp(user, phone_number, 'phone', 'login')
    
    if not success:
        return Response({
            'error': result
        }, status=status.HTTP_429_TOO_MANY_REQUESTS if 'rate limit' in result.lower() else status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Get rate limiting info
    remaining_attempts = OTPService.get_remaining_attempts(phone_number)
    resend_cooldown = OTPService.get_resend_cooldown_remaining(phone_number)
    
    masked_phone = OTPService._mask_identifier(phone_number)
    
    return Response({
        'message': f'Verification code sent to {masked_phone}',
        'phone_number': phone_number,
        'remaining_attempts': remaining_attempts,
        'resend_cooldown_seconds': resend_cooldown,
        'expires_in_minutes': 10
    }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def email_login(request):
    """Login with email and OTP with enhanced security."""
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate email format
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(email):
        return Response({
            'error': 'Invalid email format. Please enter a valid email address.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user exists
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            'error': 'No account found with this email address. Please check the email or sign up.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Send OTP with enhanced security
    success, result = OTPService.send_otp(user, email, 'email', 'login')
    
    if not success:
        return Response({
            'error': result
        }, status=status.HTTP_429_TOO_MANY_REQUESTS if 'rate limit' in result.lower() else status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Get rate limiting info
    remaining_attempts = OTPService.get_remaining_attempts(email)
    resend_cooldown = OTPService.get_resend_cooldown_remaining(email)
    
    masked_email = OTPService._mask_identifier(email)
    
    return Response({
        'message': f'Verification code sent to {masked_email}',
        'email': email,
        'remaining_attempts': remaining_attempts,
        'resend_cooldown_seconds': resend_cooldown,
        'expires_in_minutes': 10
    }, status=status.HTTP_200_OK) 