import { Link } from 'react-router-dom'
import { BoltIcon, TrophyIcon, UsersIcon, MapPinIcon, CalendarIcon, ShoppingBagIcon } from '@heroicons/react/24/outline'

export default function About() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-secondary-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <img src="/android-chrome-192x192.png" alt="CalloutRacing Logo" className="h-8 w-8" />
              <span className="ml-2 text-xl font-bold text-gray-900">CalloutRacing</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/login"
                className="text-gray-700 hover:text-primary-600 font-medium"
              >
                Login
              </Link>
              <Link
                to="/signup"
                className="btn-primary"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            The Ultimate
            <span className="text-primary-600"> Drag Racing Social Network</span>
            <br />
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Connect with racers, challenge opponents, and dominate the track. 
            CalloutRacing is where speed meets community.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/signup" className="btn-primary text-lg px-8 py-3">
              Start Racing
            </Link>
            <Link to="/contact" className="btn-secondary text-lg px-8 py-3">
              Learn More
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Everything You Need to Race
            </h2>
            <p className="text-xl text-gray-600">
              From callouts to events, we've got your racing needs covered
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Callouts */}
            <div className="card text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <BoltIcon className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Racing Callouts</h3>
              <p className="text-gray-600 mb-4">
                Challenge other racers to head-to-head competitions. Set wagers, choose locations, and prove your dominance.
              </p>
              <div className="text-primary-600 font-medium">Challenge & Conquer</div>
            </div>

            {/* Events */}
            <div className="card text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CalendarIcon className="h-8 w-8 text-secondary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Racing Events</h3>
              <p className="text-gray-600 mb-4">
                Join organized events, car meets, and test & tune sessions. Connect with the racing community.
              </p>
              <div className="text-secondary-600 font-medium">Join the Action</div>
            </div>

            {/* Marketplace */}
            <div className="card text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-accent-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <ShoppingBagIcon className="h-8 w-8 text-accent-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Racing Marketplace</h3>
              <p className="text-gray-600 mb-4">
                Buy, sell, and trade cars, parts, and racing equipment. Find the perfect upgrade for your ride.
              </p>
              <div className="text-accent-600 font-medium">Buy & Sell</div>
            </div>

            {/* Community */}
            <div className="card text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <UsersIcon className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Racing Community</h3>
              <p className="text-gray-600 mb-4">
                Connect with fellow racers, share builds, and build lasting friendships in the racing world.
              </p>
              <div className="text-primary-600 font-medium">Connect & Share</div>
            </div>

            {/* Tracks */}
            <div className="card text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <MapPinIcon className="h-8 w-8 text-secondary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Track Directory</h3>
              <p className="text-gray-600 mb-4">
                Discover tracks and facilities near you. Get information about surface types, lengths, and contact details.
              </p>
              <div className="text-secondary-600 font-medium">Find Tracks</div>
            </div>

            {/* Achievements */}
            <div className="card text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-accent-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrophyIcon className="h-8 w-8 text-accent-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Achievements</h3>
              <p className="text-gray-600 mb-4">
                Track your racing stats, wins, and achievements. Build your reputation in the racing community.
              </p>
              <div className="text-accent-600 font-medium">Track Progress</div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-primary-50 to-secondary-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Join the Racing Revolution
            </h2>
            <p className="text-xl text-gray-600">
              Thousands of racers are already part of the community
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary-600 mb-2">10K+</div>
              <div className="text-gray-600">Active Racers</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-secondary-600 mb-2">5K+</div>
              <div className="text-gray-600">Races Completed</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-accent-600 mb-2">500+</div>
              <div className="text-gray-600">Events Hosted</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600 mb-2">100+</div>
              <div className="text-gray-600">Tracks Listed</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Ready to Start Racing?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Join thousands of racers who are already dominating the track
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/signup" className="btn-primary text-lg px-8 py-3">
              Create Account
            </Link>
            <Link to="/contact" className="btn-secondary text-lg px-8 py-3">
              Contact Us
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <BoltIcon className="h-8 w-8 text-primary-400" />
                <span className="ml-2 text-xl font-bold">CalloutRacing</span>
              </div>
              <p className="text-gray-400">
                The ultimate racing social network for speed enthusiasts.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Features</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link to="/app/callouts" className="hover:text-white">Callouts</Link></li>
                <li><Link to="/app/events" className="hover:text-white">Events</Link></li>
                <li><Link to="/app/marketplace" className="hover:text-white">Marketplace</Link></li>
                <li><Link to="/app/tracks" className="hover:text-white">Tracks</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link to="/about" className="hover:text-white">About</Link></li>
                <li><Link to="/contact" className="hover:text-white">Contact</Link></li>
                <li><a href="#" className="hover:text-white">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white">Terms of Service</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Contact</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="mailto:digibin@digitalbinarysolutionsllc.com" className="hover:text-white">digibin@digitalbinarysolutionsllc.com</a></li>
                <li><a href="tel:+18562126894" className="hover:text-white">(856) 212-6894</a></li>
                <li className="hover:text-white">110 Elizabeth St</li>
                <li className="hover:text-white">Interlachen, FL 32148</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Connect</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Discord</a></li>
                <li><a href="#" className="hover:text-white">Instagram</a></li>
                <li><a href="#" className="hover:text-white">YouTube</a></li>
                <li><a href="#" className="hover:text-white">Twitter</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 CalloutRacing. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
} 