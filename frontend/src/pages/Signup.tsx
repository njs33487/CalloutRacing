import { useState, useEffect, useCallback } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { 
  EyeIcon, 
  EyeSlashIcon, 
  CheckIcon,
  ChevronRightIcon,
  ChevronLeftIcon,
  CameraIcon
} from '@heroicons/react/24/outline'
import { useAppDispatch, useAppSelector } from '../store/hooks'
import { register } from '../store/slices/authSlice'
import { SSOButtons } from '../components/SSOButtons'
import { authAPI, ensureCSRFToken } from '../services/api'

interface ProfileData {
  bio: string
  location: string
  car_make: string
  car_model: string
  car_year: string
  car_mods: string
  profile_picture?: File
}

export default function Signup() {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const { user, isLoading } = useAppSelector((state) => state.auth)
  
  // Step management
  const [currentStep, setCurrentStep] = useState(1)
  const [totalSteps] = useState(4)
  
  // Account creation data
  const [accountData, setAccountData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    agreeToTerms: false
  })
  
  // Profile creation data
  const [profileData, setProfileData] = useState<ProfileData>({
    bio: '',
    location: '',
    car_make: '',
    car_model: '',
    car_year: '',
    car_mods: ''
  })
  
  // UI states
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [errors, setErrors] = useState<{[key: string]: string}>({})
  const [availability, setAvailability] = useState<{[key: string]: boolean}>({})
  const [checkingAvailability, setCheckingAvailability] = useState<{[key: string]: boolean}>({})

  const [isSubmitting, setIsSubmitting] = useState(false)
  const [csrfInitialized, setCsrfInitialized] = useState(false)

  // Initialize CSRF token on component mount
  useEffect(() => {
    const initializeCSRF = async () => {
      try {
        console.log('Signup: Initializing CSRF token...')
        await ensureCSRFToken()
        setCsrfInitialized(true)
        console.log('Signup: CSRF token initialized')
      } catch (error) {
        console.error('Signup: Failed to initialize CSRF token:', error)
        // Still set as initialized to avoid blocking the form
        setCsrfInitialized(true)
      }
    }
    
    initializeCSRF()
  }, [])

  // Redirect if user is already authenticated
  useEffect(() => {
    if (user) {
      console.log('User is authenticated, redirecting to /app')
      navigate('/app')
    }
  }, [user, navigate])

  // Show loading while checking authentication or initializing CSRF
  if (isLoading || !csrfInitialized) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-secondary-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Initializing...</p>
        </div>
      </div>
    )
  }

  // Don't render signup form if user is already authenticated
  if (user) {
    return null
  }

  // Debounced function to check user availability
  const checkUserAvailability = useCallback(async (field: 'username' | 'email', value: string) => {
    if (!value || value.length < 3) {
      setAvailability(prev => ({ ...prev, [field]: true }))
      return
    }

    // Don't make API calls until CSRF is initialized
    if (!csrfInitialized) {
      console.log('Signup: Skipping availability check - CSRF not initialized')
      return
    }

    setCheckingAvailability(prev => ({ ...prev, [field]: true }))
    
    try {
      console.log(`Signup: Checking ${field} availability for:`, value)
      const response = await authAPI.checkUserExists({ [field]: value })
      setAvailability(prev => ({ ...prev, [field]: !response.data.exists }))
      console.log(`Signup: ${field} availability result:`, response.data)
    } catch (error) {
      console.error(`Error checking ${field} availability:`, error)
      // Don't update availability on error to avoid confusion
    } finally {
      setCheckingAvailability(prev => ({ ...prev, [field]: false }))
    }
  }, [csrfInitialized])

  // Debounced effect for username checking
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (accountData.username) {
        checkUserAvailability('username', accountData.username)
      }
    }, 500)

    return () => clearTimeout(timeoutId)
  }, [accountData.username, checkUserAvailability])

  // Debounced effect for email checking
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (accountData.email) {
        checkUserAvailability('email', accountData.email)
      }
    }, 500)

    return () => clearTimeout(timeoutId)
  }, [accountData.email, checkUserAvailability])

  const validateAccountStep = () => {
    const newErrors: {[key: string]: string} = {}

    // Username validation
    if (!accountData.username) {
      newErrors.username = 'Username is required'
    } else if (accountData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters'
    } else {
      const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
      const isEmail = emailPattern.test(accountData.username)
      
      if (isEmail) {
        if (accountData.username !== accountData.email) {
          newErrors.username = 'If using email as username, it must match the email field'
        }
      } else {
        if (!/^[a-zA-Z0-9_]+$/.test(accountData.username)) {
          newErrors.username = 'Username can only contain letters, numbers, and underscores (or use your email)'
        }
      }
    }

    // Email validation
    if (!accountData.email) {
      newErrors.email = 'Email is required'
    } else if (!/\S+@\S+\.\S+/.test(accountData.email)) {
      newErrors.email = 'Please enter a valid email address'
    }

    // Password validation
    if (!accountData.password) {
      newErrors.password = 'Password is required'
    } else if (accountData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters'
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(accountData.password)) {
      newErrors.password = 'Password must contain at least one uppercase letter, one lowercase letter, and one number'
    }

    // Confirm password validation
    if (!accountData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password'
    } else if (accountData.password !== accountData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match'
    }

    // Name validation
    if (!accountData.firstName) {
      newErrors.firstName = 'First name is required'
    }
    if (!accountData.lastName) {
      newErrors.lastName = 'Last name is required'
    }

    // Terms validation
    if (!accountData.agreeToTerms) {
      newErrors.agreeToTerms = 'You must agree to the terms and conditions'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const validateProfileStep = () => {
    const newErrors: {[key: string]: string} = {}

    if (!profileData.location) {
      newErrors.location = 'Location is required'
    }

    if (!profileData.car_make) {
      newErrors.car_make = 'Car make is required'
    }

    if (!profileData.car_model) {
      newErrors.car_model = 'Car model is required'
    }

    if (!profileData.car_year) {
      newErrors.car_year = 'Car year is required'
    } else {
      const year = parseInt(profileData.car_year)
      if (isNaN(year) || year < 1900 || year > new Date().getFullYear() + 1) {
        newErrors.car_year = 'Please enter a valid year'
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleAccountInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target
    setAccountData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
    // Clear errors when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const handleProfileInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setProfileData(prev => ({
      ...prev,
      [name]: value
    }))
    // Clear errors when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const handleProfilePictureChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setProfileData(prev => ({
        ...prev,
        profile_picture: file
      }))
    }
  }

  const handleNextStep = () => {
    if (currentStep === 1 && !validateAccountStep()) {
      return
    }
    if (currentStep === 2 && !validateProfileStep()) {
      return
    }
    if (currentStep < totalSteps) {
      setCurrentStep(prev => prev + 1)
    }
  }

  const handlePrevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(prev => prev - 1)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateAccountStep() || !validateProfileStep()) {
      return
    }

    setIsSubmitting(true)

    try {
      const response = await dispatch(register({
        username: accountData.username,
        email: accountData.email,
        password: accountData.password,
        first_name: accountData.firstName,
        last_name: accountData.lastName,
      })).unwrap()
      
      // Create profile after successful registration
      if (response.user?.id) {
        try {
          const formData = new FormData()
          formData.append('bio', profileData.bio)
          formData.append('location', profileData.location)
          formData.append('car_make', profileData.car_make)
          formData.append('car_model', profileData.car_model)
          formData.append('car_year', profileData.car_year)
          formData.append('car_mods', profileData.car_mods)
          if (profileData.profile_picture) {
            formData.append('profile_picture', profileData.profile_picture)
          }

          // You'll need to implement this API call
          // await profileAPI.create(formData)
        } catch (profileError) {
          console.error('Error creating profile:', profileError)
        }
      }
      
      setErrors({ 
        success: 'Registration successful! Please check your email to verify your account before logging in.' 
      })
      
      // Clear form data
      setAccountData({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        firstName: '',
        lastName: '',
        agreeToTerms: false
      })
      
      setProfileData({
        bio: '',
        location: '',
        car_make: '',
        car_model: '',
        car_year: '',
        car_mods: ''
      })
      
      setCurrentStep(1)
      
    } catch (error: any) {
      console.error('Registration error:', error)
      setErrors({ general: error.message || 'Registration failed. Please try again.' })
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleSSOSuccess = () => {
    navigate('/app')
  }

  const handleSSOError = (errorMessage: string) => {
    setErrors({ general: errorMessage })
  }

  const getStepTitle = (step: number) => {
    switch (step) {
      case 1: return 'Create Account'
      case 2: return 'Tell Us About You'
      case 3: return 'Your Car'
      case 4: return 'Review & Complete'
      default: return ''
    }
  }

  const getStepDescription = (step: number) => {
    switch (step) {
      case 1: return 'Set up your account credentials'
      case 2: return 'Share your racing background'
      case 3: return 'Tell us about your ride'
      case 4: return 'Review your information and complete registration'
      default: return ''
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-secondary-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-2xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <img src="/android-chrome-192x192.png" alt="CalloutRacing Logo" className="h-10 w-10" />
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-gray-900">
            Join CalloutRacing
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Create your account and start racing
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              Step {currentStep} of {totalSteps}
            </span>
            <span className="text-sm text-gray-500">
              {getStepTitle(currentStep)}
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${(currentStep / totalSteps) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Main Form Container */}
        <div className="bg-white shadow-lg rounded-lg border border-gray-200">
          {/* Step Header */}
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">
              {getStepTitle(currentStep)}
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              {getStepDescription(currentStep)}
            </p>
          </div>

          {/* Error/Success Messages */}
          {(errors.general || errors.success || errors.warning) && (
            <div className="px-6 py-4">
              {errors.general && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm text-red-800">{errors.general}</p>
                    </div>
                  </div>
                </div>
              )}

              {errors.success && (
                <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm text-green-800">{errors.success}</p>
                    </div>
                  </div>
                </div>
              )}

              {errors.warning && (
                <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm text-yellow-800">{errors.warning}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Form Content */}
          <div className="px-6 py-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Step 1: Account Creation */}
              {currentStep === 1 && (
                <div className="space-y-6">
                  {/* Name Fields */}
                  <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                    <div>
                      <label htmlFor="firstName" className="block text-sm font-medium text-gray-700">
                        First Name
                      </label>
                      <div className="mt-1">
                        <input
                          id="firstName"
                          name="firstName"
                          type="text"
                          autoComplete="given-name"
                          required
                          value={accountData.firstName}
                          onChange={handleAccountInputChange}
                          className={`input-field ${errors.firstName ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                          placeholder="John"
                        />
                      </div>
                      {errors.firstName && (
                        <p className="mt-1 text-sm text-red-600">{errors.firstName}</p>
                      )}
                    </div>

                    <div>
                      <label htmlFor="lastName" className="block text-sm font-medium text-gray-700">
                        Last Name
                      </label>
                      <div className="mt-1">
                        <input
                          id="lastName"
                          name="lastName"
                          type="text"
                          autoComplete="family-name"
                          required
                          value={accountData.lastName}
                          onChange={handleAccountInputChange}
                          className={`input-field ${errors.lastName ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                          placeholder="Doe"
                        />
                      </div>
                      {errors.lastName && (
                        <p className="mt-1 text-sm text-red-600">{errors.lastName}</p>
                      )}
                    </div>
                  </div>

                  {/* Username */}
                  <div>
                    <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                      Username or Email
                    </label>
                    <div className="mt-1 relative">
                      <input
                        id="username"
                        name="username"
                        type="text"
                        autoComplete="username"
                        required
                        value={accountData.username}
                        onChange={handleAccountInputChange}
                        className={`input-field pr-10 ${
                          errors.username ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 
                          accountData.username && availability.username === false ? 'border-red-300 focus:ring-red-500 focus:border-red-500' :
                          accountData.username && availability.username === true ? 'border-green-300 focus:ring-green-500 focus:border-green-500' : ''
                        }`}
                        placeholder="Choose a username or use your email"
                      />
                      {accountData.username && (
                        <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                          {checkingAvailability.username ? (
                            <svg className="animate-spin h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                          ) : availability.username === true ? (
                            <CheckIcon className="h-5 w-5 text-green-500" />
                          ) : availability.username === false ? (
                            <svg className="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                            </svg>
                          ) : null}
                        </div>
                      )}
                    </div>
                    <p className="mt-1 text-xs text-gray-500">
                      You can use your email address as your username
                    </p>
                    {errors.username && (
                      <p className="mt-1 text-sm text-red-600">{errors.username}</p>
                    )}
                    {accountData.username && !checkingAvailability.username && availability.username === true && (
                      <p className="mt-1 text-sm text-green-600">✓ Username is available</p>
                    )}
                    {accountData.username && !checkingAvailability.username && availability.username === false && (
                      <p className="mt-1 text-sm text-red-600">✗ Username is already taken</p>
                    )}
                  </div>

                  {/* Email */}
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                      Email Address
                    </label>
                    <div className="mt-1 relative">
                      <input
                        id="email"
                        name="email"
                        type="email"
                        autoComplete="email"
                        required
                        value={accountData.email}
                        onChange={handleAccountInputChange}
                        className={`input-field pr-10 ${
                          errors.email ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 
                          accountData.email && availability.email === false ? 'border-red-300 focus:ring-red-500 focus:border-red-500' :
                          accountData.email && availability.email === true ? 'border-green-300 focus:ring-green-500 focus:border-green-500' : ''
                        }`}
                        placeholder="your@email.com"
                      />
                      {accountData.email && (
                        <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                          {checkingAvailability.email ? (
                            <svg className="animate-spin h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                          ) : availability.email === true ? (
                            <CheckIcon className="h-5 w-5 text-green-500" />
                          ) : availability.email === false ? (
                            <svg className="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                            </svg>
                          ) : null}
                        </div>
                      )}
                    </div>
                    {errors.email && (
                      <p className="mt-1 text-sm text-red-600">{errors.email}</p>
                    )}
                    {accountData.email && !checkingAvailability.email && availability.email === true && (
                      <p className="mt-1 text-sm text-green-600">✓ Email is available</p>
                    )}
                    {accountData.email && !checkingAvailability.email && availability.email === false && (
                      <p className="mt-1 text-sm text-red-600">✗ Email is already registered</p>
                    )}
                  </div>

                  {/* Password */}
                  <div>
                    <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                      Password
                    </label>
                    <div className="mt-1 relative">
                      <input
                        id="password"
                        name="password"
                        type={showPassword ? 'text' : 'password'}
                        autoComplete="new-password"
                        required
                        value={accountData.password}
                        onChange={handleAccountInputChange}
                        className={`input-field pr-10 ${errors.password ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                        placeholder="Create a strong password"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute inset-y-0 right-0 pr-3 flex items-center"
                      >
                        {showPassword ? (
                          <EyeSlashIcon className="h-5 w-5 text-gray-400" />
                        ) : (
                          <EyeIcon className="h-5 w-5 text-gray-400" />
                        )}
                      </button>
                    </div>
                    {errors.password && (
                      <p className="mt-1 text-sm text-red-600">{errors.password}</p>
                    )}
                  </div>

                  {/* Confirm Password */}
                  <div>
                    <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                      Confirm Password
                    </label>
                    <div className="mt-1 relative">
                      <input
                        id="confirmPassword"
                        name="confirmPassword"
                        type={showConfirmPassword ? 'text' : 'password'}
                        autoComplete="new-password"
                        required
                        value={accountData.confirmPassword}
                        onChange={handleAccountInputChange}
                        className={`input-field pr-10 ${errors.confirmPassword ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                        placeholder="Confirm your password"
                      />
                      <button
                        type="button"
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        className="absolute inset-y-0 right-0 pr-3 flex items-center"
                      >
                        {showConfirmPassword ? (
                          <EyeSlashIcon className="h-5 w-5 text-gray-400" />
                        ) : (
                          <EyeIcon className="h-5 w-5 text-gray-400" />
                        )}
                      </button>
                    </div>
                    {errors.confirmPassword && (
                      <p className="mt-1 text-sm text-red-600">{errors.confirmPassword}</p>
                    )}
                  </div>

                  {/* Terms */}
                  <div className="flex items-start">
                    <div className="flex items-center h-5">
                      <input
                        id="agreeToTerms"
                        name="agreeToTerms"
                        type="checkbox"
                        checked={accountData.agreeToTerms}
                        onChange={handleAccountInputChange}
                        className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                      />
                    </div>
                    <div className="ml-3 text-sm">
                      <label htmlFor="agreeToTerms" className="font-medium text-gray-700">
                        I agree to the{' '}
                        <Link to="/terms" className="text-primary-600 hover:text-primary-500">
                          Terms of Service
                        </Link>{' '}
                        and{' '}
                        <Link to="/privacy" className="text-primary-600 hover:text-primary-500">
                          Privacy Policy
                        </Link>
                      </label>
                      {errors.agreeToTerms && (
                        <p className="mt-1 text-sm text-red-600">{errors.agreeToTerms}</p>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Step 2: Basic Profile */}
              {currentStep === 2 && (
                <div className="space-y-6">
                  {/* Profile Picture */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Profile Picture (Optional)
                    </label>
                    <div className="flex items-center space-x-4">
                      <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center">
                        {profileData.profile_picture ? (
                          <img
                            src={URL.createObjectURL(profileData.profile_picture)}
                            alt="Profile preview"
                            className="w-20 h-20 rounded-full object-cover"
                          />
                        ) : (
                          <CameraIcon className="h-8 w-8 text-gray-400" />
                        )}
                      </div>
                      <div>
                        <input
                          type="file"
                          accept="image/*"
                          onChange={handleProfilePictureChange}
                          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
                        />
                        <p className="text-xs text-gray-500 mt-1">
                          Upload a profile picture to personalize your account
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Bio */}
                  <div>
                    <label htmlFor="bio" className="block text-sm font-medium text-gray-700">
                      Bio
                    </label>
                    <div className="mt-1">
                      <textarea
                        id="bio"
                        name="bio"
                        rows={3}
                        value={profileData.bio}
                        onChange={handleProfileInputChange}
                        className="input-field"
                        placeholder="Tell us about yourself and your racing experience..."
                      />
                    </div>
                    <p className="mt-1 text-xs text-gray-500">
                      Share your racing background, experience level, or what you're looking for
                    </p>
                  </div>

                  {/* Location */}
                  <div>
                    <label htmlFor="location" className="block text-sm font-medium text-gray-700">
                      Location *
                    </label>
                    <div className="mt-1">
                      <input
                        id="location"
                        name="location"
                        type="text"
                        required
                        value={profileData.location}
                        onChange={handleProfileInputChange}
                        className={`input-field ${errors.location ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                        placeholder="City, State or Country"
                      />
                    </div>
                    {errors.location && (
                      <p className="mt-1 text-sm text-red-600">{errors.location}</p>
                    )}
                  </div>
                </div>
              )}

              {/* Step 3: Car Information */}
              {currentStep === 3 && (
                <div className="space-y-6">
                  {/* Car Make */}
                  <div>
                    <label htmlFor="car_make" className="block text-sm font-medium text-gray-700">
                      Car Make *
                    </label>
                    <div className="mt-1">
                      <input
                        id="car_make"
                        name="car_make"
                        type="text"
                        required
                        value={profileData.car_make}
                        onChange={handleProfileInputChange}
                        className={`input-field ${errors.car_make ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                        placeholder="e.g., Ford, Chevrolet, Dodge"
                      />
                    </div>
                    {errors.car_make && (
                      <p className="mt-1 text-sm text-red-600">{errors.car_make}</p>
                    )}
                  </div>

                  {/* Car Model */}
                  <div>
                    <label htmlFor="car_model" className="block text-sm font-medium text-gray-700">
                      Car Model *
                    </label>
                    <div className="mt-1">
                      <input
                        id="car_model"
                        name="car_model"
                        type="text"
                        required
                        value={profileData.car_model}
                        onChange={handleProfileInputChange}
                        className={`input-field ${errors.car_model ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                        placeholder="e.g., Mustang, Camaro, Challenger"
                      />
                    </div>
                    {errors.car_model && (
                      <p className="mt-1 text-sm text-red-600">{errors.car_model}</p>
                    )}
                  </div>

                  {/* Car Year */}
                  <div>
                    <label htmlFor="car_year" className="block text-sm font-medium text-gray-700">
                      Car Year *
                    </label>
                    <div className="mt-1">
                      <input
                        id="car_year"
                        name="car_year"
                        type="number"
                        min="1900"
                        max={new Date().getFullYear() + 1}
                        required
                        value={profileData.car_year}
                        onChange={handleProfileInputChange}
                        className={`input-field ${errors.car_year ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                        placeholder="e.g., 2020"
                      />
                    </div>
                    {errors.car_year && (
                      <p className="mt-1 text-sm text-red-600">{errors.car_year}</p>
                    )}
                  </div>

                  {/* Car Modifications */}
                  <div>
                    <label htmlFor="car_mods" className="block text-sm font-medium text-gray-700">
                      Car Modifications
                    </label>
                    <div className="mt-1">
                      <textarea
                        id="car_mods"
                        name="car_mods"
                        rows={3}
                        value={profileData.car_mods}
                        onChange={handleProfileInputChange}
                        className="input-field"
                        placeholder="List your car modifications, engine specs, or performance upgrades..."
                      />
                    </div>
                    <p className="mt-1 text-xs text-gray-500">
                      Optional: Share details about your car's modifications and performance specs
                    </p>
                  </div>
                </div>
              )}

              {/* Step 4: Review */}
              {currentStep === 4 && (
                <div className="space-y-6">
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 mb-4">Review Your Information</h4>
                    
                    {/* Account Info */}
                    <div className="space-y-3">
                      <div>
                        <h5 className="text-sm font-medium text-gray-700">Account Information</h5>
                        <div className="mt-1 text-sm text-gray-600">
                          <p><strong>Name:</strong> {accountData.firstName} {accountData.lastName}</p>
                          <p><strong>Username:</strong> {accountData.username}</p>
                          <p><strong>Email:</strong> {accountData.email}</p>
                        </div>
                      </div>

                      {/* Profile Info */}
                      <div>
                        <h5 className="text-sm font-medium text-gray-700">Profile Information</h5>
                        <div className="mt-1 text-sm text-gray-600">
                          <p><strong>Location:</strong> {profileData.location}</p>
                          <p><strong>Bio:</strong> {profileData.bio || 'Not provided'}</p>
                        </div>
                      </div>

                      {/* Car Info */}
                      <div>
                        <h5 className="text-sm font-medium text-gray-700">Car Information</h5>
                        <div className="mt-1 text-sm text-gray-600">
                          <p><strong>Car:</strong> {profileData.car_year} {profileData.car_make} {profileData.car_model}</p>
                          <p><strong>Modifications:</strong> {profileData.car_mods || 'None specified'}</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="bg-blue-50 rounded-lg p-4">
                    <div className="flex">
                      <div className="flex-shrink-0">
                        <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <div className="ml-3">
                        <h3 className="text-sm font-medium text-blue-800">
                          Almost Done!
                        </h3>
                        <div className="mt-2 text-sm text-blue-700">
                          <p>After registration, you'll receive a verification email. Please check your inbox and click the verification link to activate your account.</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Navigation Buttons */}
              <div className="flex justify-between pt-6">
                <button
                  type="button"
                  onClick={handlePrevStep}
                  disabled={currentStep === 1}
                  className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <ChevronLeftIcon className="h-4 w-4 mr-2" />
                  Previous
                </button>

                {currentStep < totalSteps ? (
                  <button
                    type="button"
                    onClick={handleNextStep}
                    className="flex items-center px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    Next
                    <ChevronRightIcon className="h-4 w-4 ml-2" />
                  </button>
                ) : (
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="flex items-center px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
                  >
                    {isSubmitting ? (
                      <>
                        <svg className="animate-spin -ml-1 mr-3 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Creating Account...
                      </>
                    ) : (
                      'Create Account'
                    )}
                  </button>
                )}
              </div>
            </form>

            {/* SSO Section */}
            <div className="mt-8">
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">Or continue with</span>
                </div>
              </div>

              <div className="mt-6">
                <SSOButtons onSuccess={handleSSOSuccess} onError={handleSSOError} />
              </div>
            </div>
          </div>
        </div>

        {/* Login Link */}
        <div className="mt-8 text-center">
          <p className="text-sm text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="font-medium text-primary-600 hover:text-primary-500">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}