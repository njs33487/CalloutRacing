import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { api } from '../services/api';

interface PurchaseSuccessProps {}

const MarketplacePurchaseSuccess: React.FC<PurchaseSuccessProps> = () => {
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(true);
  const [orderDetails, setOrderDetails] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const sessionId = searchParams.get('session_id');

  useEffect(() => {
    if (sessionId) {
      checkOrderStatus();
    } else {
      setLoading(false);
      setError('No session ID found');
    }
  }, [sessionId]);

  const checkOrderStatus = async () => {
    try {
      const response = await api.get(`/marketplace-listings/session_status/?session_id=${sessionId}`);
      const { status, payment_status } = response.data;
      
      if (status === 'complete' && payment_status === 'paid') {
        // Fetch order details if needed
        setOrderDetails({
          status: 'paid',
          sessionId,
          message: 'Payment completed successfully!'
        });
      } else {
        setError('Payment not completed. Please try again.');
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to verify payment status');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Verifying your payment...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full bg-white rounded-lg shadow-sm p-6">
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
              <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Payment Error</h2>
            <p className="text-gray-600 mb-6">{error}</p>
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
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md w-full bg-white rounded-lg shadow-sm p-6">
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 mb-4">
            <svg className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Payment Successful!</h2>
          <p className="text-gray-600 mb-6">
            Your payment has been processed successfully. The seller will be notified and should ship your item soon.
          </p>
          
          {orderDetails && (
            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <p className="text-sm text-gray-600">
                <strong>Session ID:</strong> {orderDetails.sessionId}
              </p>
              <p className="text-sm text-gray-600 mt-1">
                <strong>Status:</strong> {orderDetails.status}
              </p>
            </div>
          )}

          <div className="space-y-3">
            <Link
              to="/marketplace"
              className="inline-block w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
            >
              Continue Shopping
            </Link>
            <Link
              to="/orders"
              className="inline-block w-full bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-3 px-4 rounded-lg transition-colors"
            >
              View My Orders
            </Link>
            <Link
              to="/"
              className="inline-block w-full bg-gray-100 hover:bg-gray-200 text-gray-600 font-semibold py-3 px-4 rounded-lg transition-colors"
            >
              Go Home
            </Link>
          </div>

          <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p className="text-yellow-800 text-sm">
              <strong>Direct Charges:</strong> Your payment was processed directly on the seller's Stripe account. 
              You should receive a receipt from the seller.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketplacePurchaseSuccess; 