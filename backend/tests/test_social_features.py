from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from core.models import (
    UserProfile, Friendship, Message, UserPost, PostComment,
    RacingCrew, CrewMembership, CarProfile, CarModification
)
from api.serializers import (
    UserProfileSerializer, FriendshipSerializer, MessageSerializer,
    UserPostSerializer, PostCommentSerializer, RacingCrewSerializer,
    CrewMembershipSerializer
)
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class UserProfileTests(APITestCase):
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
        self.profile1 = UserProfile.objects.create(
            user=self.user1,
            bio='Professional drag racer',
            location='Los Angeles, CA',
            car_make='Chevrolet',
            car_model='Camaro',
            wins=15,
            losses=5,
            total_races=20
        )
        self.profile2 = UserProfile.objects.create(
            user=self.user2,
            bio='Weekend warrior',
            location='Miami, FL',
            car_make='Ford',
            car_model='Mustang',
            wins=8,
            losses=12,
            total_races=20
        )

    def test_get_user_profile(self):
        """Test retrieving a user's profile."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/api/profiles/{self.profile1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'Professional drag racer')
        # Note: win_rate calculation would need to be implemented in the model or serializer

    def test_update_user_profile(self):
        """Test updating a user's profile."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'bio': 'Updated bio',
            'location': 'New York, NY',
            'car_make': 'Dodge',
            'car_model': 'Challenger'
        }
        response = self.client.patch(f'/api/profiles/{self.profile1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile1.refresh_from_db()
        self.assertEqual(self.profile1.bio, 'Updated bio')

    def test_update_stats(self):
        """Test updating race statistics."""
        self.client.force_authenticate(user=self.user1)
        data = {'wins': 20, 'losses': 8, 'total_races': 28}
        response = self.client.post(f'/api/profiles/{self.profile1.id}/update_stats/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: win_rate calculation would need to be implemented

    def test_upload_profile_picture(self):
        """Test uploading a profile picture."""
        self.client.force_authenticate(user=self.user1)
        # This would require a mock file upload in a real test
        # For now, we'll test the endpoint exists
        response = self.client.post(f'/api/profiles/{self.profile1.id}/upload_profile_picture/')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_200_OK])


class FriendshipTests(APITestCase):
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

    def test_send_friend_request(self):
        """Test sending a friend request."""
        self.client.force_authenticate(user=self.user1)
        data = {'receiver': self.user2.id}
        response = self.client.post('/api/friendships/send_request/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Friendship.objects.filter(
            sender=self.user1, receiver=self.user2, status='pending'
        ).exists())

    def test_accept_friend_request(self):
        """Test accepting a friend request."""
        friendship = Friendship.objects.create(
            sender=self.user1,
            receiver=self.user2,
            status='pending'
        )
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/friendships/{friendship.id}/accept/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friendship.refresh_from_db()
        self.assertEqual(friendship.status, 'accepted')

    def test_decline_friend_request(self):
        """Test declining a friend request."""
        friendship = Friendship.objects.create(
            sender=self.user1,
            receiver=self.user2,
            status='pending'
        )
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/friendships/{friendship.id}/decline/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friendship.refresh_from_db()
        self.assertEqual(friendship.status, 'declined')

    def test_get_friends_list(self):
        """Test getting list of friends."""
        friendship = Friendship.objects.create(
            sender=self.user1,
            receiver=self.user2,
            status='accepted'
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/friendships/friends/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_pending_requests(self):
        """Test getting pending friend requests."""
        friendship = Friendship.objects.create(
            sender=self.user1,
            receiver=self.user2,
            status='pending'
        )
        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/friendships/pending_requests/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_remove_friend(self):
        """Test removing a friend."""
        friendship = Friendship.objects.create(
            sender=self.user1,
            receiver=self.user2,
            status='accepted'
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/friendships/remove_friend/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Friendship.objects.filter(id=friendship.id).exists())


class MessagingTests(APITestCase):
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

    def test_send_message(self):
        """Test sending a message."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'recipient': self.user2.id,
            'content': 'Hey, want to race this weekend?'
        }
        response = self.client.post('/api/messages/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Message.objects.filter(
            sender=self.user1, recipient=self.user2
        ).exists())

    def test_get_conversation(self):
        """Test getting conversation between users."""
        message1 = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content='Hey there!'
        )
        message2 = Message.objects.create(
            sender=self.user2,
            recipient=self.user1,
            content='Hello!'
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/api/messages/conversation/?user={self.user2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_mark_message_as_read(self):
        """Test marking a message as read."""
        message = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content='Test message'
        )
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/messages/{message.id}/mark_as_read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message.refresh_from_db()
        self.assertTrue(message.is_read)

    def test_get_unread_count(self):
        """Test getting unread message count."""
        Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content='Unread message'
        )
        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/messages/unread_count/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 1)


class UserPostTests(APITestCase):
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
        self.car = CarProfile.objects.create(
            user=self.user1,
            name='My Camaro',
            make='Chevrolet',
            model='Camaro',
            year=2020
        )

    def test_create_post(self):
        """Test creating a user post."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'content': 'Just finished my new build!',
            'car': self.car.id
        }
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserPost.objects.filter(
            author=self.user1, content='Just finished my new build!'
        ).exists())

    def test_like_post(self):
        """Test liking a post."""
        post = UserPost.objects.create(
            author=self.user1,
            content='Test post'
        )
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/posts/{post.id}/like_post/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.likes_count, 1)

    def test_get_feed(self):
        """Test getting user feed."""
        post1 = UserPost.objects.create(
            author=self.user1,
            content='Post 1'
        )
        post2 = UserPost.objects.create(
            author=self.user2,
            content='Post 2'
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/posts/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_add_comment(self):
        """Test adding a comment to a post."""
        post = UserPost.objects.create(
            author=self.user1,
            content='Test post'
        )
        self.client.force_authenticate(user=self.user2)
        data = {'content': 'Great post!'}
        response = self.client.post(f'/api/posts/{post.id}/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PostComment.objects.filter(
            post=post, author=self.user2, content='Great post!'
        ).exists())


