import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

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
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<'overview' | 'cars' | 'posts' | 'friends'>('overview');

  // Fetch current user's profile
  const { data: profile, isLoading, error } = useQuery({
    queryKey: ['user-profile'],
    queryFn: () => api.get('/api/user-profile/').then(res => res.data),
    enabled: !!user
  });

  // Fetch user's cars
  const { data: cars } = useQuery({
    queryKey: ['user-cars'],
    queryFn: () => api.get('/api/car-profiles/my_cars/').then(res => res.data),
    enabled: !!user
  });

  // Fetch user's posts
  const { data: posts } = useQuery({
    queryKey: ['user-posts'],
    queryFn: () => api.get('/api/posts/?user=me').then(res => res.data),
    enabled: !!user
  });

  // Like post mutation
  const likePost = useMutation({
    mutationFn: (postId: number) => api.post(`/api/posts/${postId}/like_post/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user-posts'] });
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
          <p className="text-gray-600">Unable to load your profile.</p>
        </div>
      </div>
    );
  }

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

                {/* Edit Profile Button */}
                <div className="mt-4 md:mt-0">
                  <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700">
                    Edit Profile
                  </button>
                </div>
              </div>

              {/* Racing Stats */}
              <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary-600">{profile.wins}</div>
                  <div className="text-sm text-gray-600">Wins</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">{profile.losses}</div>
                  <div className="text-sm text-gray-600">Losses</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{profile.total_races}</div>
                  <div className="text-sm text-gray-600">Total Races</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{profile.win_rate?.toFixed(1)}%</div>
                  <div className="text-sm text-gray-600">Win Rate</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-lg">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8 px-6">
              {[
                { id: 'overview', name: 'Overview' },
                { id: 'cars', name: 'My Cars' },
                { id: 'posts', name: 'Posts' },
                { id: 'friends', name: 'Friends' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {tab.name}
                </button>
              ))}
            </nav>
          </div>

          <div className="p-6">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-4">About</h3>
                  <p className="text-gray-600">{profile.bio || 'No bio added yet.'}</p>
                </div>
                
                {profile.car_make && (
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Current Car</h3>
                    <p className="text-gray-600">
                      {profile.car_year} {profile.car_make} {profile.car_model}
                    </p>
                    {profile.car_mods && (
                      <p className="text-sm text-gray-500 mt-2">{profile.car_mods}</p>
                    )}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'cars' && (
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900 mb-4">My Cars</h3>
                {cars?.results?.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {cars.results.map((car: CarProfile) => (
                      <div key={car.id} className="border rounded-lg p-4">
                        <h4 className="font-medium text-gray-900">{car.name}</h4>
                        <p className="text-sm text-gray-600">
                          {car.year} {car.make} {car.model}
                        </p>
                        {car.horsepower && (
                          <p className="text-sm text-gray-600">{car.horsepower} HP</p>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">No cars added yet.</p>
                )}
              </div>
            )}

            {activeTab === 'posts' && (
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900 mb-4">My Posts</h3>
                {posts?.results?.length > 0 ? (
                  <div className="space-y-4">
                    {posts.results.map((post: UserPost) => (
                      <div key={post.id} className="border rounded-lg p-4">
                        <p className="text-gray-900">{post.content}</p>
                        <div className="flex items-center mt-2 text-sm text-gray-500">
                          <button
                            onClick={() => handleLikePost(post.id)}
                            className="flex items-center mr-4"
                          >
                            <span className="mr-1">❤️</span>
                            {post.like_count} likes
                          </button>
                          <span>{new Date(post.created_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">No posts yet.</p>
                )}
              </div>
            )}

            {activeTab === 'friends' && (
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Friends</h3>
                <p className="text-gray-500">Friends feature coming soon.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile; 