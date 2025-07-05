import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const AdvancedFeatureButton: React.FC = () => {
  const { hasActiveSubscription, subscriptionType } = useAuth();

  if (hasActiveSubscription && subscriptionType === 'pro') {
    return (
      <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors">
        Access Pro Analytics
      </button>
    );
  } else {
    return (
      <button 
        disabled 
        onClick={() => alert('Upgrade to Pro plan for this feature!')}
        className="bg-gray-400 text-white px-4 py-2 rounded-md cursor-not-allowed opacity-50"
      >
        Access Pro Analytics (Pro Plan Required)
      </button>
    );
  }
};

export default AdvancedFeatureButton; 