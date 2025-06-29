import { useState } from 'react'
import { 
  ShareIcon, 
  ClipboardDocumentIcon, 
  CheckIcon 
} from '@heroicons/react/24/outline'
import { 
  shareToFacebook, 
  shareToTwitter, 
  shareToWhatsApp, 
  copyToClipboard,
  ShareData 
} from '../utils/socialSharing'

interface ShareButtonProps {
  shareData: ShareData;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

export default function ShareButton({ shareData, className = '', size = 'md' }: ShareButtonProps) {
  const [showDropdown, setShowDropdown] = useState(false);
  const [copied, setCopied] = useState(false);

  const sizeClasses = {
    sm: 'p-1.5',
    md: 'p-2',
    lg: 'p-3'
  };

  const iconSizes = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-6 w-6'
  };

  const handleCopyLink = async () => {
    const success = await copyToClipboard(shareData.url);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleShare = (platform: 'facebook' | 'twitter' | 'whatsapp') => {
    switch (platform) {
      case 'facebook':
        shareToFacebook(shareData);
        break;
      case 'twitter':
        shareToTwitter(shareData);
        break;
      case 'whatsapp':
        shareToWhatsApp(shareData);
        break;
    }
    setShowDropdown(false);
  };

  return (
    <div className="relative">
      <button
        onClick={() => setShowDropdown(!showDropdown)}
        className={`inline-flex items-center justify-center rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-700 transition-colors ${sizeClasses[size]} ${className}`}
        title="Share"
      >
        <ShareIcon className={iconSizes[size]} />
      </button>

      {showDropdown && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-10" 
            onClick={() => setShowDropdown(false)}
          />
          
          {/* Dropdown */}
          <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 z-20">
            <div className="p-2">
              <div className="text-xs font-medium text-gray-500 px-2 py-1">
                Share this {shareData.type}
              </div>
              
              <button
                onClick={() => handleShare('facebook')}
                className="w-full flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-blue-50 rounded-md transition-colors"
              >
                <div className="w-5 h-5 bg-blue-600 rounded mr-3 flex items-center justify-center">
                  <span className="text-white text-xs font-bold">f</span>
                </div>
                Share on Facebook
              </button>
              
              <button
                onClick={() => handleShare('twitter')}
                className="w-full flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-blue-50 rounded-md transition-colors"
              >
                <div className="w-5 h-5 bg-blue-400 rounded mr-3 flex items-center justify-center">
                  <span className="text-white text-xs font-bold">𝕏</span>
                </div>
                Share on Twitter
              </button>
              
              <button
                onClick={() => handleShare('whatsapp')}
                className="w-full flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-green-50 rounded-md transition-colors"
              >
                <div className="w-5 h-5 bg-green-500 rounded mr-3 flex items-center justify-center">
                  <span className="text-white text-xs font-bold">W</span>
                </div>
                Share on WhatsApp
              </button>
              
              <div className="border-t border-gray-200 my-1" />
              
              <button
                onClick={handleCopyLink}
                className="w-full flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-md transition-colors"
              >
                {copied ? (
                  <CheckIcon className="w-5 h-5 text-green-600 mr-3" />
                ) : (
                  <ClipboardDocumentIcon className="w-5 h-5 text-gray-500 mr-3" />
                )}
                {copied ? 'Copied!' : 'Copy link'}
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
} 