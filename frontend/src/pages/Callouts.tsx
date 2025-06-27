import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { BoltIcon, PlusIcon, MapPinIcon, CalendarIcon } from '@heroicons/react/24/outline'
import { api } from '../services/api'
import { Callout } from '../types'

export default function Callouts() {
  const [statusFilter, setStatusFilter] = useState<string>('all');

  // Fetch callouts from API
  const { data: calloutsData, isLoading, error } = useQuery({
    queryKey: ['callouts', statusFilter],
    queryFn: () => {
      const params = new URLSearchParams();
      if (statusFilter !== 'all') {
        params.append('status', statusFilter);
      }
      return api.get(`/callouts/?${params.toString()}`).then(res => res.data);
    }
  });

  const callouts = calloutsData?.results || [];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800'
      case 'accepted':
        return 'bg-green-100 text-green-800'
      case 'completed':
        return 'bg-blue-100 text-blue-800'
      case 'declined':
        return 'bg-red-100 text-red-800'
      case 'cancelled':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  }

  const getLocationDisplay = (callout: Callout) => {
    if (callout.location_type === 'track' && callout.track) {
      return callout.track.name;
    } else if (callout.location_type === 'street' && callout.street_location) {
      return callout.street_location;
    }
    return 'Location TBD';
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Callouts</h1>
            <p className="text-gray-600">Challenge other racers to head-to-head competitions</p>
          </div>
          <Link
            to="/app/callouts/create"
            className="btn-primary inline-flex items-center"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            New Callout
          </Link>
        </div>
        
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Callouts</h1>
            <p className="text-gray-600">Challenge other racers to head-to-head competitions</p>
          </div>
          <Link
            to="/app/callouts/create"
            className="btn-primary inline-flex items-center"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            New Callout
          </Link>
        </div>
        
        <div className="text-center py-12">
          <div className="text-red-600 mb-4">
            <BoltIcon className="h-12 w-12 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Error Loading Callouts</h3>
          <p className="text-gray-600">Unable to load callouts. Please try again later.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Callouts</h1>
          <p className="text-gray-600">Challenge other racers to head-to-head competitions</p>
        </div>
        <Link
          to="/app/callouts/create"
          className="btn-primary inline-flex items-center"
        >
          <PlusIcon className="h-4 w-4 mr-2" />
          New Callout
        </Link>
      </div>

      {/* Filter */}
      <div className="flex space-x-2">
        {['all', 'pending', 'accepted', 'completed', 'declined', 'cancelled'].map((status) => (
          <button
            key={status}
            onClick={() => setStatusFilter(status)}
            className={`px-3 py-1 rounded-full text-sm font-medium ${
              statusFilter === status
                ? 'bg-primary-100 text-primary-800'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {status.charAt(0).toUpperCase() + status.slice(1)}
          </button>
        ))}
      </div>

      {/* Callouts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {callouts.map((callout: Callout) => (
          <div key={callout.id} className="card hover:shadow-md transition-shadow">
            {/* Callout Image */}
            <div className="mb-4 h-48 bg-gray-100 rounded-lg overflow-hidden">
              {callout.images && callout.images.length > 0 ? (
                <img
                  src={callout.images.find(img => img.is_primary)?.image || callout.images[0].image}
                  alt="Callout"
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <BoltIcon className="h-16 w-16 text-gray-400" />
                </div>
              )}
            </div>

            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <BoltIcon className="h-6 w-6 text-primary-600 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">
                  {callout.challenger.first_name || callout.challenger.username} vs {callout.challenged.first_name || callout.challenged.username}
                </h3>
              </div>
              <span className={`px-2 py-1 text-xs rounded-full font-medium ${getStatusColor(callout.status)}`}>
                {callout.status}
              </span>
            </div>
            
            <div className="space-y-3">
              <div className="flex items-center text-sm text-gray-600">
                <CalendarIcon className="h-4 w-4 mr-2" />
                {callout.race_type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </div>
              
              <div className="flex items-center text-sm text-gray-600">
                <MapPinIcon className="h-4 w-4 mr-2" />
                {getLocationDisplay(callout)}
              </div>
              
              {callout.wager_amount > 0 && (
                <div className="text-sm">
                  <span className="text-gray-600">Wager: </span>
                  <span className="font-semibold text-green-600">${callout.wager_amount}</span>
                </div>
              )}
              
              {callout.message && (
                <p className="text-sm text-gray-700">{callout.message}</p>
              )}
              
              <div className="text-xs text-gray-500">
                Created: {formatDate(callout.created_at)}
              </div>
            </div>
            
            <div className="mt-4 pt-4 border-t border-gray-200">
              <Link
                to={`/app/callouts/${callout.id}`}
                className="w-full btn-secondary text-sm text-center block"
              >
                View Details
              </Link>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {callouts.length === 0 && (
        <div className="text-center py-12">
          <BoltIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {statusFilter === 'all' ? 'No callouts yet' : `No ${statusFilter} callouts`}
          </h3>
          <p className="text-gray-600 mb-6">
            {statusFilter === 'all' 
              ? 'Be the first to create a callout and challenge other racers!'
              : `No ${statusFilter} callouts found.`
            }
          </p>
          {statusFilter === 'all' && (
            <Link
              to="/app/callouts/create"
              className="btn-primary inline-flex items-center"
            >
              <PlusIcon className="h-4 w-4 mr-2" />
              Create Your First Callout
            </Link>
          )}
        </div>
      )}
    </div>
  )
} 