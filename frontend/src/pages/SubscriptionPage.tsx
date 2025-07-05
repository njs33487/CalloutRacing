import React, { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { EmbeddedCheckoutProvider, EmbeddedCheckout } from '@stripe/react-stripe-js';
import axios from 'axios';
import { API_URL } from '../services/api';

// Load your Stripe public key (from environment variable)
const stripePromise = loadStripe(process.env.VITE_STRIPE_PUBLISHABLE_KEY || 'pk_test_YOUR_PUBLISHABLE_KEY');

const SubscriptionPage: React.FC = () => {
  const [clientSecret, setClientSecret] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchClientSecret = async (priceId: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API_URL}/subscriptions/create-checkout-session/`, { 
        price_id: priceId 
      }, {
        headers: {
          'X-CSRFToken': document.cookie.split('csrftoken=')[1]?.split(';')[0] || '',
        },
        withCredentials: true,
      });
      
      setClientSecret(response.data.clientSecret);
    } catch (error) {
      console.error("Error creating checkout session:", error);
      setError("Failed to start subscription process. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubscribe = (priceId: string) => {
    fetchClientSecret(priceId);
  };

  if (clientSecret) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Complete Your Subscription</h1>
        <div className="bg-white rounded-lg shadow-md p-6">
          <EmbeddedCheckoutProvider
            stripe={stripePromise}
            options={{ clientSecret }}
          >
            <EmbeddedCheckout />
          </EmbeddedCheckoutProvider>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Choose Your Plan</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}
      
      <div className="grid md:grid-cols-2 gap-8">
        <div className="border border-gray-200 rounded-lg p-6 bg-white shadow-sm">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">Basic Plan</h2>
          <p className="text-3xl font-bold text-primary-600 mb-4">$9.99<span className="text-lg text-gray-500">/month</span></p>
          <ul className="space-y-2 mb-6">
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Standard Features
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Limited Ad-free Experience
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Basic Analytics
            </li>
          </ul>
          <button 
            onClick={() => handleSubscribe('price_basic')} 
            disabled={loading}
            className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'Subscribe Basic'}
          </button>
        </div>

        <div className="border border-primary-200 rounded-lg p-6 bg-white shadow-lg border-2">
          <div className="bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm font-medium mb-4 inline-block">
            Most Popular
          </div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">Pro Plan</h2>
          <p className="text-3xl font-bold text-primary-600 mb-4">$19.99<span className="text-lg text-gray-500">/month</span></p>
          <ul className="space-y-2 mb-6">
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              All Basic Features
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Advanced Analytics
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Completely Ad-free
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Priority Support
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Premium Racing Tools
            </li>
          </ul>
          <button 
            onClick={() => handleSubscribe('price_pro')} 
            disabled={loading}
            className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'Subscribe Pro'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SubscriptionPage; 