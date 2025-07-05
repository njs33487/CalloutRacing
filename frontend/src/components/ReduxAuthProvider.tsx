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
    // Check authentication status on app startup
    dispatch(checkAuth());
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