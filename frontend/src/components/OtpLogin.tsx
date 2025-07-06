import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store';
import { sendOtpAsync, verifyOtpAsync, setIdentifier, setType, resetOtp } from '../store/slices/otpSlice';
import { useNavigate } from 'react-router-dom';

const OtpLogin: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { loading, error, step, identifier, type, user } = useSelector((state: RootState) => state.otp);
  const [otp, setOtp] = useState('');

  const handleSendOtp = () => {
    if (!identifier.trim()) {
      return;
    }
    dispatch(sendOtpAsync({ identifier: identifier.trim(), type }));
  };

  const handleVerifyOtp = () => {
    if (!otp.trim()) {
      return;
    }
    dispatch(verifyOtpAsync({ identifier: identifier.trim(), otp_code: otp.trim(), type }));
  };

  const handleReset = () => {
    dispatch(resetOtp());
    setOtp('');
  };

  const handleBackToLogin = () => {
    navigate('/login');
  };

  useEffect(() => {
    if (step === 'success' && user) {
      // Store user data in localStorage for persistence
      localStorage.setItem('user', JSON.stringify(user));
      // Redirect to home page
      navigate('/');
    }
  }, [step, user, navigate]);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Login with {type === 'phone' ? 'Phone' : 'Email'} OTP
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Enter your {type === 'phone' ? 'phone number' : 'email'} to receive a verification code
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          {step === 'input' && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Login Method
                </label>
                <select 
                  value={type} 
                  onChange={e => dispatch(setType(e.target.value as 'phone' | 'email'))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                >
                  <option value="phone">Phone Number</option>
                  <option value="email">Email Address</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {type === 'phone' ? 'Phone Number' : 'Email Address'}
                </label>
                <input
                  type={type === 'phone' ? 'tel' : 'email'}
                  placeholder={type === 'phone' ? '+1234567890' : 'user@example.com'}
                  value={identifier}
                  onChange={e => dispatch(setIdentifier(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
              
              <div className="flex space-x-3">
                <button 
                  onClick={handleSendOtp}
                  disabled={loading || !identifier.trim()}
                  className="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Sending...' : 'Send OTP'}
                </button>
                <button 
                  onClick={handleBackToLogin}
                  className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Back
                </button>
              </div>
            </div>
          )}

          {step === 'otp' && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Enter Verification Code
                </label>
                <input
                  type="text"
                  placeholder="123456"
                  value={otp}
                  onChange={e => setOtp(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-center text-lg tracking-widest"
                  maxLength={6}
                  autoFocus
                />
                <p className="mt-2 text-sm text-gray-500">
                  We sent a 6-digit code to {identifier}
                </p>
              </div>
              
              <div className="flex space-x-3">
                <button 
                  onClick={handleVerifyOtp}
                  disabled={loading || !otp.trim()}
                  className="flex-1 bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Verifying...' : 'Verify OTP'}
                </button>
                <button 
                  onClick={handleReset}
                  className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Back
                </button>
              </div>
              
              <div className="text-center">
                <button 
                  onClick={handleSendOtp}
                  disabled={loading}
                  className="text-sm text-indigo-600 hover:text-indigo-500 disabled:opacity-50"
                >
                  Resend Code
                </button>
              </div>
            </div>
          )}

          {error && (
            <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          {step === 'success' && (
            <div className="text-center">
              <div className="text-green-600 text-lg font-medium mb-4">
                ✅ Login Successful!
              </div>
              <p className="text-gray-600">
                Redirecting to home page...
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default OtpLogin; 