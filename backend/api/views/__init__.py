"""
API Views for CalloutRacing Application

This module contains all API views organized by functionality:
- Authentication and user management
- Racing features (callouts, tracks, events)
- Social features (friends, messages, posts)
- Marketplace and commerce
- Location-based features (hotspots)
"""

# Import all views
from .auth import (
    UserViewSet, UserProfileViewSet,
    login_view, register_view, logout_view, user_profile,
    verify_email, resend_verification_email, check_user_exists,
    google_sso, facebook_sso, sso_config, stats_view, global_search,
    run_migrations, request_password_reset, reset_password,
    setup_otp, verify_otp_setup, disable_otp, verify_otp_login,
    generate_backup_codes
)

from .racing import (
    TrackListView, TrackDetailView,
    CalloutListView, CalloutCreateView, CalloutDetailView,
    RaceResultCreateView, RaceResultDetailView,
    accept_callout, decline_callout, cancel_callout,
    search_users_for_callout, callout_statistics
)

# Import new ViewSets
from .events import EventViewSet
from .marketplace import MarketplaceViewSet
from .hotspots import HotSpotViewSet

# Import social views
from .social import (
    FollowViewSet, BlockViewSet, FriendshipViewSet,
    MessageViewSet, UserPostViewSet, PostCommentViewSet,
    NotificationViewSet, ReputationRatingViewSet
)

# Import car views
from .cars import (
    CarProfileViewSet, CarModificationViewSet, CarImageViewSet,
    BuildLogViewSet, BuildMilestoneViewSet, BuildMediaViewSet,
    CarTourViewSet, PerformanceDataViewSet, BuildWishlistViewSet,
    WishlistSuggestionViewSet, BuildRatingViewSet, BuildCommentViewSet,
    BuildBadgeViewSet, BuildBadgeAwardViewSet
)

# Import payment views
from .payments import (
    SubscriptionViewSet, PaymentViewSet, UserWalletViewSet,
    BetViewSet, BettingPoolViewSet
)

# Import location views
from .locations import (
    RacingCrewViewSet, CrewMembershipViewSet, LocationBroadcastViewSet,
    OpenChallengeViewSet, ChallengeResponseViewSet
)

__all__ = [
    # Auth views
    'UserViewSet', 'UserProfileViewSet',
    'login_view', 'register_view', 'logout_view', 'user_profile',
    'verify_email', 'resend_verification_email', 'check_user_exists',
    'google_sso', 'facebook_sso', 'sso_config', 'stats_view', 'global_search',
    'run_migrations', 'request_password_reset', 'reset_password',
    'setup_otp', 'verify_otp_setup', 'disable_otp', 'verify_otp_login',
    'generate_backup_codes',
    
    # Racing views
    'TrackListView', 'TrackDetailView',
    'CalloutListView', 'CalloutCreateView', 'CalloutDetailView',
    'RaceResultCreateView', 'RaceResultDetailView',
    'accept_callout', 'decline_callout', 'cancel_callout',
    'search_users_for_callout', 'callout_statistics',
    
    # New ViewSets
    'EventViewSet', 'MarketplaceViewSet', 'HotSpotViewSet',
    
    # Social views
    'FollowViewSet', 'BlockViewSet', 'FriendshipViewSet',
    'MessageViewSet', 'UserPostViewSet', 'PostCommentViewSet',
    'NotificationViewSet', 'ReputationRatingViewSet',
    
    # Car views
    'CarProfileViewSet', 'CarModificationViewSet', 'CarImageViewSet',
    'BuildLogViewSet', 'BuildMilestoneViewSet', 'BuildMediaViewSet',
    'CarTourViewSet', 'PerformanceDataViewSet', 'BuildWishlistViewSet',
    'WishlistSuggestionViewSet', 'BuildRatingViewSet', 'BuildCommentViewSet',
    'BuildBadgeViewSet', 'BuildBadgeAwardViewSet',
    
    # Payment views
    'SubscriptionViewSet', 'PaymentViewSet', 'UserWalletViewSet',
    'BetViewSet', 'BettingPoolViewSet',
    
    # Location views
    'RacingCrewViewSet', 'CrewMembershipViewSet', 'LocationBroadcastViewSet',
    'OpenChallengeViewSet', 'ChallengeResponseViewSet',
] 