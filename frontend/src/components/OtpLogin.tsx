import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store';
import { sendOtpAsync, verifyOtpAsync, setIdentifier, setType, resetOtp } from '../store/slices/otpSlice';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const OtpLogin: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { loading, error, step, identifier, type, user } = useSelector((state: RootState) => state.otp);
  const { user: authUser, isLoading: authLoading } = useAuth();
  const [otp, setOtp] = useState('');
  const [countdown, setCountdown] = useState(0);
  const [remainingAttempts, setRemainingAttempts] = useState<number | null>(null);
  const [resendCooldown, setResendCooldown] = useState(0);

  // Countdown timer for OTP expiry
  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (countdown > 0) {
      timer = setTimeout(() => setCountdown(countdown - 1), 1000);
    }
    return () => clearTimeout(timer);
  }, [countdown]);

  // Resend cooldown timer
  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (resendCooldown > 0) {
      timer = setTimeout(() => setResendCooldown(resendCooldown - 1), 1000);
    }
    return () => clearTimeout(timer);
  }, [resendCooldown]);

  const handleSendOtp = async () => {
    if (!identifier.trim()) {
      return;
    }
    
    const result = await dispatch(sendOtpAsync({ identifier: identifier.trim(), type }));
    
    // Extract rate limiting info from response
    if (result.meta.requestStatus === 'fulfilled') {
      const response = result.payload as any;
      if (response.remaining_attempts !== undefined) {
        setRemainingAttempts(response.remaining_attempts);
      }
      if (response.resend_cooldown_seconds !== undefined) {
        setResendCooldown(response.resend_cooldown_seconds);
      }
      // Start countdown for OTP expiry
      setCountdown(response.expires_in_minutes * 60 || 600);
    }
  };

  const handleVerifyOtp = () => {
    if (!otp.trim() || otp.length !== 6) {
      return;
    }
    dispatch(verifyOtpAsync({ identifier: identifier.trim(), otp_code: otp.trim(), type }));
  };

  const handleReset = () => {
    dispatch(resetOtp());
    setOtp('');
    setCountdown(0);
    setResendCooldown(0);
    setRemainingAttempts(null);
  };

  const handleBackToLogin = () => {
    navigate('/login');
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const maskIdentifier = (identifier: string) => {
    if (type === 'email') {
      const [username, domain] = identifier.split('@');
      return `${username.slice(0, 3)}***@${domain}`;
    } else {
      return identifier.length > 5 
        ? `${identifier.slice(0, 3)}***${identifier.slice(-2)}`
        : '***';
    }
  };

  // Redirect if user is already authenticated
  useEffect(() => {
    if (authUser) {
      console.log('User is authenticated, redirecting to /app');
      navigate('/app');
    }
  }, [authUser, navigate]);

  // Show loading while checking authentication
  if (authLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  // Don't render OTP form if user is already authenticated
  if (authUser) {
    return null;
  }

  useEffect(() => {
    if (step === 'success' && user) {
      // Store user data in localStorage for persistence
      localStorage.setItem('user', JSON.stringify(user));
      // Redirect to home page
      navigate('/app');
    }
  }, [step, user, navigate]);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Secure Login with {type === 'phone' ? 'Phone' : 'Email'}
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Enter your {type === 'phone' ? 'phone number' : 'email'} to receive a secure verification code
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
                  <option value="phone">📱 Phone Number</option>
                  <option value="email">📧 Email Address</option>
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
                <p className="mt-1 text-xs text-gray-500">
                  {type === 'phone' 
                    ? 'Enter your phone number with country code (e.g., +1234567890)'
                    : 'Enter your email address'
                  }
                </p>
              </div>
              
              {remainingAttempts !== null && (
                <div className="text-sm text-amber-600 bg-amber-50 p-2 rounded">
                  ⚠️ Remaining attempts: {remainingAttempts}
                </div>
              )}
              
              <div className="flex space-x-3">
                <button 
                  onClick={handleSendOtp}
                  disabled={loading || !identifier.trim() || resendCooldown > 0}
                  className="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Sending...' : resendCooldown > 0 ? `Wait ${formatTime(resendCooldown)}` : 'Send Verification Code'}
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
              <div className="text-center">
                <div className="text-sm text-gray-600 mb-2">
                  Verification code sent to:
                </div>
                <div className="text-sm font-medium text-gray-900">
                  {maskIdentifier(identifier)}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Enter 6-Digit Verification Code
                </label>
                <input
                  type="text"
                  placeholder="123456"
                  value={otp}
                  onChange={e => {
                    const value = e.target.value.replace(/\D/g, '').slice(0, 6);
                    setOtp(value);
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-center text-lg tracking-widest font-mono"
                  maxLength={6}
                  autoFocus
                />
                <p className="mt-2 text-xs text-gray-500">
                  Enter the 6-digit code sent to your {type === 'phone' ? 'phone' : 'email'}
                </p>
              </div>
              
              {countdown > 0 && (
                <div className="text-center">
                  <div className="text-sm text-gray-600">
                    Code expires in: <span className="font-mono text-red-600">{formatTime(countdown)}</span>
                  </div>
                </div>
              )}
              
              <div className="flex space-x-3">
                <button 
                  onClick={handleVerifyOtp}
                  disabled={loading || otp.length !== 6}
                  className="flex-1 bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Verifying...' : 'Verify Code'}
                </button>
                <button 
                  onClick={handleReset}
                  className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Back
                </button>
              </div>
              
              <div className="text-center space-y-2">
                <button 
                  onClick={handleSendOtp}
                  disabled={loading || resendCooldown > 0}
                  className="text-sm text-indigo-600 hover:text-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {resendCooldown > 0 
                    ? `Resend in ${formatTime(resendCooldown)}` 
                    : 'Resend Code'
                  }
                </button>
                
                {countdown === 0 && (
                  <div className="text-sm text-red-600">
                    ⚠️ Code has expired. Please request a new code.
                  </div>
                )}
              </div>
            </div>
          )}

          {error && (
            <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              <div className="flex items-center">
                <span className="mr-2">⚠️</span>
                <span>{error}</span>
              </div>
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