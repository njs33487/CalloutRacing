import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useStripe, useElements, PaymentElement } from '@stripe/react-stripe-js';
import { useAppSelector } from '../store/hooks';
import { authAPI } from '../services/api';
import { CheckIcon, XMarkIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

interface MarketplaceItem {
  id: number;
  title: string;
  description: string;
  price: number;
  seller: {
    id: number;
    username: string;
  };
}

const MarketplaceCheckoutPage: React.FC = () => {
  const { itemId } = useParams<{ itemId: string }>();
  const navigate = useNavigate();
  const { user } = useAppSelector((state) => state.auth);
  const stripe = useStripe();
  const elements = useElements();

  const [item, setItem] = useState<MarketplaceItem | null>(null);
  const [clientSecret, setClientSecret] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (itemId) {
      fetchItemDetails();
    }
  }, [itemId]);

  const fetchItemDetails = async () => {
    try {
      // Fetch item details
      const itemResponse = await authAPI.getMarketplaceItem(itemId!);
      setItem(itemResponse.data);

      // Create payment intent
      const paymentResponse = await authAPI.createMarketplacePaymentIntent(itemId!);
      setClientSecret(paymentResponse.data.clientSecret);
    } catch (err: any) {
      console.error('Failed to fetch item details:', err);
      setError(err.response?.data?.error || 'Failed to load item details');
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!stripe || !elements || !clientSecret) {
      setError('Payment system not ready. Please try again.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const { error: paymentError } = await stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: `${window.location.origin}/marketplace/purchase/success?item_id=${itemId}`,
        },
      });

      if (paymentError) {
        setError(paymentError.message || 'Payment failed');
      }
      // Payment is processing, user will be redirected
    } catch (err: any) {
      console.error('Payment error:', err);
      setError('An unexpected error occurred during payment');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate(`/marketplace/item/${itemId}`);
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <ExclamationTriangleIcon className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Authentication Required</h2>
          <p className="text-gray-600 mb-6">Please log in to complete your purchase.</p>
          <button
            onClick={() => navigate('/login')}
            className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  if (!item) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading item details...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Complete Your Purchase</h1>
          <p className="text-gray-600">Secure payment powered by Stripe</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Item Details */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Order Summary</h2>
            
            <div className="border-b border-gray-200 pb-4 mb-4">
              <h3 className="font-medium text-gray-900 mb-2">{item.title}</h3>
              <p className="text-gray-600 text-sm mb-2">{item.description}</p>
              <p className="text-gray-500 text-sm">Seller: {item.seller.username}</p>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Item Price:</span>
                <span className="font-medium">${item.price.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Platform Fee:</span>
                <span className="font-medium">${(item.price * 0.05).toFixed(2)}</span>
              </div>
              <div className="border-t border-gray-200 pt-2">
                <div className="flex justify-between">
                  <span className="text-lg font-semibold text-gray-900">Total:</span>
                  <span className="text-lg font-semibold text-gray-900">
                    ${(item.price * 1.05).toFixed(2)}
                  </span>
                </div>
              </div>
            </div>

            {/* Security Notice */}
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <div className="flex">
                <CheckIcon className="h-5 w-5 text-blue-500 mt-0.5 mr-3 flex-shrink-0" />
                <div>
                  <p className="text-sm font-medium text-blue-900">Secure Payment</p>
                  <p className="text-sm text-blue-700 mt-1">
                    Your payment is processed securely by Stripe. We never store your payment information.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Payment Form */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Payment Information</h2>

            {error && (
              <div className="mb-6">
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex">
                    <XMarkIcon className="h-5 w-5 text-red-400" />
                    <div className="ml-3">
                      <p className="text-sm text-red-800">{error}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {clientSecret ? (
              <form onSubmit={handleSubmit}>
                <PaymentElement
                  options={{
                    layout: { type: 'tabs', defaultCollapsed: false },
                    fields: {
                      billingDetails: {
                        name: 'auto',
                        email: 'auto',
                        phone: 'auto',
                        address: {
                          country: 'auto',
                          line1: 'auto',
                          line2: 'auto',
                          city: 'auto',
                          state: 'auto',
                          postalCode: 'auto',
                        },
                      },
                    },
                  }}
                />

                <div className="mt-6 space-y-3">
                  <button
                    type="submit"
                    disabled={!stripe || loading}
                    className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed transition-colors"
                  >
                    {loading ? (
                      <div className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                        Processing Payment...
                      </div>
                    ) : (
                      `Pay $${(item.price * 1.05).toFixed(2)}`
                    )}
                  </button>

                  <button
                    type="button"
                    onClick={handleCancel}
                    disabled={loading}
                    className="w-full bg-gray-100 text-gray-900 py-3 px-6 rounded-lg font-medium hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-400 transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            ) : (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Loading payment form...</p>
              </div>
            )}
          </div>
        </div>

        {/* Additional Information */}
        <div className="mt-8 bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">What happens next?</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="bg-indigo-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                <span className="text-indigo-600 font-bold">1</span>
              </div>
              <h4 className="font-medium text-gray-900 mb-2">Payment Processing</h4>
              <p className="text-sm text-gray-600">Your payment is securely processed through Stripe</p>
            </div>
            <div className="text-center">
              <div className="bg-indigo-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                <span className="text-indigo-600 font-bold">2</span>
              </div>
              <h4 className="font-medium text-gray-900 mb-2">Seller Notification</h4>
              <p className="text-sm text-gray-600">The seller is automatically notified of your purchase</p>
            </div>
            <div className="text-center">
              <div className="bg-indigo-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                <span className="text-indigo-600 font-bold">3</span>
              </div>
              <h4 className="font-medium text-gray-900 mb-2">Order Confirmation</h4>
              <p className="text-sm text-gray-600">You'll receive confirmation and can contact the seller</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketplaceCheckoutPage; 