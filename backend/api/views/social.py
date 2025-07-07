"""
Social Feed API Views for CalloutRacing

This module provides API endpoints for social feed functionality:
- Live feed with posts from followed users
- Post creation and interaction
- Real-time updates via WebSocket
"""

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count, Prefetch
from django.utils import timezone
from datetime import timedelta
from core.models.auth import User

from core.models.social import UserPost, PostComment, Follow, Notification
from core.models.racing import Callout, Event
from ..serializers import (
    UserPostSerializer, 
    PostCommentSerializer,
    FeedItemSerializer,
    NotificationSerializer
)


class FeedPagination(PageNumberPagination):
    """Custom pagination for feed items."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class LiveFeedView(generics.ListAPIView):
    """
    Live social feed showing posts from followed users and trending content.
    
    GET /api/social/feed/
    - Returns posts from followed users
    - Includes trending posts from the community
    - Supports pagination
    - Filters by post type and time range
    """
    serializer_class = FeedItemSerializer
    pagination_class = FeedPagination
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Get users that the current user follows
        following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
        
        # Base query for posts from followed users
        followed_posts = UserPost.objects.filter(
            author__in=following_users,
            is_public=True
        ).select_related('author').prefetch_related('comments', 'likes')
        
        # Get trending posts from the last 7 days (posts with high engagement)
        trending_posts = UserPost.objects.filter(
            is_public=True,
            created_at__gte=timezone.now() - timedelta(days=7)
        ).annotate(
            total_engagement=Count('comments') + Count('likes')
        ).filter(
            total_engagement__gte=5  # Minimum engagement threshold
        ).select_related('author').prefetch_related('comments', 'likes')
        
        # Combine and order by engagement and recency
        combined_posts = (followed_posts | trending_posts).distinct().order_by(
            '-created_at'
        )
        
        # Apply filters
        post_type = self.request.query_params.get('post_type')
        if post_type:
            combined_posts = combined_posts.filter(post_type=post_type)
        
        time_filter = self.request.query_params.get('time_filter')
        if time_filter:
            if time_filter == 'today':
                combined_posts = combined_posts.filter(
                    created_at__gte=timezone.now().date()
                )
            elif time_filter == 'week':
                combined_posts = combined_posts.filter(
                    created_at__gte=timezone.now() - timedelta(days=7)
                )
            elif time_filter == 'month':
                combined_posts = combined_posts.filter(
                    created_at__gte=timezone.now() - timedelta(days=30)
                )
        
        return combined_posts


class CreatePostView(generics.CreateAPIView):
    """
    Create a new social post.
    
    POST /api/social/posts/
    - Creates a new post
    - Supports text, image, video, race_result, car_update, and live post types
    """
    serializer_class = UserPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        
        # Handle live streaming posts
        if post.post_type == 'live':
            post.is_live = True
            post.live_stream_title = self.request.data.get('live_stream_title', '')
            post.live_stream_url = self.request.data.get('live_stream_url', '')
            post.save()
        
        # Create notifications for followers
        followers = Follow.objects.filter(following=self.request.user)
        for follow in followers:
            notification_type = 'live' if post.post_type == 'live' else 'post'
            title = f'Live stream from {self.request.user.username}' if post.post_type == 'live' else f'New post from {self.request.user.username}'
            message = f'{self.request.user.username} is going live!' if post.post_type == 'live' else f'{self.request.user.username} just posted something new!'
            
            Notification.objects.create(
                recipient=follow.follower,
                sender=self.request.user,
                notification_type=notification_type,
                title=title,
                message=message
            )


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific post.
    
    GET /api/social/posts/{id}/
    PUT /api/social/posts/{id}/
    DELETE /api/social/posts/{id}/
    """
    serializer_class = UserPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserPost.objects.select_related('author').prefetch_related('comments', 'likes')
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated]
        return [permissions.IsAuthenticated]


