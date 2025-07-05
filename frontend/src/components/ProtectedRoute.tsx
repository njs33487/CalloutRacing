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

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  // Check email verification if required
  if (requireEmailVerification && !isEmailVerified) {
    return <Navigate to="/email-verification-required" replace />
  }

  return <>{children}</>
} 