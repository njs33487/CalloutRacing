import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { 
  BoltIcon, 
  CalendarIcon, 
  ShoppingBagIcon, 
  UserGroupIcon,
  CameraIcon, 
  HeartIcon,
  ChatBubbleLeftIcon,
  ShareIcon,
  PlusIcon,
  FireIcon,
  ArrowTrendingUpIcon,
  BellIcon,
  ArrowPathIcon,
  MapPinIcon,
  ClockIcon,
  UsersIcon,
  TrophyIcon
} from '@heroicons/react/24/outline'
import { HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid'
import { useAppSelector } from '../store/hooks'
import { calloutAPI, userAPI, postAPI } from '../services/api'
import { api } from '../services/api'
import ConfirmationDialog from '../components/ConfirmationDialog'
import CreatePost from '../components/social/CreatePost'
import axios from 'axios'
import { API_URL } from '../services/api'

interface UserProfile {
  id: number;
  user: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
  };
  bio: string;
  location: string;
  car_make: string;
  car_model: string;
  car_year: number;
  car_mods: string;
  profile_picture: string;
  cover_photo: string;
  wins: number;
  losses: number;
  total_races: number;
  win_rate: number;
  created_at: string;
  updated_at: string;
}

interface SponsoredContent {
  id: number;
  title: string;
  content: string;
  image_url?: string;
  link_url: string;
  sponsor_name: string;
  display_location: string;
}

interface SocialPost {
  id: number;
  author: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    profile_picture?: string;
  };
  content: string;
  post_type: 'text' | 'image' | 'video' | 'race_result' | 'car_update' | 'live';
  image?: string;
  video?: string;
  is_live?: boolean;
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

interface Event {
  id: number;
  title: string;
  description: string;
  event_type: string;
  start_date: string;
  end_date: string;
  max_participants: number;
  entry_fee: number;
  is_public: boolean;
  track: {
    id: number;
    name: string;
    location: string;
  };
  organizer: {
    id: number;
    username: string;
  };
  participants_count: number;
  is_active: boolean;
  created_at: string;
}

interface Callout {
  id: number;
  challenger: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
  };
  challenged: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
  };
  message: string;
  race_type: string;
  wager_amount: number;
  scheduled_date: string;
  street_location: string;
  status: string;
  created_at: string;
  time_ago: string;
}

