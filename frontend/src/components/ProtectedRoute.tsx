import { Navigate } from 'react-router-dom'
import { useAppSelector } from '../store/hooks'

interface ProtectedRouteProps {
  children: React.ReactNode
  requireEmailVerification?: boolean
}

export default function ProtectedRoute({ children, requireEmailVerification = true }: ProtectedRouteProps) {
  const { user, isLoading } = useAppSelector((state) => state.auth)
  const isAuthenticated = !!user
  const isEmailVerified = user?.email_verified || false

  console.log('ProtectedRoute - user:', user)
  console.log('ProtectedRoute - isAuthenticated:', isAuthenticated)
  console.log('ProtectedRoute - isEmailVerified:', isEmailVerified)
  console.log('ProtectedRoute - requireEmailVerification:', requireEmailVerification)

  if (isLoading) {
    console.log('ProtectedRoute - showing loading state')
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!isAuthenticated) {
    console.log('ProtectedRoute - user not authenticated, redirecting to login')
    return <Navigate to="/login" replace />
  }

  // Check email verification if required
  if (requireEmailVerification && !isEmailVerified) {
    console.log('ProtectedRoute - email not verified, redirecting to email verification')
    return <Navigate to="/email-verification-required" replace />
  }

  console.log('ProtectedRoute - user authenticated and email verified, showing content')
  return <>{children}</>
} 