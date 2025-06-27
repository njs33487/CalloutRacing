// Authentication Context - manages user authentication state across the app
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { authAPI } from '../services/api'

// User data structure
interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
}

// Authentication context interface - defines available methods and state
interface AuthContextType {
  user: User | null
  token: string | null
  login: (username: string, password: string) => Promise<void>
  register: (userData: any) => Promise<void>
  logout: () => void
  isLoading: boolean
  isAuthenticated: boolean
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
  // State for user data, authentication token, and loading status
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Check for existing authentication on app startup
  useEffect(() => {
    // Retrieve stored authentication data from localStorage
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      setToken(storedToken)
      setUser(JSON.parse(storedUser))
      
      // Verify the stored token is still valid with the server
      authAPI.profile()
        .then(response => {
          setUser(response.data)
        })
        .catch(() => {
          // Token is invalid, clear all stored authentication data
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          setToken(null)
          setUser(null)
        })
        .finally(() => {
          setIsLoading(false)
        })
    } else {
      setIsLoading(false)
    }
  }, [])

  // Login function - authenticates user and stores credentials
  const login = async (username: string, password: string) => {
    const response = await authAPI.login({ username, password })
    const { token: newToken, user: newUser } = response.data
    
    // Update state and store in localStorage
    setToken(newToken)
    setUser(newUser)
    localStorage.setItem('token', newToken)
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  // Register function - creates new user account and logs them in
  const register = async (userData: any) => {
    const response = await authAPI.register(userData)
    const { token: newToken, user: newUser } = response.data
    
    // Update state and store in localStorage
    setToken(newToken)
    setUser(newUser)
    localStorage.setItem('token', newToken)
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
      setToken(null)
      setUser(null)
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }

  // Context value object with all authentication methods and state
  const value: AuthContextType = {
    user,
    token,
    login,
    register,
    logout,
    isLoading,
    isAuthenticated: !!token && !!user
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
} 