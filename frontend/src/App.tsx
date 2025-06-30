// Main App component - handles routing and authentication context
import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import ErrorBoundary from './components/ErrorBoundary'
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
import CreateCallout from './pages/CreateCallout'
import CreateEvent from './pages/CreateEvent'
import CreateListing from './pages/CreateListing'
import HotSpots from './pages/HotSpots'
import Search from './pages/Search'
import ForgotPassword from './pages/ForgotPassword'
import ResetPassword from './pages/ResetPassword'

function App() {
  return (
    // Wrap entire app in error boundary and authentication context
    <ErrorBoundary>
      <AuthProvider>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            {/* Public routes - accessible without authentication */}
            <Route path="/" element={<About />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/verify-email/:token" element={<EmailVerification />} />
            <Route path="/email-verification-required" element={<EmailVerificationRequired />} />
            <Route path="/terms-of-service" element={<TermsOfService />} />
            <Route path="/privacy-policy" element={<PrivacyPolicy />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password/:token" element={<ResetPassword />} />
            
            {/* Shared content routes - public access for social sharing */}
            <Route path="/share/event/:id" element={<SharedEvent />} />
            <Route path="/share/callout/:id" element={<SharedCallout />} />
            
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
              <Route path="friends" element={<Friends />} />
              <Route path="search" element={<Search />} />
              
              {/* Advanced callout racing features */}
              <Route path="hotspots" element={<HotSpots />} />
            </Route>
          </Routes>
        </div>
      </AuthProvider>
    </ErrorBoundary>
  )
}

export default App 