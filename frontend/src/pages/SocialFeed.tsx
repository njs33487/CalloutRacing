import React, { useState, useEffect, useCallback } from 'react';
// import { useAuth } from '../contexts/AuthContext'; // Removed unused import
import { Plus, RefreshCw, Filter, TrendingUp, Users, Bell, Search } from 'lucide-react';
import { api } from '../services/api';
import FeedItem from '../components/social/FeedItem';
import CreatePost from '../components/social/CreatePost';
import LoadingFallback from '../components/LoadingFallback';
import UserSearch from '../components/UserSearch';

interface Post {
  id: number;
  author: {
    id: number;
    username: string;
    email: string;
  };
  content: string;
  post_type: 'text' | 'image' | 'video' | 'race_result' | 'car_update' | 'live' | 'race_callout' | 'announcement';
  image?: string;
  video?: string;
  likes_count: number;
  comments_count: number;
  is_liked: boolean;
  time_ago: string;
  comments: Array<{
    id: number;
    author: {
      username: string;
    };
    content: string;
    time_ago: string;
  }>;
  created_at: string;
}

interface Notification {
  id: number;
  sender: {
    username: string;
  };
  notification_type: string;
  title: string;
  message: string;
  is_read: boolean;
  time_ago: string;
  created_at: string;
}

