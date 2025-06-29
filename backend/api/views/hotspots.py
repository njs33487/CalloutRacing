"""
Hotspots API Views for CalloutRacing Application

This module contains views for managing racing hotspots:
- Hotspot creation and management
- Hotspot discovery and navigation
- Hotspot ratings and reviews
"""

from rest_framework import viewsets, status, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count
from django.utils import timezone
# from django.contrib.gis.geos import Point
# from django.contrib.gis.db.models.functions import Distance
from datetime import datetime, timedelta

from core.models.locations import HotSpot
from core.models.racing import Track


# Basic serializers for now
class HotspotSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSpot
        fields = '__all__'


class HotspotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSpot
        fields = ['name', 'description', 'spot_type', 'address', 'city', 'state', 
                 'zip_code', 'latitude', 'longitude', 'rules', 'amenities', 'peak_hours']


class HotspotViewSet(viewsets.ModelViewSet):
    """ViewSet for managing racing hotspots."""
    queryset = HotSpot.objects.all()
    serializer_class = HotspotSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return HotspotCreateSerializer
        return HotspotSerializer
    
    def get_queryset(self):
        queryset = HotSpot.objects.all()
        
        # Filter by hotspot type
        spot_type = self.request.query_params.get('spot_type', None)
        if spot_type:
            queryset = queryset.filter(spot_type=spot_type)
        
        # Filter by location (radius search)
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)
        radius = self.request.query_params.get('radius', None)
        
        if lat and lng and radius:
            try:
                lat = float(lat)
                lng = float(lng)
                radius = float(radius)
                # Geographic features disabled
            except ValueError:
                pass
        
        # Filter by verification status
        is_verified = self.request.query_params.get('is_verified', None)
        if is_verified is not None:
            is_verified = is_verified.lower() == 'true'
            queryset = queryset.filter(is_verified=is_verified)
        
        # Filter by city
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        # Filter by state
        state = self.request.query_params.get('state', None)
        if state:
            queryset = queryset.filter(state__icontains=state)
        
        # Filter by creator
        creator_id = self.request.query_params.get('creator_id', None)
        if creator_id:
            queryset = queryset.filter(created_by_id=creator_id)
        
        # Search by name or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search) |
                Q(address__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def report_race(self, request, pk=None):
        """Report a race at this hotspot."""
        hotspot = self.get_object()
        
        # Increment total races
        hotspot.total_races += 1
        hotspot.save()
        
        return Response({
            'detail': 'Race reported successfully.',
            'total_races': hotspot.total_races
        })
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify a hotspot (admin only)."""
        hotspot = self.get_object()
        
        # Check if user is admin or has verification permissions
        if not request.user.is_staff:
            return Response(
                {'detail': 'Only staff can verify hotspots.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        hotspot.is_verified = True
        hotspot.save()
        
        serializer = self.get_serializer(hotspot)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a hotspot."""
        hotspot = self.get_object()
        
        # Check if user is creator or admin
        if hotspot.created_by != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'Only the creator or staff can deactivate hotspots.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        hotspot.is_active = False
        hotspot.save()
        
        return Response({'detail': 'Hotspot deactivated successfully.'})
    
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Get hotspots near the user's location."""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = request.query_params.get('radius', 10)  # Default 10km
        
        if not lat or not lng:
            return Response(
                {'detail': 'Latitude and longitude are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            lat = float(lat)
            lng = float(lng)
            radius = float(radius)
            # Geographic features disabled
            nearby_hotspots = HotSpot.objects.filter(is_active=True)[:20]
            serializer = self.get_serializer(nearby_hotspots, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {'detail': 'Invalid coordinates or radius.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular hotspots."""
        popular_hotspots = HotSpot.objects.filter(
            is_active=True
        ).order_by('-total_races')[:10]
        
        serializer = self.get_serializer(popular_hotspots, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_hotspots(self, request):
        """Get hotspots created by the current user."""
        my_hotspots = HotSpot.objects.filter(created_by=request.user).order_by('-created_at')
        serializer = self.get_serializer(my_hotspots, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def types(self, request):
        """Get available hotspot types."""
        types = HotSpot.objects.values_list('spot_type', flat=True).distinct()
        return Response(list(types)) 