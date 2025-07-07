// Authentication Context - manages user authentication state across the app
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { authAPI, ensureCSRFToken } from '../services/api'

// User data structure
interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  email_verified: boolean
  subscription_status?: 'active' | 'inactive' | 'cancelled'
  subscription_type?: 'basic' | 'pro' | 'premium'
}

// Authentication context interface - defines available methods and state
interface AuthContextType {
  user: User | null
  login: (username: string, password: string) => Promise<void>
  register: (userData: any) => Promise<any>
  googleLogin: (idToken: string) => Promise<void>
  facebookLogin: (accessToken: string) => Promise<void>
  logout: () => void
  isLoading: boolean
  isAuthenticated: boolean
  isEmailVerified: boolean
  hasActiveSubscription: boolean
  subscriptionType?: 'basic' | 'pro' | 'premium'
}

// Create the authentication context
const AuthContext = createContext<AuthContextType | undefined>(undefined)

// Custom hook to use authentication context with error handling
export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

// Main authentication provider component
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  // State for user data and loading status
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Check for existing authentication on app startup
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        // Check if there's stored user data first
        const storedUser = localStorage.getItem('user')
        
        if (storedUser) {
          try {
            // Verify the stored data is valid JSON
            const parsedUser = JSON.parse(storedUser)
            
            // Only call profile API if we have valid user data with an ID
            if (parsedUser && parsedUser.id) {
              // Set user immediately from stored data for faster UI
              setUser(parsedUser)
              
              // Then verify the session is still valid in the background
              try {
                const response = await authAPI.profile()
                // Update with fresh data from server
                setUser(response.data)
                localStorage.setItem('user', JSON.stringify(response.data))
              } catch (error: any) {
                // Session expired or invalid, clear stored data
                console.log('Session expired, clearing stored user data')
                localStorage.removeItem('user')
                setUser(null)
              }
            } else {
              // Invalid user data, clear it
              localStorage.removeItem('user')
              setUser(null)
            }
          } catch (error) {
            // Invalid stored data, clear it
            localStorage.removeItem('user')
            setUser(null)
          }
        } else {
          // No stored user data, user is not authenticated
          setUser(null)
        }
      } catch (error) {
        console.error('Error initializing auth:', error)
        setUser(null)
      } finally {
        setIsLoading(false)
      }
    }

    initializeAuth()
  }, [])

  // Login function - authenticates user and stores user data
  const login = async (username: string, password: string) => {
    await ensureCSRFToken();
    const response = await authAPI.login({ username, password })
    const { user: newUser } = response.data
    
    // Update state and store in localStorage
    setUser(newUser)
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  // Register function - creates new user account and logs them in
  const register = async (userData: any) => {
    await ensureCSRFToken();
    const response = await authAPI.register(userData)
    return response
  }

  // Google SSO login function
  const googleLogin = async (idToken: string) => {
    const response = await authAPI.googleSSO(idToken)
    const { user: newUser } = response.data
    
    // Update state and store in localStorage
    setUser(newUser)
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  // Facebook SSO login function
  const facebookLogin = async (accessToken: string) => {
    const response = await authAPI.facebookSSO(accessToken)
    const { user: newUser } = response.data
    
    // Update state and store in localStorage
    setUser(newUser)
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  // Logout function - clears authentication data and notifies server
  const logout = async () => {
    try {
      await authAPI.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Always clear local authentication data
      setUser(null)
      localStorage.removeItem('user')
    }
  }

  // Context value object with all authentication methods and state
  const value: AuthContextType = {
    user,
    login,
    register,
    googleLogin,
    facebookLogin,
    logout,
    isLoading,
    isAuthenticated: !!user,
    isEmailVerified: !!user?.email_verified,
    hasActiveSubscription: user?.subscription_status === 'active',
    subscriptionType: user?.subscription_type,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
} 