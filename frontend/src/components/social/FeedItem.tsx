import React, { useState } from 'react';
import { Heart, MessageCircle, Share2, MoreHorizontal, User, Clock, Car, Wifi } from 'lucide-react';

interface FeedItemProps {
  post: {
    id: number;
    author: {
      id: number;
      username: string;
      email: string;
    };
    content: string;
    post_type: 'text' | 'image' | 'video' | 'race_result' | 'car_update' | 'live';
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
  };
  onLike: (postId: number) => void;
  onComment: (postId: number, content: string) => void;
  onShare: (postId: number) => void;
}

const FeedItem: React.FC<FeedItemProps> = ({ post, onLike, onComment, onShare }) => {
  const [showComments, setShowComments] = useState(false);
  const [commentText, setCommentText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    setIsSubmitting(true);
    try {
      await onComment(post.id, commentText);
      setCommentText('');
    } catch (error) {
      console.error('Error posting comment:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const getPostTypeIcon = () => {
    switch (post.post_type) {
      case 'race_result':
        return <Clock className="w-4 h-4 text-green-500" />;
      case 'car_update':
        return <Car className="w-4 h-4 text-blue-500" />;
      case 'live':
        return <Wifi className="w-4 h-4 text-red-500" />;
      default:
        return null;
    }
  };

  const getPostTypeLabel = () => {
    switch (post.post_type) {
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
      default:
        return 'Post';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 mb-4 overflow-hidden">
      {/* Post Header */}
      <div className="p-4 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="font-semibold text-gray-900">{post.author.username}</h3>
                {getPostTypeIcon()}
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                  {getPostTypeLabel()}
                </span>
              </div>
              <p className="text-sm text-gray-500">{post.time_ago}</p>
            </div>
          </div>
          <button className="text-gray-400 hover:text-gray-600">
            <MoreHorizontal className="w-5 h-5" />
          </button>
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
              onClick={() => onLike(post.id)}
              className={`flex items-center space-x-2 transition-colors ${
                post.is_liked 
                  ? 'text-red-500 hover:text-red-600' 
                  : 'text-gray-500 hover:text-red-500'
              }`}
            >
              <Heart className={`w-5 h-5 ${post.is_liked ? 'fill-current' : ''}`} />
              <span className="text-sm font-medium">{post.likes_count}</span>
            </button>
            
            <button
              onClick={() => setShowComments(!showComments)}
              className="flex items-center space-x-2 text-gray-500 hover:text-blue-500 transition-colors"
            >
              <MessageCircle className="w-5 h-5" />
              <span className="text-sm font-medium">{post.comments_count}</span>
            </button>
            
            <button
              onClick={() => onShare(post.id)}
              className="flex items-center space-x-2 text-gray-500 hover:text-green-500 transition-colors"
            >
              <Share2 className="w-5 h-5" />
              <span className="text-sm font-medium">Share</span>
            </button>
          </div>
        </div>
      </div>

      {/* Comments Section */}
      {showComments && (
        <div className="border-t border-gray-100">
          {/* Comment Form */}
          <div className="p-4 border-b border-gray-100">
            <form onSubmit={handleCommentSubmit} className="flex space-x-3">
              <input
                type="text"
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                placeholder="Write a comment..."
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isSubmitting}
              />
              <button
                type="submit"
                disabled={!commentText.trim() || isSubmitting}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isSubmitting ? 'Posting...' : 'Post'}
              </button>
            </form>
          </div>

          {/* Comments List */}
          <div className="p-4 space-y-3">
            {post.comments.map((comment) => (
              <div key={comment.id} className="flex space-x-3">
                <div className="w-8 h-8 bg-gradient-to-r from-gray-400 to-gray-500 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-white" />
                </div>
                <div className="flex-1">
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="font-medium text-sm text-gray-900">
                        {comment.author.username}
                      </span>
                      <span className="text-xs text-gray-500">{comment.time_ago}</span>
                    </div>
                    <p className="text-sm text-gray-700">{comment.content}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FeedItem; 