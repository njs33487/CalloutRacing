import { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  BoltIcon, 
  CalendarIcon, 
  ShoppingBagIcon, 
  UserGroupIcon,
  MapPinIcon,
  PhoneIcon,
  EnvelopeIcon,
  ArrowRightIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'

export default function Landing() {
  const [activeTab, setActiveTab] = useState<'login' | 'register'>('login')
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle form submission
    console.log('Form submitted:', formData)
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const features = [
    {
      icon: BoltIcon,
      title: 'Race Callouts',
      description: 'Challenge other racers to head-to-head competitions on track or street.'
    },
    {
      icon: CalendarIcon,
      title: 'Events & Meets',
      description: 'Join organized racing events, car meets, and test & tune sessions.'
    },
    {
      icon: ShoppingBagIcon,
      title: 'Marketplace',
      description: 'Buy, sell, and trade cars, parts, and racing equipment.'
    },
    {
      icon: UserGroupIcon,
      title: 'Racing Community',
      description: 'Connect with fellow racers, share builds, and track your racing stats.'
    }
  ]

  const stats = [
    { number: '10,000+', label: 'Active Racers' },
    { number: '500+', label: 'Events Hosted' },
    { number: '25,000+', label: 'Races Completed' },
    { number: '50+', label: 'Tracks Partnered' }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <BoltIcon className="h-8 w-8 text-primary-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">CalloutRacing</span>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setActiveTab('login')}
                className="text-gray-700 hover:text-primary-600 font-medium"
              >
                Login
              </button>
              <button
                onClick={() => setActiveTab('register')}
                className="btn-primary"
              >
                Sign Up
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-5xl font-bold mb-6">
                The Ultimate Drag Racing Social Network
              </h1>
              <p className="text-xl mb-8 text-primary-100">
                Challenge racers, join events, buy/sell parts, and build your racing legacy. 
                Where speed meets community.
              </p>
              <div className="flex space-x-4">
                <button
                  onClick={() => setActiveTab('register')}
                  className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
                >
                  Get Started
                </button>
                <Link
                  to="/about"
                  className="border border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary-600 transition-colors"
                >
                  Learn More
                </Link>
              </div>
            </div>
            <div className="relative">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-8">
                <h2 className="text-2xl font-bold mb-6">
                  {activeTab === 'login' ? 'Welcome Back' : 'Join the Community'}
                </h2>
                
                {/* Tab Navigation */}
                <div className="flex mb-6">
                  <button
                    onClick={() => setActiveTab('login')}
                    className={`flex-1 py-2 text-center font-medium border-b-2 ${
                      activeTab === 'login' 
                        ? 'border-white text-white' 
                        : 'border-transparent text-primary-200 hover:text-white'
                    }`}
                  >
                    Login
                  </button>
                  <button
                    onClick={() => setActiveTab('register')}
                    className={`flex-1 py-2 text-center font-medium border-b-2 ${
                      activeTab === 'register' 
                        ? 'border-white text-white' 
                        : 'border-transparent text-primary-200 hover:text-white'
                    }`}
                  >
                    Register
                  </button>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <input
                      type="text"
                      name="username"
                      placeholder="Username"
                      value={formData.username}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50"
                      required
                    />
                  </div>
                  
                  {activeTab === 'register' && (
                    <div>
                      <input
                        type="email"
                        name="email"
                        placeholder="Email"
                        value={formData.email}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50"
                        required
                      />
                    </div>
                  )}
                  
                  <div>
                    <input
                      type="password"
                      name="password"
                      placeholder="Password"
                      value={formData.password}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50"
                      required
                    />
                  </div>
                  
                  {activeTab === 'register' && (
                    <div>
                      <input
                        type="password"
                        name="confirmPassword"
                        placeholder="Confirm Password"
                        value={formData.confirmPassword}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50"
                        required
                      />
                    </div>
                  )}
                  
                  <button
                    type="submit"
                    className="w-full bg-white text-primary-600 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
                  >
                    {activeTab === 'login' ? 'Sign In' : 'Create Account'}
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Everything You Need to Race
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              CalloutRacing provides all the tools and community features you need to take your racing to the next level.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature) => (
              <div key={feature.title} className="text-center">
                <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <feature.icon className="h-8 w-8 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">
              Racing by the Numbers
            </h2>
            <p className="text-xl text-gray-300">
              Join thousands of racers who trust CalloutRacing
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-4xl font-bold text-primary-400 mb-2">
                  {stat.number}
                </div>
                <div className="text-gray-300">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                About CalloutRacing
              </h2>
              <p className="text-lg text-gray-600 mb-6">
                CalloutRacing was born from a simple idea: racing is better when you're part of a community. 
                We've built the ultimate platform where drag racers can connect, compete, and grow together.
              </p>
              <p className="text-lg text-gray-600 mb-8">
                Whether you're a seasoned pro or just getting started, our platform provides everything you need 
                to take your racing to the next level. From organizing callouts to finding the perfect parts, 
                we're here to fuel your passion for speed.
              </p>
              <div className="space-y-4">
                <div className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">Secure and reliable platform</span>
                </div>
                <div className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">Active community of racers</span>
                </div>
                <div className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">Professional event organization</span>
                </div>
              </div>
            </div>
            <div className="bg-gray-100 rounded-lg p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">
                Our Mission
              </h3>
              <p className="text-gray-600 mb-6">
                To create the world's most comprehensive drag racing community platform, 
                connecting racers worldwide and providing the tools they need to succeed.
              </p>
              <div className="bg-primary-50 border-l-4 border-primary-500 p-4">
                <p className="text-primary-800 font-medium">
                  "Racing isn't just about speed—it's about the people, the community, and the passion that drives us all."
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Get in Touch
            </h2>
            <p className="text-xl text-gray-600">
              Have questions? We'd love to hear from you.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <EnvelopeIcon className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Email Us</h3>
              <p className="text-gray-600 mb-2">support@calloutracing.com</p>
              <p className="text-gray-600">info@calloutracing.com</p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <PhoneIcon className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Call Us</h3>
              <p className="text-gray-600 mb-2">+1 (555) 123-4567</p>
              <p className="text-gray-600">Mon-Fri 9AM-6PM EST</p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <MapPinIcon className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Visit Us</h3>
              <p className="text-gray-600 mb-2">123 Racing Street</p>
              <p className="text-gray-600">Speed City, SC 12345</p>
            </div>
          </div>
          
          <div className="mt-12 text-center">
            <button className="btn-primary inline-flex items-center">
              Contact Support
              <ArrowRightIcon className="h-4 w-4 ml-2" />
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <BoltIcon className="h-8 w-8 text-primary-600" />
                <span className="ml-2 text-xl font-bold">CalloutRacing</span>
              </div>
              <p className="text-gray-400">
                The ultimate drag racing social network.
              </p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Platform</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link to="/callouts" className="hover:text-white">Callouts</Link></li>
                <li><Link to="/events" className="hover:text-white">Events</Link></li>
                <li><Link to="/marketplace" className="hover:text-white">Marketplace</Link></li>
                <li><Link to="/profile" className="hover:text-white">Profile</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Help Center</a></li>
                <li><Link to="/contact" className="hover:text-white">Contact Us</Link></li>
                <li><Link to="/privacy-policy" className="hover:text-white">Privacy Policy</Link></li>
                <li><Link to="/terms-of-service" className="hover:text-white">Terms of Service</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Connect</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Facebook</a></li>
                <li><a href="#" className="hover:text-white">Twitter</a></li>
                <li><a href="#" className="hover:text-white">Instagram</a></li>
                <li><a href="#" className="hover:text-white">YouTube</a></li>
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