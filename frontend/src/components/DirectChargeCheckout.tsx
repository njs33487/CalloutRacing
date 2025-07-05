import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';

interface DirectChargeCheckoutProps {
  listingId: number;
  listingTitle: string;
  listingPrice: number;
  sellerName: string;
  onSuccess?: (orderId: number) => void;
  onCancel?: () => void;
  mode?: 'hosted' | 'embedded';
}

interface CheckoutSession {
  sessionId: string;
  url?: string;
  clientSecret?: string;
  order_id: number;
}

const DirectChargeCheckout: React.FC<DirectChargeCheckoutProps> = ({
  listingId,
  listingTitle,
  listingPrice,
  sellerName,
  onSuccess,
  onCancel,
  mode = 'hosted'
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<CheckoutSession | null>(null);
  const { user } = useAuth();

  const createCheckoutSession = async () => {
    if (!user) {
      setError('You must be logged in to make a purchase');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const endpoint = mode === 'embedded' 
        ? `/marketplace-listings/${listingId}/create_embedded_direct_charge/`
        : `/marketplace-listings/${listingId}/create_direct_charge_session/`;

      const response = await api.post(endpoint);
      const sessionData = response.data;
      setSession(sessionData);

      if (mode === 'hosted' && sessionData.url) {
        // Redirect to Stripe hosted checkout
        window.location.href = sessionData.url;
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create checkout session');
    } finally {
      setLoading(false);
    }
  };

  const handleEmbeddedCheckout = () => {
    if (!session?.clientSecret) {
      setError('No checkout session available');
      return;
    }

    // For embedded checkout, you would integrate with Stripe.js
    // This is a placeholder for the embedded checkout implementation
    console.log('Embedded checkout with client secret:', session.clientSecret);
    
    // In a real implementation, you would:
    // 1. Load Stripe.js
    // 2. Create an embedded checkout component
    // 3. Handle the payment flow
  };

  const checkSessionStatus = async (sessionId: string) => {
    try {
      const response = await api.get(`/marketplace-listings/session_status/?session_id=${sessionId}`);
      const { status, payment_status } = response.data;
      
      if (status === 'complete' && payment_status === 'paid') {
        onSuccess?.(session?.order_id || 0);
      }
    } catch (err) {
      console.error('Error checking session status:', err);
    }
  };

  useEffect(() => {
    // Check for session_id in URL params (for hosted checkout return)
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session_id');
    
    if (sessionId) {
      checkSessionStatus(sessionId);
    }
  }, []);

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Purchase {listingTitle}
        </h3>
        <p className="text-gray-600 mb-4">
          You're purchasing from <span className="font-medium">{sellerName}</span>
        </p>
        
        <div className="bg-gray-50 rounded-lg p-4 mb-4">
          <div className="flex justify-between items-center">
            <span className="text-gray-700">Price:</span>
            <span className="text-lg font-semibold text-gray-900">
              ${listingPrice.toFixed(2)}
            </span>
          </div>
          <div className="text-sm text-gray-500 mt-1">
            Platform fee: ${(listingPrice * 0.05).toFixed(2)} (5%)
          </div>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}

      <div className="space-y-3">
        {mode === 'hosted' ? (
          <button
            onClick={createCheckoutSession}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
          >
            {loading ? 'Creating checkout...' : 'Proceed to Checkout'}
          </button>
        ) : (
          <div className="space-y-3">
            <button
              onClick={createCheckoutSession}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
            >
              {loading ? 'Creating checkout...' : 'Create Embedded Checkout'}
            </button>
            
            {session?.clientSecret && (
              <button
                onClick={handleEmbeddedCheckout}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
              >
                Complete Payment
              </button>
            )}
          </div>
        )}

        <button
          onClick={onCancel}
          className="w-full bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-3 px-4 rounded-lg transition-colors"
        >
          Cancel
        </button>
      </div>

      {session && mode === 'embedded' && (
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-blue-800 text-sm">
            <strong>Session ID:</strong> {session.sessionId}
          </p>
          <p className="text-blue-800 text-sm mt-1">
            <strong>Order ID:</strong> {session.order_id}
          </p>
        </div>
      )}

      <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <p className="text-yellow-800 text-sm">
          <strong>Direct Charges:</strong> This payment will be processed directly on the seller's Stripe account. 
          CalloutRacing collects a 5% platform fee from each transaction.
        </p>
      </div>
    </div>
  );
};

export default DirectChargeCheckout; 