class PostInteractionView(generics.GenericAPIView):
    """
    Handle post interactions (like, unlike, comment).
    
    POST /api/social/posts/{id}/like/
    POST /api/social/posts/{id}/unlike/
    POST /api/social/posts/{id}/comment/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk, action):
        try:
            post = UserPost.objects.get(pk=pk)
        except UserPost.DoesNotExist:
            return Response(
                {'error': 'Post not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if action == 'like':
            return self._like_post(request, post)
        elif action == 'unlike':
            return self._unlike_post(request, post)
        elif action == 'comment':
            return self._comment_post(request, post)
        else:
            return Response(
                {'error': 'Invalid action'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def _like_post(self, request, post):
        """Like a post."""
        user = request.user
        
        # Check if already liked
        if post.likes.filter(id=user.id).exists():
            return Response(
                {'error': 'Already liked this post'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add like
        post.likes.add(user)
        post.likes_count = post.likes.count()
        post.save()
        
        # Create notification
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                sender=user,
                notification_type='like',
                title=f'{user.username} liked your post',
                message=f'{user.username} liked your post: "{post.content[:50]}..."',
                related_object_id=post.id
            )
        
        return Response({'message': 'Post liked successfully'})
    
    def _unlike_post(self, request, post):
        """Unlike a post."""
        user = request.user
        
        # Remove like
        post.likes.remove(user)
        post.likes_count = post.likes.count()
        post.save()
        
        return Response({'message': 'Post unliked successfully'})
    
    def _comment_post(self, request, post):
        """Comment on a post."""
        content = request.data.get('content')
        if not content:
            return Response(
                {'error': 'Comment content is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create comment
        comment = PostComment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        
        # Update post comment count
        post.comments_count = post.comments.count()
        post.save()
        
        # Create notification
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type='comment',
                title=f'{request.user.username} commented on your post',
                message=f'{request.user.username} commented: "{content[:50]}..."',
                related_object_id=post.id
            )
        
        return Response(
            PostCommentSerializer(comment).data,
            status=status.HTTP_201_CREATED
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def trending_posts(request):
    """
    Get trending posts based on engagement.
    
    GET /api/social/trending/
    - Returns posts with high engagement in the last 7 days
    """
    trending_posts = UserPost.objects.filter(
        is_public=True,
        created_at__gte=timezone.now() - timedelta(days=7)
    ).annotate(
        total_engagement=Count('comments') + Count('likes')
    ).filter(
        total_engagement__gte=3
    ).select_related('author').prefetch_related('comments', 'likes').order_by(
        '-total_engagement', '-created_at'
    )[:20]
    
    serializer = FeedItemSerializer(trending_posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request, username):
    """
    Get posts from a specific user.
    
    GET /api/social/user/{username}/feed/
    - Returns posts from the specified user
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    posts = UserPost.objects.filter(
        author=user,
        is_public=True
    ).select_related('author').prefetch_related('comments', 'likes').order_by('-created_at')
    
    paginator = FeedPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)
    serializer = FeedItemSerializer(paginated_posts, many=True)
    
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notifications(request):
    """
    Get user notifications.
    
    GET /api/social/notifications/
    - Returns user's notifications
    """
    notifications = Notification.objects.filter(
        recipient=request.user
    ).select_related('sender').order_by('-created_at')
    
    paginator = FeedPagination()
    paginated_notifications = paginator.paginate_queryset(notifications, request)
    serializer = NotificationSerializer(paginated_notifications, many=True)
    
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_id):
    """
    Mark a notification as read.
    
    POST /api/social/notifications/{id}/read/
    """
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def live_streams(request):
    """
    Get active live streams.
    
    GET /api/social/live-streams/
    - Returns currently active live streams
    """
    live_posts = UserPost.objects.filter(
        is_live=True,
        is_public=True
    ).select_related('author').prefetch_related('comments', 'likes').order_by('-created_at')
    
    serializer = FeedItemSerializer(live_posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_live_viewers(request, post_id):
    """
    Update live stream viewer count.
    
    POST /api/social/posts/{id}/update-viewers/
    - Updates the viewer count for a live stream
    """
    try:
        post = UserPost.objects.get(pk=post_id, author=request.user, is_live=True)
        viewers_count = request.data.get('viewers_count', 0)
        post.live_viewers_count = viewers_count
        post.save()
        return Response({'status': 'success', 'viewers_count': viewers_count})
    except UserPost.DoesNotExist:
        return Response(
            {'error': 'Live stream not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )