import React from 'react';
import { useParams, Link } from 'react-router-dom';

const ConnectOnboardingReturn: React.FC = () => {
  const { accountId } = useParams();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">CalloutRacing Connect</h1>
          <p className="text-gray-600">Your account setup has been completed successfully.</p>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="text-center">
            <div className="mb-6">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Onboarding Complete!</h2>
              <p className="text-gray-600 mb-6">
                Thank you for completing your Connect account setup. Your account is now ready to accept payments.
              </p>
            </div>

            {accountId && (
              <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-blue-800">
                  <strong>Account ID:</strong> <code className="bg-blue-100 px-2 py-1 rounded">{accountId}</code>
                </p>
              </div>
            )}

            <div className="space-y-4">
              <Link
                to="/marketplace"
                className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                Go to Marketplace
              </Link>
              
              <div className="text-sm text-gray-500">
                <Link to="/marketplace/create-listing" className="text-blue-600 hover:text-blue-700 underline">
                  Create your first listing
                </Link>
              </div>
            </div>
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

export default ConnectOnboardingReturn; 