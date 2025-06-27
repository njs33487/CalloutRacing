from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet, TrackViewSet, EventViewSet,
    CalloutViewSet, RaceResultViewSet, MarketplaceViewSet, EventParticipantViewSet,
    FriendshipViewSet, MessageViewSet, CarProfileViewSet, CarModificationViewSet,
    CarImageViewSet, UserPostViewSet, PostCommentViewSet, UserProfileDetailViewSet,
    contact_form, login_view, register_view, logout_view, user_profile, stats_view
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'profiles-detail', UserProfileDetailViewSet, basename='profile-detail')
router.register(r'tracks', TrackViewSet)
router.register(r'events', EventViewSet)
router.register(r'callouts', CalloutViewSet, basename='callout')
router.register(r'race-results', RaceResultViewSet)
router.register(r'marketplace', MarketplaceViewSet, basename='marketplace')
router.register(r'event-participants', EventParticipantViewSet)
router.register(r'friendships', FriendshipViewSet, basename='friendship')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'cars', CarProfileViewSet, basename='car')
router.register(r'car-modifications', CarModificationViewSet, basename='car-modification')
router.register(r'car-images', CarImageViewSet, basename='car-image')
router.register(r'posts', UserPostViewSet, basename='post')
router.register(r'post-comments', PostCommentViewSet, basename='post-comment')

urlpatterns = [
    path('', include(router.urls)),
    path('contact/', contact_form, name='contact-form'),
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/profile/', user_profile, name='user-profile'),
    path('stats/', stats_view, name='stats'),
] 