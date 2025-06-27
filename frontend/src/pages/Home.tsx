import { useQuery } from 'react-query'
import { Link } from 'react-router-dom'
import { 
  BoltIcon, 
  CalendarIcon, 
  ShoppingBagIcon, 
  UserGroupIcon,
  MapPinIcon
} from '@heroicons/react/24/outline'
import { api } from '../services/api'

export default function Home() {
  const { data: recentCallouts } = useQuery('recent-callouts', () =>
    api.get('/api/callouts/?limit=5')
  )

  const { data: upcomingEvents } = useQuery('upcoming-events', () =>
    api.get('/api/events/?is_upcoming=true&limit=5')
  )

  const { data: marketplaceItems } = useQuery('marketplace-items', () =>
    api.get('/api/marketplace/?limit=5')
  )

  const stats = [
    { name: 'Active Callouts', value: '12', icon: BoltIcon, color: 'text-red-600' },
    { name: 'Upcoming Events', value: '8', icon: CalendarIcon, color: 'text-blue-600' },
    { name: 'Marketplace Items', value: '45', icon: ShoppingBagIcon, color: 'text-green-600' },
    { name: 'Total Racers', value: '156', icon: UserGroupIcon, color: 'text-purple-600' },
  ]

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-lg p-8 text-white">
        <div className="max-w-3xl">
          <h1 className="text-4xl font-bold mb-4">
            Welcome to CalloutRacing
          </h1>
          <p className="text-xl mb-6 text-primary-100">
            The ultimate drag racing social network. Challenge racers, join events, and buy/sell parts.
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

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
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