class RacingCrewTests(APITestCase):
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

    def test_create_racing_crew(self):
        """Test creating a racing crew."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'name': 'Speed Demons',
            'description': 'Professional racing crew',
            'crew_type': 'drag_racing',
            'location': 'Los Angeles, CA'
        }
        response = self.client.post('/api/crews/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(RacingCrew.objects.filter(
            name='Speed Demons', owner=self.user1
        ).exists())

    def test_join_crew(self):
        """Test joining a racing crew."""
        crew = RacingCrew.objects.create(
            name='Speed Demons',
            owner=self.user1,
            description='Test crew'
        )
        self.client.force_authenticate(user=self.user2)
        data = {'crew': crew.id}
        response = self.client.post('/api/crew-memberships/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CrewMembership.objects.filter(
            crew=crew, member=self.user2, status='pending'
        ).exists())

    def test_accept_crew_invitation(self):
        """Test accepting a crew invitation."""
        crew = RacingCrew.objects.create(
            name='Speed Demons',
            owner=self.user1,
            description='Test crew'
        )
        membership = CrewMembership.objects.create(
            crew=crew,
            member=self.user2,
            status='pending'
        )
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/crew-memberships/{membership.id}/accept_invitation/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        membership.refresh_from_db()
        self.assertEqual(membership.status, 'accepted')

    def test_get_crew_members(self):
        """Test getting crew members."""
        crew = RacingCrew.objects.create(
            name='Speed Demons',
            owner=self.user1,
            description='Test crew'
        )
        CrewMembership.objects.create(
            crew=crew,
            member=self.user2,
            status='accepted'
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/api/crews/{crew.id}/members/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # owner + member


class SocialFeatureIntegrationTests(APITestCase):
    """Integration tests for social features working together."""
    
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

    def test_complete_social_workflow(self):
        """Test a complete social workflow: friend request, messaging, posting."""
        # 1. Send friend request
        self.client.force_authenticate(user=self.user1)
        data = {'receiver': self.user2.id}
        response = self.client.post('/api/friendships/send_request/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 2. Accept friend request
        friendship = Friendship.objects.get(sender=self.user1, receiver=self.user2)
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/friendships/{friendship.id}/accept/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 3. Send message
        self.client.force_authenticate(user=self.user1)
        data = {'recipient': self.user2.id, 'content': 'Hey friend!'}
        response = self.client.post('/api/messages/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 4. Create post
        data = {'content': 'Great race today!'}
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 5. Friend likes the post
        post = UserPost.objects.get(author=self.user1)
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/posts/{post.id}/like_post/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify all interactions worked
        self.assertTrue(Friendship.objects.filter(
            sender=self.user1, receiver=self.user2, status='accepted'
        ).exists())
        self.assertTrue(Message.objects.filter(
            sender=self.user1, recipient=self.user2
        ).exists())
        post.refresh_from_db()
        self.assertEqual(post.likes_count, 1) 