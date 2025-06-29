import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { authAPI } from '../services/api'

export default function EmailVerificationRequired() {
  const { user, logout } = useAuth()
  const [email, setEmail] = useState(user?.email || '')
  const [isResending, setIsResending] = useState(false)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState<'success' | 'error' | ''>('')

  const handleResendVerification = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email) return

    setIsResending(true)
    setMessage('')
    setMessageType('')

    try {
      await authAPI.resendVerification(email)
      setMessage('Verification email sent successfully! Please check your inbox.')
      setMessageType('success')
    } catch (error: any) {
      console.error('Resend verification failed:', error)
      setMessage(error.response?.data?.error || 'Failed to resend verification email')
      setMessageType('error')
    } finally {
      setIsResending(false)
    }
  }

  const handleLogout = () => {
    logout()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-secondary-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <img src="/android-chrome-192x192.png" alt="CalloutRacing Logo" className="h-12 w-12" />
        </div>
        <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
          Email Verification Required
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Please verify your email address to access CalloutRacing
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-lg sm:rounded-lg sm:px-10 border border-gray-200">
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-yellow-100">
              <svg className="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-900">Verify Your Email</h3>
            <p className="mt-2 text-sm text-gray-600">
              We sent a verification email to <strong>{user?.email}</strong>. 
              Please check your inbox and click the verification link to continue.
            </p>
          </div>

          {message && (
            <div className={`mt-4 p-4 rounded-lg ${
              messageType === 'success' 
                ? 'bg-green-50 border border-green-200 text-green-800' 
                : 'bg-red-50 border border-red-200 text-red-800'
            }`}>
              <p className="text-sm">{message}</p>
            </div>
          )}

          <div className="mt-6">
            <form onSubmit={handleResendVerification} className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                  Email Address
                </label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="mt-1 input-field"
                  placeholder="Enter your email address"
                  required
                />
              </div>
              <button
                type="submit"
                disabled={isResending}
                className="w-full btn-primary disabled:opacity-50"
              >
                {isResending ? 'Sending...' : 'Resend Verification Email'}
              </button>
            </form>
          </div>

          <div className="mt-6 space-y-3">
            <button
              onClick={handleLogout}
              className="w-full btn-secondary"
            >
              Sign Out
            </button>
            
            <div className="text-center">
              <Link
                to="/login"
                className="text-sm text-primary-600 hover:text-primary-500"
              >
                Back to Login
              </Link>
            </div>
          </div>

          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h4 className="text-sm font-medium text-blue-900 mb-2">Need Help?</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Check your spam/junk folder</li>
              <li>• Make sure you entered the correct email address</li>
              <li>• Wait a few minutes for the email to arrive</li>
              <li>• Contact support if you continue to have issues</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
} 