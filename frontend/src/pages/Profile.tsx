import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { CarProfile, UserPost } from '../types';
import { PhotoIcon, XMarkIcon } from '@heroicons/react/24/outline';

interface ImageFile {
  file: File;
  preview: string;
  id: string;
}

const Profile = () => {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<'overview' | 'cars' | 'posts' | 'friends'>('overview');
  const [isEditing, setIsEditing] = useState(false);
  const [profileImage, setProfileImage] = useState<ImageFile | null>(null);
  const [coverImage, setCoverImage] = useState<ImageFile | null>(null);
  const [editForm, setEditForm] = useState({
    bio: '',
    location: '',
    car_make: '',
    car_model: '',
    car_year: '',
    car_mods: ''
  });

  // Fetch current user's profile
  const { data: profile, isLoading, error } = useQuery({
    queryKey: ['user-profile'],
    queryFn: () => api.get('/auth/profile/').then(res => res.data),
    enabled: !!user
  });

  // Fetch user's cars
  const { data: cars } = useQuery({
    queryKey: ['user-cars'],
    queryFn: () => api.get('/cars/my_cars/').then(res => res.data),
    enabled: !!user
  });

  // Fetch user's posts
  const { data: posts } = useQuery({
    queryKey: ['user-posts'],
    queryFn: () => api.get('/posts/?user=me').then(res => res.data),
    enabled: !!user
  });

  // Update profile mutation
  const updateProfile = useMutation({
    mutationFn: async (data: any) => {
      const formData = new FormData();
      
      // Add form fields
      Object.keys(data).forEach(key => {
        if (key !== 'profile_image' && key !== 'cover_image') {
          formData.append(key, data[key]);
        }
      });
      
      // Add images
      if (profileImage) {
        formData.append('profile_picture', profileImage.file);
      }
      if (coverImage) {
        formData.append('cover_photo', coverImage.file);
      }
      
      return api.patch('/profiles/me/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user-profile'] });
      setIsEditing(false);
      setProfileImage(null);
      setCoverImage(null);
    }
  });

  // Like post mutation
  const likePost = useMutation({
    mutationFn: (postId: number) => api.post(`/posts/${postId}/like_post/`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user-posts'] });
    }
  });

  const handleEditClick = () => {
    if (profile) {
      setEditForm({
        bio: profile.bio || '',
        location: profile.location || '',
        car_make: profile.car_make || '',
        car_model: profile.car_model || '',
        car_year: profile.car_year || '',
        car_mods: profile.car_mods || ''
      });
    }
    setIsEditing(true);
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>, type: 'profile' | 'cover') => {
    const file = e.target.files?.[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const imageFile: ImageFile = {
          file,
          preview: e.target?.result as string,
          id: Math.random().toString(36).substr(2, 9)
        };
        if (type === 'profile') {
          setProfileImage(imageFile);
        } else {
          setCoverImage(imageFile);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updateProfile.mutate(editForm);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setEditForm({
      ...editForm,
      [e.target.name]: e.target.value
    });
  };

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
                  <button 
                    onClick={handleEditClick}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                  >
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

      {/* Edit Profile Modal */}
      {isEditing && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Edit Profile</h2>
              <button
                onClick={() => setIsEditing(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <XMarkIcon className="h-6 w-6" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-6">
                {/* Profile Picture Upload */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Profile Picture
                  </label>
                  <div>
                    <div className="flex items-center space-x-4">
                      <div className="w-20 h-20 rounded-full bg-gradient-to-r from-red-600 to-yellow-500 flex items-center justify-center text-white text-xl font-bold overflow-hidden">
                        {profileImage ? (
                          <img
                            src={profileImage.preview}
                            alt="Profile Preview"
                            className="w-full h-full object-cover"
                          />
                        ) : profile.profile_picture ? (
                          <img
                            src={profile.profile_picture}
                            alt="Current Profile"
                            className="w-full h-full object-cover"
                          />
                        ) : (
                          profile.user.first_name?.[0] || profile.user.username[0]
                        )}
                      </div>
                      <div>
                        <label
                          htmlFor="profile-image-upload"
                          className="cursor-pointer inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                        >
                          <div className="flex items-center">
                            <PhotoIcon className="h-4 w-4 mr-2" />
                            <span>Upload Photo</span>
                          </div>
                          <input
                            id="profile-image-upload"
                            type="file"
                            accept="image/*"
                            onChange={(e) => handleImageUpload(e, 'profile')}
                            className="sr-only"
                          />
                        </label>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Cover Photo Upload */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Cover Photo
                  </label>
                  <div className="relative">
                    <div className="h-32 bg-gradient-to-r from-red-600 to-yellow-500 rounded-lg overflow-hidden">
                      {coverImage ? (
                        <img
                          src={coverImage.preview}
                          alt="Cover Preview"
                          className="w-full h-full object-cover"
                        />
                      ) : profile.cover_photo ? (
                        <img
                          src={profile.cover_photo}
                          alt="Current Cover"
                          className="w-full h-full object-cover"
                        />
                      ) : null}
                    </div>
                    <div className="absolute top-2 right-2">
                      <label
                        htmlFor="cover-image-upload"
                        className="cursor-pointer inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                      >
                        <div className="flex items-center">
                          <PhotoIcon className="h-4 w-4 mr-2" />
                          <span>Upload Cover</span>
                        </div>
                        <input
                          id="cover-image-upload"
                          type="file"
                          accept="image/*"
                          onChange={(e) => handleImageUpload(e, 'cover')}
                          className="sr-only"
                        />
                      </label>
                    </div>
                  </div>
                </div>

                {/* Bio */}
                <div>
                  <label htmlFor="bio" className="block text-sm font-medium text-gray-700 mb-2">
                    Bio
                  </label>
                  <textarea
                    id="bio"
                    name="bio"
                    value={editForm.bio}
                    onChange={handleChange}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Tell us about yourself..."
                  />
                </div>

                {/* Location */}
                <div>
                  <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
                    Location
                  </label>
                  <input
                    type="text"
                    id="location"
                    name="location"
                    value={editForm.location}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="City, State"
                  />
                </div>

                {/* Car Information */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="car_make" className="block text-sm font-medium text-gray-700 mb-2">
                      Car Make
                    </label>
                    <input
                      type="text"
                      id="car_make"
                      name="car_make"
                      value={editForm.car_make}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      placeholder="e.g., Ford"
                    />
                  </div>
                  <div>
                    <label htmlFor="car_model" className="block text-sm font-medium text-gray-700 mb-2">
                      Car Model
                    </label>
                    <input
                      type="text"
                      id="car_model"
                      name="car_model"
                      value={editForm.car_model}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      placeholder="e.g., Mustang"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="car_year" className="block text-sm font-medium text-gray-700 mb-2">
                      Car Year
                    </label>
                    <input
                      type="number"
                      id="car_year"
                      name="car_year"
                      value={editForm.car_year}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      placeholder="e.g., 2020"
                      min="1900"
                      max="2030"
                    />
                  </div>
                  <div>
                    <label htmlFor="car_mods" className="block text-sm font-medium text-gray-700 mb-2">
                      Modifications
                    </label>
                    <input
                      type="text"
                      id="car_mods"
                      name="car_mods"
                      value={editForm.car_mods}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      placeholder="e.g., Turbo, Exhaust"
                    />
                  </div>
                </div>

                {updateProfile.error && (
                  <div className="p-4 bg-red-50 border border-red-200 rounded-md">
                    <p className="text-red-800">
                      {(updateProfile.error as any)?.response?.data?.error || 'Failed to update profile. Please try again.'}
                    </p>
                  </div>
                )}

                <div className="flex space-x-4">
                  <button
                    type="button"
                    onClick={() => setIsEditing(false)}
                    className="btn-secondary flex-1"
                    disabled={updateProfile.isPending}
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="btn-primary flex-1"
                    disabled={updateProfile.isPending}
                  >
                    {updateProfile.isPending ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile; 