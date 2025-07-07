import React, { useState, useRef } from 'react';
import { Image, Video, Car, Clock, X, Send, VideoIcon, Wifi, Users, Megaphone, MapPin, DollarSign } from 'lucide-react';

interface CreatePostProps {
  onSubmit: (postData: {
    content: string;
    post_type: 'text' | 'image' | 'video' | 'race_result' | 'car_update' | 'live' | 'race_callout' | 'announcement';
    image?: File;
    video?: File;
    // Callout-specific fields
    callout_challenged_user?: string;
    callout_location?: string;
    callout_location_type?: 'street' | 'dragstrip';
    callout_race_type?: string;
    callout_wager_amount?: number;
    callout_scheduled_date?: string;
    // Announcement-specific fields
    is_pinned?: boolean;
    announcement_type?: 'general' | 'feature' | 'maintenance' | 'promotion' | 'event';
    announcement_priority?: 'low' | 'medium' | 'high' | 'critical';
  }) => void;
  onCancel: () => void;
  isLoading?: boolean;
}

const CreatePost: React.FC<CreatePostProps> = ({ onSubmit, onCancel, isLoading = false }) => {
  const [content, setContent] = useState('');
  const [postType, setPostType] = useState<'text' | 'image' | 'video' | 'race_result' | 'car_update' | 'live' | 'race_callout' | 'announcement'>('text');
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [selectedVideo, setSelectedVideo] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [videoPreview, setVideoPreview] = useState<string | null>(null);
  const [isLiveStreaming, setIsLiveStreaming] = useState(false);
  const [liveStreamTitle, setLiveStreamTitle] = useState('');

  // Callout-specific state
  const [calloutChallengedUser, setCalloutChallengedUser] = useState('');
  const [calloutLocation, setCalloutLocation] = useState('');
  const [calloutLocationType, setCalloutLocationType] = useState<'street' | 'dragstrip'>('street');
  const [calloutRaceType, setCalloutRaceType] = useState('');
  const [calloutWagerAmount, setCalloutWagerAmount] = useState<number>(0);
  const [calloutScheduledDate, setCalloutScheduledDate] = useState('');

  // Announcement-specific state
  const [isPinned, setIsPinned] = useState(false);
  const [announcementType, setAnnouncementType] = useState<'general' | 'feature' | 'maintenance' | 'promotion' | 'event'>('general');
  const [announcementPriority, setAnnouncementPriority] = useState<'low' | 'medium' | 'high' | 'critical'>('medium');

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
      callout_challenged_user: calloutChallengedUser,
      callout_location: calloutLocation,
      callout_location_type: calloutLocationType,
      callout_race_type: calloutRaceType,
      callout_wager_amount: calloutWagerAmount,
      callout_scheduled_date: calloutScheduledDate,
      is_pinned: isPinned,
      announcement_type: announcementType,
      announcement_priority: announcementPriority,
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

  const startLiveStream = async () => {
    try {
      await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      });
      // Here you would typically connect to your streaming service
      // For now, we'll just simulate the live stream
      setIsLiveStreaming(true);
      console.log('Live stream started');
    } catch (error) {
      console.error('Error starting live stream:', error);
    }
  };

  const stopLiveStream = () => {
    setIsLiveStreaming(false);
    setLiveStreamTitle('');
    // Here you would stop the actual stream
    console.log('Live stream stopped');
  };

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
      case 'live':
        return 'Live Stream';
      case 'race_callout':
        return 'Race Callout';
      case 'announcement':
        return 'Announcement';
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
          <div className="grid grid-cols-6 gap-2">
            {[
              { type: 'text', label: 'Text', icon: null },
              { type: 'image', label: 'Photo', icon: <Image className="w-4 h-4" /> },
              { type: 'video', label: 'Video', icon: <Video className="w-4 h-4" /> },
              { type: 'race_result', label: 'Race', icon: <Clock className="w-4 h-4" /> },
              { type: 'car_update', label: 'Car', icon: <Car className="w-4 h-4" /> },
              { type: 'live', label: 'Live', icon: <VideoIcon className="w-4 h-4" /> },
              { type: 'race_callout', label: 'Race Callout', icon: <Users className="w-4 h-4" /> },
              { type: 'announcement', label: 'Announcement', icon: <Megaphone className="w-4 h-4" /> },
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

        {/* Live Stream Controls */}
        {postType === 'live' && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <Wifi className="w-5 h-5 text-red-600" />
              <h4 className="font-medium text-red-900">Live Stream</h4>
            </div>
            
            {!isLiveStreaming ? (
              <div className="space-y-3">
                <input
                  type="text"
                  value={liveStreamTitle}
                  onChange={(e) => setLiveStreamTitle(e.target.value)}
                  placeholder="Enter stream title..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-500"
                />
                <button
                  type="button"
                  onClick={startLiveStream}
                  className="flex items-center space-x-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                >
                  <VideoIcon className="w-4 h-4" />
                  <span>Start Live Stream</span>
                </button>
              </div>
            ) : (
              <div className="space-y-3">
                <div className="flex items-center space-x-2 text-red-600">
                  <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                  <span className="text-sm font-medium">LIVE</span>
                </div>
                <p className="text-sm text-red-700">{liveStreamTitle}</p>
                <button
                  type="button"
                  onClick={stopLiveStream}
                  className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
                >
                  Stop Stream
                </button>
              </div>
            )}
          </div>
        )}

        {/* Content Input */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {getPostTypeLabel()}
          </label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder={`What's on your mind? ${postType === 'race_result' ? 'Share your race results...' : postType === 'car_update' ? 'Share your car updates...' : postType === 'live' ? 'Describe your live stream...' : postType === 'race_callout' ? 'Describe the race callout...' : postType === 'announcement' ? 'Describe the announcement...' : ''}`}
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

        {/* Callout-specific fields */}
        {postType === 'race_callout' && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Callout Details
            </label>
            <div className="space-y-2">
              <input
                type="text"
                value={calloutChallengedUser}
                onChange={(e) => setCalloutChallengedUser(e.target.value)}
                placeholder="Challenged User"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                type="text"
                value={calloutLocation}
                onChange={(e) => setCalloutLocation(e.target.value)}
                placeholder="Location"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <select
                value={calloutLocationType}
                onChange={(e) => setCalloutLocationType(e.target.value as 'street' | 'dragstrip')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="street">Street</option>
                <option value="dragstrip">Dragstrip</option>
              </select>
              <input
                type="text"
                value={calloutRaceType}
                onChange={(e) => setCalloutRaceType(e.target.value)}
                placeholder="Race Type"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                type="number"
                value={calloutWagerAmount}
                onChange={(e) => setCalloutWagerAmount(Number(e.target.value))}
                placeholder="Wager Amount"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                type="text"
                value={calloutScheduledDate}
                onChange={(e) => setCalloutScheduledDate(e.target.value)}
                placeholder="Scheduled Date"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        )}

        {/* Announcement-specific fields */}
        {postType === 'announcement' && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Announcement Details
            </label>
            <div className="space-y-2">
              <input
                type="text"
                value={isPinned ? 'Pinned' : 'Not Pinned'}
                onChange={(e) => setIsPinned(e.target.value === 'Pinned')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <select
                value={announcementType}
                onChange={(e) => setAnnouncementType(e.target.value as 'general' | 'feature' | 'maintenance' | 'promotion' | 'event')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="general">General</option>
                <option value="feature">Feature</option>
                <option value="maintenance">Maintenance</option>
                <option value="promotion">Promotion</option>
                <option value="event">Event</option>
              </select>
              <select
                value={announcementPriority}
                onChange={(e) => setAnnouncementPriority(e.target.value as 'low' | 'medium' | 'high' | 'critical')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div className="flex justify-end space-x-3">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={!content.trim() || isLoading || (postType === 'live' && !isLiveStreaming)}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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