export default function Dashboard() {
  const { user } = useAppSelector((state) => state.auth)
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [socialPosts, setSocialPosts] = useState<SocialPost[]>([])
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [showProfileConfirmation, setShowProfileConfirmation] = useState(false)
  const [showPostConfirmation, setShowPostConfirmation] = useState(false)
  const [confirmationData, setConfirmationData] = useState<any>(null)
  const [sponsoredContent, setSponsoredContent] = useState<SponsoredContent[]>([])
  
  // Social feed states
  const [showCreatePost, setShowCreatePost] = useState(false)
  const [showNotifications, setShowNotifications] = useState(false)
  const [activeTab, setActiveTab] = useState<'feed' | 'trending' | 'live'>('feed')
  const [postTypeFilter, setPostTypeFilter] = useState<string>('')
  const [timeFilter, setTimeFilter] = useState<string>('')
  const [hasMore, setHasMore] = useState(true)
  const [page, setPage] = useState(1)
  const [refreshing, setRefreshing] = useState(false)
  const [showComments, setShowComments] = useState<number | null>(null)
  const [commentText, setCommentText] = useState('')
  const [isSubmittingComment, setIsSubmittingComment] = useState(false)

  // Events and Callouts states
  const [upcomingEvents, setUpcomingEvents] = useState<Event[]>([])
  const [recentCallouts, setRecentCallouts] = useState<Callout[]>([])
  const [showEventsSection, setShowEventsSection] = useState(true)
  const [showCalloutsSection, setShowCalloutsSection] = useState(true)

  // User-specific data
  const { data: userCallouts } = useQuery({
    queryKey: ['user-callouts'],
    queryFn: () => calloutAPI.list().then(res => res.data),
    enabled: !!user
  })

  const { data: stats } = useQuery({
    queryKey: ['stats'],
    queryFn: () => api.get('/stats/').then(res => res.data)
  })

  // Fetch upcoming events
  const { data: eventsData } = useQuery({
    queryKey: ['upcoming-events'],
    queryFn: () => api.get('/api/events/upcoming/').then(res => res.data),
    enabled: !!user
  })

  // Fetch recent callouts
  const { data: calloutsData } = useQuery({
    queryKey: ['recent-callouts'],
    queryFn: () => api.get('/api/callouts/?status=pending&limit=5').then(res => res.data),
    enabled: !!user
  })

  useEffect(() => {
    if (user) {
      loadProfile()
      loadSocialFeed()
      loadNotifications()
    }
  }, [user])

  // Update events and callouts data
  useEffect(() => {
    if (eventsData) {
      setUpcomingEvents(eventsData)
    }
  }, [eventsData])

  useEffect(() => {
    if (calloutsData) {
      setRecentCallouts(calloutsData.results || calloutsData)
    }
  }, [calloutsData])

  // Clear messages after 5 seconds
  useEffect(() => {
    if (error || success) {
      const timer = setTimeout(() => {
        setError(null)
        setSuccess(null)
      }, 5000)
      return () => clearTimeout(timer)
    }
  }, [error, success])

  useEffect(() => {
    const fetchSponsoredContent = async () => {
      try {
        const response = await axios.get<SponsoredContent[]>(`${API_URL}/sponsored-content/?display_location=homepage`);
        setSponsoredContent(response.data);
      } catch (error) {
        console.error('Error fetching sponsored content:', error);
      }
    };
    fetchSponsoredContent();
  }, []);

  const loadProfile = async () => {
    try {
      if (user) {
        const response = await userAPI.profile(user.id)
        setProfile(response.data)
      }
    } catch (error) {
      console.error('Error loading profile:', error)
      setError('Failed to load profile. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const loadSocialFeed = async (pageNum = 1, refresh = false) => {
    try {
      const params = new URLSearchParams({
        page: pageNum.toString(),
        ...(postTypeFilter && { post_type: postTypeFilter }),
        ...(timeFilter && { time_filter: timeFilter }),
      });

      const endpoint = activeTab === 'trending' ? '/api/social/trending/' : '/api/social/feed/';
      const response = await api.get(`${endpoint}?${params}`);
      
      const newPosts = response.data.results || response.data;
      
      if (refresh) {
        setSocialPosts(newPosts);
      } else {
        setSocialPosts(prev => pageNum === 1 ? newPosts : [...prev, ...newPosts]);
      }
      
      setHasMore(newPosts.length === 20); // Assuming page size is 20
      setPage(pageNum);
    } catch (error) {
      console.error('Error fetching social posts:', error);
    }
  }

  const loadNotifications = async () => {
    try {
      const response = await api.get('/api/social/notifications/');
      setNotifications(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching notifications:', error);
    }
  }

  const handleRefresh = async () => {
    setRefreshing(true);
    await Promise.all([loadSocialFeed(1, true), loadNotifications()]);
    setRefreshing(false);
  }

  const handleLoadMore = () => {
    if (hasMore && !isLoading) {
      loadSocialFeed(page + 1);
    }
  }

  const handleCreatePost = async (postData: {
    content: string;
    post_type: 'text' | 'image' | 'video' | 'race_result' | 'car_update' | 'live';
    image?: File;
    video?: File;
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

      await api.post('/api/social/posts/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setShowCreatePost(false);
      handleRefresh();
    } catch (error) {
      console.error('Error creating post:', error);
    }
  }

  const handleLike = async (postId: number) => {
    try {
      const post = socialPosts.find(p => p.id === postId);
      if (!post) return;

      const action = post.is_liked ? 'unlike' : 'like';
      await api.post(`/api/social/posts/${postId}/${action}/`);

      setSocialPosts(prev => prev.map(p => 
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
  }

  const handleComment = async (postId: number, content: string) => {
    try {
      const response = await api.post(`/api/social/posts/${postId}/comment/`, {
        content
      });

      setSocialPosts(prev => prev.map(p => 
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
  }

  const handleShare = async (postId: number) => {
    try {
      const post = socialPosts.find(p => p.id === postId);
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
  }

  const handleMarkNotificationRead = async (notificationId: number) => {
    try {
      await api.post(`/api/social/notifications/${notificationId}/read/`);
      setNotifications(prev => prev.map(n => 
        n.id === notificationId ? { ...n, is_read: true } : n
      ));
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  }

  const handleCommentSubmit = async (postId: number) => {
    if (!commentText.trim()) return;

    setIsSubmittingComment(true);
    try {
      await handleComment(postId, commentText);
      setCommentText('');
      setShowComments(null);
    } catch (error) {
      console.error('Error posting comment:', error);
    } finally {
      setIsSubmittingComment(false);
    }
  }

  // Filter user's callouts (frontend filtering since backend doesn't support user filtering)
  const activeCallouts = userCallouts?.filter((callout: any) => 
    callout.status !== 'completed' && callout.status !== 'cancelled'
  ) || []

  // Global stats data
  const globalStats = [
    {
      name: 'Total Users',
      value: stats?.total_users || 0,
      icon: UserGroupIcon,
      color: 'text-blue-600'
    },
    {
      name: 'Active Events',
      value: stats?.active_events || 0,
      icon: CalendarIcon,
      color: 'text-green-600'
    },
    {
      name: 'Total Callouts',
      value: stats?.total_callouts || 0,
      icon: BoltIcon,
      color: 'text-red-600'
    },
    {
      name: 'Marketplace Items',
      value: stats?.marketplace_items || 0,
      icon: ShoppingBagIcon,
      color: 'text-purple-600'
    }
  ]

  const unreadNotificationsCount = notifications.filter(n => !n.is_read).length;

  // Post CRUD Operations
  const handleConfirmPostCreate = async () => {
    if (confirmationData?.type === 'post') {
      try {
        const formData = new FormData()
        formData.append('content', confirmationData.data.content)
        if (confirmationData.data.image) {
          formData.append('image', confirmationData.data.image)
        }

        await postAPI.create(formData)
        setSuccess('Post created successfully!')
      } catch (error) {
        console.error('Error creating post:', error)
        setError('Failed to create post. Please try again.')
      }
    }
    setShowPostConfirmation(false)
    setConfirmationData(null)
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Welcome to CalloutRacing
          </h1>
          <p className="text-xl mb-6 text-primary-100">
            {user ? 
              `Ready to race? You have ${activeCallouts.length} active callouts.` :
              'The ultimate drag racing social network. Challenge racers, join events, and buy/sell parts.'
            }
          </p>
        </div>

        {/* Error and Success Messages */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
            {success}
          </div>
        )}

        {/* Main Layout - Social Feed + Sidebar */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Main Social Feed */}
          <div className="lg:col-span-3">
            {/* Featured Banner - Events & Callouts */}
            {(upcomingEvents.length > 0 || recentCallouts.length > 0) && (
              <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-orange-600 rounded-lg shadow-lg mb-6 overflow-hidden">
                <div className="p-6 text-white">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-2xl font-bold">Featured Racing Activity</h2>
                    <div className="flex items-center space-x-4 text-sm">
                      {upcomingEvents.length > 0 && (
                        <span className="flex items-center space-x-1">
                          <CalendarIcon className="w-4 h-4" />
                          <span>{upcomingEvents.length} Events</span>
                        </span>
                      )}
                      {recentCallouts.length > 0 && (
                        <span className="flex items-center space-x-1">
                          <TrophyIcon className="w-4 h-4" />
                          <span>{recentCallouts.length} Callouts</span>
                        </span>
                      )}
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Featured Event */}
                    {upcomingEvents.length > 0 && (
                      <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
                        <div className="flex items-center space-x-2 mb-2">
                          <CalendarIcon className="w-5 h-5" />
                          <span className="font-semibold">Featured Event</span>
                        </div>
                        <h3 className="font-bold text-lg mb-1">{upcomingEvents[0].title}</h3>
                        <p className="text-sm text-white/90 mb-2 line-clamp-2">{upcomingEvents[0].description}</p>
                        <div className="flex items-center justify-between text-xs">
                          <span>{upcomingEvents[0].track?.name || 'TBD'}</span>
                          <span>{new Date(upcomingEvents[0].start_date).toLocaleDateString()}</span>
                        </div>
                      </div>
                    )}
                    
                    {/* Featured Callout */}
                    {recentCallouts.length > 0 && (
                      <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
                        <div className="flex items-center space-x-2 mb-2">
                          <TrophyIcon className="w-5 h-5" />
                          <span className="font-semibold">Featured Callout</span>
                        </div>
                        <div className="flex items-center space-x-1 mb-1">
                          <span className="font-bold">{recentCallouts[0].challenger.username}</span>
                          <span>vs</span>
                          <span className="font-bold">{recentCallouts[0].challenged.username}</span>
                        </div>
                        <p className="text-sm text-white/90 mb-2 line-clamp-2">{recentCallouts[0].message}</p>
                        <div className="flex items-center justify-between text-xs">
                          <span>{recentCallouts[0].race_type}</span>
                          <span>{recentCallouts[0].time_ago}</span>
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="flex items-center justify-center mt-4 space-x-4">
                    <button className="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg text-white font-medium transition-colors">
                      View All Events
                    </button>
                    <button className="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg text-white font-medium transition-colors">
                      View All Callouts
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Feed Header */}
            <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 mb-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-4">
                  <h2 className="text-2xl font-bold text-gray-900">Racing Community Feed</h2>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => setActiveTab('feed')}
                      className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                        activeTab === 'feed'
                          ? 'bg-blue-500 text-white'
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      }`}
                    >
                      <UserGroupIcon className="w-4 h-4 inline mr-1" />
                      My Feed
                    </button>
                    <button
                      onClick={() => setActiveTab('trending')}
                      className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                        activeTab === 'trending'
                          ? 'bg-blue-500 text-white'
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      }`}
                    >
                      <ArrowTrendingUpIcon className="w-4 h-4 inline mr-1" />
                      Trending
                    </button>
                    <button
                      onClick={() => setActiveTab('live')}
                      className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                        activeTab === 'live'
                          ? 'bg-red-500 text-white'
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      }`}
                    >
                      <FireIcon className="w-4 h-4 inline mr-1" />
                      Live
                    </button>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <button
                    onClick={handleRefresh}
                    disabled={refreshing}
                    className="p-2 text-gray-600 hover:text-gray-900 transition-colors disabled:opacity-50"
                  >
                    <ArrowPathIcon className={`w-5 h-5 ${refreshing ? 'animate-spin' : ''}`} />
                  </button>
                  <button
                    onClick={() => setShowNotifications(!showNotifications)}
                    className="relative p-2 text-gray-600 hover:text-gray-900 transition-colors"
                  >
                    <BellIcon className="w-6 h-6" />
                    {unreadNotificationsCount > 0 && (
                      <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                        {unreadNotificationsCount}
                      </span>
                    )}
                  </button>
                  <button
                    onClick={() => setShowCreatePost(true)}
                    className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                  >
                    <PlusIcon className="w-5 h-5" />
                    <span>Create Post</span>
                  </button>
                </div>
              </div>

              {/* Filters */}
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <span className="text-sm font-medium text-gray-700">Filters:</span>
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
              </div>
            </div>

            {/* Notifications Panel */}
            {showNotifications && (
              <div className="bg-white rounded-lg shadow-md border border-gray-200 p-4 mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Notifications</h3>
                {notifications.length === 0 ? (
                  <p className="text-gray-500 text-center py-4">No notifications</p>
                ) : (
                  <div className="space-y-3">
                    {notifications.map((notification) => (
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

            {/* Social Posts Feed */}
            <div className="space-y-6">
              {/* Events Feed Posts */}
              {upcomingEvents.length > 0 && (
                <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
                  <div className="p-4 border-b border-gray-100 bg-gradient-to-r from-blue-500 to-purple-600">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <CalendarIcon className="w-6 h-6 text-white" />
                        <h3 className="text-lg font-semibold text-white">Upcoming Events</h3>
                      </div>
                      <span className="text-white text-sm font-medium">{upcomingEvents.length} events</span>
                    </div>
                  </div>
                  <div className="p-4">
                    <div className="space-y-4">
                      {upcomingEvents.slice(0, 2).map((event) => (
                        <div key={event.id} className="border border-gray-100 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <h4 className="font-semibold text-gray-900 mb-2">{event.title}</h4>
                              <p className="text-sm text-gray-600 mb-3 line-clamp-2">{event.description}</p>
                              <div className="grid grid-cols-2 gap-4 text-xs text-gray-500">
                                <div className="flex items-center space-x-1">
                                  <MapPinIcon className="w-3 h-3" />
                                  <span>{event.track?.name || 'TBD'}</span>
                                </div>
                                <div className="flex items-center space-x-1">
                                  <ClockIcon className="w-3 h-3" />
                                  <span>{new Date(event.start_date).toLocaleDateString()}</span>
                                </div>
                                <div className="flex items-center space-x-1">
                                  <UsersIcon className="w-3 h-3" />
                                  <span>{event.participants_count}/{event.max_participants || '∞'} participants</span>
                                </div>
                                <div className="flex items-center space-x-1">
                                  <span className="font-medium">{event.event_type}</span>
                                </div>
                              </div>
                            </div>
                            <div className="text-right">
                              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                {event.event_type}
                              </span>
                            </div>
                          </div>
                          {event.entry_fee > 0 && (
                            <div className="mt-3 text-xs text-gray-600">
                              Entry Fee: ${event.entry_fee}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                    {upcomingEvents.length > 2 && (
                      <div className="text-center mt-4">
                        <button className="text-sm text-blue-600 hover:text-blue-800 font-medium">
                          View All Events ({upcomingEvents.length})
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Callouts Feed Posts */}
              {recentCallouts.length > 0 && (
                <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
                  <div className="p-4 border-b border-gray-100 bg-gradient-to-r from-orange-500 to-red-600">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <TrophyIcon className="w-6 h-6 text-white" />
                        <h3 className="text-lg font-semibold text-white">Recent Callouts</h3>
                      </div>
                      <span className="text-white text-sm font-medium">{recentCallouts.length} callouts</span>
                    </div>
                  </div>
                  <div className="p-4">
                    <div className="space-y-4">
                      {recentCallouts.slice(0, 2).map((callout) => (
                        <div key={callout.id} className="border border-gray-100 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center space-x-2 mb-2">
                                <span className="font-semibold text-gray-900">{callout.challenger.username}</span>
                                <span className="text-gray-500">vs</span>
                                <span className="font-semibold text-gray-900">{callout.challenged.username}</span>
                              </div>
                              <p className="text-sm text-gray-700 mb-3">{callout.message}</p>
                              <div className="grid grid-cols-2 gap-4 text-xs text-gray-500">
                                <div className="flex items-center space-x-1">
                                  <MapPinIcon className="w-3 h-3" />
                                  <span>{callout.street_location}</span>
                                </div>
                                <div className="flex items-center space-x-1">
                                  <ClockIcon className="w-3 h-3" />
                                  <span>{callout.time_ago}</span>
                                </div>
                                <div className="flex items-center space-x-1">
                                  <span className="font-medium">{callout.race_type}</span>
                                </div>
                                <div className="flex items-center space-x-1">
                                  <span className="font-medium">{callout.status}</span>
                                </div>
                              </div>
                            </div>
                            <div className="text-right">
                              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                                {callout.race_type}
                              </span>
                            </div>
                          </div>
                          {callout.wager_amount > 0 && (
                            <div className="mt-3 text-xs text-gray-600">
                              Wager: ${callout.wager_amount}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                    {recentCallouts.length > 2 && (
                      <div className="text-center mt-4">
                        <button className="text-sm text-blue-600 hover:text-blue-800 font-medium">
                          View All Callouts ({recentCallouts.length})
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {socialPosts.length === 0 ? (
                <div className="text-center py-12 bg-white rounded-lg shadow-md border border-gray-200">
                  <UserGroupIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No posts yet</h3>
                  <p className="text-gray-600 mb-4">
                    {activeTab === 'feed' 
                      ? 'Follow some users to see their posts in your feed'
                      : activeTab === 'trending'
                      ? 'No trending posts at the moment'
                      : 'No live streams at the moment'
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
                socialPosts.map((post) => (
                  <div key={post.id} className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
                    {/* Post Header */}
                    <div className="p-4 border-b border-gray-100">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                            <span className="text-white font-medium">
                              {post.author.first_name?.[0] || post.author.username[0]}
                            </span>
                          </div>
                          <div>
                            <div className="flex items-center space-x-2">
                              <h3 className="font-semibold text-gray-900">
                                {post.author.first_name} {post.author.last_name}
                              </h3>
                              {post.is_live && (
                                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                  <FireIcon className="w-3 h-3 mr-1" />
                                  LIVE
                                </span>
                              )}
                              <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                                {post.post_type === 'race_result' ? 'Race Result' :
                                 post.post_type === 'car_update' ? 'Car Update' :
                                 post.post_type === 'image' ? 'Photo' :
                                 post.post_type === 'video' ? 'Video' :
                                 post.post_type === 'live' ? 'Live Stream' : 'Post'}
                              </span>
                            </div>
                            <p className="text-sm text-gray-500">{post.time_ago}</p>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Post Content */}
                    <div className="p-4">
                      <p className="text-gray-900 mb-4 whitespace-pre-wrap">{post.content}</p>
                      
                      {/* Media Content */}
                      {post.image && (
                        <div className="mb-4">
                          <img 
                            src={post.image} 
                            alt="Post content" 
                            className="w-full rounded-lg max-h-96 object-cover"
                          />
                        </div>
                      )}
                      
                      {post.video && (
                        <div className="mb-4">
                          <video 
                            src={post.video} 
                            controls 
                            className="w-full rounded-lg max-h-96"
                          />
                        </div>
                      )}
                    </div>

                    {/* Post Actions */}
                    <div className="px-4 py-3 border-t border-gray-100">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-6">
                          <button
                            onClick={() => handleLike(post.id)}
                            className={`flex items-center space-x-2 transition-colors ${
                              post.is_liked 
                                ? 'text-red-500 hover:text-red-600' 
                                : 'text-gray-500 hover:text-red-500'
                            }`}
                          >
                            {post.is_liked ? (
                              <HeartSolidIcon className="w-5 h-5" />
                            ) : (
                              <HeartIcon className="w-5 h-5" />
                            )}
                            <span className="text-sm font-medium">{post.likes_count}</span>
                          </button>
                          
                          <button
                            onClick={() => setShowComments(showComments === post.id ? null : post.id)}
                            className="flex items-center space-x-2 text-gray-500 hover:text-blue-500 transition-colors"
                          >
                            <ChatBubbleLeftIcon className="w-5 h-5" />
                            <span className="text-sm font-medium">{post.comments_count}</span>
                          </button>
                          
                          <button
                            onClick={() => handleShare(post.id)}
                            className="flex items-center space-x-2 text-gray-500 hover:text-green-500 transition-colors"
                          >
                            <ShareIcon className="w-5 h-5" />
                            <span className="text-sm font-medium">Share</span>
                          </button>
                        </div>
                      </div>
                    </div>

                    {/* Comments Section */}
                    {showComments === post.id && (
                      <div className="px-4 py-3 border-t border-gray-100 bg-gray-50">
                        <div className="space-y-3 mb-3">
                          {post.comments.map((comment) => (
                            <div key={comment.id} className="flex items-start space-x-2">
                              <div className="w-6 h-6 bg-gray-300 rounded-full flex items-center justify-center">
                                <span className="text-xs font-medium text-gray-600">
                                  {comment.author.username[0]}
                                </span>
                              </div>
                              <div className="flex-1">
                                <div className="flex items-center space-x-2">
                                  <span className="text-sm font-medium text-gray-900">
                                    {comment.author.username}
                                  </span>
                                  <span className="text-xs text-gray-500">{comment.time_ago}</span>
                                </div>
                                <p className="text-sm text-gray-700">{comment.content}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                        <form onSubmit={(e) => { e.preventDefault(); handleCommentSubmit(post.id); }} className="flex space-x-2">
                          <input
                            type="text"
                            value={commentText}
                            onChange={(e) => setCommentText(e.target.value)}
                            placeholder="Write a comment..."
                            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            disabled={isSubmittingComment}
                          />
                          <button
                            type="submit"
                            disabled={!commentText.trim() || isSubmittingComment}
                            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50"
                          >
                            {isSubmittingComment ? 'Posting...' : 'Post'}
                          </button>
                        </form>
                      </div>
                    )}
                  </div>
                ))
              )}

              {/* Load More */}
              {hasMore && socialPosts.length > 0 && (
                <div className="text-center">
                  <button
                    onClick={handleLoadMore}
                    disabled={isLoading}
                    className="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50"
                  >
                    {isLoading ? 'Loading...' : 'Load More'}
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            {/* User Profile Summary */}
            {user && profile && (
              <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
                <div className="text-center mb-4">
                  <div className="w-20 h-20 mx-auto rounded-full overflow-hidden bg-gray-200 mb-3">
                    {profile.profile_picture ? (
                      <img
                        src={profile.profile_picture}
                        alt="Profile"
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-400">
                        <CameraIcon className="h-8 w-8" />
                      </div>
                    )}
                  </div>
                  <h3 className="font-semibold text-gray-900">
                    {profile.user.first_name} {profile.user.last_name}
                  </h3>
                  <p className="text-sm text-gray-600">@{profile.user.username}</p>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Races</span>
                    <span className="font-medium">{profile.total_races}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Wins</span>
                    <span className="font-medium">{profile.wins}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Win Rate</span>
                    <span className="font-medium">{profile.win_rate || 0}%</span>
                  </div>
                </div>
              </div>
            )}

            {/* Quick Stats */}
            <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
              <h3 className="font-semibold text-gray-900 mb-4">Community Stats</h3>
              <div className="space-y-3">
                {globalStats.map((stat) => (
                  <div key={stat.name} className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <stat.icon className="w-4 h-4 text-gray-500" />
                      <span className="text-sm text-gray-600">{stat.name}</span>
                    </div>
                    <span className="text-sm font-medium">{stat.value}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Sponsored Content */}
            {sponsoredContent.length > 0 && (
              <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
                <h3 className="font-semibold text-gray-900 mb-4">Featured</h3>
                {sponsoredContent.map((item) => (
                  <div key={item.id} className="mb-4 last:mb-0">
                    {item.image_url && (
                      <img 
                        src={item.image_url} 
                        alt={item.title} 
                        className="w-full h-32 object-cover rounded-lg mb-2"
                      />
                    )}
                    <h4 className="font-medium text-gray-900 text-sm mb-1">{item.title}</h4>
                    <p className="text-xs text-gray-600 mb-2">{item.content}</p>
                    <a 
                      href={item.link_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-xs text-blue-600 hover:text-blue-800"
                    >
                      Learn More →
                    </a>
                  </div>
                ))}
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

        {/* Confirmation Dialogs */}
        <ConfirmationDialog
          isOpen={showProfileConfirmation}
          onClose={() => setShowProfileConfirmation(false)}
          onConfirm={() => {}}
          title="Update Profile"
          message="Are you sure you want to update your profile?"
        />

        <ConfirmationDialog
          isOpen={showPostConfirmation}
          onClose={() => setShowPostConfirmation(false)}
          onConfirm={handleConfirmPostCreate}
          title="Create Post"
          message="Are you sure you want to create this post?"
        />
      </div>
    </div>
  )
} 