import { Link } from 'react-router-dom'
import { 
  BoltIcon, 
  TrophyIcon, 
  UsersIcon, 
  MapPinIcon, 
  CalendarIcon, 
  ShoppingBagIcon,
  MagnifyingGlassIcon,
  ShieldCheckIcon,
  CogIcon,
  GlobeAltIcon
} from '@heroicons/react/24/outline'

export default function About() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-secondary-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <img src="/android-chrome-192x192.png" alt="CalloutRacing Logo" className="h-8 w-8" />
              <span className="ml-2 text-lg sm:text-xl font-bold text-gray-900">CalloutRacing</span>
            </div>
            <div className="flex items-center space-x-2 sm:space-x-4">
              <Link
                to="/login"
                className="text-sm sm:text-base text-gray-700 hover:text-primary-600 font-medium px-2 sm:px-3 py-2"
              >
                Login
              </Link>
              <Link
                to="/signup"
                className="btn-primary text-sm sm:text-base px-3 sm:px-4 py-2"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative py-12 sm:py-16 lg:py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          {/* Logo */}
          <div className="mb-6 sm:mb-8">
            <div className="relative mx-auto mb-4">
              <img 
                src="/callourRacingLaunch.jpg" 
                alt="CalloutRacing Launch" 
                className="w-48 h-48 sm:w-64 sm:h-64 md:w-80 md:h-80 lg:w-96 lg:h-96 xl:w-[400px] xl:h-[400px] 2xl:w-[500px] 2xl:h-[500px] mx-auto object-cover rounded-lg shadow-lg transition-all duration-300 ease-in-out"
              />
            </div>
          </div>
          
          <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-4 sm:mb-6">
            The Ultimate
            <span className="text-primary-600 block sm:inline"> Drag Racing Social Network</span>
          </h1>
          <p className="text-lg sm:text-xl text-gray-600 mb-6 sm:mb-8 max-w-3xl mx-auto px-4">
            Connect with racers, challenge opponents, and dominate the track. 
            CalloutRacing is where speed meets community with advanced features for the modern racer.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center px-4">
            <Link to="/signup" className="btn-primary text-base sm:text-lg px-6 sm:px-8 py-3">
              Start Racing
            </Link>
            <Link to="/contact" className="btn-secondary text-base sm:text-lg px-6 sm:px-8 py-3">
              Learn More
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12 sm:py-16 lg:py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-3 sm:mb-4">
              Everything You Need to Race
            </h2>
            <p className="text-lg sm:text-xl text-gray-600 px-4">
              From callouts to events, we've got your racing needs covered with advanced features
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
            {/* Callouts */}
            <div className="card text-center hover:shadow-lg transition-shadow p-6 sm:p-8">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <BoltIcon className="h-6 w-6 sm:h-8 sm:w-8 text-primary-600" />
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">Racing Callouts</h3>
              <p className="text-sm sm:text-base text-gray-600 mb-4">
                Challenge other racers to head-to-head competitions. Set wagers, choose locations, and prove your dominance with confirmation dialogs for safety.
              </p>
              <div className="text-primary-600 font-medium text-sm sm:text-base">Challenge & Conquer</div>
            </div>

            {/* Events */}
            <div className="card text-center hover:shadow-lg transition-shadow p-6 sm:p-8">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CalendarIcon className="h-6 w-6 sm:h-8 sm:w-8 text-secondary-600" />
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">Racing Events</h3>
              <p className="text-sm sm:text-base text-gray-600 mb-4">
                Join organized events, car meets, and test & tune sessions. Create events with detailed confirmation and review processes.
              </p>
              <div className="text-secondary-600 font-medium text-sm sm:text-base">Join the Action</div>
            </div>

            {/* Marketplace */}
            <div className="card text-center hover:shadow-lg transition-shadow p-6 sm:p-8">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-accent-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <ShoppingBagIcon className="h-6 w-6 sm:h-8 sm:w-8 text-accent-600" />
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">Racing Marketplace</h3>
              <p className="text-sm sm:text-base text-gray-600 mb-4">
                Buy, sell, and trade cars, parts, and racing equipment. Find the perfect upgrade for your ride with advanced search capabilities.
              </p>
              <div className="text-accent-600 font-medium text-sm sm:text-base">Buy & Sell</div>
            </div>

            {/* Advanced Search */}
            <div className="card text-center hover:shadow-lg transition-shadow p-6 sm:p-8">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <MagnifyingGlassIcon className="h-6 w-6 sm:h-8 sm:w-8 text-blue-600" />
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">Advanced Search</h3>
              <p className="text-sm sm:text-base text-gray-600 mb-4">
                Find racers, events, tracks, and marketplace items instantly. Global search with filters, real-time results, and smart relevance scoring.
              </p>
              <div className="text-blue-600 font-medium text-sm sm:text-base">Discover Everything</div>
            </div>

            {/* Safety & Confirmation */}
            <div className="card text-center hover:shadow-lg transition-shadow p-6 sm:p-8">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <ShieldCheckIcon className="h-6 w-6 sm:h-8 sm:w-8 text-green-600" />
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">Safety First</h3>
              <p className="text-sm sm:text-base text-gray-600 mb-4">
                Confirmation dialogs ensure you never accidentally create content. Review all details before committing with our smart preview system.
              </p>
              <div className="text-green-600 font-medium text-sm sm:text-base">Safe & Secure</div>
            </div>

            {/* Community */}
            <div className="card text-center hover:shadow-lg transition-shadow p-6 sm:p-8">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <UsersIcon className="h-6 w-6 sm:h-8 sm:w-8 text-primary-600" />
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">Racing Community</h3>
              <p className="text-sm sm:text-base text-gray-600 mb-4">
                Connect with fellow racers, share builds, and build lasting friendships in the racing world with enhanced profile features.
              </p>
              <div className="text-primary-600 font-medium text-sm sm:text-base">Connect & Share</div>
            </div>

            {/* Tracks */}
            <div className="card text-center hover:shadow-lg transition-shadow p-6 sm:p-8">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <MapPinIcon className="h-6 w-6 sm:h-8 sm:w-8 text-secondary-600" />
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">Track Directory</h3>
              <p className="text-sm sm:text-base text-gray-600 mb-4">
                Discover tracks and facilities near you. Get information about surface types, lengths, and contact details with location-based search.
              </p>
              <div className="text-secondary-600 font-medium text-sm sm:text-base">Find Tracks</div>
            </div>

            {/* Achievements */}
            <div className="card text-center hover:shadow-lg transition-shadow p-6 sm:p-8">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-accent-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrophyIcon className="h-6 w-6 sm:h-8 sm:w-8 text-accent-600" />
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">Achievements</h3>
              <p className="text-sm sm:text-base text-gray-600 mb-4">
                Track your racing stats, wins, and achievements. Build your reputation in the racing community with detailed progress tracking.
              </p>
              <div className="text-accent-600 font-medium text-sm sm:text-base">Track Progress</div>
            </div>

            {/* Modern Technology */}
            <div className="card text-center hover:shadow-lg transition-shadow p-6 sm:p-8">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CogIcon className="h-6 w-6 sm:h-8 sm:w-8 text-purple-600" />
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">Modern Technology</h3>
              <p className="text-sm sm:text-base text-gray-600 mb-4">
                Built with React, TypeScript, and modern web technologies. Responsive design, real-time updates, and seamless user experience.
              </p>
              <div className="text-purple-600 font-medium text-sm sm:text-base">Cutting Edge</div>
            </div>

            {/* SSO Authentication */}
            <div className="card text-center hover:shadow-lg transition-shadow p-6 sm:p-8">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <GlobeAltIcon className="h-6 w-6 sm:h-8 sm:w-8 text-orange-600" />
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">Quick Sign-In</h3>
              <p className="text-sm sm:text-base text-gray-600 mb-4">
                Sign in instantly with Google or Facebook. No need to remember passwords - just click and go with secure SSO authentication.
              </p>
              <div className="text-orange-600 font-medium text-sm sm:text-base">One-Click Login</div>
            </div>
          </div>
        </div>
      </section>

      {/* New Features Section */}
      <section className="py-12 sm:py-16 lg:py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-50 to-purple-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-3 sm:mb-4">
              Latest Features & Capabilities
            </h2>
            <p className="text-lg sm:text-xl text-gray-600 px-4">
              Discover what makes CalloutRacing the most advanced racing platform
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Global Search */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center mb-4">
                <MagnifyingGlassIcon className="h-8 w-8 text-blue-600 mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Global Search</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Search across users, events, marketplace items, tracks, and callouts with real-time results and smart filtering.
              </p>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Real-time search results</li>
                <li>• Advanced filtering options</li>
                <li>• Relevance scoring</li>
                <li>• Keyboard navigation</li>
              </ul>
            </div>

            {/* Confirmation Dialogs */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center mb-4">
                <ShieldCheckIcon className="h-8 w-8 text-green-600 mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Smart Confirmations</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Prevent accidental submissions with detailed confirmation dialogs that show data previews before committing.
              </p>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Data preview before submission</li>
                <li>• Formatted display of all fields</li>
                <li>• Loading states during processing</li>
                <li>• Multiple dialog types</li>
              </ul>
            </div>

            {/* Responsive Design */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center mb-4">
                <GlobeAltIcon className="h-8 w-8 text-purple-600 mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Responsive Design</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Optimized for all devices - desktop, tablet, and mobile. Seamless experience across all screen sizes.
              </p>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Mobile-first design</li>
                <li>• Touch-friendly interfaces</li>
                <li>• Adaptive layouts</li>
                <li>• Cross-platform compatibility</li>
              </ul>
            </div>

            {/* Real-time Updates */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center mb-4">
                <BoltIcon className="h-8 w-8 text-yellow-600 mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Real-time Features</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Live updates, instant notifications, and dynamic content that keeps you connected to the racing community.
              </p>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Live search results</li>
                <li>• Instant notifications</li>
                <li>• Dynamic content updates</li>
                <li>• Real-time messaging</li>
              </ul>
            </div>

            {/* Advanced Profiles */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center mb-4">
                <UsersIcon className="h-8 w-8 text-indigo-600 mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Enhanced Profiles</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Detailed racing profiles with stats, achievements, car information, and social features for building your reputation.
              </p>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Racing statistics</li>
                <li>• Achievement tracking</li>
                <li>• Car specifications</li>
                <li>• Social connections</li>
              </ul>
            </div>

            {/* Security & Privacy */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center mb-4">
                <ShieldCheckIcon className="h-8 w-8 text-red-600 mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Security First</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Built with security in mind. Protected user data, secure authentication, and privacy controls for your peace of mind.
              </p>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Secure authentication</li>
                <li>• Data encryption</li>
                <li>• Privacy controls</li>
                <li>• Regular security updates</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 sm:py-16 lg:py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-primary-50 to-secondary-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-8 sm:mb-12">
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-3 sm:mb-4">
              Join the Racing Revolution
            </h2>
            <p className="text-lg sm:text-xl text-gray-600 px-4">
              Thousands of racers are already part of the community
            </p>
          </div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8 text-center">
            <div className="p-4">
              <div className="text-2xl sm:text-3xl lg:text-4xl font-bold text-primary-600 mb-1 sm:mb-2">10K+</div>
              <div className="text-sm sm:text-base text-gray-600">Active Racers</div>
            </div>
            <div className="p-4">
              <div className="text-2xl sm:text-3xl lg:text-4xl font-bold text-secondary-600 mb-1 sm:mb-2">5K+</div>
              <div className="text-sm sm:text-base text-gray-600">Races Completed</div>
            </div>
            <div className="p-4">
              <div className="text-2xl sm:text-3xl lg:text-4xl font-bold text-accent-600 mb-1 sm:mb-2">500+</div>
              <div className="text-sm sm:text-base text-gray-600">Events Hosted</div>
            </div>
            <div className="p-4">
              <div className="text-2xl sm:text-3xl lg:text-4xl font-bold text-primary-600 mb-1 sm:mb-2">100+</div>
              <div className="text-sm sm:text-base text-gray-600">Tracks Listed</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 sm:py-16 lg:py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-3 sm:mb-4">
            Ready to Start Racing?
          </h2>
          <p className="text-lg sm:text-xl text-gray-600 mb-6 sm:mb-8 px-4">
            Join thousands of racers who are already dominating the track with our advanced features
          </p>
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center px-4">
            <Link to="/signup" className="btn-primary text-base sm:text-lg px-6 sm:px-8 py-3">
              Create Account
            </Link>
            <Link to="/contact" className="btn-secondary text-base sm:text-lg px-6 sm:px-8 py-3">
              Contact Us
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 sm:py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6 sm:gap-8">
            <div className="sm:col-span-2 lg:col-span-1">
              <div className="flex items-center mb-4">
                <BoltIcon className="h-6 w-6 sm:h-8 sm:w-8 text-primary-400" />
                <span className="ml-2 text-lg sm:text-xl font-bold">CalloutRacing</span>
              </div>
              <p className="text-sm sm:text-base text-gray-400">
                The ultimate racing social network for speed enthusiasts with advanced features.
              </p>
            </div>
            <div>
              <h3 className="text-base sm:text-lg font-semibold mb-3 sm:mb-4">Features</h3>
              <ul className="space-y-2 text-sm sm:text-base text-gray-400">
                <li><Link to="/app/callouts" className="hover:text-white">Callouts</Link></li>
                <li><Link to="/app/events" className="hover:text-white">Events</Link></li>
                <li><Link to="/app/marketplace" className="hover:text-white">Marketplace</Link></li>
                <li><Link to="/app/tracks" className="hover:text-white">Tracks</Link></li>
                <li><Link to="/app/search" className="hover:text-white">Advanced Search</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="text-base sm:text-lg font-semibold mb-3 sm:mb-4">Company</h3>
              <ul className="space-y-2 text-sm sm:text-base text-gray-400">
                <li><Link to="/about" className="hover:text-white">About</Link></li>
                <li><Link to="/contact" className="hover:text-white">Contact</Link></li>
                <li><Link to="/privacy-policy" className="hover:text-white">Privacy Policy</Link></li>
                <li><Link to="/terms-of-service" className="hover:text-white">Terms of Service</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="text-base sm:text-lg font-semibold mb-3 sm:mb-4">Contact</h3>
              <ul className="space-y-2 text-sm sm:text-base text-gray-400">
                <li><a href="mailto:digibin@digitalbinarysolutionsllc.com" className="hover:text-white break-all">digibin@digitalbinarysolutionsllc.com</a></li>
                <li><a href="tel:+18562126894" className="hover:text-white">(856) 212-6894</a></li>
                <li className="hover:text-white">110 Elizabeth St</li>
                <li className="hover:text-white">Interlachen, FL 32148</li>
              </ul>
            </div>
            <div>
              <h3 className="text-base sm:text-lg font-semibold mb-3 sm:mb-4">Connect</h3>
              <ul className="space-y-2 text-sm sm:text-base text-gray-400">
                <li><a href="#" className="hover:text-white">Discord</a></li>
                <li><a href="#" className="hover:text-white">Instagram</a></li>
                <li><a href="#" className="hover:text-white">YouTube</a></li>
                <li><a href="#" className="hover:text-white">Twitter</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-6 sm:mt-8 pt-6 sm:pt-8 text-center text-sm sm:text-base text-gray-400">
            <p>&copy; 2024 CalloutRacing. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
} 