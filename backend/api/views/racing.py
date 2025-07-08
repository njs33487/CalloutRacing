"""
Racing API Views for CalloutRacing Application

This module contains API views for racing-related functionality:
- Callout creation, management, and search
- Track listing and search
- Race result management
"""

from rest_framework import status, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from core.models.racing import Callout, Track, RaceResult
from core.models.auth import User
from ..serializers import (
    CalloutSerializer, 
    TrackSerializer, 
    RaceResultSerializer,
    CalloutCreateSerializer,
    CalloutDetailSerializer
)


class TrackListView(generics.ListAPIView):
    """List and search tracks with filtering and sorting."""
    queryset = Track.objects.filter(is_active=True)
    serializer_class = TrackSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'location', 'description']
    ordering_fields = ['name', 'location', 'track_type', 'surface_type', 'length']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by track type
        track_type = self.request.query_params.get('track_type', None)
        if track_type:
            queryset = queryset.filter(track_type=track_type)
        
        # Filter by surface type
        surface_type = self.request.query_params.get('surface_type', None)
        if surface_type:
            queryset = queryset.filter(surface_type=surface_type)
        
        # Filter by location (city/state)
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(
                Q(location__icontains=location) |
                Q(name__icontains=location)
            )
        
        return queryset


class TrackDetailView(generics.RetrieveAPIView):
    """Get detailed track information."""
    queryset = Track.objects.filter(is_active=True)
    serializer_class = TrackSerializer
    lookup_field = 'id'


class CalloutListView(generics.ListAPIView):
    """List callouts with search, filtering, and sorting."""
    serializer_class = CalloutSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['challenger__username', 'challenged__username', 'message', 'street_location']
    ordering_fields = ['created_at', 'scheduled_date', 'wager_amount', 'race_type']
    ordering = ['-created_at']
    
    def get_queryset(self):
        try:
            user = self.request.user
            queryset = Callout.objects.select_related(
                'challenger', 'challenged', 'track', 'winner'
            ).prefetch_related('race_result')
            
            # Filter by status
            status_filter = self.request.query_params.get('status', None)
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            # Filter by race type
            race_type = self.request.query_params.get('race_type', None)
            if race_type:
                queryset = queryset.filter(race_type=race_type)
            
            # Filter by location type
            location_type = self.request.query_params.get('location_type', None)
            if location_type:
                queryset = queryset.filter(location_type=location_type)
            
            # Filter by experience level
            experience_level = self.request.query_params.get('experience_level', None)
            if experience_level:
                queryset = queryset.filter(experience_level=experience_level)
            
            # Filter by wager amount range
            min_wager = self.request.query_params.get('min_wager', None)
            max_wager = self.request.query_params.get('max_wager', None)
            if min_wager:
                queryset = queryset.filter(wager_amount__gte=min_wager)
            if max_wager:
                queryset = queryset.filter(wager_amount__lte=max_wager)
            
            # Filter by date range
            date_from = self.request.query_params.get('date_from', None)
            date_to = self.request.query_params.get('date_to', None)
            if date_from:
                queryset = queryset.filter(scheduled_date__gte=date_from)
            if date_to:
                queryset = queryset.filter(scheduled_date__lte=date_to)
            
            # Filter by user involvement
            user_filter = self.request.query_params.get('user', None)
            if user_filter == 'sent':
                queryset = queryset.filter(challenger=user)
            elif user_filter == 'received':
                queryset = queryset.filter(challenged=user)
            elif user_filter == 'involved':
                queryset = queryset.filter(
                    Q(challenger=user) | Q(challenged=user)
                )
            
            # Filter out private callouts unless user is involved
            if not user.is_authenticated:
                queryset = queryset.filter(is_private=False)
            else:
                queryset = queryset.filter(
                    Q(is_private=False) | 
                    Q(challenger=user) | 
                    Q(challenged=user)
                )
            
            # Filter out expired callouts unless completed/cancelled
            show_expired = self.request.query_params.get('show_expired', 'false').lower() == 'true'
            if not show_expired:
                expired_date = timezone.now() - timedelta(days=7)
                queryset = queryset.filter(
                    Q(created_at__gte=expired_date) |
                    Q(status__in=['completed', 'cancelled'])
                )
            
            return queryset
        except Exception as e:
            # Log the error for debugging
            print(f"Error in CalloutListView get_queryset: {e}")
            return Callout.objects.none()


