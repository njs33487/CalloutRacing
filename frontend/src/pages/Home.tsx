import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { 
  BoltIcon, 
  CalendarIcon, 
  ShoppingBagIcon, 
  TrophyIcon, 
  ClockIcon, 
  UserGroupIcon,
  CameraIcon, 
  PencilIcon, 
  MapPinIcon,
  TruckIcon
} from '@heroicons/react/24/outline'
import { useAuth } from '../contexts/AuthContext'
import { calloutAPI, eventAPI, userAPI, postAPI } from '../services/api'
import { api } from '../services/api'
import ConfirmationDialog from '../components/ConfirmationDialog'

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

interface UserPost {
  id: number;
  user: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
  };
  content: string;
  image: string;
  car: {
    id: number;
    name: string;
    make: string;
    model: string;
    year: number;
  } | null;
  likes: number[];
  like_count: number;
  comments: PostComment[];
  created_at: string;
}

interface PostComment {
  id: number;
  user: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
  };
  content: string;
  created_at: string;
}

export default function Dashboard() {
  const { user } = useAuth()
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [posts, setPosts] = useState<UserPost[]>([])
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [showProfileConfirmation, setShowProfileConfirmation] = useState(false)
  const [showPostConfirmation, setShowPostConfirmation] = useState(false)
  const [confirmationData, setConfirmationData] = useState<any>(null)

  const [editForm, setEditForm] = useState({
    bio: '',
    location: '',
    car_make: '',
    car_model: '',
    car_year: '',
    car_mods: ''
  })

  // User-specific data
  const { data: userCallouts } = useQuery({
    queryKey: ['user-callouts'],
    queryFn: () => calloutAPI.list().then(res => res.data),
    enabled: !!user
  })

  const { data: userEvents } = useQuery({
    queryKey: ['user-events'],
    queryFn: () => eventAPI.list().then(res => res.data),
    enabled: !!user
  })

  const { data: stats } = useQuery({
    queryKey: ['stats'],
    queryFn: () => api.get('/stats/').then(res => res.data)
  })

  useEffect(() => {
    if (user) {
      loadProfile()
      loadPosts()
    }
  }, [user])

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

  const loadProfile = async () => {
    try {
      if (user) {
        const response = await userAPI.profile(user.id)
        setProfile(response.data)
        setEditForm({
          bio: response.data.bio || '',
          location: response.data.location || '',
          car_make: response.data.car_make || '',
          car_model: response.data.car_model || '',
          car_year: response.data.car_year?.toString() || '',
          car_mods: response.data.car_mods || ''
        })
      }
    } catch (error) {
      console.error('Error loading profile:', error)
      setError('Failed to load profile. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const loadPosts = async () => {
    try {
      const response = await postAPI.list()
      // Ensure posts is always an array
      const postsData = response.data?.results || response.data || []
      setPosts(Array.isArray(postsData) ? postsData : [])
    } catch (error) {
      console.error('Error loading posts:', error)
      setError('Failed to load posts. Please try again.')
      // Set empty array on error to prevent map errors
      setPosts([])
    }
  }

  // Filter user's callouts (frontend filtering since backend doesn't support user filtering)
  const userCalloutsFiltered = userCallouts?.results?.filter((callout: any) => 
    callout.challenger?.id === user?.id || callout.challenged?.id === user?.id
  ) || []

  const pendingCallouts = userCalloutsFiltered.filter((c: any) => c.status === 'pending')
  const activeCallouts = userCalloutsFiltered.filter((c: any) => c.status === 'pending' || c.status === 'accepted')

  // User stats
  const userStats = [
    { 
      name: 'My Wins', 
      value: profile?.wins || 0, 
      icon: TrophyIcon, 
      color: 'text-yellow-600' 
    },
    { 
      name: 'My Races', 
      value: profile?.total_races || 0, 
      icon: BoltIcon, 
      color: 'text-red-600' 
    },
    { 
      name: 'My Events', 
      value: userEvents?.results?.length || 0, 
      icon: CalendarIcon, 
      color: 'text-blue-600' 
    },
    { 
      name: 'Active Callouts', 
      value: activeCallouts.length || 0, 
      icon: ClockIcon, 
      color: 'text-green-600' 
    },
  ]

  // Global stats
  const globalStats = [
    { name: 'Active Callouts', value: stats?.active_callouts || 0, icon: BoltIcon, color: 'text-red-600' },
    { name: 'Upcoming Events', value: stats?.upcoming_events || 0, icon: CalendarIcon, color: 'text-blue-600' },
    { name: 'Marketplace Items', value: stats?.marketplace_items || 0, icon: ShoppingBagIcon, color: 'text-green-600' },
    { name: 'Total Racers', value: stats?.total_racers || 0, icon: UserGroupIcon, color: 'text-purple-600' },
  ]

  // Profile CRUD Operations
  const handleProfilePictureUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file && profile) {
      try {
        await userAPI.uploadProfilePicture(profile.id, file)
        await loadProfile()
        setSuccess('Profile picture updated successfully!')
      } catch (error) {
        console.error('Error uploading profile picture:', error)
        setError('Failed to upload profile picture. Please try again.')
      }
    }
  }

  const handleCoverPhotoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file && profile) {
      try {
        await userAPI.uploadCoverPhoto(profile.id, file)
        await loadProfile()
        setSuccess('Cover photo updated successfully!')
      } catch (error) {
        console.error('Error uploading cover photo:', error)
        setError('Failed to upload cover photo. Please try again.')
      }
    }
  }

  const handleSubmitProfile = async (e: React.FormEvent) => {
    e.preventDefault()
    if (profile) {
      setConfirmationData({
        type: 'profile',
        data: editForm
      })
      setShowProfileConfirmation(true)
    }
  }

  const handleConfirmProfileUpdate = async () => {
    if (profile && confirmationData?.type === 'profile') {
      try {
        await userAPI.updateProfile(profile.id, confirmationData.data)
        await loadProfile()
        setIsEditing(false)
        setSuccess('Profile updated successfully!')
      } catch (error) {
        console.error('Error updating profile:', error)
        setError('Failed to update profile. Please try again.')
      }
    }
    setShowProfileConfirmation(false)
    setConfirmationData(null)
  }

  const handleCancelEdit = () => {
    if (profile) {
      setEditForm({
        bio: profile.bio || '',
        location: profile.location || '',
        car_make: profile.car_make || '',
        car_model: profile.car_model || '',
        car_year: profile.car_year?.toString() || '',
        car_mods: profile.car_mods || ''
      })
    }
    setIsEditing(false)
  }

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
        await loadPosts()
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
    <div className="space-y-8">
      {/* Error and Success Messages */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}
      {success && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
          {success}
        </div>
      )}

      {/* Personalized Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-lg p-8 text-white">
        <div className="max-w-3xl">
          <h1 className="text-4xl font-bold mb-4">
            {user ? `Welcome back, ${user.first_name || user.username}!` : 'Welcome to CalloutRacing'}
          </h1>
          <p className="text-xl mb-6 text-primary-100">
            {user ? 
              `Ready to race? You have ${pendingCallouts.length} pending callouts.` :
              'The ultimate drag racing social network. Challenge racers, join events, and buy/sell parts.'
            }
          </p>
          <div className="flex space-x-4">
            <Link
              to="/app/callouts/create"
              className="bg-white text-primary-600 px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors"
            >
              Create Callout
            </Link>
            <Link
              to="/app/events"
              className="border border-white text-white px-6 py-3 rounded-lg font-medium hover:bg-white hover:text-primary-600 transition-colors"
            >
              Browse Events
            </Link>
          </div>
        </div>
      </div>

      {/* Profile Section */}
      {user && profile && (
        <div className="card">
          <div className="flex items-start justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">My Profile</h2>
            <button
              onClick={() => setIsEditing(!isEditing)}
              className="flex items-center space-x-2 text-primary-600 hover:text-primary-700"
            >
              <PencilIcon className="h-5 w-5" />
              <span>{isEditing ? 'Cancel' : 'Edit Profile'}</span>
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Profile Picture and Cover Photo */}
            <div className="lg:col-span-1">
              <div className="space-y-4">
                {/* Profile Picture */}
                <div className="relative">
                  <div className="w-32 h-32 mx-auto rounded-full overflow-hidden bg-gray-200">
                    {profile.profile_picture ? (
                      <img
                        src={profile.profile_picture}
                        alt="Profile"
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-400">
                        <CameraIcon className="h-12 w-12" />
                      </div>
                    )}
                  </div>
                  <label className="absolute bottom-0 right-0 bg-primary-600 text-white p-2 rounded-full cursor-pointer hover:bg-primary-700">
                    <CameraIcon className="h-4 w-4" />
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleProfilePictureUpload}
                      className="hidden"
                    />
                  </label>
                </div>

                {/* Cover Photo */}
                <div className="relative">
                  <div className="w-full h-32 rounded-lg overflow-hidden bg-gray-200">
                    {profile.cover_photo ? (
                      <img
                        src={profile.cover_photo}
                        alt="Cover"
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-400">
                        <CameraIcon className="h-8 w-8" />
                      </div>
                    )}
                  </div>
                  <label className="absolute bottom-2 right-2 bg-primary-600 text-white p-2 rounded-full cursor-pointer hover:bg-primary-700">
                    <CameraIcon className="h-4 w-4" />
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleCoverPhotoUpload}
                      className="hidden"
                    />
                  </label>
                </div>
              </div>
            </div>

            {/* Profile Information */}
            <div className="lg:col-span-2">
              {isEditing ? (
                <form onSubmit={handleSubmitProfile} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Bio</label>
                    <textarea
                      value={editForm.bio}
                      onChange={(e) => setEditForm({...editForm, bio: e.target.value})}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      rows={3}
                    />
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                      <input
                        type="text"
                        value={editForm.location}
                        onChange={(e) => setEditForm({...editForm, location: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Car Make</label>
                      <input
                        type="text"
                        value={editForm.car_make}
                        onChange={(e) => setEditForm({...editForm, car_make: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Car Model</label>
                      <input
                        type="text"
                        value={editForm.car_model}
                        onChange={(e) => setEditForm({...editForm, car_model: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Car Year</label>
                      <input
                        type="number"
                        value={editForm.car_year}
                        onChange={(e) => setEditForm({...editForm, car_year: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      />
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Car Modifications</label>
                    <textarea
                      value={editForm.car_mods}
                      onChange={(e) => setEditForm({...editForm, car_mods: e.target.value})}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      rows={2}
                    />
                  </div>
                  
                  <div className="flex space-x-4">
                    <button
                      type="submit"
                      className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors"
                    >
                      Save Changes
                    </button>
                    <button
                      type="button"
                      onClick={handleCancelEdit}
                      className="bg-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-400 transition-colors"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              ) : (
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Bio</h3>
                    <p className="text-gray-600">{profile.bio || 'No bio added yet.'}</p>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">Location</h3>
                      <p className="text-gray-600 flex items-center">
                        <MapPinIcon className="h-4 w-4 mr-2" />
                        {profile.location || 'Not specified'}
                      </p>
                    </div>
                    
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">Car</h3>
                      <p className="text-gray-600 flex items-center">
                        <TruckIcon className="h-4 w-4 mr-2" />
                        {profile.car_year} {profile.car_make} {profile.car_model}
                      </p>
                    </div>
                  </div>
                  
                  {profile.car_mods && (
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">Modifications</h3>
                      <p className="text-gray-600">{profile.car_mods}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* User Stats */}
      {user && (
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Racing Stats</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {userStats.map((stat) => (
              <div key={stat.name} className="card">
                <div className="flex items-center">
                  <div className={`p-2 rounded-lg bg-gray-100 ${stat.color}`}>
                    <stat.icon className="h-6 w-6" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                    <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Global Stats */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Community Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {globalStats.map((stat) => (
            <div key={stat.name} className="card">
              <div className="flex items-center">
                <div className={`p-2 rounded-lg bg-gray-100 ${stat.color}`}>
                  <stat.icon className="h-6 w-6" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* User-specific sections */}
      {user && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* My Active Callouts */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">My Active Callouts</h2>
              <Link to="/app/callouts" className="text-primary-600 hover:text-primary-700 text-sm">
                View all
              </Link>
            </div>
            <div className="space-y-3">
              {activeCallouts.slice(0, 3).map((callout: any) => (
                <div key={callout.id} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                  <BoltIcon className="h-5 w-5 text-primary-600" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">
                      {callout.challenger.username} vs {callout.challenged.username}
                    </p>
                    <p className="text-xs text-gray-500">
                      {callout.race_type} • {callout.location_type}
                    </p>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    callout.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                    callout.status === 'accepted' ? 'bg-green-100 text-green-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {callout.status}
                  </span>
                </div>
              ))}
              {activeCallouts.length === 0 && (
                <p className="text-gray-500 text-center py-4">No active callouts</p>
              )}
            </div>
          </div>

          {/* Recent Posts */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Recent Posts</h2>
              <Link to="/app/posts" className="text-primary-600 hover:text-primary-700 text-sm">
                View all
              </Link>
            </div>
            <div className="space-y-4">
              {posts.slice(0, 3).map((post) => (
                <div key={post.id} className="border-b border-gray-200 pb-4 last:border-b-0">
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center text-white text-sm font-medium">
                      {post.user.first_name?.[0] || post.user.username[0]}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <span className="font-medium text-gray-900">
                          {post.user.first_name} {post.user.last_name}
                        </span>
                        <span className="text-gray-500 text-sm">
                          {new Date(post.created_at).toLocaleDateString()}
                        </span>
                      </div>
                      <p className="text-gray-700 text-sm">{post.content}</p>
                      {post.image && (
                        <img
                          src={post.image}
                          alt="Post"
                          className="mt-2 rounded-lg max-w-full h-32 object-cover"
                        />
                      )}
                    </div>
                  </div>
                </div>
              ))}
              {posts.length === 0 && (
                <p className="text-gray-500 text-center py-4">No posts yet</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Confirmation Dialogs */}
      <ConfirmationDialog
        isOpen={showProfileConfirmation}
        onClose={() => setShowProfileConfirmation(false)}
        onConfirm={handleConfirmProfileUpdate}
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
  )
} 