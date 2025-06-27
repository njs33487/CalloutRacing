import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';
import { UserIcon, TruckIcon } from '@heroicons/react/24/outline'

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
  profile_picture: string;
  cover_photo: string;
  wins: number;
  losses: number;
  total_races: number;
  win_rate: number;
  friends_count: number;
  is_friend: boolean;
  friendship_status: string;
  cars: CarProfile[];
  posts: UserPost[];
}

interface CarProfile {
  id: number;
  name: string;
  make: string;
  model: string;
  year: number;
  trim: string;
  color: string;
  engine_size: number;
  engine_type: string;
  horsepower: number;
  torque: number;
  weight: number;
  transmission: string;
  drivetrain: string;
  best_quarter_mile: number;
  best_eighth_mile: number;
  best_trap_speed: number;
  description: string;
  is_primary: boolean;
  modifications: CarModification[];
  images: CarImage[];
}

interface CarModification {
  id: number;
  category: string;
  name: string;
  brand: string;
  description: string;
  cost: number;
  installed_date: string;
  is_installed: boolean;
}

interface CarImage {
  id: number;
  image: string;
  caption: string;
  is_primary: boolean;
}

interface UserPost {
  id: number;
  content: string;
  image: string;
  like_count: number;
  is_liked: boolean;
  created_at: string;
  comments: PostComment[];
}

interface PostComment {
  id: number;
  content: string;
  user: {
    id: number;
    username: string;
  };
  created_at: string;
}

