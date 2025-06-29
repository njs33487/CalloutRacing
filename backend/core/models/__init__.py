"""
Core models package for CalloutRacing application.

This package contains all database models organized by domain:
- auth: User authentication and profiles
- racing: Events, tracks, callouts, and race results
- marketplace: Marketplace listings and transactions
- social: Friends, messages, posts, and social features
- cars: Car profiles, modifications, and build logs
- payments: Subscriptions, payments, and wallets
- locations: Hot spots, crews, and location broadcasting
"""

# Import all models to maintain backward compatibility
from .auth import User, UserProfile
from .racing import Track, Event, Callout, RaceResult, EventParticipant
from .marketplace import (
    Marketplace, MarketplaceImage, MarketplaceOrder, 
    MarketplaceReview, ContactSubmission
)
from .social import (
    Follow, Block, Friendship, Message, UserPost, PostComment, 
    Notification, ReputationRating
)
from .cars import (
    CarProfile, CarModification, CarImage, BuildLog, 
    BuildMilestone, BuildMedia, CarTour, PerformanceData,
    BuildWishlist, WishlistSuggestion, BuildRating, 
    BuildComment, BuildBadge, BuildBadgeAward
)
from .payments import (
    Subscription, Payment, UserWallet, Bet, BettingPool
)
from .locations import (
    HotSpot, RacingCrew, CrewMembership, LocationBroadcast,
    OpenChallenge, ChallengeResponse
)

__all__ = [
    # Auth models
    'User', 'UserProfile',
    
    # Racing models
    'Track', 'Event', 'Callout', 'RaceResult', 'EventParticipant',
    
    # Marketplace models
    'Marketplace', 'MarketplaceImage', 'MarketplaceOrder', 
    'MarketplaceReview', 'ContactSubmission',
    
    # Social models
    'Follow', 'Block', 'Friendship', 'Message', 'UserPost', 'PostComment', 
    'Notification', 'ReputationRating',
    
    # Car models
    'CarProfile', 'CarModification', 'CarImage', 'BuildLog', 
    'BuildMilestone', 'BuildMedia', 'CarTour', 'PerformanceData',
    'BuildWishlist', 'WishlistSuggestion', 'BuildRating', 
    'BuildComment', 'BuildBadge', 'BuildBadgeAward',
    
    # Payment models
    'Subscription', 'Payment', 'UserWallet', 'Bet', 'BettingPool',
    
    # Location models
    'HotSpot', 'RacingCrew', 'CrewMembership', 'LocationBroadcast',
    'OpenChallenge', 'ChallengeResponse',
] 