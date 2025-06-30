"""
API Views for CalloutRacing Application

This module contains all API views organized by functionality:
- Authentication and user management
- Racing features (callouts, tracks, events)
- Marketplace and commerce
- Location-based features (hotspots)
"""

# Import all views
from .auth import (
    UserViewSet, UserProfileViewSet,
    login_view, register_view, logout_view, user_profile,
    verify_email, resend_verification_email, check_user_exists,
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
from .marketplace import ListingViewSet, TransactionViewSet, ReviewViewSet
from .hotspots import HotspotViewSet

# Import utility views
from .utils import sso_config

# Import ViewSets from main views.py
from ..views import (
    TrackViewSet, CalloutViewSet, RaceResultViewSet, MarketplaceViewSet,
    EventParticipantViewSet, FriendshipViewSet, MessageViewSet,
    CarProfileViewSet, CarModificationViewSet, CarImageViewSet,
    UserPostViewSet, PostCommentViewSet, SubscriptionViewSet,
    PaymentViewSet, UserWalletViewSet, MarketplaceOrderViewSet,
    MarketplaceReviewViewSet, BetViewSet, BettingPoolViewSet,
    NotificationViewSet, HotSpotViewSet, RacingCrewViewSet,
    CrewMembershipViewSet, LocationBroadcastViewSet,
    ReputationRatingViewSet, OpenChallengeViewSet, ChallengeResponseViewSet
)

__all__ = [
    # Auth views
    'UserViewSet', 'UserProfileViewSet',
    'login_view', 'register_view', 'logout_view', 'user_profile',
    'verify_email', 'resend_verification_email', 'check_user_exists',
    'run_migrations', 'request_password_reset', 'reset_password',
    'setup_otp', 'verify_otp_setup', 'disable_otp', 'verify_otp_login',
    'generate_backup_codes',
    
    # Racing views
    'TrackListView', 'TrackDetailView',
    'CalloutListView', 'CalloutCreateView', 'CalloutDetailView',
    'RaceResultCreateView', 'RaceResultDetailView',
    'accept_callout', 'decline_callout', 'cancel_callout',
    'search_users_for_callout', 'callout_statistics',
    
    # ViewSets
    'EventViewSet', 'ListingViewSet', 'TransactionViewSet', 'ReviewViewSet', 'HotspotViewSet',
    'TrackViewSet', 'CalloutViewSet', 'RaceResultViewSet', 'MarketplaceViewSet',
    'EventParticipantViewSet', 'FriendshipViewSet', 'MessageViewSet',
    'CarProfileViewSet', 'CarModificationViewSet', 'CarImageViewSet',
    'UserPostViewSet', 'PostCommentViewSet', 'SubscriptionViewSet',
    'PaymentViewSet', 'UserWalletViewSet', 'MarketplaceOrderViewSet',
    'MarketplaceReviewViewSet', 'BetViewSet', 'BettingPoolViewSet',
    'NotificationViewSet', 'HotSpotViewSet', 'RacingCrewViewSet',
    'CrewMembershipViewSet', 'LocationBroadcastViewSet',
    'ReputationRatingViewSet', 'OpenChallengeViewSet', 'ChallengeResponseViewSet',
    
    # Utility views
    'sso_config',
] 