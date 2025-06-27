import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { 
  BoltIcon, 
  CalendarIcon, 
  ShoppingBagIcon, 
  UserGroupIcon,
  MapPinIcon,
  TrophyIcon,
  ClockIcon
} from '@heroicons/react/24/outline'
import { api } from '../services/api'
import { useAuth } from '../contexts/AuthContext'

export default function Home() {
  const { user } = useAuth()

  // User-specific data
  const { data: userProfile } = useQuery({
    queryKey: ['user-profile'],
    queryFn: () => api.get('/api/user-profile/'),
    enabled: !!user
  })

  const { data: userCallouts } = useQuery({
    queryKey: ['user-callouts'],
    queryFn: () => api.get('/api/callouts/?challenger=me&challenged=me'),
    enabled: !!user
  })

  const { data: userEvents } = useQuery({
    queryKey: ['user-events'],
    queryFn: () => api.get('/api/events/?participant=me'),
    enabled: !!user
  })

  // General data
  const { data: recentCallouts } = useQuery({
    queryKey: ['recent-callouts'],
    queryFn: () => api.get('/api/callouts/?limit=5')
  })

  const { data: upcomingEvents } = useQuery({
    queryKey: ['upcoming-events'],
    queryFn: () => api.get('/api/events/?is_upcoming=true&limit=5')
  })

  const { data: marketplaceItems } = useQuery({
    queryKey: ['marketplace-items'],
    queryFn: () => api.get('/api/marketplace/?limit=5')
  })

  const { data: stats } = useQuery({
    queryKey: ['stats'],
    queryFn: () => api.get('/api/stats/')
  })

  // User stats
  const userStats = [
    { 
      name: 'My Wins', 
      value: userProfile?.data?.wins || 0, 
      icon: TrophyIcon, 
      color: 'text-yellow-600' 
    },
    { 
      name: 'My Races', 
      value: userProfile?.data?.total_races || 0, 
      icon: BoltIcon, 
      color: 'text-red-600' 
    },
    { 
      name: 'My Events', 
      value: userEvents?.data?.results?.length || 0, 
      icon: CalendarIcon, 
      color: 'text-blue-600' 
    },
    { 
      name: 'Active Callouts', 
      value: userCallouts?.data?.results?.filter((c: any) => c.status === 'pending' || c.status === 'accepted').length || 0, 
      icon: ClockIcon, 
      color: 'text-green-600' 
    },
  ]

  // Global stats
  const globalStats = [
    { name: 'Active Callouts', value: stats?.data?.active_callouts || 0, icon: BoltIcon, color: 'text-red-600' },
    { name: 'Upcoming Events', value: stats?.data?.upcoming_events || 0, icon: CalendarIcon, color: 'text-blue-600' },
    { name: 'Marketplace Items', value: stats?.data?.marketplace_items || 0, icon: ShoppingBagIcon, color: 'text-green-600' },
    { name: 'Total Racers', value: stats?.data?.total_racers || 0, icon: UserGroupIcon, color: 'text-purple-600' },
  ]

  return (
    <div className="space-y-8">
      {/* Personalized Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-lg p-8 text-white">
        <div className="max-w-3xl">
          <h1 className="text-4xl font-bold mb-4">
            {user ? `Welcome back, ${user.first_name || user.username}!` : 'Welcome to CalloutRacing'}
          </h1>
          <p className="text-xl mb-6 text-primary-100">
            {user ? 
              `Ready to race? You have ${userCallouts?.data?.results?.filter((c: any) => c.status === 'pending').length || 0} pending callouts.` :
              'The ultimate drag racing social network. Challenge racers, join events, and buy/sell parts.'
            }
          </p>
          <div className="flex space-x-4">
            <Link
              to="/callouts/create"
              className="bg-white text-primary-600 px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors"
            >
              Create Callout
            </Link>
            <Link
              to="/events"
              className="border border-white text-white px-6 py-3 rounded-lg font-medium hover:bg-white hover:text-primary-600 transition-colors"
            >
              Browse Events
            </Link>
          </div>
        </div>
      </div>

      {/* User Stats (if logged in) */}
      {user && (
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Racing Stats</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {userStats.map((stat) => (
              <div key={stat.name} className="card">
                <div className="flex items-center">
                  <div className={`p-2 rounded-lg bg-gray-100 ${stat.color}`}>
                    <stat.icon className="h-6 w-6" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                    <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Global Stats */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Community Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {globalStats.map((stat) => (
            <div key={stat.name} className="card">
              <div className="flex items-center">
                <div className={`p-2 rounded-lg bg-gray-100 ${stat.color}`}>
                  <stat.icon className="h-6 w-6" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* User-specific sections */}
      {user && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* My Active Callouts */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">My Active Callouts</h2>
              <Link to="/callouts" className="text-primary-600 hover:text-primary-700 text-sm">
                View all
              </Link>
            </div>
            <div className="space-y-3">
              {userCallouts?.data?.results?.filter((c: any) => c.status === 'pending' || c.status === 'accepted').slice(0, 3).map((callout: any) => (
                <div key={callout.id} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                  <BoltIcon className="h-5 w-5 text-primary-600" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">
                      {callout.challenger.username} vs {callout.challenged.username}
                    </p>
                    <p className="text-xs text-gray-500">
                      {callout.race_type} • {callout.location_type}
                    </p>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    callout.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                    callout.status === 'accepted' ? 'bg-green-100 text-green-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {callout.status}
                  </span>
                </div>
              ))}
              {(!userCallouts?.data?.results || userCallouts.data.results.length === 0) && (
                <p className="text-gray-500 text-sm">No active callouts. Create one to get started!</p>
              )}
            </div>
          </div>

          {/* My Upcoming Events */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">My Upcoming Events</h2>
              <Link to="/events" className="text-primary-600 hover:text-primary-700 text-sm">
                View all
              </Link>
            </div>
            <div className="space-y-3">
              {userEvents?.data?.results?.slice(0, 3).map((event: any) => (
                <div key={event.id} className="p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-start space-x-3">
                    <CalendarIcon className="h-5 w-5 text-blue-600 mt-0.5" />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900">{event.title}</p>
                      <p className="text-xs text-gray-500 flex items-center">
                        <MapPinIcon className="h-3 w-3 mr-1" />
                        {event.track?.name}
                      </p>
                      <p className="text-xs text-gray-500">
                        {new Date(event.start_date).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
              {(!userEvents?.data?.results || userEvents.data.results.length === 0) && (
                <p className="text-gray-500 text-sm">No upcoming events. Join one to get started!</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Callouts */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Recent Callouts</h2>
            <Link to="/callouts" className="text-primary-600 hover:text-primary-700 text-sm">
              View all
            </Link>
          </div>
          <div className="space-y-3">
            {recentCallouts?.data?.results?.slice(0, 3).map((callout: any) => (
              <div key={callout.id} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <BoltIcon className="h-5 w-5 text-primary-600" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">
                    {callout.challenger.username} vs {callout.challenged.username}
                  </p>
                  <p className="text-xs text-gray-500">
                    {callout.race_type} • {callout.location_type}
                  </p>
                </div>
                <span className={`px-2 py-1 text-xs rounded-full ${
                  callout.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                  callout.status === 'accepted' ? 'bg-green-100 text-green-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {callout.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Upcoming Events */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Upcoming Events</h2>
            <Link to="/events" className="text-primary-600 hover:text-primary-700 text-sm">
              View all
            </Link>
          </div>
          <div className="space-y-3">
            {upcomingEvents?.data?.results?.slice(0, 3).map((event: any) => (
              <div key={event.id} className="p-3 bg-gray-50 rounded-lg">
                <div className="flex items-start space-x-3">
                  <CalendarIcon className="h-5 w-5 text-blue-600 mt-0.5" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{event.title}</p>
                    <p className="text-xs text-gray-500 flex items-center">
                      <MapPinIcon className="h-3 w-3 mr-1" />
                      {event.track?.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {new Date(event.start_date).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Marketplace */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Marketplace</h2>
            <Link to="/marketplace" className="text-primary-600 hover:text-primary-700 text-sm">
              View all
            </Link>
          </div>
          <div className="space-y-3">
            {marketplaceItems?.data?.results?.slice(0, 3).map((item: any) => (
              <div key={item.id} className="p-3 bg-gray-50 rounded-lg">
                <div className="flex items-start space-x-3">
                  <ShoppingBagIcon className="h-5 w-5 text-green-600 mt-0.5" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{item.title}</p>
                    <p className="text-xs text-gray-500">{item.category}</p>
                    <p className="text-sm font-semibold text-primary-600">
                      ${item.price}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
} 