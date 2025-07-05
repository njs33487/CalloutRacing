import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';

interface ConnectAccountStatus {
  has_account: boolean;
  account_id?: string;
  charges_enabled?: boolean;
  payouts_enabled?: boolean;
  details_submitted?: boolean;
  requirements?: any;
}

const ConnectOnboarding: React.FC = () => {
  const [accountCreatePending, setAccountCreatePending] = useState(false);
  const [accountLinkCreatePending, setAccountLinkCreatePending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [connectedAccountId, setConnectedAccountId] = useState<string | null>(null);
  const [accountStatus, setAccountStatus] = useState<ConnectAccountStatus | null>(null);
  
  const { user } = useAuth();
  const { accountId } = useParams();

  useEffect(() => {
    // Check if we have an account ID from URL params
    if (accountId) {
      setConnectedAccountId(accountId);
    }
    
    // Check current account status
    checkAccountStatus();
  }, [accountId]);

  const checkAccountStatus = async () => {
    try {
      const response = await api.get('/connect/account-status/');
      setAccountStatus(response.data);
      
      if (response.data.has_account && response.data.account_id) {
        setConnectedAccountId(response.data.account_id);
      }
    } catch (err) {
      console.error('Error checking account status:', err);
    }
  };

  const createAccount = async () => {
    setAccountCreatePending(true);
    setError(null);
    
    try {
      const response = await api.post('/connect/create-account/');
      const { account_id } = response.data;
      
      setConnectedAccountId(account_id);
      setAccountCreatePending(false);
      
      // Refresh account status
      await checkAccountStatus();
    } catch (err: any) {
      setAccountCreatePending(false);
      setError(err.response?.data?.error || 'Failed to create account');
    }
  };

  const createAccountLink = async () => {
    if (!connectedAccountId) return;
    
    setAccountLinkCreatePending(true);
    setError(null);
    
    try {
      const response = await api.post('/connect/create-account-link/', {
        account_id: connectedAccountId
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

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Authentication Required</h2>
          <p className="text-gray-600">Please log in to access Connect onboarding.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">CalloutRacing Connect</h1>
          <p className="text-gray-600">Start selling on our marketplace and earn money from your listings.</p>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          {!connectedAccountId && (
            <>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Get Ready to Start Selling</h2>
              <p className="text-gray-600 mb-6">
                CalloutRacing is the premier platform for racing enthusiasts. Join our community of sellers 
                to help racers find the parts and services they need.
              </p>
              
              {!accountCreatePending && (
                <button
                  onClick={createAccount}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
                >
                  Create Connect Account
                </button>
              )}
            </>
          )}

          {connectedAccountId && (
            <>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Complete Your Onboarding</h2>
              <p className="text-gray-600 mb-6">
                Complete your account setup to start accepting payments and receiving payouts.
              </p>
              
              {!accountLinkCreatePending && (
                <button
                  onClick={createAccountLink}
                  className="bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
                >
                  Complete Onboarding
                </button>
              )}
            </>
          )}

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          {/* Status Indicators */}
          {(connectedAccountId || accountCreatePending || accountLinkCreatePending) && (
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              {connectedAccountId && (
                <p className="text-blue-800">
                  <strong>Account ID:</strong> <code className="bg-blue-100 px-2 py-1 rounded">{connectedAccountId}</code>
                </p>
              )}
              {accountCreatePending && (
                <p className="text-blue-800">Creating your Connect account...</p>
              )}
              {accountLinkCreatePending && (
                <p className="text-blue-800">Preparing onboarding link...</p>
              )}
            </div>
          )}

          {/* Account Status Details */}
          {accountStatus && accountStatus.has_account && (
            <div className="mt-6 p-4 bg-gray-50 border border-gray-200 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-3">Account Status</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-center">
                  <span className={`w-3 h-3 rounded-full mr-2 ${accountStatus.charges_enabled ? 'bg-green-500' : 'bg-yellow-500'}`}></span>
                  <span className="text-sm text-gray-700">
                    Charges: {accountStatus.charges_enabled ? 'Enabled' : 'Pending'}
                  </span>
                </div>
                <div className="flex items-center">
                  <span className={`w-3 h-3 rounded-full mr-2 ${accountStatus.payouts_enabled ? 'bg-green-500' : 'bg-yellow-500'}`}></span>
                  <span className="text-sm text-gray-700">
                    Payouts: {accountStatus.payouts_enabled ? 'Enabled' : 'Pending'}
                  </span>
                </div>
                <div className="flex items-center">
                  <span className={`w-3 h-3 rounded-full mr-2 ${accountStatus.details_submitted ? 'bg-green-500' : 'bg-yellow-500'}`}></span>
                  <span className="text-sm text-gray-700">
                    Details: {accountStatus.details_submitted ? 'Submitted' : 'Pending'}
                  </span>
                </div>
              </div>
            </div>
          )}
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

export default ConnectOnboarding; 