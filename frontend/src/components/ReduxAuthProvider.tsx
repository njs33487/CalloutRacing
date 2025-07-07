import React, { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../store/hooks';
// import { checkAuth } from '../store/slices/authSlice';

interface ReduxAuthProviderProps {
  children: React.ReactNode;
}

export const ReduxAuthProvider: React.FC<ReduxAuthProviderProps> = ({ children }) => {
  const dispatch = useAppDispatch();
  const { isLoading } = useAppSelector((state) => state.auth);

  useEffect(() => {
    // Temporarily disable auth check to test if this is causing the hanging
    console.log('ReduxAuthProvider: Skipping auth check for testing');
    /*
    // Check if there's stored user data before making API calls
    const storedUser = localStorage.getItem('user');
    
    if (storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        // Only check auth if we have valid user data
        if (parsedUser && parsedUser.id) {
          dispatch(checkAuth());
        } else {
          // Invalid stored data, clear it and don't make API call
          localStorage.removeItem('user');
        }
      } catch (error) {
        // Invalid stored data, clear it and don't make API call
        localStorage.removeItem('user');
      }
    }
    // If no stored user data, don't make any API calls - user is not authenticated
    */
  }, [dispatch]);

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return <>{children}</>;
}; 