const SocialFeed: React.FC = () => {
  // const { user } = useAuth(); // Removed unused variable
  const [posts, setPosts] = useState<Post[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [showCreatePost, setShowCreatePost] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [activeTab, setActiveTab] = useState<'feed' | 'global' | 'trending'>('feed');
  const [postTypeFilter, setPostTypeFilter] = useState<string>('');
  const [timeFilter, setTimeFilter] = useState<string>('');
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(1);

  const fetchPosts = useCallback(async (pageNum = 1, refresh = false) => {
    try {
      const params = new URLSearchParams({
        page: pageNum.toString(),
        ...(postTypeFilter && { post_type: postTypeFilter }),
        ...(timeFilter && { time_filter: timeFilter }),
      });

      let endpoint;
      if (activeTab === 'trending') {
        endpoint = '/social/trending/';
      } else if (activeTab === 'global') {
        endpoint = '/social/global/';
      } else {
        endpoint = '/social/feed/';
      }
      
      const response = await api.get(`${endpoint}?${params}`);
      
      const newPosts = response.data.results || response.data;
      
      if (refresh) {
        setPosts(newPosts);
      } else {
        setPosts(prev => pageNum === 1 ? newPosts : [...prev, ...newPosts]);
      }
      
      setHasMore(newPosts.length === 20); // Assuming page size is 20
      setPage(pageNum);
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  }, [activeTab, postTypeFilter, timeFilter]);

  const fetchNotifications = useCallback(async () => {
    try {
      const response = await api.get('/social/notifications/');
      setNotifications(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching notifications:', error);
    }
  }, []);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([fetchPosts(1, true), fetchNotifications()]);
      setLoading(false);
    };
    loadData();
  }, [fetchPosts, fetchNotifications]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await Promise.all([fetchPosts(1, true), fetchNotifications()]);
    setRefreshing(false);
  };

  const handleLoadMore = () => {
    if (hasMore && !loading) {
      fetchPosts(page + 1);
    }
  };

  const handleCreatePost = async (postData: {
    content: string;
    post_type: 'text' | 'image' | 'video' | 'race_result' | 'car_update' | 'live' | 'race_callout' | 'announcement';
    image?: File;
    video?: File;
    callout_challenged_user?: string;
    callout_location?: string;
    callout_location_type?: 'street' | 'dragstrip';
    callout_race_type?: string;
    callout_scheduled_date?: string;
    is_pinned?: boolean;
    announcement_type?: 'general' | 'feature' | 'maintenance' | 'promotion' | 'event';
    announcement_priority?: 'low' | 'medium' | 'high' | 'critical';
  }) => {
    try {
      const formData = new FormData();
      formData.append('content', postData.content);
      formData.append('post_type', postData.post_type);
      if (postData.image) {
        formData.append('image', postData.image);
      }
      if (postData.video) {
        formData.append('video', postData.video);
      }
      if (postData.callout_challenged_user) {
        formData.append('callout_challenged_user', postData.callout_challenged_user);
      }
      if (postData.callout_location) {
        formData.append('callout_location', postData.callout_location);
      }
      if (postData.callout_location_type) {
        formData.append('callout_location_type', postData.callout_location_type);
      }
      if (postData.callout_race_type) {
        formData.append('callout_race_type', postData.callout_race_type);
      }
      if (postData.callout_scheduled_date) {
        formData.append('callout_scheduled_date', postData.callout_scheduled_date);
      }
      if (postData.is_pinned) {
        formData.append('is_pinned', postData.is_pinned.toString());
      }
      if (postData.announcement_type) {
        formData.append('announcement_type', postData.announcement_type);
      }
      if (postData.announcement_priority) {
        formData.append('announcement_priority', postData.announcement_priority);
      }

      await api.post('/social/posts/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setShowCreatePost(false);
      handleRefresh();
    } catch (error) {
      console.error('Error creating post:', error);
    }
  };

  const handleLike = async (postId: number) => {
    try {
      const post = posts.find(p => p.id === postId);
      if (!post) return;

      const action = post.is_liked ? 'unlike' : 'like';
      await api.post(`/social/posts/${postId}/${action}/`);

      setPosts(prev => prev.map(p => 
        p.id === postId 
          ? { 
              ...p, 
              is_liked: !p.is_liked,
              likes_count: p.is_liked ? p.likes_count - 1 : p.likes_count + 1
            }
          : p
      ));
    } catch (error) {
      console.error('Error liking post:', error);
    }
  };

  const handleComment = async (postId: number, content: string) => {
    try {
      const response = await api.post(`/social/posts/${postId}/comment/`, {
        content
      });

      setPosts(prev => prev.map(p => 
        p.id === postId 
          ? { 
              ...p, 
              comments_count: p.comments_count + 1,
              comments: [...p.comments, response.data]
            }
          : p
      ));
    } catch (error) {
      console.error('Error commenting on post:', error);
      throw error;
    }
  };

  const handleShare = async (postId: number) => {
    try {
      const post = posts.find(p => p.id === postId);
      if (!post) return;

      const shareData = {
        title: `Post by ${post.author.username}`,
        text: post.content,
        url: `${window.location.origin}/social/post/${postId}`,
      };

      if (navigator.share) {
        await navigator.share(shareData);
      } else {
        // Fallback: copy to clipboard
        await navigator.clipboard.writeText(shareData.url);
        alert('Post URL copied to clipboard!');
      }
    } catch (error) {
      console.error('Error sharing post:', error);
    }
  };

  const handleMarkNotificationRead = async (notificationId: number) => {
    try {
      await api.post(`/social/notifications/${notificationId}/read/`);
      setNotifications(prev => prev.map(n => 
        n.id === notificationId ? { ...n, is_read: true } : n
      ));
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  const unreadNotificationsCount = notifications.filter(n => !n.is_read).length;

  if (loading) {
    return <LoadingFallback />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Social Feed</h1>
            <p className="text-gray-600">Connect with the racing community</p>
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative p-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <Bell className="w-6 h-6" />
              {unreadNotificationsCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {unreadNotificationsCount}
                </span>
              )}
            </button>
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="p-2 text-gray-600 hover:text-gray-900 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-6 h-6 ${refreshing ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={() => setShowCreatePost(true)}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              <Plus className="w-5 h-5" />
              <span>Create Post</span>
            </button>
          </div>
        </div>

        {/* Notifications Panel */}
        {showNotifications && (
          <div className="mb-6 bg-white rounded-lg shadow-md border border-gray-200 p-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Notifications</h3>
            {notifications.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No notifications</p>
            ) : (
              <div className="space-y-3">
                {(notifications || []).map((notification) => (
                  <div
                    key={notification.id}
                    className={`p-3 rounded-lg border ${
                      notification.is_read ? 'bg-gray-50 border-gray-200' : 'bg-blue-50 border-blue-200'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-gray-900">{notification.title}</p>
                        <p className="text-sm text-gray-600">{notification.message}</p>
                        <p className="text-xs text-gray-500 mt-1">{notification.time_ago}</p>
                      </div>
                      {!notification.is_read && (
                        <button
                          onClick={() => handleMarkNotificationRead(notification.id)}
                          className="text-xs text-blue-600 hover:text-blue-800"
                        >
                          Mark read
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Tabs */}
        <div className="flex items-center space-x-6 mb-6">
          <button
            onClick={() => setActiveTab('feed')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              activeTab === 'feed'
                ? 'bg-blue-500 text-white'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Users className="w-5 h-5" />
            <span>My Feed</span>
          </button>
          <button
            onClick={() => setActiveTab('global')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              activeTab === 'global'
                ? 'bg-blue-500 text-white'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Users className="w-5 h-5" />
            <span>Global</span>
          </button>
          <button
            onClick={() => setActiveTab('trending')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              activeTab === 'trending'
                ? 'bg-blue-500 text-white'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <TrendingUp className="w-5 h-5" />
            <span>Trending</span>
          </button>
        </div>

        {/* Filters */}
        <div className="flex items-center space-x-4 mb-6">
          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-gray-500" />
            <span className="text-sm font-medium text-gray-700">Filters:</span>
          </div>
          
          <select
            value={postTypeFilter}
            onChange={(e) => setPostTypeFilter(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Types</option>
            <option value="text">Text</option>
            <option value="image">Photo</option>
            <option value="video">Video</option>
            <option value="race_result">Race Result</option>
            <option value="car_update">Car Update</option>
            <option value="live">Live Stream</option>
          </select>

          <select
            value={timeFilter}
            onChange={(e) => setTimeFilter(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Time</option>
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>
        </div>

        {/* User Search Section */}
        <div className="mb-6 bg-white rounded-lg shadow-md border border-gray-200 p-4">
          <div className="flex items-center space-x-2 mb-3">
            <Search className="w-5 h-5 text-gray-500" />
            <h3 className="text-lg font-semibold text-gray-900">Discover Users</h3>
          </div>
          <UserSearch 
            placeholder="Search for users to follow..."
            onUserSelect={(user) => {
              console.log('Selected user:', user);
              // You can add follow functionality here
            }}
          />
        </div>

        {/* Posts */}
        <div className="space-y-6">
          {posts.length === 0 ? (
            <div className="text-center py-12">
              <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No posts yet</h3>
              <p className="text-gray-600 mb-4">
                {activeTab === 'feed' 
                  ? 'Follow some users to see their posts in your feed'
                  : 'No trending posts at the moment'
                }
              </p>
              <button
                onClick={() => setShowCreatePost(true)}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
              >
                Create First Post
              </button>
            </div>
          ) : (
                            (posts || []).map((post) => (
              <FeedItem
                key={post.id}
                post={post}
                onLike={handleLike}
                onComment={handleComment}
                onShare={handleShare}
              />
            ))
          )}

          {/* Load More */}
                        {hasMore && (posts || []).length > 0 && (
            <div className="text-center">
              <button
                onClick={handleLoadMore}
                disabled={loading}
                className="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50"
              >
                {loading ? 'Loading...' : 'Load More'}
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Create Post Modal */}
      {showCreatePost && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="w-full max-w-2xl">
            <CreatePost
              onSubmit={handleCreatePost}
              onCancel={() => setShowCreatePost(false)}
              isLoading={false}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default SocialFeed; 