"""
Events API Views for CalloutRacing Application

This module contains views for managing racing events:
- Event listing, creation, and management
- Event participation
- Event statistics
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta

from core.models.racing import Event, EventParticipant
from .serializers import EventSerializer, EventCreateSerializer, EventParticipantSerializer


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for managing racing events."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EventCreateSerializer
        return EventSerializer
    
    def get_queryset(self):
        queryset = Event.objects.all()
        
        # Filter by event type
        event_type = self.request.query_params.get('event_type', None)
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            try:
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                queryset = queryset.filter(start_date__gte=start_date)
            except ValueError:
                pass
        
        end_date = self.request.query_params.get('end_date', None)
        if end_date:
            try:
                end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                queryset = queryset.filter(end_date__lte=end_date)
            except ValueError:
                pass
        
        # Filter by location/track
        track_id = self.request.query_params.get('track_id', None)
        if track_id:
            queryset = queryset.filter(track_id=track_id)
        
        # Filter by organizer
        organizer_id = self.request.query_params.get('organizer_id', None)
        if organizer_id:
            queryset = queryset.filter(organizer_id=organizer_id)
        
        # Filter by status (active/inactive)
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        # Filter by public/private
        is_public = self.request.query_params.get('is_public', None)
        if is_public is not None:
            is_public = is_public.lower() == 'true'
            queryset = queryset.filter(is_public=is_public)
        
        # Search by title or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-start_date')
    
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join an event."""
        event = self.get_object()
        user = request.user
        
        # Check if user is already a participant
        if EventParticipant.objects.filter(event=event, user=user).exists():
            return Response(
                {'detail': 'You are already registered for this event.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if event is full
        if event.max_participants and event.participants.count() >= event.max_participants:
            return Response(
                {'detail': 'This event is full.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create participation
        participant = EventParticipant.objects.create(
            event=event,
            user=user
        )
        
        serializer = EventParticipantSerializer(participant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave an event."""
        event = self.get_object()
        user = request.user
        
        try:
            participant = EventParticipant.objects.get(event=event, user=user)
            participant.delete()
            return Response({'detail': 'Successfully left the event.'})
        except EventParticipant.DoesNotExist:
            return Response(
                {'detail': 'You are not registered for this event.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        """Get list of event participants."""
        event = self.get_object()
        participants = event.participants.all()
        serializer = EventParticipantSerializer(participants, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm_participant(self, request, pk=None):
        """Confirm a participant (organizer only)."""
        event = self.get_object()
        
        # Check if user is organizer
        if event.organizer != request.user:
            return Response(
                {'detail': 'Only the organizer can confirm participants.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        participant_id = request.data.get('participant_id')
        if not participant_id:
            return Response(
                {'detail': 'participant_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            participant = EventParticipant.objects.get(
                event=event,
                id=participant_id
            )
            participant.is_confirmed = True
            participant.save()
            
            serializer = EventParticipantSerializer(participant)
            return Response(serializer.data)
        except EventParticipant.DoesNotExist:
            return Response(
                {'detail': 'Participant not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming events."""
        now = timezone.now()
        upcoming_events = Event.objects.filter(
            start_date__gte=now,
            is_active=True
        ).order_by('start_date')[:10]
        
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_events(self, request):
        """Get events organized by the current user."""
        my_events = Event.objects.filter(organizer=request.user).order_by('-start_date')
        serializer = self.get_serializer(my_events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def participating(self, request):
        """Get events the current user is participating in."""
        participating_events = Event.objects.filter(
            participants__user=request.user
        ).order_by('-start_date')
        serializer = self.get_serializer(participating_events, many=True)
        return Response(serializer.data) 