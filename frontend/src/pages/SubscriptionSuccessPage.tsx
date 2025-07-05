import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import { API_URL } from '../services/api';

const SubscriptionSuccessPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [sessionStatus, setSessionStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initialize = async () => {
      const sessionId = searchParams.get('session_id');
      
      if (sessionId) {
        try {
          const response = await axios.get(`${API_URL}/subscriptions/session-status/?session_id=${sessionId}`);
          const session = response.data;
          setSessionStatus(session);

          if (session.status === 'open') {
            // Remount embedded Checkout
            navigate('/subscription');
          } else if (session.status === 'complete') {
            // Show success page
            setLoading(false);
          }
        } catch (error) {
          console.error('Error fetching session status:', error);
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };

    initialize();
  }, [searchParams, navigate]);

  useEffect(() => {
    if (sessionStatus?.status === 'complete') {
      const timer = setTimeout(() => {
        navigate('/app'); // Redirect to dashboard after a short delay
      }, 5000); // 5 seconds
      return () => clearTimeout(timer);
    }
  }, [sessionStatus, navigate]);

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto p-6 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
        <p>Processing your subscription...</p>
      </div>
    );
  }

  if (sessionStatus?.status === 'complete') {
    return (
      <div className="max-w-2xl mx-auto p-6 text-center">
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
          <h1 className="text-3xl font-bold mb-4">Subscription Successful! 🎉</h1>
          <p className="text-lg mb-4">Thank you for subscribing to CalloutRacing Pro!</p>
          {sessionStatus.customer_email && (
            <p className="text-sm">Confirmation sent to: {sessionStatus.customer_email}</p>
          )}
          <p className="text-sm mt-4">Redirecting to your dashboard...</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">What's Next?</h2>
          <ul className="text-left space-y-2">
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Enjoy an ad-free experience
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Access premium racing tools
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Get priority support
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Advanced analytics and insights
            </li>
          </ul>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-6 text-center">
      <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mb-6">
        <h1 className="text-3xl font-bold mb-4">Payment Processing</h1>
        <p className="text-lg mb-4">Your payment is being processed. We'll update you when it's complete.</p>
      </div>
    </div>
  );
};

export default SubscriptionSuccessPage; 