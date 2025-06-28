import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom'
import { 
  HomeIcon, 
  BoltIcon, 
  CalendarIcon, 
  ShoppingBagIcon, 
  UserIcon,
  PlusIcon,
  ArrowRightOnRectangleIcon,
  UsersIcon,
  MapPinIcon
} from '@heroicons/react/24/outline'
import { useAuth } from '../contexts/AuthContext'

const navigation = [
  { name: 'Dashboard', href: '/app', icon: HomeIcon },
  { name: 'Callouts', href: '/app/callouts', icon: BoltIcon },
  { name: 'Events', href: '/app/events', icon: CalendarIcon },
  { name: 'Marketplace', href: '/app/marketplace', icon: ShoppingBagIcon },
  { name: 'Hot Spots', href: '/app/hotspots', icon: MapPinIcon },
  { name: 'Friends', href: '/app/friends', icon: UsersIcon },
  { name: 'Profile', href: '/app/profile', icon: UserIcon },
]

export default function Layout() {
  const location = useLocation()
  const navigate = useNavigate()
  const { logout } = useAuth()

  const handleLogout = async () => {
    await logout()
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link to="/app" className="flex items-center">
                <img src="/android-chrome-192x192.png" alt="CalloutRacing Logo" className="h-8 w-8 mr-2" />
                <span className="ml-2 text-xl font-bold text-gray-900">CalloutRacing</span>
              </Link>
            </div>
            
            <div className="flex items-center space-x-4">
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
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <nav className="w-64 bg-white shadow-sm border-r border-gray-200 min-h-screen">
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
        <main className="flex-1 p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
} 