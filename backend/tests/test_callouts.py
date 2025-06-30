"""
Callout System Tests

Tests for core racing functionality including callouts, tracks, and race results.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone

from core.models.racing import Callout, Track, RaceResult
from core.models.cars import CarProfile

User = get_user_model()


class CalloutModelTests(TestCase):
    """Test Callout model functionality."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.track = Track.objects.create(
            name='Test Track',
            location='Test Location',
            description='Test track description',
            created_by=self.user
        )
        self.car = CarProfile.objects.create(
            user=self.user,
            make='Toyota',
            model='Supra',
            year=2020,
            engine='2JZ',
            horsepower=300
        )
    
    def test_callout_creation(self):
        """Test basic callout creation."""
        callout = Callout.objects.create(
            challenger=self.user,
            track=self.track,
            car=self.car,
            title='Test Callout',
            description='Test callout description',
            experience_level='BEGINNER',
            is_invite_only=False
        )
        
        self.assertEqual(callout.challenger, self.user)
        self.assertEqual(callout.track, self.track)
        self.assertEqual(callout.car, self.car)
        self.assertEqual(callout.title, 'Test Callout')
        self.assertEqual(callout.status, 'PENDING')
        self.assertFalse(callout.is_invite_only)
    
    def test_callout_str_representation(self):
        """Test callout string representation."""
        callout = Callout.objects.create(
            challenger=self.user,
            track=self.track,
            car=self.car,
            title='Test Callout',
            description='Test callout description'
        )
        
        self.assertEqual(str(callout), 'Test Callout')
    
    def test_callout_status_transitions(self):
        """Test callout status transitions."""
        callout = Callout.objects.create(
            challenger=self.user,
            track=self.track,
            car=self.car,
            title='Test Callout',
            description='Test callout description'
        )
        
        # Initial status should be PENDING
        self.assertEqual(callout.status, 'PENDING')
        
        # Accept callout
        callout.status = 'ACCEPTED'
        callout.save()
        self.assertEqual(callout.status, 'ACCEPTED')
        
        # Complete callout
        callout.status = 'COMPLETED'
        callout.save()
        self.assertEqual(callout.status, 'COMPLETED')
    
    def test_callout_experience_levels(self):
        """Test callout experience level validation."""
        callout = Callout.objects.create(
            challenger=self.user,
            track=self.track,
            car=self.car,
            title='Test Callout',
            description='Test callout description',
            experience_level='BEGINNER'
        )
        
        self.assertEqual(callout.experience_level, 'BEGINNER')
        
        # Test other experience levels
        callout.experience_level = 'INTERMEDIATE'
        callout.save()
        self.assertEqual(callout.experience_level, 'INTERMEDIATE')
        
        callout.experience_level = 'ADVANCED'
        callout.save()
        self.assertEqual(callout.experience_level, 'ADVANCED')


