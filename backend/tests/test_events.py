"""
Event Management Tests

Tests for event creation, participation, and management functionality.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta

from core.models.racing import Event, EventParticipant, Track

User = get_user_model()


class EventModelTests(TestCase):
    """Test Event model functionality."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.track = Track.objects.create(
            name='Test Track',
            location='Test Location',
            description='Test track description'
        )
    
    def test_event_creation(self):
        """Test basic event creation."""
        event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            max_participants=20,
            entry_fee=50.00,
            is_public=True,
            organizer=self.user,
            track=self.track
        )
        
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.organizer, self.user)
        self.assertEqual(event.track, self.track)
        self.assertEqual(event.event_type, 'RACE')
        self.assertTrue(event.is_public)
        self.assertTrue(event.is_active)
    
    def test_event_str_representation(self):
        """Test event string representation."""
        event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        
        self.assertEqual(str(event), 'Test Event')
    
    def test_event_participant_creation(self):
        """Test event participant creation."""
        event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        
        participant = EventParticipant.objects.create(
            event=event,
            user=self.user,
            registration_date=timezone.now()
        )
        
        self.assertEqual(participant.event, event)
        self.assertEqual(participant.user, self.user)
        self.assertIsNotNone(participant.registration_date)
    
    def test_event_participant_str_representation(self):
        """Test event participant string representation."""
        event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        
        participant = EventParticipant.objects.create(
            event=event,
            user=self.user,
            registration_date=timezone.now()
        )
        
        expected = f'{self.user.username} - {event.title}'
        self.assertEqual(str(participant), expected)
    
    def test_event_participants_relationship(self):
        """Test event participants relationship."""
        event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        
        EventParticipant.objects.create(
            event=event,
            user=self.user,
            registration_date=timezone.now()
        )
        
        # Test the reverse relationship
        self.assertEqual(event.participants.count(), 1)
        self.assertEqual(event.participants.first().user, self.user)
    
    def test_event_max_participants(self):
        """Test event maximum participants functionality."""
        event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            max_participants=2,
            organizer=self.user,
            track=self.track
        )
        
        # Create participants
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='testpass123'
        )
        
        EventParticipant.objects.create(
            event=event,
            user=self.user,
            registration_date=timezone.now()
        )
        EventParticipant.objects.create(
            event=event,
            user=user2,
            registration_date=timezone.now()
        )
        
        # Check if event is full
        self.assertEqual(event.participants.count(), 2)
        self.assertTrue(event.participants.count() >= event.max_participants)
    
    def test_event_types(self):
        """Test different event types."""
        event_types = ['RACE', 'MEETUP', 'TRAINING', 'COMPETITION']
        
        for event_type in event_types:
            event = Event.objects.create(
                title=f'Test {event_type} Event',
                description=f'Test {event_type} event description',
                event_type=event_type,
                start_date=timezone.now() + timedelta(days=7),
                end_date=timezone.now() + timedelta(days=7, hours=2),
                organizer=self.user,
                track=self.track
            )
            
            self.assertEqual(event.event_type, event_type)


