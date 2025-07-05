import React from 'react';
import { Link } from 'react-router-dom';

const SubscriptionCancelPage: React.FC = () => {
  return (
    <div className="max-w-2xl mx-auto p-6 text-center">
      <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mb-6">
        <h1 className="text-3xl font-bold mb-4">Subscription Cancelled</h1>
        <p className="text-lg mb-4">No worries! You can try again anytime.</p>
      </div>
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Why Subscribe?</h2>
        <ul className="text-left space-y-2 mb-6">
          <li className="flex items-center">
            <span className="text-blue-500 mr-2">→</span>
            Remove all advertisements
          </li>
          <li className="flex items-center">
            <span className="text-blue-500 mr-2">→</span>
            Access premium racing tools
          </li>
          <li className="flex items-center">
            <span className="text-blue-500 mr-2">→</span>
            Get priority customer support
          </li>
          <li className="flex items-center">
            <span className="text-blue-500 mr-2">→</span>
            Advanced analytics and insights
          </li>
        </ul>
        <div className="space-y-3">
          <Link 
            to="/subscription" 
            className="inline-block bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 transition-colors"
          >
            Try Again
          </Link>
          <br />
          <Link 
            to="/app" 
            className="inline-block text-gray-600 hover:text-gray-800 transition-colors"
          >
            Back to Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
};

export default SubscriptionCancelPage; 