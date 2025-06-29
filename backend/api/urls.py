from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet, UserProfileDetailViewSet,
    login_view, register_view, logout_view, user_profile,
    verify_email, resend_verification_email, check_user_exists,
    google_sso, facebook_sso, sso_config, stats_view, global_search,
    run_migrations, request_password_reset, reset_password,
    setup_otp, verify_otp_setup, disable_otp, verify_otp_login,
    generate_backup_codes
)

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
router.register(r'profiles', UserProfileViewSet)
router.register(r'profiles-detail', UserProfileDetailViewSet, basename='profile-detail')

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

urlpatterns = [
    path('', include(router.urls)),
    # path('contact/', contact_form, name='contact-form'),
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('auth/check-user/', check_user_exists, name='check-user'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/profile/', user_profile, name='user-profile'),
    path('auth/google/', google_sso, name='google-sso'),
    path('auth/facebook/', facebook_sso, name='facebook-sso'),
    path('auth/sso-config/', sso_config, name='sso-config'),
    path('auth/verify-email/<str:token>/', verify_email, name='verify-email'),
    path('auth/resend-verification/', resend_verification_email, name='resend-verification'),
    path('auth/request-password-reset/', request_password_reset, name='request-password-reset'),
    path('auth/reset-password/', reset_password, name='reset-password'),
    path('auth/setup-otp/', setup_otp, name='setup-otp'),
    path('auth/verify-otp-setup/', verify_otp_setup, name='verify-otp-setup'),
    path('auth/disable-otp/', disable_otp, name='disable-otp'),
    path('auth/verify-otp-login/', verify_otp_login, name='verify-otp-login'),
    path('auth/generate-backup-codes/', generate_backup_codes, name='generate-backup-codes'),
    path('auth/run-migrations/', run_migrations, name='run-migrations'),
    path('stats/', stats_view, name='stats'),
    path('search/', global_search, name='global-search'),
] 