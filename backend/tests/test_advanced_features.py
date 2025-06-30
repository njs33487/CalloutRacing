from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from core.models import (
    UserProfile, LocationBroadcast, HotSpot, OpenChallenge,
    ChallengeResponse, Bet, BettingPool, BuildLog, BuildLogEntry,
    PerformanceData, CarProfile, CarModification, Track
)
from api.serializers import (
    LocationBroadcastSerializer, HotSpotSerializer, OpenChallengeSerializer,
    ChallengeResponseSerializer, BetSerializer, BettingPoolSerializer,
    BuildLogSerializer, BuildLogEntrySerializer, PerformanceDataSerializer
)
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import json

User = get_user_model()


class LocationBroadcastingTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='racer1',
            email='racer1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='racer2',
            email='racer2@test.com',
            password='testpass123'
        )
        self.user3 = User.objects.create_user(
            username='racer3',
            email='racer3@test.com',
            password='testpass123'
        )

    def test_broadcast_location(self):
        """Test broadcasting current location."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'latitude': 34.0522,
            'longitude': -118.2437,
            'message': 'I\'m Here, Who\'s There?',
            'duration_minutes': 30
        }
        response = self.client.post('/api/location/broadcast/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(LocationBroadcast.objects.filter(
            user=self.user1, message='I\'m Here, Who\'s There?'
        ).exists())

    def test_get_nearby_broadcasts(self):
        """Test getting nearby location broadcasts."""
        # Create broadcasts at different locations
        LocationBroadcast.objects.create(
            user=self.user1,
            latitude=34.0522,
            longitude=-118.2437,
            message='At LA Raceway',
            expires_at=timezone.now() + timedelta(minutes=30)
        )
        LocationBroadcast.objects.create(
            user=self.user2,
            latitude=34.0523,
            longitude=-118.2438,
            message='Also at LA Raceway',
            expires_at=timezone.now() + timedelta(minutes=30)
        )
        LocationBroadcast.objects.create(
            user=self.user3,
            latitude=25.7617,
            longitude=-80.1918,
            message='At Miami Speedway',
            expires_at=timezone.now() + timedelta(minutes=30)
        )
        
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/location/nearby_broadcasts/?lat=34.0522&lng=-118.2437&radius=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should only get LA broadcasts

    def test_respond_to_broadcast(self):
        """Test responding to a location broadcast."""
        broadcast = LocationBroadcast.objects.create(
            user=self.user1,
            latitude=34.0522,
            longitude=-118.2437,
            message='I\'m Here, Who\'s There?',
            expires_at=timezone.now() + timedelta(minutes=30)
        )
        self.client.force_authenticate(user=self.user2)
        data = {'message': 'I\'m nearby! Let\'s race!'}
        response = self.client.post(f'/api/location/broadcasts/{broadcast.id}/respond/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_extend_broadcast_duration(self):
        """Test extending broadcast duration."""
        broadcast = LocationBroadcast.objects.create(
            user=self.user1,
            latitude=34.0522,
            longitude=-118.2437,
            message='I\'m Here, Who\'s There?',
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        self.client.force_authenticate(user=self.user1)
        data = {'duration_minutes': 60}
        response = self.client.patch(f'/api/location/broadcasts/{broadcast.id}/extend/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        broadcast.refresh_from_db()
        self.assertTrue(broadcast.expires_at > timezone.now() + timedelta(minutes=50))

    def test_stop_broadcast(self):
        """Test stopping a location broadcast."""
        broadcast = LocationBroadcast.objects.create(
            user=self.user1,
            latitude=34.0522,
            longitude=-118.2437,
            message='I\'m Here, Who\'s There?',
            expires_at=timezone.now() + timedelta(minutes=30)
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'/api/location/broadcasts/{broadcast.id}/stop/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        broadcast.refresh_from_db()
        self.assertTrue(broadcast.expires_at <= timezone.now())


class HotSpotsTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='racer1',
            email='racer1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='racer2',
            email='racer2@test.com',
            password='testpass123'
        )

    def test_create_hot_spot(self):
        """Test creating a hot spot."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'name': 'LA Raceway',
            'description': 'Popular racing spot in Los Angeles',
            'latitude': 34.0522,
            'longitude': -118.2437,
            'category': 'race_track',
            'address': '123 Racing Blvd, Los Angeles, CA'
        }
        response = self.client.post('/api/hotspots/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(HotSpot.objects.filter(
            name='LA Raceway', created_by=self.user1
        ).exists())

    def test_get_hot_spots(self):
        """Test getting hot spots."""
        HotSpot.objects.create(
            name='LA Raceway',
            description='Popular racing spot',
            latitude=34.0522,
            longitude=-118.2437,
            category='race_track',
            created_by=self.user1
        )
        response = self.client.get('/api/hotspots/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_hot_spots_by_location(self):
        """Test searching hot spots by location."""
        HotSpot.objects.create(
            name='LA Raceway',
            description='Popular racing spot',
            latitude=34.0522,
            longitude=-118.2437,
            category='race_track',
            created_by=self.user1
        )
        response = self.client.get('/api/hotspots/search/?lat=34.0522&lng=-118.2437&radius=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_hot_spots_by_category(self):
        """Test filtering hot spots by category."""
        HotSpot.objects.create(
            name='LA Raceway',
            description='Popular racing spot',
            latitude=34.0522,
            longitude=-118.2437,
            category='race_track',
            created_by=self.user1
        )
        HotSpot.objects.create(
            name='Downtown Meet Point',
            description='Car meet location',
            latitude=34.0522,
            longitude=-118.2437,
            category='meet_point',
            created_by=self.user1
        )
        response = self.client.get('/api/hotspots/?category=race_track')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_rate_hot_spot(self):
        """Test rating a hot spot."""
        hotspot = HotSpot.objects.create(
            name='LA Raceway',
            description='Popular racing spot',
            latitude=34.0522,
            longitude=-118.2437,
            category='race_track',
            created_by=self.user1
        )
        self.client.force_authenticate(user=self.user2)
        data = {'rating': 5, 'comment': 'Great racing spot!'}
        response = self.client.post(f'/api/hotspots/{hotspot.id}/rate/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_in_to_hot_spot(self):
        """Test checking in to a hot spot."""
        hotspot = HotSpot.objects.create(
            name='LA Raceway',
            description='Popular racing spot',
            latitude=34.0522,
            longitude=-118.2437,
            category='race_track',
            created_by=self.user1
        )
        self.client.force_authenticate(user=self.user2)
        data = {'message': 'Just arrived!'}
        response = self.client.post(f'/api/hotspots/{hotspot.id}/check_in/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OpenChallengesTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='racer1',
            email='racer1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='racer2',
            email='racer2@test.com',
            password='testpass123'
        )
        self.track = Track.objects.create(
            name='LA Raceway',
            location='Los Angeles, CA',
            track_type='drag_strip'
        )

    def test_create_open_challenge(self):
        """Test creating an open challenge."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'Quarter Mile Challenge',
            'description': 'Any takers for a quarter mile race?',
            'track': self.track.id,
            'challenge_type': 'quarter_mile',
            'stakes': 'bragging_rights',
            'expires_at': (timezone.now() + timedelta(hours=2)).isoformat()
        }
        response = self.client.post('/api/challenges/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(OpenChallenge.objects.filter(
            title='Quarter Mile Challenge', challenger=self.user1
        ).exists())

    def test_get_open_challenges(self):
        """Test getting open challenges."""
        OpenChallenge.objects.create(
            challenger=self.user1,
            title='Quarter Mile Challenge',
            description='Any takers?',
            track=self.track,
            challenge_type='quarter_mile',
            stakes='bragging_rights',
            expires_at=timezone.now() + timedelta(hours=2)
        )
        response = self.client.get('/api/challenges/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_respond_to_challenge(self):
        """Test responding to an open challenge."""
        challenge = OpenChallenge.objects.create(
            challenger=self.user1,
            title='Quarter Mile Challenge',
            description='Any takers?',
            track=self.track,
            challenge_type='quarter_mile',
            stakes='bragging_rights',
            expires_at=timezone.now() + timedelta(hours=2)
        )
        self.client.force_authenticate(user=self.user2)
        data = {'message': 'I accept your challenge!'}
        response = self.client.post(f'/api/challenges/{challenge.id}/respond/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ChallengeResponse.objects.filter(
            challenge=challenge, responder=self.user2
        ).exists())

    def test_filter_challenges_by_type(self):
        """Test filtering challenges by type."""
        OpenChallenge.objects.create(
            challenger=self.user1,
            title='Quarter Mile Challenge',
            description='Any takers?',
            track=self.track,
            challenge_type='quarter_mile',
            stakes='bragging_rights',
            expires_at=timezone.now() + timedelta(hours=2)
        )
        OpenChallenge.objects.create(
            challenger=self.user1,
            title='Dyno Challenge',
            description='Dyno competition',
            track=self.track,
            challenge_type='dyno',
            stakes='bragging_rights',
            expires_at=timezone.now() + timedelta(hours=2)
        )
        response = self.client.get('/api/challenges/?challenge_type=quarter_mile')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_cancel_challenge(self):
        """Test canceling an open challenge."""
        challenge = OpenChallenge.objects.create(
            challenger=self.user1,
            title='Quarter Mile Challenge',
            description='Any takers?',
            track=self.track,
            challenge_type='quarter_mile',
            stakes='bragging_rights',
            expires_at=timezone.now() + timedelta(hours=2)
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'/api/challenges/{challenge.id}/cancel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        challenge.refresh_from_db()
        self.assertEqual(challenge.status, 'cancelled')


class BettingSystemTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='racer1',
            email='racer1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='racer2',
            email='racer2@test.com',
            password='testpass123'
        )
        self.user3 = User.objects.create_user(
            username='racer3',
            email='racer3@test.com',
            password='testpass123'
        )

    def test_create_betting_pool(self):
        """Test creating a betting pool for a race."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'Quarter Mile Race',
            'description': 'Race between two cars',
            'participants': [self.user1.id, self.user2.id],
            'total_pot': Decimal('1000.00'),
            'entry_fee': Decimal('50.00'),
            'race_date': (timezone.now() + timedelta(days=1)).isoformat()
        }
        response = self.client.post('/api/betting/pools/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(BettingPool.objects.filter(
            title='Quarter Mile Race', created_by=self.user1
        ).exists())

    def test_place_bet(self):
        """Test placing a bet on a race."""
        pool = BettingPool.objects.create(
            title='Quarter Mile Race',
            description='Race between two cars',
            created_by=self.user1,
            total_pot=Decimal('1000.00'),
            entry_fee=Decimal('50.00'),
            race_date=timezone.now() + timedelta(days=1)
        )
        self.client.force_authenticate(user=self.user3)
        data = {
            'pool': pool.id,
            'predicted_winner': self.user1.id,
            'amount': Decimal('100.00')
        }
        response = self.client.post('/api/betting/bets/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Bet.objects.filter(
            bettor=self.user3, pool=pool
        ).exists())

    def test_get_betting_pools(self):
        """Test getting available betting pools."""
        BettingPool.objects.create(
            title='Quarter Mile Race',
            description='Race between two cars',
            created_by=self.user1,
            total_pot=Decimal('1000.00'),
            entry_fee=Decimal('50.00'),
            race_date=timezone.now() + timedelta(days=1)
        )
        response = self.client.get('/api/betting/pools/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_pool_details(self):
        """Test getting detailed information about a betting pool."""
        pool = BettingPool.objects.create(
            title='Quarter Mile Race',
            description='Race between two cars',
            created_by=self.user1,
            total_pot=Decimal('1000.00'),
            entry_fee=Decimal('50.00'),
            race_date=timezone.now() + timedelta(days=1)
        )
        Bet.objects.create(
            bettor=self.user2,
            pool=pool,
            predicted_winner=self.user1,
            amount=Decimal('100.00')
        )
        response = self.client.get(f'/api/betting/pools/{pool.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_bets'], 1)

    def test_set_race_winner(self):
        """Test setting the winner of a race and distributing winnings."""
        pool = BettingPool.objects.create(
            title='Quarter Mile Race',
            description='Race between two cars',
            created_by=self.user1,
            total_pot=Decimal('1000.00'),
            entry_fee=Decimal('50.00'),
            race_date=timezone.now() + timedelta(days=1)
        )
        Bet.objects.create(
            bettor=self.user2,
            pool=pool,
            predicted_winner=self.user1,
            amount=Decimal('100.00')
        )
        Bet.objects.create(
            bettor=self.user3,
            pool=pool,
            predicted_winner=self.user2,
            amount=Decimal('50.00')
        )
        
        self.client.force_authenticate(user=self.user1)
        data = {'winner': self.user1.id}
        response = self.client.post(f'/api/betting/pools/{pool.id}/set_winner/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pool.refresh_from_db()
        self.assertEqual(pool.winner, self.user1)


class BuildLogsTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='racer1',
            email='racer1@test.com',
            password='testpass123'
        )
        self.car = CarProfile.objects.create(
            user=self.user1,
            name='My Camaro',
            make='Chevrolet',
            model='Camaro',
            year=2020
        )

    def test_create_build_log(self):
        """Test creating a build log for a car."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'car': self.car.id,
            'title': 'Camaro Build Log',
            'description': 'Documenting my Camaro build progress'
        }
        response = self.client.post('/api/build-logs/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(BuildLog.objects.filter(
            title='Camaro Build Log', owner=self.user1
        ).exists())

    def test_add_build_log_entry(self):
        """Test adding an entry to a build log."""
        build_log = BuildLog.objects.create(
            owner=self.user1,
            car=self.car,
            title='Camaro Build Log',
            description='Documenting my Camaro build progress'
        )
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'Installed Turbocharger',
            'content': 'Added a new turbocharger for more power',
            'modifications': ['turbocharger'],
            'cost': '2500.00',
            'hours_spent': 8
        }
        response = self.client.post(f'/api/build-logs/{build_log.id}/entries/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(BuildLogEntry.objects.filter(
            build_log=build_log, title='Installed Turbocharger'
        ).exists())

    def test_get_build_logs(self):
        """Test getting build logs."""
        BuildLog.objects.create(
            owner=self.user1,
            car=self.car,
            title='Camaro Build Log',
            description='Documenting my Camaro build progress'
        )
        response = self.client.get('/api/build-logs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_build_log_entries(self):
        """Test getting entries for a build log."""
        build_log = BuildLog.objects.create(
            owner=self.user1,
            car=self.car,
            title='Camaro Build Log',
            description='Documenting my Camaro build progress'
        )
        BuildLogEntry.objects.create(
            build_log=build_log,
            title='Installed Turbocharger',
            content='Added a new turbocharger',
            modifications=['turbocharger'],
            cost=Decimal('2500.00'),
            hours_spent=8
        )
        response = self.client.get(f'/api/build-logs/{build_log.id}/entries/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_build_log_entry(self):
        """Test updating a build log entry."""
        build_log = BuildLog.objects.create(
            owner=self.user1,
            car=self.car,
            title='Camaro Build Log',
            description='Documenting my Camaro build progress'
        )
        entry = BuildLogEntry.objects.create(
            build_log=build_log,
            title='Installed Turbocharger',
            content='Added a new turbocharger',
            modifications=['turbocharger'],
            cost=Decimal('2500.00'),
            hours_spent=8
        )
        self.client.force_authenticate(user=self.user1)
        data = {'content': 'Updated: Added a new turbocharger with custom tuning'}
        response = self.client.patch(f'/api/build-logs/entries/{entry.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        entry.refresh_from_db()
        self.assertIn('custom tuning', entry.content)


class PerformanceDataTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='racer1',
            email='racer1@test.com',
            password='testpass123'
        )
        self.car = CarProfile.objects.create(
            user=self.user1,
            name='My Camaro',
            make='Chevrolet',
            model='Camaro',
            year=2020
        )
        self.track = Track.objects.create(
            name='LA Raceway',
            location='Los Angeles, CA',
            track_type='drag_strip'
        )

    def test_add_quarter_mile_time(self):
        """Test adding a quarter mile time."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'car': self.car.id,
            'track': self.track.id,
            'time_seconds': 12.5,
            'speed_mph': 115.0,
            'reaction_time': 0.2,
            'sixty_foot_time': 2.1,
            'date': timezone.now().date().isoformat(),
            'conditions': 'good',
            'notes': 'First run with new turbo'
        }
        response = self.client.post('/api/performance/quarter-mile/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PerformanceData.objects.filter(
            car=self.car, track=self.track, time_seconds=12.5
        ).exists())

    def test_add_dyno_results(self):
        """Test adding dyno results."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'car': self.car.id,
            'horsepower': 450,
            'torque': 420,
            'rpm_peak_hp': 6500,
            'rpm_peak_torque': 4500,
            'date': timezone.now().date().isoformat(),
            'dyno_type': 'dynojet',
            'notes': 'After turbo installation'
        }
        response = self.client.post('/api/performance/dyno/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PerformanceData.objects.filter(
            car=self.car, horsepower=450, dyno_type='dynojet'
        ).exists())

    def test_get_car_performance_history(self):
        """Test getting performance history for a car."""
        PerformanceData.objects.create(
            car=self.car,
            track=self.track,
            time_seconds=12.5,
            speed_mph=115.0,
            performance_type='quarter_mile',
            date=timezone.now().date()
        )
        PerformanceData.objects.create(
            car=self.car,
            horsepower=450,
            torque=420,
            performance_type='dyno',
            date=timezone.now().date()
        )
        response = self.client.get(f'/api/performance/car/{self.car.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_best_times(self):
        """Test getting best performance times."""
        PerformanceData.objects.create(
            car=self.car,
            track=self.track,
            time_seconds=12.5,
            speed_mph=115.0,
            performance_type='quarter_mile',
            date=timezone.now().date()
        )
        PerformanceData.objects.create(
            car=self.car,
            track=self.track,
            time_seconds=12.2,
            speed_mph=118.0,
            performance_type='quarter_mile',
            date=timezone.now().date()
        )
        response = self.client.get(f'/api/performance/car/{self.car.id}/best-times/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quarter_mile']['time_seconds'], 12.2)

    def test_verify_performance_data(self):
        """Test verifying performance data."""
        performance = PerformanceData.objects.create(
            car=self.car,
            track=self.track,
            time_seconds=12.5,
            speed_mph=115.0,
            performance_type='quarter_mile',
            date=timezone.now().date(),
            verified_by=None
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'/api/performance/{performance.id}/verify/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        performance.refresh_from_db()
        self.assertIsNotNone(performance.verified_by)

    def test_compare_performance(self):
        """Test comparing performance between cars."""
        car2 = CarProfile.objects.create(
            user=self.user1,
            name='My Mustang',
            make='Ford',
            model='Mustang',
            year=2019
        )
        PerformanceData.objects.create(
            car=self.car,
            track=self.track,
            time_seconds=12.5,
            speed_mph=115.0,
            performance_type='quarter_mile',
            date=timezone.now().date()
        )
        PerformanceData.objects.create(
            car=car2,
            track=self.track,
            time_seconds=12.8,
            speed_mph=112.0,
            performance_type='quarter_mile',
            date=timezone.now().date()
        )
        response = self.client.get(f'/api/performance/compare/?car1={self.car.id}&car2={car2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('comparison', response.data)


class AdvancedFeaturesIntegrationTests(APITestCase):
    """Integration tests for advanced features working together."""
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='racer1',
            email='racer1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='racer2',
            email='racer2@test.com',
            password='testpass123'
        )
        self.track = Track.objects.create(
            name='LA Raceway',
            location='Los Angeles, CA',
            track_type='drag_strip'
        )
        self.car = CarProfile.objects.create(
            user=self.user1,
            name='My Camaro',
            make='Chevrolet',
            model='Camaro',
            year=2020
        )

    def test_complete_advanced_workflow(self):
        """Test a complete advanced features workflow."""
        # 1. Create hot spot
        self.client.force_authenticate(user=self.user1)
        hotspot_data = {
            'name': 'LA Raceway',
            'description': 'Popular racing spot',
            'latitude': 34.0522,
            'longitude': -118.2437,
            'category': 'race_track',
            'address': '123 Racing Blvd, Los Angeles, CA'
        }
        response = self.client.post('/api/hotspots/', hotspot_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        hotspot = HotSpot.objects.get(name='LA Raceway')
        
        # 2. Broadcast location at hot spot
        broadcast_data = {
            'latitude': 34.0522,
            'longitude': -118.2437,
            'message': 'I\'m Here, Who\'s There?',
            'duration_minutes': 30
        }
        response = self.client.post('/api/location/broadcast/', broadcast_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 3. Create open challenge
        challenge_data = {
            'title': 'Quarter Mile Challenge',
            'description': 'Any takers for a quarter mile race?',
            'track': self.track.id,
            'challenge_type': 'quarter_mile',
            'stakes': 'bragging_rights',
            'expires_at': (timezone.now() + timedelta(hours=2)).isoformat()
        }
        response = self.client.post('/api/challenges/', challenge_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        challenge = OpenChallenge.objects.get(title='Quarter Mile Challenge')
        
        # 4. Add performance data
        performance_data = {
            'car': self.car.id,
            'track': self.track.id,
            'time_seconds': 12.5,
            'speed_mph': 115.0,
            'reaction_time': 0.2,
            'sixty_foot_time': 2.1,
            'date': timezone.now().date().isoformat(),
            'conditions': 'good',
            'notes': 'Recent run'
        }
        response = self.client.post('/api/performance/quarter-mile/', performance_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 5. Create build log entry
        build_log = BuildLog.objects.create(
            owner=self.user1,
            car=self.car,
            title='Camaro Build Log',
            description='Documenting my Camaro build progress'
        )
        entry_data = {
            'title': 'Installed Turbocharger',
            'content': 'Added a new turbocharger for more power',
            'modifications': ['turbocharger'],
            'cost': '2500.00',
            'hours_spent': 8
        }
        response = self.client.post(f'/api/build-logs/{build_log.id}/entries/', entry_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify all features worked together
        self.assertTrue(LocationBroadcast.objects.filter(user=self.user1).exists())
        self.assertTrue(OpenChallenge.objects.filter(challenger=self.user1).exists())
        self.assertTrue(PerformanceData.objects.filter(car=self.car).exists())
        self.assertTrue(BuildLogEntry.objects.filter(build_log=build_log).exists())
        
        # 6. Check in to hot spot
        response = self.client.post(f'/api/hotspots/{hotspot.id}/check_in/', {'message': 'Ready to race!'})
        self.assertEqual(response.status_code, status.HTTP_200_OK) 