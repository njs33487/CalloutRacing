// Main App component - handles routing and authentication context
import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import About from './pages/About'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Contact from './pages/Contact'
import EmailVerification from './pages/EmailVerification'
import TermsOfService from './pages/TermsOfService'
import PrivacyPolicy from './pages/PrivacyPolicy'
import Layout from './components/Layout'
import Home from './pages/Home'
import Callouts from './pages/Callouts'
import Events from './pages/Events'
import Marketplace from './pages/Marketplace'
import Profile from './pages/Profile'
import Friends from './pages/Friends'
import CreateCallout from './pages/CreateCallout'
import CreateEvent from './pages/CreateEvent'
import CreateListing from './pages/CreateListing'
import HotSpots from './pages/HotSpots'
import Search from './pages/Search'

function App() {
  return (
    // Wrap entire app in authentication context
    <AuthProvider>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          {/* Public routes - accessible without authentication */}
          <Route path="/" element={<About />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/verify-email/:token" element={<EmailVerification />} />
          <Route path="/terms-of-service" element={<TermsOfService />} />
          <Route path="/privacy-policy" element={<PrivacyPolicy />} />
          
          {/* Protected routes - require authentication and use shared layout */}
          <Route path="/app" element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }>
            {/* Dashboard and main app pages */}
            <Route index element={<Home />} />
            <Route path="callouts" element={<Callouts />} />
            <Route path="callouts/create" element={<CreateCallout />} />
            <Route path="events" element={<Events />} />
            <Route path="events/create" element={<CreateEvent />} />
            <Route path="marketplace" element={<Marketplace />} />
            <Route path="marketplace/create" element={<CreateListing />} />
            <Route path="profile" element={<Profile />} />
            <Route path="friends" element={<Friends />} />
            <Route path="search" element={<Search />} />
            
            {/* Advanced callout racing features */}
            <Route path="hotspots" element={<HotSpots />} />
          </Route>
        </Routes>
      </div>
    </AuthProvider>
  )
}

export default App 