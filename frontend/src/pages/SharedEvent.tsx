import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { 
  CalendarIcon, 
  MapPinIcon, 
  UserGroupIcon, 
  CurrencyDollarIcon,
  ArrowLeftIcon
} from '@heroicons/react/24/outline'
import { eventAPI } from '../services/api'
import { generateEventShareData, updateMetaTags } from '../utils/socialSharing'
import ShareButton from '../components/ShareButton'

export default function SharedEvent() {
  const { id } = useParams<{ id: string }>()
  const [shareData, setShareData] = useState<any>(null)

  const { data: event, isLoading, error } = useQuery({
    queryKey: ['shared-event', id],
    queryFn: () => eventAPI.get(parseInt(id!)).then(res => res.data),
    enabled: !!id
  })

  useEffect(() => {
    if (event) {
      const data = generateEventShareData(event)
      setShareData(data)
      updateMetaTags(data)
    }
  }, [event])

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  const formatTime = (dateString: string) => {
    return new Date(dateString).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    })
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
      <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-secondary-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (error || !event) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-secondary-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Event Not Found</h1>
          <p className="text-gray-600 mb-6">The event you're looking for doesn't exist or has been removed.</p>
          <Link
            to="/"
            className="btn-primary inline-flex items-center"
          >
            <ArrowLeftIcon className="h-4 w-4 mr-2" />
            Go Home
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-secondary-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link
              to="/"
              className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
            >
              <ArrowLeftIcon className="h-5 w-5 mr-2" />
              Back to CalloutRacing
            </Link>
            
            {shareData && (
              <ShareButton shareData={shareData} />
            )}
          </div>
        </div>
      </div>

      {/* Event Content */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          {/* Event Image */}
          {event.images && event.images.length > 0 && (
            <div className="h-64 bg-gray-200 overflow-hidden">
              <img
                src={event.images[0].image}
                alt={event.title}
                className="w-full h-full object-cover"
              />
            </div>
          )}

          {/* Event Details */}
          <div className="p-6">
            {/* Event Type Badge */}
            <div className="mb-4">
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getEventTypeColor(event.event_type)}`}>
                {getEventTypeDisplay(event.event_type)}
              </span>
            </div>

            {/* Event Title */}
            <h1 className="text-3xl font-bold text-gray-900 mb-4">{event.title}</h1>

            {/* Event Description */}
            <p className="text-gray-600 mb-6 leading-relaxed">{event.description}</p>

            {/* Event Details Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              {/* Date & Time */}
              <div className="flex items-start space-x-3">
                <CalendarIcon className="h-6 w-6 text-gray-400 mt-1" />
                <div>
                  <h3 className="font-medium text-gray-900">Date & Time</h3>
                  <p className="text-gray-600">
                    {formatDate(event.start_date)}
                    {event.start_date !== event.end_date && (
                      <span> - {formatDate(event.end_date)}</span>
                    )}
                  </p>
                  <p className="text-sm text-gray-500">
                    {formatTime(event.start_date)} - {formatTime(event.end_date)}
                  </p>
                </div>
              </div>

              {/* Location */}
              <div className="flex items-start space-x-3">
                <MapPinIcon className="h-6 w-6 text-gray-400 mt-1" />
                <div>
                  <h3 className="font-medium text-gray-900">Location</h3>
                  <p className="text-gray-600">{event.track.name}</p>
                  <p className="text-sm text-gray-500">{event.track.location}</p>
                </div>
              </div>

              {/* Organizer */}
              <div className="flex items-start space-x-3">
                <UserGroupIcon className="h-6 w-6 text-gray-400 mt-1" />
                <div>
                  <h3 className="font-medium text-gray-900">Organizer</h3>
                  <p className="text-gray-600">
                    {event.organizer.first_name} {event.organizer.last_name}
                  </p>
                </div>
              </div>

              {/* Entry Fee */}
              <div className="flex items-start space-x-3">
                <CurrencyDollarIcon className="h-6 w-6 text-gray-400 mt-1" />
                <div>
                  <h3 className="font-medium text-gray-900">Entry Fee</h3>
                  <p className="text-gray-600">
                    {event.entry_fee > 0 ? `$${event.entry_fee}` : 'Free'}
                  </p>
                </div>
              </div>
            </div>

            {/* Additional Info */}
            {event.max_participants && (
              <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                <h3 className="font-medium text-gray-900 mb-2">Participation</h3>
                <p className="text-gray-600">
                  {event.participants_count || 0} of {event.max_participants} participants
                </p>
              </div>
            )}

            {/* Call to Action */}
            <div className="border-t border-gray-200 pt-6">
              <div className="text-center">
                <p className="text-gray-600 mb-4">
                  Want to join this event? Sign up for CalloutRacing to participate!
                </p>
                <div className="space-x-4">
                  <Link
                    to="/signup"
                    className="btn-primary inline-flex items-center"
                  >
                    Sign Up
                  </Link>
                  <Link
                    to="/login"
                    className="btn-secondary inline-flex items-center"
                  >
                    Log In
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 