class EventAPITests(TestCase):
    """Test event API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.track = Track.objects.create(
            name='Test Track',
            location='Test Location',
            description='Test track description'
        )
    
    def test_create_event(self):
        """Test creating a new event."""
        data = {
            'title': 'Test Event',
            'description': 'Test event description',
            'event_type': 'race',
            'start_date': (timezone.now() + timedelta(days=7)).isoformat(),
            'end_date': (timezone.now() + timedelta(days=7, hours=2)).isoformat(),
            'max_participants': 20,
            'entry_fee': 50.00,
            'is_public': True,
            'track': self.track.id
        }
        response = self.client.post('/api/events/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # List events and find the created one
        list_response = self.client.get('/api/events/')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        found = False
        for event in list_response.data['results']:
            if event['title'] == 'Test Event' and event['organizer'] == self.user.id:
                found = True
                self.assertEqual(event['track'], self.track.id)
                break
        self.assertTrue(found, 'Created event not found in event list')
    
    def test_list_events(self):
        """Test listing events."""
        Event.objects.create(
            title='Event 1',
            description='Event 1 description',
            event_type='race',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        Event.objects.create(
            title='Event 2',
            description='Event 2 description',
            event_type='meet',
            start_date=timezone.now() + timedelta(days=14),
            end_date=timezone.now() + timedelta(days=14, hours=3),
            organizer=self.user,
            track=self.track
        )
        
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_get_event_detail(self):
        """Test getting event details."""
        event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        
        response = self.client.get(f'/api/events/{event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Event')
    
    def test_join_event(self):
        """Test joining an event."""
        event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            max_participants=20,
            organizer=self.user,
            track=self.track
        )
        
        response = self.client.post(f'/api/events/{event.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if participant was created
        self.assertTrue(EventParticipant.objects.filter(event=event, user=self.user).exists())
    
    def test_join_event_already_participating(self):
        """Test joining an event when already participating."""
        event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        
        # Join event first time
        EventParticipant.objects.create(
            event=event,
            user=self.user,
            registration_date=timezone.now()
        )
        
        # Try to join again
        response = self.client.post(f'/api/events/{event.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_join_full_event(self):
        """Test joining a full event."""
        event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            max_participants=1,
            organizer=self.user,
            track=self.track
        )
        
        # Fill the event
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        EventParticipant.objects.create(
            event=event,
            user=user2,
            registration_date=timezone.now()
        )
        
        # Try to join full event
        response = self.client.post(f'/api/events/{event.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_leave_event(self):
        """Test leaving an event."""
        event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        
        # Join event first
        EventParticipant.objects.create(
            event=event,
            user=self.user,
            registration_date=timezone.now()
        )
        
        # Leave event
        response = self.client.post(f'/api/events/{event.id}/leave/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if participant was removed
        self.assertFalse(EventParticipant.objects.filter(event=event, user=self.user).exists())
    
    def test_leave_event_not_participating(self):
        """Test leaving an event when not participating."""
        event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        
        response = self.client.post(f'/api/events/{event.id}/leave/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_event_participants(self):
        """Test getting event participants."""
        event = Event.objects.create(
            title='Test Event',
            description='Test event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        
        EventParticipant.objects.create(
            event=event,
            user=self.user,
            registration_date=timezone.now()
        )
        
        response = self.client.get(f'/api/events/{event.id}/participants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_upcoming_events(self):
        """Test getting upcoming events."""
        # Create upcoming event
        Event.objects.create(
            title='Upcoming Event',
            description='Upcoming event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        
        # Create past event
        Event.objects.create(
            title='Past Event',
            description='Past event description',
            event_type='RACE',
            start_date=timezone.now() - timedelta(days=7),
            end_date=timezone.now() - timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        
        response = self.client.get('/api/events/upcoming/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Upcoming Event')
    
    def test_get_my_events(self):
        """Test getting events organized by current user."""
        Event.objects.create(
            title='My Event',
            description='My event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        
        # Create event by different user
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        Event.objects.create(
            title='Other Event',
            description='Other event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=user2,
            track=self.track
        )
        
        response = self.client.get('/api/events/my_events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'My Event')
    
    def test_get_participating_events(self):
        """Test getting events the user is participating in."""
        event = Event.objects.create(
            title='Participating Event',
            description='Participating event description',
            event_type='RACE',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        
        EventParticipant.objects.create(
            event=event,
            user=self.user,
            registration_date=timezone.now()
        )
        
        response = self.client.get('/api/events/participating/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Participating Event')
    
    def test_event_filtering(self):
        """Test event filtering by various parameters."""
        # Create an event with type 'race'
        Event.objects.create(
            title='Race Event',
            description='A race event',
            event_type='race',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=2),
            organizer=self.user,
            track=self.track
        )
        # Filter by event type
        response = self.client.get('/api/events/?event_type=race')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        found = any(event['title'] == 'Race Event' for event in response.data['results'])
        self.assertTrue(found, 'Filtered event not found in results') 