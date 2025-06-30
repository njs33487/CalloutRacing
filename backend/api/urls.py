"""
API URL Configuration for CalloutRacing Application

This module contains URL patterns for all API endpoints:
- Authentication (login, register, password reset, OTP)
- Racing (callouts, tracks, race results, events)
- Marketplace (listings, cars)
- Social (friends, profiles)
- Hotspots (location-based features)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet,
    login_view, register_view, logout_view, user_profile,
    verify_email, resend_verification_email, check_user_exists,
    run_migrations, request_password_reset, reset_password,
    setup_otp, verify_otp_setup, disable_otp, verify_otp_login,
    generate_backup_codes, auth, racing, sso_config,
    # Racing views
    TrackListView, TrackDetailView,
    CalloutListView, CalloutCreateView, CalloutDetailView,
    RaceResultCreateView, RaceResultDetailView,
    accept_callout, decline_callout, cancel_callout,
    search_users_for_callout, callout_statistics,
    # ViewSets
    EventViewSet, ListingViewSet, HotspotViewSet
)
from .views.auth import test_auth

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'events', EventViewSet, basename='event')
router.register(r'marketplace', ListingViewSet, basename='marketplace')
router.register(r'hotspots', HotspotViewSet, basename='hotspot')

# Authentication URLs
auth_patterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile, name='user-profile'),
    path('test-auth/', test_auth, name='test-auth'),
    path('verify-email/<str:token>/', verify_email, name='verify-email'),
    path('resend-verification/', resend_verification_email, name='resend-verification'),
    path('check-user/', check_user_exists, name='check-user'),
    path('request-password-reset/', request_password_reset, name='request-password-reset'),
    path('reset-password/', reset_password, name='reset-password'),
    path('otp/setup/', setup_otp, name='otp-setup'),
    path('otp/verify-setup/', verify_otp_setup, name='otp-verify-setup'),
    path('otp/disable/', disable_otp, name='otp-disable'),
    path('otp/verify-login/', verify_otp_login, name='otp-verify-login'),
    path('generate-backup-codes/', generate_backup_codes, name='generate-backup-codes'),
    path('run-migrations/', run_migrations, name='run-migrations'),
    path('sso-config/', sso_config, name='sso-config'),
]

# Racing URLs
racing_patterns = [
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('tracks/<int:id>/', TrackDetailView.as_view(), name='track-detail'),
    path('callouts/', CalloutListView.as_view(), name='callout-list'),
    path('callouts/create/', CalloutCreateView.as_view(), name='callout-create'),
    path('callouts/<int:pk>/', CalloutDetailView.as_view(), name='callout-detail'),
    path('callouts/<int:callout_id>/accept/', accept_callout, name='callout-accept'),
    path('callouts/<int:callout_id>/decline/', decline_callout, name='callout-decline'),
    path('callouts/<int:callout_id>/cancel/', cancel_callout, name='callout-cancel'),
    path('race-results/', RaceResultCreateView.as_view(), name='race-result-create'),
    path('race-results/<int:pk>/', RaceResultDetailView.as_view(), name='race-result-detail'),
    path('search-users/', search_users_for_callout, name='search-users'),
    path('callout-stats/', callout_statistics, name='callout-statistics'),
    path('stats/', callout_statistics, name='stats'),  # Alias for stats
]

# Combine all URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_patterns)),
    path('racing/', include(racing_patterns)),
    # Aliases for convenience
    path('tracks/', TrackListView.as_view(), name='track-list-alias'),
    path('callouts/', CalloutListView.as_view(), name='callout-list-alias'),
    path('users/search/', search_users_for_callout, name='user-search-alias'),
    path('stats/', callout_statistics, name='stats-alias'),  # Global stats endpoint
    # Username-based profile access (like Facebook)
    path('@<str:username>/', UserProfileViewSet.as_view({'get': 'by_username'}), name='profile-by-username'),
] 