const Profile: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<'overview' | 'cars' | 'posts' | 'friends'>('overview');

  // Fetch user profile
  const { data: profile, isLoading, error } = useQuery({
    queryKey: ['profile', userId],
    queryFn: () => api.get(`/profiles-detail/${userId}/`).then(res => res.data),
    enabled: !!userId
  });

  // Friend request mutation
  const sendFriendRequest = useMutation({
    mutationFn: (receiverId: number) => api.post('/friendships/', { receiver: receiverId }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile', userId] });
    }
  });

  // Accept friend request mutation
  const acceptFriendRequest = useMutation({
    mutationFn: (friendshipId: number) => api.post(`/friendships/${friendshipId}/accept_friend_request/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile', userId] });
    }
  });

  // Like post mutation
  const likePost = useMutation({
    mutationFn: (postId: number) => api.post(`/posts/${postId}/like_post/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile', userId] });
    }
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-red-600"></div>
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Profile Not Found</h2>
          <p className="text-gray-600">The profile you're looking for doesn't exist.</p>
        </div>
      </div>
    );
  }

  const handleFriendRequest = () => {
    sendFriendRequest.mutate(profile.user.id);
  };

  const handleAcceptFriendRequest = (friendshipId: number) => {
    acceptFriendRequest.mutate(friendshipId);
  };

  const handleLikePost = (postId: number) => {
    likePost.mutate(postId);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Cover Photo */}
      <div className="relative h-64 bg-gradient-to-r from-red-600 to-yellow-500">
        {profile.cover_photo && (
          <img 
            src={profile.cover_photo} 
            alt="Cover" 
            className="w-full h-full object-cover"
          />
        )}
        <div className="absolute inset-0 bg-black bg-opacity-30"></div>
      </div>

      {/* Profile Info */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 -mt-20 relative z-10">
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex flex-col md:flex-row items-start md:items-center space-y-4 md:space-y-0 md:space-x-6">
            {/* Profile Picture */}
            <div className="relative">
              <div className="w-32 h-32 rounded-full bg-gradient-to-r from-red-600 to-yellow-500 flex items-center justify-center text-white text-4xl font-bold">
                {profile.profile_picture ? (
                  <img 
                    src={profile.profile_picture} 
                    alt="Profile" 
                    className="w-full h-full rounded-full object-cover"
                  />
                ) : (
                  profile.user.first_name?.[0] || profile.user.username[0]
                )}
              </div>
            </div>

            {/* Profile Details */}
            <div className="flex-1">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                <div>
                  <h1 className="text-3xl font-bold text-gray-900">
                    {profile.user.first_name} {profile.user.last_name}
                  </h1>
                  <p className="text-gray-600 text-lg">@{profile.user.username}</p>
                  {profile.location && (
                    <p className="text-gray-500 flex items-center mt-1">
                      <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                      </svg>
                      {profile.location}
                    </p>
                  )}
                </div>

                {/* Friend Button */}
                <div className="mt-4 md:mt-0">
                  {profile.friendship_status === 'accepted' ? (
                    <span className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600">
                      <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      Friends
                    </span>
                  ) : profile.friendship_status === 'pending' ? (
                    <button
                      onClick={() => handleAcceptFriendRequest(profile.id)}
                      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                    >
                      Accept Request
                    </button>
                  ) : (
                    <button
                      onClick={handleFriendRequest}
                      disabled={sendFriendRequest.isPending}
                      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 disabled:opacity-50"
                    >
                      {sendFriendRequest.isPending ? 'Sending...' : 'Add Friend'}
                    </button>
                  )}
                </div>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">{profile.wins}</div>
                  <div className="text-sm text-gray-600">Wins</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-600">{profile.losses}</div>
                  <div className="text-sm text-gray-600">Losses</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-600">{profile.total_races}</div>
                  <div className="text-sm text-gray-600">Total Races</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{profile.friends_count}</div>
                  <div className="text-sm text-gray-600">Friends</div>
                </div>
              </div>

              {/* Bio */}
              {profile.bio && (
                <div className="mt-6">
                  <p className="text-gray-700">{profile.bio}</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-lg mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8 px-6">
              {[
                { id: 'overview', label: 'Overview' },
                { id: 'cars', label: 'Cars' },
                { id: 'posts', label: 'Posts' },
                { id: 'friends', label: 'Friends' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-red-600 text-red-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {/* Current Car */}
                {profile.cars?.find((car: CarProfile) => car.is_primary) && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Current Ride</h3>
                    <div className="bg-gray-50 rounded-lg p-4">
                      <div className="flex items-center space-x-4">
                        {profile.cars.find((car: CarProfile) => car.is_primary)?.images?.find((img: CarImage) => img.is_primary) && (
                          <img 
                            src={profile.cars.find((car: CarProfile) => car.is_primary)?.images?.find((img: CarImage) => img.is_primary)?.image} 
                            alt="Car" 
                            className="w-24 h-24 rounded-lg object-cover"
                          />
                        )}
                        <div>
                          <h4 className="font-semibold text-gray-900">
                            {profile.cars.find((car: CarProfile) => car.is_primary)?.year} {profile.cars.find((car: CarProfile) => car.is_primary)?.make} {profile.cars.find((car: CarProfile) => car.is_primary)?.model}
                          </h4>
                          {profile.cars.find((car: CarProfile) => car.is_primary)?.horsepower && (
                            <p className="text-gray-600">{profile.cars.find((car: CarProfile) => car.is_primary)?.horsepower} HP</p>
                          )}
                          {profile.cars.find((car: CarProfile) => car.is_primary)?.best_quarter_mile && (
                            <p className="text-gray-600">Best: {profile.cars.find((car: CarProfile) => car.is_primary)?.best_quarter_mile}s</p>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Recent Posts */}
                {profile.posts && profile.posts.length > 0 && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Posts</h3>
                    <div className="space-y-4">
                      {profile.posts.slice(0, 3).map((post: UserPost) => (
                        <div key={post.id} className="bg-gray-50 rounded-lg p-4">
                          <p className="text-gray-700">{post.content}</p>
                          <div className="flex items-center justify-between mt-2">
                            <span className="text-sm text-gray-500">
                              {new Date(post.created_at).toLocaleDateString()}
                            </span>
                            <div className="flex items-center space-x-2">
                              <span className="text-sm text-gray-500">{post.like_count} likes</span>
                              <span className="text-sm text-gray-500">{post.comments.length} comments</span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'cars' && (
              <div className="space-y-6">
                {profile.cars && profile.cars.length > 0 ? (
                  profile.cars.map((car: CarProfile) => (
                    <div key={car.id} className="border rounded-lg p-6">
                      <div className="flex items-start space-x-4">
                        {car.images?.find((img: CarImage) => img.is_primary) && (
                          <img 
                            src={car.images.find((img: CarImage) => img.is_primary)?.image} 
                            alt={car.name} 
                            className="w-32 h-32 rounded-lg object-cover"
                          />
                        )}
                        <div className="flex-1">
                          <div className="flex items-center justify-between">
                            <h3 className="text-xl font-semibold text-gray-900">{car.name}</h3>
                            {car.is_primary && (
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                Primary
                              </span>
                            )}
                          </div>
                          <p className="text-lg text-gray-600">
                            {car.year} {car.make} {car.model} {car.trim}
                          </p>
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                            {car.horsepower && (
                              <div>
                                <span className="text-sm text-gray-500">Horsepower</span>
                                <p className="font-semibold">{car.horsepower} HP</p>
                              </div>
                            )}
                            {car.torque && (
                              <div>
                                <span className="text-sm text-gray-500">Torque</span>
                                <p className="font-semibold">{car.torque} lb-ft</p>
                              </div>
                            )}
                            {car.best_quarter_mile && (
                              <div>
                                <span className="text-sm text-gray-500">Best 1/4 Mile</span>
                                <p className="font-semibold">{car.best_quarter_mile}s</p>
                              </div>
                            )}
                            {car.best_trap_speed && (
                              <div>
                                <span className="text-sm text-gray-500">Trap Speed</span>
                                <p className="font-semibold">{car.best_trap_speed} mph</p>
                              </div>
                            )}
                          </div>
                          {car.modifications && car.modifications.length > 0 && (
                            <div className="mt-4">
                              <h4 className="font-semibold text-gray-900 mb-2">Modifications</h4>
                              <div className="flex flex-wrap gap-2">
                                {car.modifications.slice(0, 5).map((mod: CarModification) => (
                                  <span key={mod.id} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                    {mod.name}
                                  </span>
                                ))}
                                {car.modifications.length > 5 && (
                                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                                    +{car.modifications.length - 5} more
                                  </span>
                                )}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8">
                    <p className="text-gray-500">No cars added yet.</p>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'posts' && (
              <div className="space-y-6">
                {profile.posts && profile.posts.length > 0 ? (
                  profile.posts.map((post: UserPost) => (
                    <div key={post.id} className="border rounded-lg p-6">
                      <div className="flex items-start space-x-3">
                        <div className="flex-shrink-0">
                          <div className="w-10 h-10 rounded-full bg-gradient-to-r from-red-600 to-yellow-500 flex items-center justify-center text-white font-semibold">
                            {profile.user.first_name?.[0] || profile.user.username[0]}
                          </div>
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="font-semibold text-gray-900">
                                {profile.user.first_name} {profile.user.last_name}
                              </p>
                              <p className="text-sm text-gray-500">
                                {new Date(post.created_at).toLocaleDateString()}
                              </p>
                            </div>
                          </div>
                          <p className="mt-2 text-gray-700">{post.content}</p>
                          {post.image && (
                            <img 
                              src={post.image} 
                              alt="Post" 
                              className="mt-3 rounded-lg max-w-md"
                            />
                          )}
                          <div className="flex items-center justify-between mt-4">
                            <button
                              onClick={() => handleLikePost(post.id)}
                              className={`flex items-center space-x-2 text-sm ${
                                post.is_liked ? 'text-red-600' : 'text-gray-500 hover:text-red-600'
                              }`}
                            >
                              <svg className="w-4 h-4" fill={post.is_liked ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                              </svg>
                              <span>{post.like_count}</span>
                            </button>
                            <span className="text-sm text-gray-500">{post.comments.length} comments</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8">
                    <p className="text-gray-500">No posts yet.</p>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'friends' && (
              <div className="text-center py-8">
                <p className="text-gray-500">Friends feature coming soon!</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile; 