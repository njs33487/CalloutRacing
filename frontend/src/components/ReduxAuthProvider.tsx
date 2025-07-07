import React, { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { checkAuth } from '../store/slices/authSlice';

interface ReduxAuthProviderProps {
  children: React.ReactNode;
}

export const ReduxAuthProvider: React.FC<ReduxAuthProviderProps> = ({ children }) => {
  const dispatch = useAppDispatch();
  const { isLoading } = useAppSelector((state) => state.auth);

  useEffect(() => {
    console.log('ReduxAuthProvider: Starting auth check');
    
    // Check if there's stored user data before making API calls
    const storedUser = localStorage.getItem('user');
    
    if (storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        console.log('ReduxAuthProvider: Found stored user data:', parsedUser?.id ? 'valid' : 'invalid');
        
        // Only check auth if we have valid user data
        if (parsedUser && parsedUser.id) {
          console.log('ReduxAuthProvider: Dispatching checkAuth');
          dispatch(checkAuth()).catch(error => {
            console.error('ReduxAuthProvider: Auth check failed:', error);
            // Clear invalid data on error
            localStorage.removeItem('user');
          });
        } else {
          console.log('ReduxAuthProvider: Invalid stored data, clearing');
          localStorage.removeItem('user');
        }
      } catch (error) {
        console.error('ReduxAuthProvider: Error parsing stored data:', error);
        localStorage.removeItem('user');
      }
    } else {
      console.log('ReduxAuthProvider: No stored user data, skipping auth check');
    }
  }, [dispatch]);

  // Show loading state while checking authentication
  if (isLoading) {
    console.log('ReduxAuthProvider: Showing loading spinner');
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  console.log('ReduxAuthProvider: Rendering children');
  return <>{children}</>;
}; 