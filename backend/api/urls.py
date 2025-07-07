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
    run_migrations,
    setup_otp, verify_otp_setup, disable_otp, verify_otp_login,
    generate_backup_codes, sso_config,
    verify_email, request_password_reset, reset_password,
    # ViewSets from other files
    ListingViewSet, EventViewSet, HotspotViewSet
)

# Import auth views directly
from .views.auth import resend_verification_email_view, check_user_exists, get_csrf_token

# Import OTP auth views
from .views.auth import send_otp, verify_otp, phone_login, email_login

# Import racing views directly
from .views.racing import (
    TrackListView, TrackDetailView,
    CalloutListView, CalloutCreateView, CalloutDetailView,
    RaceResultCreateView, RaceResultDetailView,
    accept_callout, decline_callout, cancel_callout,
    search_users_for_callout, callout_statistics
)

# Import social views directly
from .views.social import (
    LiveFeedView, CreatePostView, PostDetailView, PostInteractionView,
    trending_posts, user_feed, notifications, mark_notification_read,
    live_streams, update_live_viewers
)

from api.views.sponsored_views import SponsoredContentViewSet
from api.views.subscription_views import (
    stripe_webhook, 
    get_subscription_plans, 
    create_subscription_checkout_session, 
    get_subscription_status,
    create_customer_portal_session,
    create_marketplace_payment_intent
)
from api.views.marketplace import create_connect_account, create_account_link, get_connect_account_status
from api.views.marketplace_views import MarketplaceListingViewSet, marketplace_webhook

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'marketplace', ListingViewSet, basename='marketplace')
router.register(r'marketplace-listings', MarketplaceListingViewSet, basename='marketplace-listing')
router.register(r'events', EventViewSet, basename='event')
router.register(r'hotspots', HotspotViewSet, basename='hotspot')
router.register(r'sponsored-content', SponsoredContentViewSet, basename='sponsored-content')

# Authentication URLs
auth_patterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile, name='user-profile'),
    path('csrf/', get_csrf_token, name='get-csrf-token'),

    path('verify-email/<str:token>/', verify_email, name='verify-email'),
    path('resend-verification/', resend_verification_email_view, name='resend-verification'),
    path('check-user/', check_user_exists, name='check-user'),
    path('request-password-reset/', request_password_reset, name='request-password-reset'),
    path('reset-password/', reset_password, name='reset-password'),
    
    # OTP Authentication URLs
    path('otp/send/', send_otp, name='send-otp'),
    path('otp/verify/', verify_otp, name='verify-otp'),
    path('phone-login/', phone_login, name='phone-login'),
    path('email-login/', email_login, name='email-login'),
    
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

# Social Feed URLs
social_patterns = [
    path('feed/', LiveFeedView.as_view(), name='live-feed'),
    path('trending/', trending_posts, name='trending-posts'),
    path('live-streams/', live_streams, name='live-streams'),
    path('posts/', CreatePostView.as_view(), name='create-post'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/<str:action>/', PostInteractionView.as_view(), name='post-interaction'),
    path('posts/<int:post_id>/update-viewers/', update_live_viewers, name='update-live-viewers'),
    path('user/<str:username>/feed/', user_feed, name='user-feed'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', mark_notification_read, name='mark-notification-read'),
]

# Add subscription URLs
subscription_patterns = [
    path('plans/', get_subscription_plans, name='get-subscription-plans'),
    path('create-checkout-session/', create_subscription_checkout_session, name='create-checkout-session'),
    path('create-portal-session/', create_customer_portal_session, name='create-portal-session'),
    path('status/', get_subscription_status, name='get-subscription-status'),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
]

# Add Connect onboarding URLs
connect_patterns = [
    path('create-account/', create_connect_account, name='create-connect-account'),
    path('create-account-link/', create_account_link, name='create-account-link'),
    path('account-status/', get_connect_account_status, name='connect-account-status'),
]

# Add marketplace webhook URL
marketplace_patterns = [
    path('webhook/', marketplace_webhook, name='marketplace-webhook'),
    path('items/<int:item_id>/create-payment-intent/', create_marketplace_payment_intent, name='create-marketplace-payment-intent'),
]

# Combine all URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_patterns)),
    path('racing/', include(racing_patterns)),
    path('social/', include(social_patterns)),
    path('subscriptions/', include(subscription_patterns)),
    path('connect/', include(connect_patterns)),
    path('marketplace/', include(marketplace_patterns)),
    # Aliases for convenience
    path('tracks/', TrackListView.as_view(), name='track-list-alias'),
    path('callouts/', CalloutListView.as_view(), name='callout-list-alias'),
    path('users/search/', search_users_for_callout, name='user-search-alias'),
    path('stats/', callout_statistics, name='stats-alias'),  # Global stats endpoint
    # Username-based profile access (like Facebook)
    path('@<str:username>/', UserProfileViewSet.as_view({'get': 'by_username'}), name='profile-by-username'),
] 