import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../services/api';

const ConnectOnboardingRefresh: React.FC = () => {
  const [accountLinkCreatePending, setAccountLinkCreatePending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { accountId } = useParams();

  useEffect(() => {
    if (accountId) {
      createAccountLink();
    }
  }, [accountId]);

  const createAccountLink = async () => {
    if (!accountId) return;
    
    setAccountLinkCreatePending(true);
    setError(null);
    
    try {
      const response = await api.post('/connect/create-account-link/', {
        account_id: accountId
      });
      
      const { url } = response.data;
      if (url) {
        window.location.href = url;
      }
    } catch (err: any) {
      setAccountLinkCreatePending(false);
      setError(err.response?.data?.error || 'Failed to create account link');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">CalloutRacing Connect</h1>
          <p className="text-gray-600">Complete your account setup to start accepting payments.</p>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Complete Your Onboarding</h2>
            <p className="text-gray-600 mb-6">
              CalloutRacing partners with Stripe to help you receive payments and keep your personal 
              bank and details secure.
            </p>
            
            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600">{error}</p>
                <button
                  onClick={createAccountLink}
                  className="mt-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                >
                  Try Again
                </button>
              </div>
            )}

            {accountId && (
              <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-blue-800">
                  <strong>Account ID:</strong> <code className="bg-blue-100 px-2 py-1 rounded">{accountId}</code>
                </p>
              </div>
            )}

            {accountLinkCreatePending && (
              <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <p className="text-yellow-800">Creating a new Account Link...</p>
                <div className="mt-3 flex justify-center">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-yellow-600"></div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Info Callout */}
        <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-yellow-800 text-sm">
            This is a Stripe Connect integration for marketplace sellers. 
            <a 
              href="https://docs.stripe.com/connect/onboarding/quickstart" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-yellow-900 underline ml-1"
            >
              View Stripe Connect docs
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default ConnectOnboardingRefresh; 