import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { 
  HomeIcon, 
  BoltIcon, 
  CalendarIcon, 
  ShoppingBagIcon, 
  PlusIcon,
  ArrowRightOnRectangleIcon,
  UsersIcon,
  MapPinIcon,
  MagnifyingGlassIcon,
  ChatBubbleLeftRightIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/react/24/outline'
import { useAppDispatch } from '../store/hooks'
import { logout } from '../store/slices/authSlice'
import GlobalSearchBar from './GlobalSearchBar'

const navigation = [
  { name: 'Dashboard', href: '/app', icon: HomeIcon },
  { name: 'Callouts', href: '/app/callouts', icon: BoltIcon },
  { name: 'Events', href: '/app/events', icon: CalendarIcon },
  { name: 'Marketplace', href: '/app/marketplace', icon: ShoppingBagIcon },
  { name: 'Social Feed', href: '/app/social', icon: ChatBubbleLeftRightIcon },
  { name: 'Hot Spots', href: '/app/hotspots', icon: MapPinIcon },
  { name: 'Friends', href: '/app/friends', icon: UsersIcon },
  { name: 'Search', href: '/app/search', icon: MagnifyingGlassIcon },
]

export default function Layout() {
  const location = useLocation()
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleLogout = async () => {
    await dispatch(logout()).unwrap()
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo and Mobile Menu Button */}
            <div className="flex items-center">
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="lg:hidden p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
              >
                {mobileMenuOpen ? (
                  <XMarkIcon className="h-6 w-6" />
                ) : (
                  <Bars3Icon className="h-6 w-6" />
                )}
              </button>
              <Link to="/app" className="flex items-center ml-2 lg:ml-0">
                <img src="/android-chrome-192x192.png" alt="CalloutRacing Logo" className="h-8 w-8 mr-2" />
                <span className="text-lg lg:text-xl font-bold text-gray-900">CalloutRacing</span>
              </Link>
            </div>
            
            {/* Global Search Bar - Hidden on mobile */}
            <div className="hidden md:block flex-1 max-w-md mx-4">
              <GlobalSearchBar />
            </div>
            
            {/* Desktop Actions */}
            <div className="hidden lg:flex items-center space-x-4">
              <Link
                to="/app/callouts/create"
                className="btn-primary flex items-center"
              >
                <PlusIcon className="h-4 w-4 mr-1" />
                New Callout
              </Link>
              <button
                onClick={handleLogout}
                className="text-gray-700 hover:text-red-600 font-medium flex items-center"
              >
                <ArrowRightOnRectangleIcon className="h-4 w-4 mr-1" />
                Logout
              </button>
            </div>

            {/* Mobile Actions */}
            <div className="lg:hidden flex items-center space-x-2">
              <Link
                to="/app/callouts/create"
                className="p-2 text-gray-600 hover:text-gray-900"
                title="New Callout"
              >
                <PlusIcon className="h-5 w-5" />
              </Link>
              <button
                onClick={handleLogout}
                className="p-2 text-gray-600 hover:text-red-600"
                title="Logout"
              >
                <ArrowRightOnRectangleIcon className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Mobile Navigation Overlay */}
        {mobileMenuOpen && (
          <div className="lg:hidden fixed inset-0 z-40">
            <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setMobileMenuOpen(false)} />
            <div className="fixed inset-y-0 left-0 flex w-64 flex-col bg-white shadow-xl">
              <div className="flex h-16 items-center justify-between px-4 border-b border-gray-200">
                <span className="text-lg font-semibold text-gray-900">Menu</span>
                <button
                  onClick={() => setMobileMenuOpen(false)}
                  className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                >
                  <XMarkIcon className="h-6 w-6" />
                </button>
              </div>
              <nav className="flex-1 px-4 py-6 space-y-2">
                {navigation.map((item) => {
                  const isActive = location.pathname === item.href
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      onClick={() => setMobileMenuOpen(false)}
                      className={`flex items-center px-3 py-3 rounded-lg text-base font-medium transition-colors ${
                        isActive
                          ? 'bg-primary-100 text-primary-700'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <item.icon className="h-6 w-6 mr-3" />
                      {item.name}
                    </Link>
                  )
                })}
              </nav>
            </div>
          </div>
        )}

        {/* Desktop Sidebar */}
        <nav className="hidden lg:block w-64 bg-white shadow-sm border-r border-gray-200 min-h-screen">
          <div className="p-4">
            <nav className="space-y-2">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-primary-100 text-primary-700'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <item.icon className="h-5 w-5 mr-3" />
                    {item.name}
                  </Link>
                )
              })}
            </nav>
          </div>
        </nav>

        {/* Main content */}
        <main className="flex-1 p-4 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
} 