import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { userAPI, postAPI } from '../services/api';
import { 
  CameraIcon, 
  PencilIcon, 
  MapPinIcon,
  TruckIcon,
  HeartIcon,
  ChatBubbleLeftIcon,
  ShareIcon,
  TrashIcon,
  XMarkIcon,
  CheckIcon
} from '@heroicons/react/24/outline';
import ConfirmationDialog from '../components/ConfirmationDialog';

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
  const [isPosting, setIsPosting] = useState(false);
  const [editingPost, setEditingPost] = useState<number | null>(null);
  const [editPostContent, setEditPostContent] = useState('');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [showProfileConfirmation, setShowProfileConfirmation] = useState(false);
  const [showPostConfirmation, setShowPostConfirmation] = useState(false);
  const [confirmationData, setConfirmationData] = useState<any>(null);

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

  // Clear messages after 5 seconds
  useEffect(() => {
    if (error || success) {
      const timer = setTimeout(() => {
        setError(null);
        setSuccess(null);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error, success]);

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
          car_year: response.data.car_year?.toString() || '',
          car_mods: response.data.car_mods || ''
        });
      }
    } catch (error) {
      console.error('Error loading profile:', error);
      setError('Failed to load profile. Please try again.');
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
      setError('Failed to load posts. Please try again.');
    }
  };

  // Profile CRUD Operations
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
        setSuccess('Profile picture updated successfully!');
      } catch (error) {
        console.error('Error uploading profile picture:', error);
        setError('Failed to upload profile picture. Please try again.');
      }
    }
  };

  const handleCoverPhotoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && profile) {
      try {
        await userAPI.uploadCoverPhoto(profile.id, file);
        await loadProfile();
        setSuccess('Cover photo updated successfully!');
      } catch (error) {
        console.error('Error uploading cover photo:', error);
        setError('Failed to upload cover photo. Please try again.');
      }
    }
  };

  const handleRemoveProfilePicture = async () => {
    if (profile) {
      try {
        await userAPI.removeProfilePicture(profile.id);
        await loadProfile();
        setSuccess('Profile picture removed successfully!');
      } catch (error) {
        console.error('Error removing profile picture:', error);
        setError('Failed to remove profile picture. Please try again.');
      }
    }
  };

  const handleRemoveCoverPhoto = async () => {
    if (profile) {
      try {
        await userAPI.removeCoverPhoto(profile.id);
        await loadProfile();
        setSuccess('Cover photo removed successfully!');
      } catch (error) {
        console.error('Error removing cover photo:', error);
        setError('Failed to remove cover photo. Please try again.');
      }
    }
  };

  const handleSubmitProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      // Prepare data for confirmation dialog
      const confirmationData = {
        'Bio': editForm.bio || 'No bio',
        'Location': editForm.location || 'Not specified',
        'Car Make': editForm.car_make || 'Not specified',
        'Car Model': editForm.car_model || 'Not specified',
        'Car Year': editForm.car_year || 'Not specified',
        'Car Modifications': editForm.car_mods || 'None'
      };

      setConfirmationData(confirmationData);
      setShowProfileConfirmation(true);
    } catch (error) {
      console.error('Error preparing profile update:', error);
      setError('Failed to prepare profile update. Please try again.');
    }
  };

  const handleConfirmProfileUpdate = async () => {
    try {
      if (profile) {
        await userAPI.updateProfile(profile.id, editForm);
        await loadProfile();
        setIsEditing(false);
        setShowProfileConfirmation(false);
        setSuccess('Profile updated successfully!');
      }
    } catch (error) {
      console.error('Error updating profile:', error);
      setError('Failed to update profile. Please try again.');
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    if (profile) {
      setEditForm({
        bio: profile.bio || '',
        location: profile.location || '',
        car_make: profile.car_make || '',
        car_model: profile.car_model || '',
        car_year: profile.car_year?.toString() || '',
        car_mods: profile.car_mods || ''
      });
    }
  };

  // Posts CRUD Operations
  const handleSubmitPost = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPost.trim()) return;

    setError('');

    try {
      // Prepare data for confirmation dialog
      const confirmationData = {
        'Content': newPost.substring(0, 100) + (newPost.length > 100 ? '...' : ''),
        'Has Image': selectedImage ? 'Yes' : 'No',
        'Image Name': selectedImage ? selectedImage.name : 'N/A'
      };

      setConfirmationData(confirmationData);
      setShowPostConfirmation(true);
    } catch (error) {
      console.error('Error preparing post:', error);
      setError('Failed to prepare post. Please try again.');
    }
  };

  const handleConfirmPostCreate = async () => {
    setIsPosting(true);
    try {
      const postData: any = { content: newPost };
      if (selectedImage) {
        postData.image = selectedImage;
      }
      
      await postAPI.create(postData);
      setNewPost('');
      setSelectedImage(null);
      setImagePreview(null);
      setShowPostConfirmation(false);
      await loadPosts();
      setSuccess('Post created successfully!');
    } catch (error) {
      console.error('Error creating post:', error);
      setError('Failed to create post. Please try again.');
    } finally {
      setIsPosting(false);
    }
  };

  const handleEditPost = async (postId: number) => {
    try {
      await postAPI.update(postId, { content: editPostContent });
      setEditingPost(null);
      setEditPostContent('');
      await loadPosts();
      setSuccess('Post updated successfully!');
    } catch (error) {
      console.error('Error updating post:', error);
      setError('Failed to update post. Please try again.');
    }
  };

  const handleDeletePost = async (postId: number) => {
    try {
      await postAPI.delete(postId);
      setShowDeleteConfirm(null);
      await loadPosts();
      setSuccess('Post deleted successfully!');
    } catch (error) {
      console.error('Error deleting post:', error);
      setError('Failed to delete post. Please try again.');
    }
  };

  const handleLikePost = async (postId: number) => {
    try {
      await postAPI.likePost(postId);
      await loadPosts();
    } catch (error) {
      console.error('Error liking post:', error);
      setError('Failed to like post. Please try again.');
    }
  };

  const startEditPost = (post: UserPost) => {
    setEditingPost(post.id);
    setEditPostContent(post.content);
  };

  const cancelEditPost = () => {
    setEditingPost(null);
    setEditPostContent('');
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
        <p className="text-gray-600">Unable to load your profile. Please try again.</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Error/Success Messages */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          </div>
        </div>
      )}

      {success && (
        <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-green-800">{success}</p>
            </div>
          </div>
        </div>
      )}

      {/* Profile Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        {/* Cover Photo */}
        <div className="relative h-48 bg-gradient-to-r from-primary-600 to-primary-800">
          {profile.cover_photo && (
            <img 
              src={profile.cover_photo} 
              alt="Cover" 
              className="w-full h-full object-cover"
            />
          )}
          <div className="absolute top-4 right-4 flex space-x-2">
            <label className="cursor-pointer bg-white bg-opacity-20 hover:bg-opacity-30 p-2 rounded-full transition-colors">
              <CameraIcon className="h-5 w-5 text-white" />
              <input
                type="file"
                accept="image/*"
                onChange={handleCoverPhotoUpload}
                className="hidden"
              />
            </label>
            {profile.cover_photo && (
              <button
                onClick={handleRemoveCoverPhoto}
                className="bg-red-500 hover:bg-red-600 p-2 rounded-full transition-colors"
              >
                <XMarkIcon className="h-5 w-5 text-white" />
              </button>
            )}
          </div>
        </div>

        {/* Profile Info */}
        <div className="relative px-6 pb-6">
          <div className="flex items-end -mt-16 mb-4">
            <div className="relative">
              <div className="w-32 h-32 rounded-full bg-gray-200 overflow-hidden border-4 border-white">
                {profile.profile_picture ? (
                  <img 
                    src={profile.profile_picture} 
                    alt="Profile" 
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-4xl font-bold text-gray-600">
                    {profile.user.first_name[0]}
                  </div>
                )}
              </div>
              <div className="absolute bottom-0 right-0 flex space-x-1">
                <label className="cursor-pointer bg-primary-600 hover:bg-primary-700 p-2 rounded-full transition-colors">
                  <CameraIcon className="h-4 w-4 text-white" />
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleProfilePictureUpload}
                    className="hidden"
                  />
                </label>
                {profile.profile_picture && (
                  <button
                    onClick={handleRemoveProfilePicture}
                    className="bg-red-500 hover:bg-red-600 p-2 rounded-full transition-colors"
                  >
                    <XMarkIcon className="h-4 w-4 text-white" />
                  </button>
                )}
              </div>
            </div>
            
            <div className="ml-6 flex-1">
              <h1 className="text-3xl font-bold text-gray-900">
                {profile.user.first_name} {profile.user.last_name}
              </h1>
              <p className="text-gray-600">@{profile.user.username}</p>
            </div>
            
            <button
              onClick={() => setIsEditing(true)}
              className="btn-primary flex items-center"
            >
              <PencilIcon className="h-4 w-4 mr-2" />
              Edit Profile
            </button>
          </div>

          {/* Profile Stats */}
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-600">{profile.wins}</div>
              <div className="text-sm text-gray-600">Wins</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{profile.total_races}</div>
              <div className="text-sm text-gray-600">Total Races</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{profile.win_rate.toFixed(1)}%</div>
              <div className="text-sm text-gray-600">Win Rate</div>
            </div>
          </div>

          {/* Profile Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">About</h3>
              <p className="text-gray-700">{profile.bio || 'No bio added yet.'}</p>
              
              {profile.location && (
                <div className="flex items-center mt-3 text-gray-600">
                  <MapPinIcon className="h-4 w-4 mr-2" />
                  <span>{profile.location}</span>
                </div>
              )}
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Current Car</h3>
              {(profile.car_make || profile.car_model) ? (
                <div className="flex items-center text-gray-700">
                  <TruckIcon className="h-5 w-5 mr-2" />
                  <span>{profile.car_year} {profile.car_make} {profile.car_model}</span>
                </div>
              ) : (
                <p className="text-gray-600">No car information added.</p>
              )}
              
              {profile.car_mods && (
                <div className="mt-2">
                  <h4 className="text-sm font-medium text-gray-900">Modifications:</h4>
                  <p className="text-sm text-gray-600">{profile.car_mods}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Edit Profile Modal */}
      {isEditing && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Edit Profile</h3>
            <form onSubmit={handleSubmitProfile} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Bio</label>
                <textarea
                  value={editForm.bio}
                  onChange={(e) => setEditForm({...editForm, bio: e.target.value})}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  rows={3}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Location</label>
                <input
                  type="text"
                  value={editForm.location}
                  onChange={(e) => setEditForm({...editForm, location: e.target.value})}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Car Make</label>
                  <input
                    type="text"
                    value={editForm.car_make}
                    onChange={(e) => setEditForm({...editForm, car_make: e.target.value})}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Car Model</label>
                  <input
                    type="text"
                    value={editForm.car_model}
                    onChange={(e) => setEditForm({...editForm, car_model: e.target.value})}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Car Year</label>
                  <input
                    type="number"
                    value={editForm.car_year}
                    onChange={(e) => setEditForm({...editForm, car_year: e.target.value})}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Modifications</label>
                  <input
                    type="text"
                    value={editForm.car_mods}
                    onChange={(e) => setEditForm({...editForm, car_mods: e.target.value})}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
              </div>
              
              <div className="flex space-x-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 transition-colors"
                >
                  Save Changes
                </button>
                <button
                  type="button"
                  onClick={handleCancelEdit}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Create Post */}
      <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Create Post</h3>
        <form onSubmit={handleSubmitPost} className="space-y-4">
          <textarea
            value={newPost}
            onChange={(e) => setNewPost(e.target.value)}
            placeholder="What's on your mind?"
            className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            rows={3}
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
                <XMarkIcon className="h-4 w-4" />
              </button>
            </div>
          )}
          
          <div className="flex items-center justify-between">
            <label className="cursor-pointer bg-gray-100 hover:bg-gray-200 p-2 rounded-lg transition-colors">
              <CameraIcon className="h-5 w-5 text-gray-600" />
              <input
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                className="hidden"
              />
            </label>
            
            <button
              type="submit"
              disabled={!newPost.trim() || isPosting}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isPosting ? 'Posting...' : 'Post'}
            </button>
          </div>
        </form>
      </div>

      {/* Posts Feed */}
      <div className="mt-8 space-y-6">
        <h3 className="text-2xl font-bold text-gray-900">Posts</h3>
        
        {posts.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow-sm border border-gray-200">
            <p className="text-gray-600">No posts yet. Create your first post!</p>
          </div>
        ) : (
          posts.map((post) => (
            <div key={post.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <div className="w-10 h-10 rounded-full bg-gray-200 mr-3">
                    {post.user.first_name[0]}
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">
                      {post.user.first_name} {post.user.last_name}
                    </h4>
                    <p className="text-sm text-gray-600">
                      {new Date(post.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                
                {post.user.id === authUser?.id && (
                  <div className="flex space-x-2">
                    <button
                      onClick={() => startEditPost(post)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      <PencilIcon className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => setShowDeleteConfirm(post.id)}
                      className="text-red-400 hover:text-red-600"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                )}
              </div>
              
              {editingPost === post.id ? (
                <div className="space-y-4">
                  <textarea
                    value={editPostContent}
                    onChange={(e) => setEditPostContent(e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    rows={3}
                  />
                  <div className="flex space-x-3">
                    <button
                      onClick={() => handleEditPost(post.id)}
                      className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                    >
                      <CheckIcon className="h-4 w-4" />
                    </button>
                    <button
                      onClick={cancelEditPost}
                      className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400 transition-colors"
                    >
                      <XMarkIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <p className="text-gray-900 mb-4">{post.content}</p>
                  
                  {post.image && (
                    <img src={post.image} alt="Post" className="w-full rounded-lg mb-4" />
                  )}
                  
                  <div className="flex items-center space-x-4 text-gray-600">
                    <button
                      onClick={() => handleLikePost(post.id)}
                      className={`flex items-center space-x-1 hover:text-primary-600 transition-colors ${
                        post.likes.includes(authUser?.id || 0) ? 'text-primary-600' : ''
                      }`}
                    >
                      <HeartIcon className="h-5 w-5" />
                      <span>{post.like_count}</span>
                    </button>
                    <button className="flex items-center space-x-1 hover:text-gray-800 transition-colors">
                      <ChatBubbleLeftIcon className="h-5 w-5" />
                      <span>{post.comments.length}</span>
                    </button>
                    <button className="flex items-center space-x-1 hover:text-gray-800 transition-colors">
                      <ShareIcon className="h-5 w-5" />
                    </button>
                  </div>
                </>
              )}
            </div>
          ))
        )}
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Delete Post</h3>
            <p className="text-gray-600 mb-6">Are you sure you want to delete this post? This action cannot be undone.</p>
            <div className="flex space-x-3">
              <button
                onClick={() => handleDeletePost(showDeleteConfirm)}
                className="flex-1 bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition-colors"
              >
                Delete
              </button>
              <button
                onClick={() => setShowDeleteConfirm(null)}
                className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Profile Confirmation Dialog */}
      <ConfirmationDialog
        isOpen={showProfileConfirmation}
        onClose={() => setShowProfileConfirmation(false)}
        onConfirm={handleConfirmProfileUpdate}
        title="Confirm Profile Update"
        message="Please review your profile changes below before updating. This will update your public profile information."
        confirmText="Update Profile"
        cancelText="Cancel"
        type="info"
        loading={false}
        data={confirmationData}
      />

      {/* Post Confirmation Dialog */}
      <ConfirmationDialog
        isOpen={showPostConfirmation}
        onClose={() => setShowPostConfirmation(false)}
        onConfirm={handleConfirmPostCreate}
        title="Confirm Post Creation"
        message="Please review your post content below before creating. This will be visible to other users."
        confirmText="Create Post"
        cancelText="Cancel"
        type="info"
        loading={isPosting}
        data={confirmationData}
      />
    </div>
  );
} 