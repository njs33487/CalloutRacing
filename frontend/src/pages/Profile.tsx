import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { userAPI, postAPI } from '../services/api';
import { 
  CameraIcon, 
  PencilIcon, 
  TrophyIcon, 
  FlagIcon,
  MapPinIcon,
  TruckIcon,
  HeartIcon,
  ChatBubbleLeftIcon,
  ShareIcon
} from '@heroicons/react/24/outline';

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

export default function Profile() {
  const { user: authUser } = useAuth();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [posts, setPosts] = useState<UserPost[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [newPost, setNewPost] = useState('');
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const [editForm, setEditForm] = useState({
    bio: '',
    location: '',
    car_make: '',
    car_model: '',
    car_year: '',
    car_mods: ''
  });

  useEffect(() => {
    loadProfile();
    loadPosts();
  }, []);

  const loadProfile = async () => {
    try {
      if (authUser) {
        const response = await userAPI.profile(authUser.id);
        setProfile(response.data);
        setEditForm({
          bio: response.data.bio || '',
          location: response.data.location || '',
          car_make: response.data.car_make || '',
          car_model: response.data.car_model || '',
          car_year: response.data.car_year || '',
          car_mods: response.data.car_mods || ''
        });
      }
    } catch (error) {
      console.error('Error loading profile:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadPosts = async () => {
    try {
      const response = await postAPI.list();
      setPosts(response.data.results || response.data);
    } catch (error) {
      console.error('Error loading posts:', error);
    }
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleProfilePictureUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && profile) {
      try {
        await userAPI.uploadProfilePicture(profile.id, file);
        await loadProfile();
      } catch (error) {
        console.error('Error uploading profile picture:', error);
        alert('Failed to upload profile picture. Please try again.');
      }
    }
  };

  const handleCoverPhotoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && profile) {
      try {
        await userAPI.uploadCoverPhoto(profile.id, file);
        await loadProfile();
      } catch (error) {
        console.error('Error uploading cover photo:', error);
        alert('Failed to upload cover photo. Please try again.');
      }
    }
  };

  const handleRemoveProfilePicture = async () => {
    if (profile) {
      try {
        await userAPI.removeProfilePicture(profile.id);
        await loadProfile();
      } catch (error) {
        console.error('Error removing profile picture:', error);
        alert('Failed to remove profile picture. Please try again.');
      }
    }
  };

  const handleRemoveCoverPhoto = async () => {
    if (profile) {
      try {
        await userAPI.removeCoverPhoto(profile.id);
        await loadProfile();
      } catch (error) {
        console.error('Error removing cover photo:', error);
        alert('Failed to remove cover photo. Please try again.');
      }
    }
  };

  const handleSubmitProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (profile) {
        await userAPI.updateProfile(profile.id, editForm);
        await loadProfile();
        setIsEditing(false);
      }
    } catch (error) {
      console.error('Error updating profile:', error);
    }
  };

  const handleSubmitPost = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPost.trim()) return;

    try {
      const formData = new FormData();
      formData.append('content', newPost);
      if (selectedImage) {
        formData.append('image', selectedImage);
      }

      await postAPI.create(formData);
      setNewPost('');
      setSelectedImage(null);
      setImagePreview(null);
      await loadPosts();
    } catch (error) {
      console.error('Error creating post:', error);
    }
  };

  const handleLikePost = async (postId: number) => {
    try {
      await postAPI.likePost(postId);
      await loadPosts();
    } catch (error) {
      console.error('Error liking post:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Profile Not Found</h2>
        <p className="text-gray-600">Unable to load profile information.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Cover Photo */}
      <div className="relative h-64 bg-gradient-to-r from-primary-600 to-primary-800">
        {profile.cover_photo && (
          <img 
            src={profile.cover_photo} 
            alt="Cover" 
            className="w-full h-full object-cover"
          />
        )}
        <div className="absolute inset-0 bg-black bg-opacity-30"></div>
        
        {/* Cover Photo Upload Button */}
        <div className="absolute top-4 left-4">
          <label className="cursor-pointer bg-white bg-opacity-90 text-gray-900 px-3 py-2 rounded-lg font-medium hover:bg-opacity-100 flex items-center space-x-2">
            <input
              type="file"
              accept="image/*"
              onChange={handleCoverPhotoUpload}
              className="hidden"
            />
            <CameraIcon className="w-4 h-4" />
            <span>Upload Cover</span>
          </label>
          {profile.cover_photo && (
            <button
              onClick={handleRemoveCoverPhoto}
              className="ml-2 bg-red-500 bg-opacity-90 text-white px-3 py-2 rounded-lg font-medium hover:bg-opacity-100"
            >
              Remove
            </button>
          )}
        </div>
        
        {/* Profile Picture */}
        <div className="absolute bottom-0 left-8 transform translate-y-1/2">
          <div className="relative">
            <div className="w-32 h-32 rounded-full border-4 border-white bg-gray-200 overflow-hidden">
              {profile.profile_picture ? (
                <img 
                  src={profile.profile_picture} 
                  alt="Profile" 
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center bg-gray-300">
                  <CameraIcon className="w-12 h-12 text-gray-500" />
                </div>
              )}
            </div>
            <label className="absolute bottom-0 right-0 bg-primary-600 text-white p-2 rounded-full hover:bg-primary-700 cursor-pointer">
              <input
                type="file"
                accept="image/*"
                onChange={handleProfilePictureUpload}
                className="hidden"
              />
              <CameraIcon className="w-4 h-4" />
            </label>
            {profile.profile_picture && (
              <button
                onClick={handleRemoveProfilePicture}
                className="absolute top-0 right-0 bg-red-500 text-white p-1 rounded-full hover:bg-red-600"
              >
                ×
              </button>
            )}
          </div>
        </div>

        {/* Edit Profile Button */}
        <div className="absolute top-4 right-4">
          <button 
            onClick={() => setIsEditing(!isEditing)}
            className="bg-white bg-opacity-90 text-gray-900 px-4 py-2 rounded-lg font-medium hover:bg-opacity-100 flex items-center space-x-2"
          >
            <PencilIcon className="w-4 h-4" />
            <span>{isEditing ? 'Cancel' : 'Edit Profile'}</span>
          </button>
        </div>
      </div>

      {/* Profile Info */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mt-16 mb-8">
          <div className="flex items-end justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                {profile.user.first_name} {profile.user.last_name}
              </h1>
              <p className="text-gray-600">@{profile.user.username}</p>
              {profile.location && (
                <div className="flex items-center mt-2 text-gray-600">
                  <MapPinIcon className="w-4 h-4 mr-1" />
                  <span>{profile.location}</span>
                </div>
              )}
            </div>
          </div>

          {profile.bio && (
            <p className="mt-4 text-gray-700 max-w-2xl">{profile.bio}</p>
          )}
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg p-6 text-center shadow-sm">
            <TrophyIcon className="w-8 h-8 text-yellow-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">{profile.wins}</div>
            <div className="text-sm text-gray-600">Wins</div>
          </div>
          <div className="bg-white rounded-lg p-6 text-center shadow-sm">
            <FlagIcon className="w-8 h-8 text-red-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">{profile.losses}</div>
            <div className="text-sm text-gray-600">Losses</div>
          </div>
          <div className="bg-white rounded-lg p-6 text-center shadow-sm">
            <TruckIcon className="w-8 h-8 text-blue-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">{profile.total_races}</div>
            <div className="text-sm text-gray-600">Total Races</div>
          </div>
          <div className="bg-white rounded-lg p-6 text-center shadow-sm">
            <div className="text-2xl font-bold text-gray-900">{profile.win_rate.toFixed(1)}%</div>
            <div className="text-sm text-gray-600">Win Rate</div>
          </div>
        </div>

        {/* Car Info */}
        {(profile.car_make || profile.car_model || profile.car_year) && (
          <div className="bg-white rounded-lg p-6 mb-8 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Current Car</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="text-sm text-gray-600">Make/Model:</span>
                <p className="font-medium">
                  {profile.car_year} {profile.car_make} {profile.car_model}
                </p>
              </div>
              {profile.car_mods && (
                <div>
                  <span className="text-sm text-gray-600">Modifications:</span>
                  <p className="font-medium">{profile.car_mods}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Edit Profile Form */}
        {isEditing && (
          <div className="bg-white rounded-lg p-6 mb-8 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Edit Profile</h3>
            <form onSubmit={handleSubmitProfile} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Bio</label>
                <textarea
                  value={editForm.bio}
                  onChange={(e) => setEditForm({...editForm, bio: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  rows={3}
                  placeholder="Tell us about yourself..."
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                  <input
                    type="text"
                    value={editForm.location}
                    onChange={(e) => setEditForm({...editForm, location: e.target.value})}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="City, State"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Car Make</label>
                  <input
                    type="text"
                    value={editForm.car_make}
                    onChange={(e) => setEditForm({...editForm, car_make: e.target.value})}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="e.g., Ford"
                  />
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Car Model</label>
                  <input
                    type="text"
                    value={editForm.car_model}
                    onChange={(e) => setEditForm({...editForm, car_model: e.target.value})}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="e.g., Mustang"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Car Year</label>
                  <input
                    type="number"
                    value={editForm.car_year}
                    onChange={(e) => setEditForm({...editForm, car_year: e.target.value})}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="e.g., 2020"
                    min="1900"
                    max="2030"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Modifications</label>
                <input
                  type="text"
                  value={editForm.car_mods}
                  onChange={(e) => setEditForm({...editForm, car_mods: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="e.g., Turbo, Exhaust, Wheels"
                />
              </div>
              <div className="flex space-x-4">
                <button
                  type="button"
                  onClick={() => setIsEditing(false)}
                  className="flex-1 bg-gray-200 text-gray-900 py-2 px-4 rounded-lg font-medium hover:bg-gray-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-primary-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-primary-700"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Create Post */}
        <div className="bg-white rounded-lg p-6 mb-8 shadow-sm">
          <form onSubmit={handleSubmitPost} className="space-y-4">
            <textarea
              value={newPost}
              onChange={(e) => setNewPost(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={3}
              placeholder="What's on your mind?"
            />
            {imagePreview && (
              <div className="relative">
                <img src={imagePreview} alt="Preview" className="w-full max-h-64 object-cover rounded-lg" />
                <button
                  type="button"
                  onClick={() => {
                    setSelectedImage(null);
                    setImagePreview(null);
                  }}
                  className="absolute top-2 right-2 bg-red-500 text-white p-1 rounded-full hover:bg-red-600"
                >
                  ×
                </button>
              </div>
            )}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <label className="cursor-pointer">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    className="hidden"
                  />
                  <CameraIcon className="w-6 h-6 text-gray-500 hover:text-primary-600" />
                </label>
              </div>
              <button
                type="submit"
                disabled={!newPost.trim()}
                className="bg-primary-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Post
              </button>
            </div>
          </form>
        </div>

        {/* Posts Feed */}
        <div className="space-y-6">
          <h3 className="text-xl font-semibold text-gray-900">Recent Posts</h3>
          {posts.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600">No posts yet. Start sharing your racing adventures!</p>
            </div>
          ) : (
            posts.map((post) => (
              <div key={post.id} className="bg-white rounded-lg shadow-sm overflow-hidden">
                <div className="p-6">
                  <div className="flex items-center mb-4">
                    <div className="w-10 h-10 rounded-full bg-gray-200 mr-3">
                      {post.user.first_name && (
                        <div className="w-full h-full flex items-center justify-center text-sm font-medium text-gray-600">
                          {post.user.first_name[0]}
                        </div>
                      )}
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">
                        {post.user.first_name} {post.user.last_name}
                      </p>
                      <p className="text-sm text-gray-600">@{post.user.username}</p>
                    </div>
                    <div className="ml-auto text-sm text-gray-500">
                      {new Date(post.created_at).toLocaleDateString()}
                    </div>
                  </div>
                  
                  <p className="text-gray-900 mb-4">{post.content}</p>
                  
                  {post.image && (
                    <img src={post.image} alt="Post" className="w-full rounded-lg mb-4" />
                  )}
                  
                  {post.car && (
                    <div className="bg-gray-50 rounded-lg p-3 mb-4">
                      <p className="text-sm text-gray-600">Featured Car:</p>
                      <p className="font-medium">{post.car.year} {post.car.make} {post.car.model}</p>
                    </div>
                  )}
                  
                  <div className="flex items-center space-x-6 text-gray-500">
                    <button
                      onClick={() => handleLikePost(post.id)}
                      className="flex items-center space-x-1 hover:text-red-500"
                    >
                      <HeartIcon className="w-5 h-5" />
                      <span>{post.like_count}</span>
                    </button>
                    <button className="flex items-center space-x-1 hover:text-blue-500">
                      <ChatBubbleLeftIcon className="w-5 h-5" />
                      <span>{post.comments?.length || 0}</span>
                    </button>
                    <button className="flex items-center space-x-1 hover:text-green-500">
                      <ShareIcon className="w-5 h-5" />
                      <span>Share</span>
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
} 