class CalloutCreateView(generics.CreateAPIView):
    """Create a new callout."""
    serializer_class = CalloutCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(challenger=self.request.user)


class CalloutDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a callout."""
    serializer_class = CalloutDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Callout.objects.filter(
            Q(challenger=user) | Q(challenged=user) | Q(is_private=False)
        ).select_related('challenger', 'challenged', 'track', 'winner')
    
    def perform_update(self, serializer):
        callout = serializer.instance
        user = self.request.user
        
        # Only challenger can update callout
        if callout.challenger != user:
            raise PermissionError("Only the challenger can update this callout")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        user = self.request.user
        
        # Only challenger can delete callout
        if instance.challenger != user:
            raise PermissionError("Only the challenger can delete this callout")
        
        instance.delete()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_callout(request, callout_id):
    """Accept a callout."""
    callout = get_object_or_404(Callout, id=callout_id, challenged=request.user)
    
    if callout.status != 'pending':
        return Response(
            {'error': 'Callout is not in pending status'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    callout.status = 'accepted'
    callout.save()
    
    serializer = CalloutDetailSerializer(callout)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_callout(request, callout_id):
    """Decline a callout."""
    callout = get_object_or_404(Callout, id=callout_id, challenged=request.user)
    
    if callout.status != 'pending':
        return Response(
            {'error': 'Callout is not in pending status'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    callout.status = 'declined'
    callout.save()
    
    serializer = CalloutDetailSerializer(callout)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_callout(request, callout_id):
    """Cancel a callout."""
    callout = get_object_or_404(Callout, id=callout_id)
    
    if callout.challenger != request.user and callout.challenged != request.user:
        return Response(
            {'error': 'You can only cancel callouts you are involved in'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if callout.status not in ['pending', 'accepted']:
        return Response(
            {'error': 'Callout cannot be cancelled in its current status'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    callout.status = 'cancelled'
    callout.save()
    
    serializer = CalloutDetailSerializer(callout)
    return Response(serializer.data)


class RaceResultCreateView(generics.CreateAPIView):
    """Create a race result for a completed callout."""
    serializer_class = RaceResultSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        callout = serializer.validated_data['callout']
        
        # Check if user is involved in the callout
        if callout.challenger != self.request.user and callout.challenged != self.request.user:
            raise PermissionError("You can only create results for callouts you are involved in")
        
        # Check if callout is accepted
        if callout.status != 'accepted':
            raise PermissionError("Can only create results for accepted callouts")
        
        # Update callout status to completed
        callout.status = 'completed'
        callout.save()
        
        serializer.save()


class RaceResultDetailView(generics.RetrieveUpdateAPIView):
    """Get or update race result details."""
    serializer_class = RaceResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return RaceResult.objects.filter(
            Q(callout__challenger=user) | Q(callout__challenged=user)
        ).select_related('callout', 'callout__challenger', 'callout__challenged')


@api_view(['GET'])
def search_users_for_callout(request):
    """Search users to challenge in a callout."""
    query = request.query_params.get('q', '')
    if not query or len(query) < 2:
        return Response({'error': 'Search query must be at least 2 characters'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    users = User.objects.filter(
        Q(username__icontains=query) | Q(email__icontains=query)
    ).exclude(id=request.user.id)[:10]
    
    results = [{'id': user.id, 'username': user.username, 'email': user.email} 
               for user in users]
    
    return Response({'results': results})


@api_view(['GET'])
def callout_statistics(request):
    """Get callout statistics for the current user."""
    user = request.user
    
    stats = {
        'total_sent': Callout.objects.filter(challenger=user).count(),
        'total_received': Callout.objects.filter(challenged=user).count(),
        'pending_sent': Callout.objects.filter(challenger=user, status='pending').count(),
        'pending_received': Callout.objects.filter(challenged=user, status='pending').count(),
        'accepted': Callout.objects.filter(
            Q(challenger=user) | Q(challenged=user), 
            status='accepted'
        ).count(),
        'completed': Callout.objects.filter(
            Q(challenger=user) | Q(challenged=user), 
            status='completed'
        ).count(),
        'wins': Callout.objects.filter(winner=user, status='completed').count(),
        'losses': Callout.objects.filter(
            Q(challenger=user) | Q(challenged=user),
            status='completed'
        ).exclude(winner=user).count(),
    }
    
    return Response(stats) 