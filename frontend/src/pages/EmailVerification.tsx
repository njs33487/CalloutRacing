import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { authAPI } from '../services/api'

export default function EmailVerification() {
  const { token } = useParams<{ token: string }>()
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading')
  const [message, setMessage] = useState('')
  const [email, setEmail] = useState('')
  const [showResend, setShowResend] = useState(false)
  const [resendStatus, setResendStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')
  const [resendMessage, setResendMessage] = useState('')

  useEffect(() => {
    if (token) {
      verifyEmail(token)
    } else {
      setStatus('error')
      setMessage('Invalid verification link')
    }
  }, [token])

  const verifyEmail = async (verificationToken: string) => {
    try {
      const response = await authAPI.verifyEmail(verificationToken)
      setStatus('success')
      setMessage(response.data.message)
    } catch (error: any) {
      setStatus('error')
      setMessage(error.response?.data?.error || 'Email verification failed')
      if (error.response?.data?.error?.includes('expired')) {
        setShowResend(true)
      }
    }
  }

  const handleResendVerification = async () => {
    if (!email) {
      setResendMessage('Please enter your email address')
      return
    }

    setResendStatus('loading')
    try {
      const response = await authAPI.resendVerification(email)
      setResendStatus('success')
      setResendMessage(response.data.message)
    } catch (error: any) {
      setResendStatus('error')
      setResendMessage(error.response?.data?.error || 'Failed to resend verification email')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-secondary-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <img src="/android-chrome-192x192.png" alt="CalloutRacing Logo" className="h-12 w-12" />
        </div>
        <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
          Email Verification
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-lg sm:rounded-lg sm:px-10 border border-gray-200">
          {status === 'loading' && (
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Verifying your email address...</p>
            </div>
          )}

          {status === 'success' && (
            <div className="text-center">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
                <svg className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3 className="mt-4 text-lg font-medium text-gray-900">Email Verified!</h3>
              <p className="mt-2 text-sm text-gray-600">{message}</p>
              <div className="mt-6">
                <Link
                  to="/login"
                  className="btn-primary w-full"
                >
                  Continue to Login
                </Link>
              </div>
            </div>
          )}

          {status === 'error' && (
            <div className="text-center">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
                <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </div>
              <h3 className="mt-4 text-lg font-medium text-gray-900">Verification Failed</h3>
              <p className="mt-2 text-sm text-gray-600">{message}</p>
              
              {showResend && (
                <div className="mt-6">
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Resend Verification Email</h4>
                  <div className="space-y-3">
                    <input
                      type="email"
                      placeholder="Enter your email address"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="input-field"
                    />
                    <button
                      onClick={handleResendVerification}
                      disabled={resendStatus === 'loading'}
                      className="btn-primary w-full disabled:opacity-50"
                    >
                      {resendStatus === 'loading' ? 'Sending...' : 'Resend Verification'}
                    </button>
                    {resendMessage && (
                      <p className={`text-sm ${resendStatus === 'success' ? 'text-green-600' : 'text-red-600'}`}>
                        {resendMessage}
                      </p>
                    )}
                  </div>
                </div>
              )}
              
              <div className="mt-6 space-y-3">
                <Link
                  to="/login"
                  className="btn-secondary w-full"
                >
                  Back to Login
                </Link>
                <Link
                  to="/signup"
                  className="btn-primary w-full"
                >
                  Create New Account
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="mt-8 text-center">
        <p className="text-sm text-gray-600">
          <Link to="/" className="font-medium text-primary-600 hover:text-primary-500">
            Back to home
          </Link>
        </p>
      </div>
    </div>
  )
} 