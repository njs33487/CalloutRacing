"""
Utility Views for CalloutRacing Application

This module contains utility views including:
- SSO authentication views (Google, Facebook)
- SSO configuration endpoint
- Stats and search views
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.authtoken.models import Token
import requests

from core.models import User, UserProfile


@api_view(['POST'])
@permission_classes([AllowAny])
def google_sso(request):
    """
    Google SSO authentication endpoint.
    
    Receives Google ID token from frontend and verifies it with Google.
    Creates or logs in user based on Google account.
    """
    id_token = request.data.get('id_token')
    
    if not id_token:
        return Response({
            'error': 'Google ID token is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Verify the token with Google
        google_response = requests.get(
            'https://oauth2.googleapis.com/tokeninfo',
            params={'id_token': id_token}
        )
        
        if google_response.status_code != 200:
            return Response({
                'error': 'Invalid Google token'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        google_data = google_response.json()
        
        # Extract user information from Google response
        google_user_id = google_data.get('sub')
        email = google_data.get('email')
        first_name = google_data.get('given_name', '')
        last_name = google_data.get('family_name', '')
        name = google_data.get('name', '')
        
        if not email:
            return Response({
                'error': 'Email not provided by Google'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Create new user
            username = email.split('@')[0]  # Use email prefix as username
            base_username = username
            counter = 1
            
            # Ensure unique username
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=None,  # No password for SSO users
                email_verified=True  # Google emails are verified
            )
            
            # Create user profile
            UserProfile.objects.create(user=user)
        
        # Generate or get token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email_verified': user.email_verified
            },
            'is_new_user': created
        })
        
    except requests.RequestException as e:
        return Response({
            'error': 'Failed to verify Google token'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({
            'error': 'Authentication failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def facebook_sso(request):
    """
    Facebook SSO authentication endpoint.
    
    Receives Facebook access token from frontend and verifies it with Facebook.
    Creates or logs in user based on Facebook account.
    """
    access_token = request.data.get('access_token')
    
    if not access_token:
        return Response({
            'error': 'Facebook access token is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Verify the token with Facebook
        facebook_response = requests.get(
            'https://graph.facebook.com/me',
            params={
                'access_token': access_token,
                'fields': 'id,name,email,first_name,last_name'
            }
        )
        
        if facebook_response.status_code != 200:
            return Response({
                'error': 'Invalid Facebook token'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        facebook_data = facebook_response.json()
        
        # Extract user information from Facebook response
        facebook_user_id = facebook_data.get('id')
        email = facebook_data.get('email')
        first_name = facebook_data.get('first_name', '')
        last_name = facebook_data.get('last_name', '')
        name = facebook_data.get('name', '')
        
        if not email:
            return Response({
                'error': 'Email not provided by Facebook'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Create new user
            username = email.split('@')[0]  # Use email prefix as username
            base_username = username
            counter = 1
            
            # Ensure unique username
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=None,  # No password for SSO users
                email_verified=True  # Facebook emails are verified
            )
            
            # Create user profile
            UserProfile.objects.create(user=user)
        
        # Generate or get token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email_verified': user.email_verified
            },
            'is_new_user': created
        })
        
    except requests.RequestException as e:
        return Response({
            'error': 'Failed to verify Facebook token'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({
            'error': 'Authentication failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def sso_config(request):
    """
    Get SSO configuration for frontend.
    
    Returns the necessary configuration for Google and Facebook SSO.
    """
    config = {
        'google': {
            'client_id': getattr(settings, 'GOOGLE_CLIENT_ID', ''),
            'enabled': bool(getattr(settings, 'GOOGLE_CLIENT_ID', None))
        },
        'facebook': {
            'app_id': getattr(settings, 'FACEBOOK_APP_ID', ''),
            'enabled': bool(getattr(settings, 'FACEBOOK_APP_ID', None))
        }
    }
    
    return Response(config)


@api_view(['GET'])
@permission_classes([AllowAny])
def stats_view(request):
    """
    Get application statistics.
    """
    from core.models import User, UserProfile
    
    total_users = User.objects.count()
    verified_users = User.objects.filter(email_verified=True).count()
    
    return Response({
        'total_users': total_users,
        'verified_users': verified_users,
        'verification_rate': (verified_users / total_users * 100) if total_users > 0 else 0
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def global_search(request):
    """
    Global search endpoint.
    """
    query = request.GET.get('q', '')
    
    if not query:
        return Response({
            'results': [],
            'query': query
        })
    
    # For now, just return empty results
    # TODO: Implement actual search functionality
    return Response({
        'results': [],
        'query': query
    }) 