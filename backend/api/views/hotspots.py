"""
HotSpots API Views for CalloutRacing Application

This module contains views for managing racing hotspots:
- Hot spot locations and information
- Location-based features
- Hot spot ratings and reviews
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from core.models.locations import HotSpot
from .serializers import HotSpotSerializer, HotSpotCreateSerializer


class HotSpotViewSet(viewsets.ModelViewSet):
    """ViewSet for managing racing hotspots."""
    queryset = HotSpot.objects.all()
    serializer_class = HotSpotSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return HotSpotCreateSerializer
        return HotSpotSerializer
    
    def get_queryset(self):
        queryset = HotSpot.objects.filter(is_active=True)
        
        # Filter by spot type
        spot_type = self.request.query_params.get('spot_type', None)
        if spot_type:
            queryset = queryset.filter(spot_type=spot_type)
        
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
        
        # Filter by zip code
        zip_code = self.request.query_params.get('zip_code', None)
        if zip_code:
            queryset = queryset.filter(zip_code__icontains=zip_code)
        
        # Search by name or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search) |
                Q(address__icontains=search)
            )
        
        # Location-based filtering (if coordinates provided)
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)
        radius = self.request.query_params.get('radius', 50)  # Default 50km radius
        
        if lat and lng:
            try:
                lat = float(lat)
                lng = float(lng)
                radius = float(radius)
                
                user_location = Point(lng, lat, srid=4326)
                queryset = queryset.annotate(
                    distance=Distance('location', user_location)
                ).filter(distance__lte=radius * 1000).order_by('distance')
            except ValueError:
                pass
        
        # Sort options
        sort_by = self.request.query_params.get('sort_by', 'name')
        if sort_by == 'distance' and lat and lng:
            # Already sorted by distance above
            pass
        elif sort_by == 'total_races':
            queryset = queryset.order_by('-total_races')
        elif sort_by == 'name':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by('name')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def report_race(self, request, pk=None):
        """Report a race at this hotspot."""
        hotspot = self.get_object()
        user = request.user
        
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
        radius = request.query_params.get('radius', 25)  # Default 25km
        
        if not lat or not lng:
            return Response(
                {'detail': 'Latitude and longitude are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            lat = float(lat)
            lng = float(lng)
            radius = float(radius)
            
            user_location = Point(lng, lat, srid=4326)
            nearby_spots = HotSpot.objects.filter(
                is_active=True
            ).annotate(
                distance=Distance('location', user_location)
            ).filter(
                distance__lte=radius * 1000
            ).order_by('distance')[:20]
            
            serializer = self.get_serializer(nearby_spots, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {'detail': 'Invalid coordinates provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most popular hotspots."""
        popular_spots = HotSpot.objects.filter(
            is_active=True
        ).order_by('-total_races')[:10]
        
        serializer = self.get_serializer(popular_spots, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def verified(self, request):
        """Get verified hotspots only."""
        verified_spots = HotSpot.objects.filter(
            is_active=True,
            is_verified=True
        ).order_by('name')
        
        serializer = self.get_serializer(verified_spots, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_hotspots(self, request):
        """Get hotspots created by the current user."""
        my_hotspots = HotSpot.objects.filter(
            created_by=request.user
        ).order_by('-created_at')
        
        serializer = self.get_serializer(my_hotspots, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def cities(self, request):
        """Get list of cities with hotspots."""
        cities = HotSpot.objects.filter(
            is_active=True
        ).values_list('city', flat=True).distinct().order_by('city')
        
        return Response(list(cities))
    
    @action(detail=False, methods=['get'])
    def states(self, request):
        """Get list of states with hotspots."""
        states = HotSpot.objects.filter(
            is_active=True
        ).values_list('state', flat=True).distinct().order_by('state')
        
        return Response(list(states)) 