class TrackModelTests(TestCase):
    """Test Track model functionality."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_track_creation(self):
        """Test basic track creation."""
        track = Track.objects.create(
            name='Test Track',
            location='Test Location',
            description='Test track description',
            created_by=self.user
        )
        
        self.assertEqual(track.name, 'Test Track')
        self.assertEqual(track.location, 'Test Location')
        self.assertEqual(track.created_by, self.user)
        self.assertTrue(track.is_active)
    
    def test_track_str_representation(self):
        """Test track string representation."""
        track = Track.objects.create(
            name='Test Track',
            location='Test Location',
            description='Test track description',
            created_by=self.user
        )
        
        self.assertEqual(str(track), 'Test Track')
    
    def test_track_verification(self):
        """Test track verification functionality."""
        track = Track.objects.create(
            name='Test Track',
            location='Test Location',
            description='Test track description',
            created_by=self.user
        )
        
        self.assertFalse(track.is_verified)
        
        track.is_verified = True
        track.save()
        self.assertTrue(track.is_verified)


class RaceResultModelTests(TestCase):
    """Test RaceResult model functionality."""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.track = Track.objects.create(
            name='Test Track',
            location='Test Location',
            description='Test track description',
            created_by=self.user1
        )
        self.car1 = CarProfile.objects.create(
            user=self.user1,
            make='Toyota',
            model='Supra',
            year=2020,
            engine='2JZ',
            horsepower=300
        )
        self.car2 = CarProfile.objects.create(
            user=self.user2,
            make='Nissan',
            model='Skyline',
            year=2019,
            engine='RB26',
            horsepower=280
        )
        self.callout = Callout.objects.create(
            challenger=self.user1,
            track=self.track,
            car=self.car1,
            title='Test Callout',
            description='Test callout description'
        )
    
    def test_race_result_creation(self):
        """Test basic race result creation."""
        result = RaceResult.objects.create(
            callout=self.callout,
            winner=self.user1,
            winner_car=self.car1,
            loser=self.user2,
            loser_car=self.car2,
            winner_time=12.5,
            loser_time=13.2,
            race_date=timezone.now()
        )
        
        self.assertEqual(result.winner, self.user1)
        self.assertEqual(result.loser, self.user2)
        self.assertEqual(result.winner_time, 12.5)
        self.assertEqual(result.loser_time, 13.2)
    
    def test_race_result_str_representation(self):
        """Test race result string representation."""
        result = RaceResult.objects.create(
            callout=self.callout,
            winner=self.user1,
            winner_car=self.car1,
            loser=self.user2,
            loser_car=self.car2,
            winner_time=12.5,
            loser_time=13.2,
            race_date=timezone.now()
        )
        
        expected = f'{self.user1.username} vs {self.user2.username} - {self.user1.username} wins'
        self.assertEqual(str(result), expected)


class CalloutAPITests(TestCase):
    """Test callout API endpoints."""
    
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
            description='Test track description',
            created_by=self.user
        )
        self.car = CarProfile.objects.create(
            user=self.user,
            make='Toyota',
            model='Supra',
            year=2020,
            engine='2JZ',
            horsepower=300
        )
    
    def test_create_callout(self):
        """Test creating a new callout."""
        data = {
            'track': self.track.id,
            'car': self.car.id,
            'title': 'Test Callout',
            'description': 'Test callout description',
            'experience_level': 'BEGINNER',
            'is_invite_only': False
        }
        
        response = self.client.post('/api/callouts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        callout = Callout.objects.get(id=response.data['id'])
        self.assertEqual(callout.challenger, self.user)
        self.assertEqual(callout.title, 'Test Callout')
        self.assertEqual(callout.status, 'PENDING')
    
    def test_list_callouts(self):
        """Test listing callouts."""
        Callout.objects.create(
            challenger=self.user,
            track=self.track,
            car=self.car,
            title='Test Callout 1',
            description='Test callout description'
        )
        Callout.objects.create(
            challenger=self.user,
            track=self.track,
            car=self.car,
            title='Test Callout 2',
            description='Test callout description'
        )
        
        response = self.client.get('/api/callouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_callout_detail(self):
        """Test getting callout details."""
        callout = Callout.objects.create(
            challenger=self.user,
            track=self.track,
            car=self.car,
            title='Test Callout',
            description='Test callout description'
        )
        
        response = self.client.get(f'/api/callouts/{callout.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Callout')
    
    def test_accept_callout(self):
        """Test accepting a callout."""
        callout = Callout.objects.create(
            challenger=self.user,
            track=self.track,
            car=self.car,
            title='Test Callout',
            description='Test callout description'
        )
        
        response = self.client.post(f'/api/callouts/{callout.id}/accept/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        callout.refresh_from_db()
        self.assertEqual(callout.status, 'ACCEPTED')
    
    def test_decline_callout(self):
        """Test declining a callout."""
        callout = Callout.objects.create(
            challenger=self.user,
            track=self.track,
            car=self.car,
            title='Test Callout',
            description='Test callout description'
        )
        
        response = self.client.post(f'/api/callouts/{callout.id}/decline/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        callout.refresh_from_db()
        self.assertEqual(callout.status, 'DECLINED')
    
    def test_cancel_callout(self):
        """Test canceling a callout."""
        callout = Callout.objects.create(
            challenger=self.user,
            track=self.track,
            car=self.car,
            title='Test Callout',
            description='Test callout description'
        )
        
        response = self.client.post(f'/api/callouts/{callout.id}/cancel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        callout.refresh_from_db()
        self.assertEqual(callout.status, 'CANCELLED')


class TrackAPITests(TestCase):
    """Test track API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_list_tracks(self):
        """Test listing tracks."""
        Track.objects.create(
            name='Track 1',
            location='Location 1',
            description='Description 1',
            created_by=self.user
        )
        Track.objects.create(
            name='Track 2',
            location='Location 2',
            description='Description 2',
            created_by=self.user
        )
        
        response = self.client.get('/api/tracks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_track_detail(self):
        """Test getting track details."""
        track = Track.objects.create(
            name='Test Track',
            location='Test Location',
            description='Test track description',
            created_by=self.user
        )
        
        response = self.client.get(f'/api/tracks/{track.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Track')
    
    def test_create_track(self):
        """Test creating a new track."""
        data = {
            'name': 'New Track',
            'location': 'New Location',
            'description': 'New track description'
        }
        
        response = self.client.post('/api/tracks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        track = Track.objects.get(id=response.data['id'])
        self.assertEqual(track.name, 'New Track')
        self.assertEqual(track.created_by, self.user)


class RaceResultAPITests(TestCase):
    """Test race result API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.token, _ = Token.objects.get_or_create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.track = Track.objects.create(
            name='Test Track',
            location='Test Location',
            description='Test track description',
            created_by=self.user1
        )
        self.car1 = CarProfile.objects.create(
            user=self.user1,
            make='Toyota',
            model='Supra',
            year=2020,
            engine='2JZ',
            horsepower=300
        )
        self.car2 = CarProfile.objects.create(
            user=self.user2,
            make='Nissan',
            model='Skyline',
            year=2019,
            engine='RB26',
            horsepower=280
        )
        self.callout = Callout.objects.create(
            challenger=self.user1,
            track=self.track,
            car=self.car1,
            title='Test Callout',
            description='Test callout description'
        )
    
    def test_create_race_result(self):
        """Test creating a race result."""
        data = {
            'callout': self.callout.id,
            'winner': self.user1.id,
            'winner_car': self.car1.id,
            'loser': self.user2.id,
            'loser_car': self.car2.id,
            'winner_time': 12.5,
            'loser_time': 13.2,
            'race_date': timezone.now().isoformat()
        }
        
        response = self.client.post('/api/race-results/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        result = RaceResult.objects.get(id=response.data['id'])
        self.assertEqual(result.winner, self.user1)
        self.assertEqual(result.loser, self.user2)
        self.assertEqual(result.winner_time, 12.5)
    
    def test_list_race_results(self):
        """Test listing race results."""
        RaceResult.objects.create(
            callout=self.callout,
            winner=self.user1,
            winner_car=self.car1,
            loser=self.user2,
            loser_car=self.car2,
            winner_time=12.5,
            loser_time=13.2,
            race_date=timezone.now()
        )
        
        response = self.client.get('/api/race-results/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 