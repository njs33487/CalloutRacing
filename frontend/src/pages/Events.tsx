import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { CalendarIcon, PlusIcon, MapPinIcon, UserGroupIcon, TrashIcon, PencilIcon } from '@heroicons/react/24/outline'
import { eventAPI } from '../services/api'
import { Event } from '../types'
import { useAppSelector } from '../store/hooks'
import { generateEventShareData } from '../utils/socialSharing'
import ShareButton from '../components/ShareButton'

export default function Events() {
  const { user: authUser } = useAppSelector((state) => state.auth);
  const queryClient = useQueryClient();
  const [eventTypeFilter, setEventTypeFilter] = useState<string>('all');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Fetch events from API
  const { data: eventsData, isLoading, error: fetchError } = useQuery({
    queryKey: ['events', eventTypeFilter],
    queryFn: () => {
      const params = new URLSearchParams();
      if (eventTypeFilter !== 'all') {
        params.append('event_type', eventTypeFilter);
      }
      return eventAPI.list().then(res => res.data);
    }
  });

  const events = eventsData?.results || [];

  // Mutations for CRUD operations
  const joinMutation = useMutation({
    mutationFn: (eventId: number) => eventAPI.join(eventId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['events'] });
      setSuccess('Successfully joined the event!');
    },
    onError: (error) => {
      console.error('Error joining event:', error);
      setError('Failed to join event. Please try again.');
    }
  });

  const leaveMutation = useMutation({
    mutationFn: (eventId: number) => eventAPI.leave(eventId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['events'] });
      setSuccess('Successfully left the event.');
    },
    onError: (error) => {
      console.error('Error leaving event:', error);
      setError('Failed to leave event. Please try again.');
    }
  });

  const deleteMutation = useMutation({
    mutationFn: (eventId: number) => eventAPI.delete(eventId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['events'] });
      setShowDeleteConfirm(null);
      setSuccess('Event deleted successfully!');
    },
    onError: (error) => {
      console.error('Error deleting event:', error);
      setError('Failed to delete event. Please try again.');
    }
  });

  // Clear messages after 5 seconds
  useState(() => {
    if (error || success) {
      const timer = setTimeout(() => {
        setError(null);
        setSuccess(null);
      }, 5000);
      return () => clearTimeout(timer);
    }
  });

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

  const isEventOrganizer = (event: Event) => {
    return authUser && event.organizer.id === authUser.id;
  };

  const isEventParticipant = (_event: Event) => {
    // Since the Event type doesn't include participants array, we'll use a different approach
    // This would need to be implemented based on the actual API response
    return false; // Placeholder - would need API endpoint to check participation
  };

  const canJoinEvent = (event: Event) => {
    if (!authUser) return false;
    if (isEventOrganizer(event)) return false;
    if (isEventParticipant(event)) return false;
    if (event.max_participants && (event.participants_count || 0) >= event.max_participants) return false;
    return true;
  };

  const canLeaveEvent = (event: Event) => {
    if (!authUser) return false;
    if (isEventOrganizer(event)) return false;
    return isEventParticipant(event);
  };

  const canDeleteEvent = (event: Event) => {
    return isEventOrganizer(event);
  };

  const handleJoinEvent = (eventId: number) => {
    joinMutation.mutate(eventId);
  };

  const handleLeaveEvent = (eventId: number) => {
    leaveMutation.mutate(eventId);
  };

  const handleDeleteEvent = (eventId: number) => {
    deleteMutation.mutate(eventId);
  };

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

  if (fetchError) {
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
      {/* Error/Success Messages */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          </div>
        </div>
      )}

      {success && (
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-green-800">{success}</p>
            </div>
          </div>
        </div>
      )}

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
            {/* Event Image */}
            <div className="mb-4 h-48 bg-gray-100 rounded-lg overflow-hidden">
              {event.images && event.images.length > 0 ? (
                <img
                  src={event.images.find(img => img.is_primary)?.image || event.images[0].image}
                  alt={event.title}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <CalendarIcon className="h-16 w-16 text-gray-400" />
                </div>
              )}
            </div>

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
                Organized by: {event.organizer.first_name} {event.organizer.last_name}
              </div>
            </div>
            
            {/* Action Buttons */}
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex items-center justify-between">
                <Link
                  to={`/app/events/${event.id}`}
                  className="text-primary-600 hover:text-primary-700 font-medium text-sm"
                >
                  View Details
                </Link>
                
                <div className="flex space-x-2">
                  <ShareButton 
                    shareData={generateEventShareData(event)} 
                    size="sm"
                  />
                  
                  {canJoinEvent(event) && (
                    <button
                      onClick={() => handleJoinEvent(event.id)}
                      disabled={joinMutation.isPending}
                      className="bg-green-600 text-white px-3 py-1 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                    >
                      {joinMutation.isPending ? 'Joining...' : 'Join'}
                    </button>
                  )}
                  
                  {canLeaveEvent(event) && (
                    <button
                      onClick={() => handleLeaveEvent(event.id)}
                      disabled={leaveMutation.isPending}
                      className="bg-red-600 text-white px-3 py-1 rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                    >
                      {leaveMutation.isPending ? 'Leaving...' : 'Leave'}
                    </button>
                  )}
                  
                  {isEventParticipant(event) && (
                    <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-lg text-sm">
                      Joined
                    </span>
                  )}
                  
                  {isEventOrganizer(event) && (
                    <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-lg text-sm">
                      Organizer
                    </span>
                  )}
                  
                  {canDeleteEvent(event) && (
                    <button
                      onClick={() => setShowDeleteConfirm(event.id)}
                      className="bg-gray-600 text-white p-2 rounded-lg hover:bg-gray-700"
                      title="Delete Event"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  )}
                  
                  {isEventOrganizer(event) && (
                    <Link
                      to={`/app/events/${event.id}/edit`}
                      className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700"
                      title="Edit Event"
                    >
                      <PencilIcon className="h-4 w-4" />
                    </Link>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {events.length === 0 && (
        <div className="text-center py-12">
          <CalendarIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Events Found</h3>
          <p className="text-gray-600 mb-6">
            {eventTypeFilter === 'all' 
              ? "No events have been created yet. Be the first to organize one!"
              : `No ${eventTypeFilter} events found.`
            }
          </p>
          {eventTypeFilter === 'all' && (
            <Link
              to="/app/events/create"
              className="btn-primary inline-flex items-center"
            >
              <PlusIcon className="h-4 w-4 mr-2" />
              Create First Event
            </Link>
          )}
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Delete Event</h3>
            <p className="text-gray-600 mb-6">Are you sure you want to delete this event? This action cannot be undone.</p>
            <div className="flex space-x-3">
              <button
                onClick={() => handleDeleteEvent(showDeleteConfirm)}
                disabled={deleteMutation.isPending}
                className="flex-1 bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition-colors disabled:opacity-50"
              >
                {deleteMutation.isPending ? 'Deleting...' : 'Delete'}
              </button>
              <button
                onClick={() => setShowDeleteConfirm(null)}
                className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}