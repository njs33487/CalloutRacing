from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet, TrackViewSet, EventViewSet,
    CalloutViewSet, RaceResultViewSet, MarketplaceViewSet, EventParticipantViewSet,
    contact_form, login_view, register_view, logout_view, user_profile, stats_view
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'tracks', TrackViewSet)
router.register(r'events', EventViewSet)
router.register(r'callouts', CalloutViewSet, basename='callout')
router.register(r'race-results', RaceResultViewSet)
router.register(r'marketplace', MarketplaceViewSet, basename='marketplace')
router.register(r'event-participants', EventParticipantViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('contact/', contact_form, name='contact-form'),
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/profile/', user_profile, name='user-profile'),
    path('stats/', stats_view, name='stats'),
] 