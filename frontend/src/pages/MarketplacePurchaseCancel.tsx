import React from 'react';
import { Link } from 'react-router-dom';

interface PurchaseCancelProps {}

const MarketplacePurchaseCancel: React.FC<PurchaseCancelProps> = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md w-full bg-white rounded-lg shadow-sm p-6">
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-yellow-100 mb-4">
            <svg className="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Payment Cancelled</h2>
          <p className="text-gray-600 mb-6">
            Your payment was cancelled. No charges were made to your account.
          </p>
          
          <div className="space-y-3">
            <Link
              to="/marketplace"
              className="inline-block w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
            >
              Return to Marketplace
            </Link>
            <Link
              to="/"
              className="inline-block w-full bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-3 px-4 rounded-lg transition-colors"
            >
              Go Home
            </Link>
          </div>

          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-blue-800 text-sm">
              <strong>Need help?</strong> If you have any questions about the payment process, 
              please contact our support team.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketplacePurchaseCancel; 