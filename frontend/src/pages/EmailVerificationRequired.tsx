import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';

const EmailVerificationRequired: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleResendVerification = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email) {
      setStatus('error');
      setMessage('Please enter your email address');
      return;
    }

    setStatus('loading');
    
    try {
      const response = await api.post('/auth/resend-verification/', { email });
      setStatus('success');
      setMessage(response.data.message || 'Verification email sent successfully!');
    } catch (error: any) {
      setStatus('error');
      setMessage(error.response?.data?.error || 'Failed to send verification email');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-yellow-100">
            <svg className="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          
          <h2 className="mt-4 text-xl font-semibold text-gray-900">Email Verification Required</h2>
          <p className="mt-2 text-gray-600">
          Please verify your email address. before you can access your account.
          </p>
          
          <div className="mt-6">
            <form onSubmit={handleResendVerification} className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 text-left">
                  Email Address
                </label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500"
                  placeholder="Enter your email address"
                  required
                />
              </div>
              
              {status === 'success' && (
                <div className="bg-green-50 border border-green-200 rounded-md p-3">
                  <p className="text-sm text-green-800">{message}</p>
                </div>
              )}
              
              {status === 'error' && (
                <div className="bg-red-50 border border-red-200 rounded-md p-3">
                  <p className="text-sm text-red-800">{message}</p>
                </div>
              )}
              
              <button
                type="submit"
                disabled={status === 'loading'}
                className="w-full bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {status === 'loading' ? 'Sending...' : 'Resend Verification Email'}
              </button>
            </form>
            
            <div className="mt-4 space-y-2">
              <button
                onClick={() => navigate('/login')}
                className="w-full bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700 transition-colors"
              >
                Back to Login
              </button>
              
              <button
                onClick={() => navigate('/signup')}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
              >
                Create New Account
              </button>
            </div>
          </div>
          
          <div className="mt-6 text-sm text-gray-500">
            <p>Didn't receive the email? Check your spam folder or contact support.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmailVerificationRequired; 