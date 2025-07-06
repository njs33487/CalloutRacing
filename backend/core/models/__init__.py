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
from .auth import User, UserProfile, OTP
from .racing import Track, Event, Callout, RaceResult, EventParticipant
from .marketplace import (
    Marketplace, MarketplaceImage, MarketplaceOrder, 
    MarketplaceReview, ContactSubmission, ListingCategory, MarketplaceListing,
    ListingImage, CarListing, Review, Rating, PaymentTransaction,
    Order, OrderItem, ShippingAddress
)
from .social import (
    Follow, Block, Friendship, Message, UserPost, PostComment, 
    Notification, ReputationRating, RacingCrew, CrewMembership
)
from .cars import (
    CarProfile, CarModification, CarImage, BuildLog, 
    BuildMilestone, BuildMedia, CarTour, PerformanceData,
    BuildWishlist, WishlistSuggestion, BuildRating, 
    BuildComment, BuildBadge, BuildBadgeAward
)
from .payments import UserWallet, Payment, MarketplaceTransaction
from .locations import (
    HotSpot, LocationBroadcast, OpenChallenge, ChallengeResponse
)

__all__ = [
    # Auth models
    'User', 'UserProfile', 'OTP',
    
    # Racing models
    'Track', 'Event', 'Callout', 'RaceResult', 'EventParticipant',
    
    # Marketplace models
    'Marketplace', 'MarketplaceImage', 'MarketplaceOrder', 
    'MarketplaceReview', 'ContactSubmission', 'ListingCategory', 'MarketplaceListing',
    'ListingImage', 'CarListing', 'Review', 'Rating', 'PaymentTransaction',
    'Order', 'OrderItem', 'ShippingAddress',
    
    # Social models
    'Follow', 'Block', 'Friendship', 'Message', 'UserPost', 'PostComment', 
    'Notification', 'ReputationRating', 'RacingCrew', 'CrewMembership',
    
    # Car models
    'CarProfile', 'CarModification', 'CarImage', 'BuildLog', 
    'BuildMilestone', 'BuildMedia', 'CarTour', 'PerformanceData',
    'BuildWishlist', 'WishlistSuggestion', 'BuildRating', 
    'BuildComment', 'BuildBadge', 'BuildBadgeAward',
    
    # Payment models
    'Subscription', 'Payment', 'UserWallet', 'MarketplaceTransaction',
    
    # Location models
    'HotSpot', 'LocationBroadcast', 'OpenChallenge', 'ChallengeResponse',
] 