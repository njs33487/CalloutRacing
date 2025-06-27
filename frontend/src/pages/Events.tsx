import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { CalendarIcon, PlusIcon, MapPinIcon, UserGroupIcon } from '@heroicons/react/24/outline'
import { api } from '../services/api'
import { Event } from '../types'

export default function Events() {
  const [eventTypeFilter, setEventTypeFilter] = useState<string>('all');

  // Fetch events from API
  const { data: eventsData, isLoading, error } = useQuery({
    queryKey: ['events', eventTypeFilter],
    queryFn: () => {
      const params = new URLSearchParams();
      if (eventTypeFilter !== 'all') {
        params.append('event_type', eventTypeFilter);
      }
      return api.get(`/events/?${params.toString()}`).then(res => res.data);
    }
  });

  const events = eventsData?.results || [];

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  }

  const getEventTypeColor = (eventType: string) => {
    switch (eventType) {
      case 'race':
        return 'bg-red-100 text-red-800'
      case 'meet':
        return 'bg-blue-100 text-blue-800'
      case 'show':
        return 'bg-purple-100 text-purple-800'
      case 'test':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getEventTypeDisplay = (eventType: string) => {
    switch (eventType) {
      case 'race':
        return 'Race Event'
      case 'meet':
        return 'Car Meet'
      case 'show':
        return 'Car Show'
      case 'test':
        return 'Test & Tune'
      default:
        return eventType
    }
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Events</h1>
            <p className="text-gray-600">Join racing events, car meets, and test & tune sessions</p>
          </div>
          <Link
            to="/app/events/create"
            className="btn-primary inline-flex items-center"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            Create Event
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
            <h1 className="text-3xl font-bold text-gray-900">Events</h1>
            <p className="text-gray-600">Join racing events, car meets, and test & tune sessions</p>
          </div>
          <Link
            to="/app/events/create"
            className="btn-primary inline-flex items-center"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            Create Event
          </Link>
        </div>
        
        <div className="text-center py-12">
          <div className="text-red-600 mb-4">
            <CalendarIcon className="h-12 w-12 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Error Loading Events</h3>
          <p className="text-gray-600">Unable to load events. Please try again later.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Events</h1>
          <p className="text-gray-600">Join racing events, car meets, and test & tune sessions</p>
        </div>
        <Link
          to="/app/events/create"
          className="btn-primary inline-flex items-center"
        >
          <PlusIcon className="h-4 w-4 mr-2" />
          Create Event
        </Link>
      </div>

      {/* Filter */}
      <div className="flex space-x-2">
        {['all', 'race', 'meet', 'show', 'test'].map((type) => (
          <button
            key={type}
            onClick={() => setEventTypeFilter(type)}
            className={`px-3 py-1 rounded-full text-sm font-medium ${
              eventTypeFilter === type
                ? 'bg-primary-100 text-primary-800'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {type === 'all' ? 'All Events' : getEventTypeDisplay(type)}
          </button>
        ))}
      </div>

      {/* Events Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {events.map((event: Event) => (
          <div key={event.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <CalendarIcon className="h-6 w-6 text-primary-600 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">
                  {event.title}
                </h3>
              </div>
              <span className={`px-2 py-1 text-xs rounded-full font-medium ${getEventTypeColor(event.event_type)}`}>
                {getEventTypeDisplay(event.event_type)}
              </span>
            </div>
            
            <div className="space-y-3">
              <div className="flex items-center text-sm text-gray-600">
                <MapPinIcon className="h-4 w-4 mr-2" />
                {event.track.name}
              </div>
              
              <div className="flex items-center text-sm text-gray-600">
                <CalendarIcon className="h-4 w-4 mr-2" />
                {formatDate(event.start_date)} - {formatDate(event.end_date)}
              </div>
              
              {event.max_participants && (
                <div className="flex items-center text-sm text-gray-600">
                  <UserGroupIcon className="h-4 w-4 mr-2" />
                  {event.participants_count || 0}/{event.max_participants} participants
                </div>
              )}
              
              <div className="text-sm">
                <span className="text-gray-600">Entry Fee: </span>
                <span className="font-semibold text-green-600">${event.entry_fee}</span>
              </div>
              
              <p className="text-sm text-gray-700 line-clamp-2">{event.description}</p>
              
              <div className="text-xs text-gray-500">
                Organized by: {event.organizer.first_name || event.organizer.username}
              </div>
            </div>
            
            <div className="mt-4 pt-4 border-t border-gray-200">
              <Link
                to={`/app/events/${event.id}`}
                className="w-full btn-secondary text-sm text-center block"
              >
                View Details
              </Link>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {events.length === 0 && (
        <div className="text-center py-12">
          <CalendarIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {eventTypeFilter === 'all' ? 'No events yet' : `No ${getEventTypeDisplay(eventTypeFilter)} events`}
          </h3>
          <p className="text-gray-600 mb-6">
            {eventTypeFilter === 'all' 
              ? 'Be the first to create an event and bring the racing community together!'
              : `No ${getEventTypeDisplay(eventTypeFilter)} events found.`
            }
          </p>
          {eventTypeFilter === 'all' && (
            <Link
              to="/app/events/create"
              className="btn-primary inline-flex items-center"
            >
              <PlusIcon className="h-4 w-4 mr-2" />
              Create Your First Event
            </Link>
          )}
        </div>
      )}
    </div>
  )
}