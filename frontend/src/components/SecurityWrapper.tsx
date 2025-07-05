import { useState, useEffect, ReactNode } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAppSelector } from '../store/hooks';

interface SecurityWrapperProps {
  children: ReactNode;
  requireAuth?: boolean;
  fallback?: ReactNode;
}

export default function SecurityWrapper({ 
  children, 
  requireAuth = true,
  fallback 
}: SecurityWrapperProps) {
  const { user, isLoading } = useAppSelector((state) => state.auth);
  const isAuthenticated = !!user;
  const navigate = useNavigate();
  const location = useLocation();
  const [hasError, setHasError] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Handle authentication requirements
  useEffect(() => {
    if (!isLoading && requireAuth && !isAuthenticated) {
      setHasError(true);
      setErrorMessage('Authentication required');
      // Redirect to login after a short delay
      setTimeout(() => {
        navigate('/login', { state: { from: location } });
      }, 2000);
    }
  }, [isAuthenticated, isLoading, requireAuth, navigate, location]);

  // Handle page visibility changes (security measure)
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden) {
        // Page is hidden (user switched tabs/windows)
        // Could implement additional security measures here
        console.log('Page visibility changed - security check');
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  // Handle beforeunload event (warn user about unsaved changes)
  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      // You can customize this message based on form state
      const message = 'You have unsaved changes. Are you sure you want to leave?';
      e.preventDefault();
      e.returnValue = message;
      return message;
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-center">Verifying authentication...</p>
        </div>
      </div>
    );
  }

  // Show error state
  if (hasError) {
    if (fallback) {
      return <>{fallback}</>;
    }

    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-6">
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-yellow-100 mb-4">
              <svg className="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Security Check Required
            </h3>
            
            <p className="text-sm text-gray-600 mb-4">
              {errorMessage || 'Please log in to access this page.'}
            </p>

            <div className="animate-pulse">
              <div className="h-2 bg-gray-200 rounded mb-2"></div>
              <div className="h-2 bg-gray-200 rounded w-3/4 mx-auto"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Render children if all checks pass
  return <>{children}</>;
}

// Specialized security wrapper for forms
export function FormSecurityWrapper({ children }: { children: ReactNode }) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Prevent multiple form submissions
  useEffect(() => {
    // Reset submitting state after a delay
    if (isSubmitting) {
      const timer = setTimeout(() => {
        setIsSubmitting(false);
      }, 5000); // 5 second timeout

      return () => clearTimeout(timer);
    }
  }, [isSubmitting]);

  return (
    <SecurityWrapper>
      <div className={isSubmitting ? 'pointer-events-none opacity-75' : ''}>
        {children}
      </div>
    </SecurityWrapper>
  );
} 