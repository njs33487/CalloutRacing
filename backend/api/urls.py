"""
API URL Configuration for CalloutRacing Application

This module contains URL patterns for all API endpoints:
- Authentication (login, register, password reset, OTP)
- Racing (callouts, tracks, race results)
- Marketplace (listings, cars)
- Social (friends, profiles)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet,
    login_view, register_view, logout_view, user_profile,
    verify_email, resend_verification_email, check_user_exists,
    google_sso, facebook_sso, sso_config, stats_view, global_search,
    run_migrations, request_password_reset, reset_password,
    setup_otp, verify_otp_setup, disable_otp, verify_otp_login,
    generate_backup_codes, auth, racing,
    # Racing views
    TrackListView, TrackDetailView,
    CalloutListView, CalloutCreateView, CalloutDetailView,
    RaceResultCreateView, RaceResultDetailView,
    accept_callout, decline_callout, cancel_callout,
    search_users_for_callout, callout_statistics
)
from django.http import JsonResponse

# TODO: Import these when the view modules are created
# from .views import (
#     TrackViewSet, EventViewSet, CalloutViewSet, RaceResultViewSet,
#     MarketplaceViewSet, EventParticipantViewSet, FriendshipViewSet, 
#     MessageViewSet, CarProfileViewSet, CarModificationViewSet,
#     CarImageViewSet, UserPostViewSet, PostCommentViewSet,
#     contact_form
# )

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet, basename='profile')

# TODO: Register these when the view modules are created
# router.register(r'tracks', TrackViewSet)
# router.register(r'events', EventViewSet)
# router.register(r'callouts', CalloutViewSet, basename='callout')
# router.register(r'race-results', RaceResultViewSet)
# router.register(r'marketplace', MarketplaceViewSet, basename='marketplace')
# router.register(r'event-participants', EventParticipantViewSet)
# router.register(r'friendships', FriendshipViewSet, basename='friendship')
# router.register(r'messages', MessageViewSet, basename='message')
# router.register(r'cars', CarProfileViewSet, basename='car')
# router.register(r'car-modifications', CarModificationViewSet, basename='car-modification')
# router.register(r'car-images', CarImageViewSet, basename='car-image')
# router.register(r'posts', UserPostViewSet, basename='post')
# router.register(r'post-comments', PostCommentViewSet, basename='post-comment')

# Hot spots and location-based features
# router.register(r'hotspots', HotSpotViewSet, basename='hotspot')
# router.register(r'location-broadcasts', LocationBroadcastViewSet, basename='locationbroadcast')

# Racing crews and groups
# router.register(r'crews', RacingCrewViewSet, basename='racingcrew')
# router.register(r'crew-memberships', CrewMembershipViewSet, basename='crewmembership')

# Reputation and ratings
# router.register(r'reputation-ratings', ReputationRatingViewSet, basename='reputationrating')

# Open challenges
# router.register(r'open-challenges', OpenChallengeViewSet, basename='openchallenge')
# router.register(r'challenge-responses', ChallengeResponseViewSet, basename='challengeresponse')

# Authentication URLs
auth_patterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile, name='user-profile'),
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
]

# Stub views for missing endpoints
def marketplace_stub(request):
    return JsonResponse({'detail': 'Marketplace endpoint not implemented yet.'}, status=501)

def hotspots_stub(request):
    return JsonResponse({'detail': 'Hotspots endpoint not implemented yet.'}, status=501)

def friendships_stub(request):
    return JsonResponse({'detail': 'Friendships endpoint not implemented yet.'}, status=501)

def events_stub(request):
    return JsonResponse({'detail': 'Events endpoint not implemented yet.'}, status=501)

# Combine all URL patterns
urlpatterns = [
    path('', include(router.urls)),
    # path('contact/', contact_form, name='contact-form'),
    path('auth/', include(auth_patterns)),
    path('racing/', include(racing_patterns)),
    # Aliases for convenience
    path('tracks/', TrackListView.as_view(), name='track-list-alias'),
    path('callouts/', CalloutListView.as_view(), name='callout-list-alias'),
    path('events/', events_stub, name='events-alias'),
    path('users/search/', search_users_for_callout, name='user-search-alias'),
    path('marketplace/', marketplace_stub, name='marketplace-stub'),
    path('hotspots/', hotspots_stub, name='hotspots-stub'),
    path('friendships/', friendships_stub, name='friendships-stub'),
    path('auth/google/', google_sso, name='google-sso'),
    path('auth/facebook/', facebook_sso, name='facebook-sso'),
    path('auth/sso-config/', sso_config, name='sso-config'),
    path('stats/', stats_view, name='stats'),
    path('search/', global_search, name='global-search'),
    # Username-based profile access (like Facebook)
    path('@<str:username>/', UserProfileViewSet.as_view({'get': 'by_username'}), name='profile-by-username'),
] 