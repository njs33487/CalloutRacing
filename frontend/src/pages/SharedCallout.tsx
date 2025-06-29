import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { 
  BoltIcon, 
  CalendarIcon, 
  MapPinIcon, 
  CurrencyDollarIcon,
  ArrowLeftIcon,
  TrophyIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline'
import { calloutAPI } from '../services/api'
import { Callout } from '../types'
import { generateCalloutShareData, updateMetaTags } from '../utils/socialSharing'
import ShareButton from '../components/ShareButton'

export default function SharedCallout() {
  const { id } = useParams<{ id: string }>()
  const [shareData, setShareData] = useState<any>(null)

  const { data: callout, isLoading, error } = useQuery({
    queryKey: ['shared-callout', id],
    queryFn: () => calloutAPI.get(parseInt(id!)).then(res => res.data),
    enabled: !!id
  })

  useEffect(() => {
    if (callout) {
      const data = generateCalloutShareData(callout)
      setShareData(data)
      updateMetaTags(data)
    }
  }, [callout])

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'accepted':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'completed':
        return 'bg-blue-100 text-blue-800 border-blue-200'
      case 'declined':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'cancelled':
        return 'bg-gray-100 text-gray-800 border-gray-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getStatusDisplay = (status: string) => {
    switch (status) {
      case 'pending':
        return 'Pending Response'
      case 'accepted':
        return 'Accepted'
      case 'completed':
        return 'Completed'
      case 'declined':
        return 'Declined'
      case 'cancelled':
        return 'Cancelled'
      default:
        return status
    }
  }

  const getRaceTypeDisplay = (raceType: string) => {
    switch (raceType) {
      case 'quarter_mile':
        return 'Quarter Mile'
      case 'eighth_mile':
        return 'Eighth Mile'
      case 'roll_race':
        return 'Roll Race'
      case 'dig_race':
        return 'Dig Race'
      case 'heads_up':
        return 'Heads Up'
      case 'bracket':
        return 'Bracket Race'
      default:
        return raceType.replace('_', ' ').toUpperCase()
    }
  }

  const getExperienceLevelDisplay = (level: string) => {
    switch (level) {
      case 'beginner':
        return 'Beginner'
      case 'intermediate':
        return 'Intermediate'
      case 'experienced':
        return 'Experienced'
      case 'pro':
        return 'Professional'
      default:
        return level
    }
  }

  const getExperienceLevelColor = (level: string) => {
    switch (level) {
      case 'beginner':
        return 'bg-green-100 text-green-800'
      case 'intermediate':
        return 'bg-yellow-100 text-yellow-800'
      case 'experienced':
        return 'bg-orange-100 text-orange-800'
      case 'pro':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getLocationDisplay = (callout: Callout) => {
    if (callout.location_type === 'track' && callout.track) {
      return {
        type: 'track',
        name: callout.track.name,
        location: callout.track.location,
        icon: '🏁'
      };
    } else if (callout.location_type === 'street' && callout.street_location) {
      return {
        type: 'street',
        name: callout.street_location,
        location: 'Street Location',
        icon: '🛣️'
      };
    }
    return {
      type: 'unknown',
      name: 'Location TBD',
      location: 'To be determined',
      icon: '📍'
    };
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-secondary-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (error || !callout) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-secondary-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Callout Not Found</h1>
          <p className="text-gray-600 mb-6">The callout you're looking for doesn't exist or has been removed.</p>
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

  const location = getLocationDisplay(callout)

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

      {/* Callout Content */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          {/* Callout Image */}
          {callout.images && callout.images.length > 0 && (
            <div className="h-64 bg-gray-200 overflow-hidden">
              <img
                src={callout.images[0].image}
                alt="Race Challenge"
                className="w-full h-full object-cover"
              />
            </div>
          )}

          {/* Callout Details */}
          <div className="p-6">
            {/* Status Badge */}
            <div className="mb-4">
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(callout.status)}`}>
                {getStatusDisplay(callout.status)}
              </span>
            </div>

            {/* Race Type Badge */}
            <div className="mb-4">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800 mr-2">
                <BoltIcon className="h-4 w-4 mr-1" />
                {getRaceTypeDisplay(callout.race_type)}
              </span>
              
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getExperienceLevelColor(callout.experience_level)}`}>
                <ShieldCheckIcon className="h-4 w-4 mr-1" />
                {getExperienceLevelDisplay(callout.experience_level)}
              </span>
            </div>

            {/* Title */}
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Race Challenge: {callout.challenger.first_name} {callout.challenger.last_name} vs {callout.challenged.first_name} {callout.challenged.last_name}
            </h1>

            {/* Message */}
            <p className="text-gray-600 mb-6 leading-relaxed">{callout.message}</p>

            {/* Callout Details Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              {/* Date */}
              {callout.scheduled_date && (
                <div className="flex items-start space-x-3">
                  <CalendarIcon className="h-6 w-6 text-gray-400 mt-1" />
                  <div>
                    <h3 className="font-medium text-gray-900">Scheduled Date</h3>
                    <p className="text-gray-600">{formatDate(callout.scheduled_date)}</p>
                  </div>
                </div>
              )}

              {/* Location */}
              <div className="flex items-start space-x-3">
                <MapPinIcon className="h-6 w-6 text-gray-400 mt-1" />
                <div>
                  <h3 className="font-medium text-gray-900">Location</h3>
                  <p className="text-gray-600">{location.name}</p>
                  <p className="text-sm text-gray-500">{location.location}</p>
                </div>
              </div>

              {/* Wager */}
              <div className="flex items-start space-x-3">
                <CurrencyDollarIcon className="h-6 w-6 text-gray-400 mt-1" />
                <div>
                  <h3 className="font-medium text-gray-900">Wager Amount</h3>
                  <p className="text-gray-600">
                    {callout.wager_amount > 0 ? `$${callout.wager_amount}` : 'No wager'}
                  </p>
                </div>
              </div>

              {/* Winner */}
              {callout.winner && (
                <div className="flex items-start space-x-3">
                  <TrophyIcon className="h-6 w-6 text-gray-400 mt-1" />
                  <div>
                    <h3 className="font-medium text-gray-900">Winner</h3>
                    <p className="text-gray-600">
                      {callout.winner.first_name} {callout.winner.last_name}
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Additional Details */}
            <div className="space-y-4 mb-8">
              {/* Rules */}
              {callout.rules && (
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-medium text-gray-900 mb-2">Rules</h3>
                  <p className="text-gray-600">{callout.rules}</p>
                </div>
              )}

              {/* Tire Requirements */}
              {callout.tire_requirement && (
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-medium text-gray-900 mb-2">Tire Requirements</h3>
                  <p className="text-gray-600">{callout.tire_requirement}</p>
                </div>
              )}

              {/* Horsepower Limits */}
              {(callout.min_horsepower || callout.max_horsepower) && (
                <div className="p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-medium text-gray-900 mb-2">Horsepower Limits</h3>
                  <p className="text-gray-600">
                    {callout.min_horsepower && callout.max_horsepower 
                      ? `${callout.min_horsepower} - ${callout.max_horsepower} HP`
                      : callout.min_horsepower 
                        ? `Minimum ${callout.min_horsepower} HP`
                        : `Maximum ${callout.max_horsepower} HP`
                    }
                  </p>
                </div>
              )}
            </div>

            {/* Call to Action */}
            <div className="border-t border-gray-200 pt-6">
              <div className="text-center">
                <p className="text-gray-600 mb-4">
                  Want to join the racing community? Sign up for CalloutRacing to challenge racers!
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