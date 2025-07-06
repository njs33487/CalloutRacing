// Main App component - handles routing and Redux store
import { Routes, Route } from 'react-router-dom'
import { Provider } from 'react-redux'
import { store } from './store'
import { ReduxAuthProvider } from './components/ReduxAuthProvider'
import ProtectedRoute from './components/ProtectedRoute'
import ErrorBoundary from './components/ErrorBoundary'
import { Elements } from '@stripe/react-stripe-js'
import { loadStripe } from '@stripe/stripe-js'
import About from './pages/About'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Contact from './pages/Contact'
import EmailVerification from './pages/EmailVerification'
import EmailVerificationRequired from './pages/EmailVerificationRequired'
import TermsOfService from './pages/TermsOfService'
import PrivacyPolicy from './pages/PrivacyPolicy'
import SharedEvent from './pages/SharedEvent'
import SharedCallout from './pages/SharedCallout'
import Layout from './components/Layout'
import Dashboard from './pages/Home'
import Callouts from './pages/Callouts'
import Events from './pages/Events'
import Marketplace from './pages/Marketplace'
import Friends from './pages/Friends'
import SocialFeed from './pages/SocialFeed'
import CreateCallout from './pages/CreateCallout'
import CreateEvent from './pages/CreateEvent'
import CreateListing from './pages/CreateListing'
import HotSpots from './pages/HotSpots'
import Search from './pages/Search'
import ForgotPassword from './pages/ForgotPassword'
import ResetPassword from './pages/ResetPassword'
import ConnectOnboarding from './pages/ConnectOnboarding'
import ConnectOnboardingReturn from './pages/ConnectOnboardingReturn'
import ConnectOnboardingRefresh from './pages/ConnectOnboardingRefresh'
import OtpLogin from './components/OtpLogin'
import SubscriptionPage from './pages/SubscriptionPage'
import MarketplaceCheckoutPage from './pages/MarketplaceCheckoutPage'

// Load Stripe outside of component to avoid recreating on every render
const stripePromise = loadStripe((import.meta as any).env?.VITE_STRIPE_PUBLISHABLE_KEY || 'pk_test_dummy_key')

function App() {
  return (
    // Wrap entire app in error boundary and Redux store
    <ErrorBoundary>
      <Provider store={store}>
        <ReduxAuthProvider>
          <Elements stripe={stripePromise}>
            <div className="min-h-screen bg-gray-50">
            <Routes>
              {/* Public routes - accessible without authentication */}
              <Route path="/" element={<About />} />
              <Route path="/login" element={<Login />} />
              <Route path="/otp-login" element={<OtpLogin />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/verify-email/:token" element={<EmailVerification />} />
              <Route path="/email-verification-required" element={<EmailVerificationRequired />} />
              <Route path="/terms-of-service" element={<TermsOfService />} />
              <Route path="/privacy-policy" element={<PrivacyPolicy />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/reset-password/:token" element={<ResetPassword />} />
              <Route path="/subscription" element={<SubscriptionPage />} />
              
              {/* Shared content routes - public access for social sharing */}
              <Route path="/share/event/:id" element={<SharedEvent />} />
              <Route path="/share/callout/:id" element={<SharedCallout />} />
              
              {/* Connect onboarding routes */}
              <Route path="/connect" element={<ConnectOnboarding />} />
              <Route path="/connect/return/:accountId" element={<ConnectOnboardingReturn />} />
              <Route path="/connect/refresh/:accountId" element={<ConnectOnboardingRefresh />} />
              
              {/* Protected routes - require authentication and use shared layout */}
              <Route path="/app" element={
                <ProtectedRoute>
                  <Layout />
                </ProtectedRoute>
              }>
                {/* Dashboard and main app pages */}
                <Route index element={<Dashboard />} />
                <Route path="callouts" element={<Callouts />} />
                <Route path="callouts/create" element={<CreateCallout />} />
                <Route path="events" element={<Events />} />
                <Route path="events/create" element={<CreateEvent />} />
                <Route path="marketplace" element={<Marketplace />} />
                <Route path="marketplace/create" element={<CreateListing />} />
                <Route path="marketplace/item/:itemId/checkout" element={<MarketplaceCheckoutPage />} />
                <Route path="friends" element={<Friends />} />
                <Route path="social" element={<SocialFeed />} />
                <Route path="search" element={<Search />} />
                
                {/* Advanced callout racing features */}
                <Route path="hotspots" element={<HotSpots />} />
              </Route>
            </Routes>
            </div>
          </Elements>
        </ReduxAuthProvider>
      </Provider>
    </ErrorBoundary>
  )
}

export default App 