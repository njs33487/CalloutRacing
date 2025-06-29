"""
API Views Package for CalloutRacing Application

This package contains all API views organized by domain:
- auth: Authentication and user management views
- racing: Racing events, tracks, callouts, and race results
- marketplace: Marketplace listings and transactions
- social: Friends, messages, posts, and social features
- cars: Car profiles, modifications, and build logs
- payments: Subscriptions, payments, and wallets
- locations: Hot spots, crews, and location broadcasting
- utils: Utility views like search and SSO
"""

# Import all views to maintain backward compatibility
from .auth import (
    UserViewSet, UserProfileViewSet, UserProfileDetailViewSet,
    login_view, register_view, logout_view, user_profile,
    verify_email, resend_verification_email, check_user_exists,
    run_migrations, request_password_reset, reset_password,
    setup_otp, verify_otp_setup, disable_otp, verify_otp_login,
    generate_backup_codes
)

# TODO: Import these when the modules are created
# from .racing import (
#     TrackViewSet, EventViewSet, CalloutViewSet, RaceResultViewSet,
#     EventParticipantViewSet
# )
# from .marketplace import (
#     MarketplaceViewSet, MarketplaceOrderViewSet, MarketplaceReviewViewSet,
#     contact_form
# )
# from .social import (
#     FriendshipViewSet, MessageViewSet, UserPostViewSet, PostCommentViewSet,
#     NotificationViewSet
# )
# from .cars import (
#     CarProfileViewSet, CarModificationViewSet, CarImageViewSet
# )
# from .payments import (
#     SubscriptionViewSet, PaymentViewSet, UserWalletViewSet,
#     BetViewSet, BettingPoolViewSet, subscription_plans
# )
# from .locations import (
#     HotSpotViewSet, RacingCrewViewSet, CrewMembershipViewSet,
#     LocationBroadcastViewSet, ReputationRatingViewSet,
#     OpenChallengeViewSet, ChallengeResponseViewSet
# )
from .utils import (
    stats_view, global_search, google_sso, facebook_sso, sso_config
)

__all__ = [
    # Auth views
    'UserViewSet', 'UserProfileViewSet', 'UserProfileDetailViewSet',
    'login_view', 'register_view', 'logout_view', 'user_profile',
    'verify_email', 'resend_verification_email', 'check_user_exists',
    'run_migrations', 'request_password_reset', 'reset_password',
    'setup_otp', 'verify_otp_setup', 'disable_otp', 'verify_otp_login',
    'generate_backup_codes',
    
    # TODO: Add these when the modules are created
    # Racing views
    # 'TrackViewSet', 'EventViewSet', 'CalloutViewSet', 'RaceResultViewSet',
    # 'EventParticipantViewSet',
    
    # Marketplace views
    # 'MarketplaceViewSet', 'MarketplaceOrderViewSet', 'MarketplaceReviewViewSet',
    # 'contact_form',
    
    # Social views
    # 'FriendshipViewSet', 'MessageViewSet', 'UserPostViewSet', 'PostCommentViewSet',
    # 'NotificationViewSet',
    
    # Car views
    # 'CarProfileViewSet', 'CarModificationViewSet', 'CarImageViewSet',
    
    # Payment views
    # 'SubscriptionViewSet', 'PaymentViewSet', 'UserWalletViewSet',
    # 'BetViewSet', 'BettingPoolViewSet', 'subscription_plans',
    
    # Location views
    # 'HotSpotViewSet', 'RacingCrewViewSet', 'CrewMembershipViewSet',
    # 'LocationBroadcastViewSet', 'ReputationRatingViewSet',
    # 'OpenChallengeViewSet', 'ChallengeResponseViewSet',
    
    # Utility views
    'stats_view', 'global_search', 'google_sso', 'facebook_sso', 'sso_config',
] 