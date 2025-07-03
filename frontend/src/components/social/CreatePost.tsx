import React, { useState, useRef } from 'react';
import { Image, Video, Car, Clock, X, Send } from 'lucide-react';

interface CreatePostProps {
  onSubmit: (postData: {
    content: string;
    post_type: 'text' | 'image' | 'video' | 'race_result' | 'car_update';
    image?: File;
    video?: File;
  }) => void;
  onCancel: () => void;
  isLoading?: boolean;
}

const CreatePost: React.FC<CreatePostProps> = ({ onSubmit, onCancel, isLoading = false }) => {
  const [content, setContent] = useState('');
  const [postType, setPostType] = useState<'text' | 'image' | 'video' | 'race_result' | 'car_update'>('text');
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [selectedVideo, setSelectedVideo] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [videoPreview, setVideoPreview] = useState<string | null>(null);
  
  const imageInputRef = useRef<HTMLInputElement>(null);
  const videoInputRef = useRef<HTMLInputElement>(null);

  const handleImageSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      setSelectedVideo(null);
      setVideoPreview(null);
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleVideoSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type.startsWith('video/')) {
      setSelectedVideo(file);
      setSelectedImage(null);
      setImagePreview(null);
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setVideoPreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) return;

    onSubmit({
      content: content.trim(),
      post_type: postType,
      image: selectedImage || undefined,
      video: selectedVideo || undefined,
    });
  };

  const removeMedia = () => {
    setSelectedImage(null);
    setSelectedVideo(null);
    setImagePreview(null);
    setVideoPreview(null);
    if (imageInputRef.current) imageInputRef.current.value = '';
    if (videoInputRef.current) videoInputRef.current.value = '';
  };

  // Removed unused function

  const getPostTypeLabel = () => {
    switch (postType) {
      case 'race_result':
        return 'Race Result';
      case 'car_update':
        return 'Car Update';
      case 'image':
        return 'Photo';
      case 'video':
        return 'Video';
      default:
        return 'Text Post';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Create Post</h3>
        <button
          onClick={onCancel}
          className="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        {/* Post Type Selector */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Post Type
          </label>
          <div className="grid grid-cols-5 gap-2">
            {[
              { type: 'text', label: 'Text', icon: null },
              { type: 'image', label: 'Photo', icon: <Image className="w-4 h-4" /> },
              { type: 'video', label: 'Video', icon: <Video className="w-4 h-4" /> },
              { type: 'race_result', label: 'Race', icon: <Clock className="w-4 h-4" /> },
              { type: 'car_update', label: 'Car', icon: <Car className="w-4 h-4" /> },
            ].map(({ type, label, icon }) => (
              <button
                key={type}
                type="button"
                onClick={() => setPostType(type as any)}
                className={`p-3 rounded-lg border-2 transition-colors ${
                  postType === type
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-gray-200 hover:border-gray-300 text-gray-600'
                }`}
              >
                <div className="flex flex-col items-center space-y-1">
                  {icon}
                  <span className="text-xs font-medium">{label}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Content Input */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {getPostTypeLabel()}
          </label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder={`What's on your mind? ${postType === 'race_result' ? 'Share your race results...' : postType === 'car_update' ? 'Share your car updates...' : ''}`}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows={4}
            disabled={isLoading}
          />
        </div>

        {/* Media Upload */}
        {(postType === 'image' || postType === 'video') && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {postType === 'image' ? 'Upload Image' : 'Upload Video'}
            </label>
            
            {!selectedImage && !selectedVideo ? (
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <div className="flex flex-col items-center space-y-2">
                  {postType === 'image' ? (
                    <Image className="w-8 h-8 text-gray-400" />
                  ) : (
                    <Video className="w-8 h-8 text-gray-400" />
                  )}
                  <p className="text-sm text-gray-600">
                    Click to upload {postType === 'image' ? 'an image' : 'a video'}
                  </p>
                  <button
                    type="button"
                    onClick={() => {
                      if (postType === 'image') {
                        imageInputRef.current?.click();
                      } else {
                        videoInputRef.current?.click();
                      }
                    }}
                    className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                  >
                    Choose File
                  </button>
                </div>
              </div>
            ) : (
              <div className="relative">
                {imagePreview && (
                  <div className="relative">
                    <img
                      src={imagePreview}
                      alt="Preview"
                      className="w-full rounded-lg max-h-64 object-cover"
                    />
                    <button
                      type="button"
                      onClick={removeMedia}
                      className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                )}
                {videoPreview && (
                  <div className="relative">
                    <video
                      src={videoPreview}
                      controls
                      className="w-full rounded-lg max-h-64"
                    />
                    <button
                      type="button"
                      onClick={removeMedia}
                      className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                )}
              </div>
            )}

            <input
              ref={imageInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              className="hidden"
            />
            <input
              ref={videoInputRef}
              type="file"
              accept="video/*"
              onChange={handleVideoSelect}
              className="hidden"
            />
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex items-center justify-end space-x-3">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
            disabled={isLoading}
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={!content.trim() || isLoading}
            className="flex items-center space-x-2 px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-4 h-4" />
            <span>{isLoading ? 'Posting...' : 'Post'}</span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreatePost; 