import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  BoltIcon, 
  PlusIcon, 
  CalendarIcon, 
  CheckIcon, 
  XMarkIcon, 
  TrashIcon, 
  PencilIcon,
  EyeSlashIcon,
  ShieldCheckIcon,
  CurrencyDollarIcon,
  UserIcon,
  ClockIcon,
  TrophyIcon
} from '@heroicons/react/24/outline'
import { calloutAPI } from '../services/api'
import { Callout } from '../types'
import { useAuth } from '../contexts/AuthContext'

export default function Callouts() {
  const { user: authUser } = useAuth();
  const queryClient = useQueryClient();
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [locationFilter, setLocationFilter] = useState<string>('all');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Fetch callouts from API
  const { data: calloutsData, isLoading, error: fetchError } = useQuery({
    queryKey: ['callouts', statusFilter, locationFilter],
    queryFn: () => calloutAPI.list().then(res => res.data)
  });

  const callouts = calloutsData?.results || [];

  // Filter callouts by status and location on the frontend
  const filteredCallouts = callouts.filter((callout: Callout) => {
    const statusMatch = statusFilter === 'all' || callout.status === statusFilter;
    const locationMatch = locationFilter === 'all' || callout.location_type === locationFilter;
    return statusMatch && locationMatch;
  });

  // Mutations for CRUD operations
  const acceptMutation = useMutation({
    mutationFn: (calloutId: number) => calloutAPI.accept(calloutId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['callouts'] });
      setSuccess('Callout accepted successfully!');
    },
    onError: (error) => {
      console.error('Error accepting callout:', error);
      setError('Failed to accept callout. Please try again.');
    }
  });

  const declineMutation = useMutation({
    mutationFn: (calloutId: number) => calloutAPI.decline(calloutId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['callouts'] });
      setSuccess('Callout declined successfully!');
    },
    onError: (error) => {
      console.error('Error declining callout:', error);
      setError('Failed to decline callout. Please try again.');
    }
  });

  const deleteMutation = useMutation({
    mutationFn: (calloutId: number) => calloutAPI.delete(calloutId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['callouts'] });
      setShowDeleteConfirm(null);
      setSuccess('Callout deleted successfully!');
    },
    onError: (error) => {
      console.error('Error deleting callout:', error);
      setError('Failed to delete callout. Please try again.');
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

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <ClockIcon className="h-4 w-4" />
      case 'accepted':
        return <CheckIcon className="h-4 w-4" />
      case 'completed':
        return <TrophyIcon className="h-4 w-4" />
      case 'declined':
        return <XMarkIcon className="h-4 w-4" />
      case 'cancelled':
        return <XMarkIcon className="h-4 w-4" />
      default:
        return <ClockIcon className="h-4 w-4" />
    }
  }

  const getRaceTypeIcon = (raceType: string) => {
    switch (raceType) {
      case 'quarter_mile':
        return '🏁'
      case 'eighth_mile':
        return '⚡'
      case 'roll_race':
        return '🔄'
      case 'dig_race':
        return '🚀'
      case 'heads_up':
        return '👥'
      case 'bracket':
        return '🎯'
      default:
        return '🏁'
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

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  }

  const getLocationDisplay = (callout: Callout) => {
    if (callout.location_type === 'track' && callout.track) {
      return {
        type: 'track',
        name: callout.track.name,
        icon: '🏁'
      };
    } else if (callout.location_type === 'street' && callout.street_location) {
      return {
        type: 'street',
        name: callout.street_location,
        icon: '🛣️'
      };
    }
    return {
      type: 'unknown',
      name: 'Location TBD',
      icon: '📍'
    };
  }

  const canManageCallout = (callout: Callout) => {
    if (!authUser) return false;
    return callout.challenger.id === authUser.id || callout.challenged.id === authUser.id;
  }

  const canAcceptDecline = (callout: Callout) => {
    if (!authUser) return false;
    return callout.status === 'pending' && callout.challenged.id === authUser.id;
  }

  const canDelete = (callout: Callout) => {
    if (!authUser) return false;
    return callout.challenger.id === authUser.id && callout.status === 'pending';
  }

  const handleAcceptCallout = (calloutId: number) => {
    acceptMutation.mutate(calloutId);
  };

  const handleDeclineCallout = (calloutId: number) => {
    declineMutation.mutate(calloutId);
  };

  const handleDeleteCallout = (calloutId: number) => {
    deleteMutation.mutate(calloutId);
  };

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

  if (fetchError) {
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

      {/* Success/Error Messages */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center">
          <BoltIcon className="h-5 w-5 mr-2" />
          {error}
        </div>
      )}
      
      {success && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center">
          <BoltIcon className="h-5 w-5 mr-2" />
          {success}
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        <div className="flex space-x-2">
          <span className="text-sm font-medium text-gray-700 self-center">Status:</span>
          {['all', 'pending', 'accepted', 'completed', 'declined', 'cancelled'].map((status) => (
            <button
              key={status}
              onClick={() => setStatusFilter(status)}
              className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                statusFilter === status
                  ? 'bg-primary-100 text-primary-800'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </button>
          ))}
        </div>
        
        <div className="flex space-x-2 ml-4">
          <span className="text-sm font-medium text-gray-700 self-center">Location:</span>
          {['all', 'track', 'street'].map((location) => (
            <button
              key={location}
              onClick={() => setLocationFilter(location)}
              className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                locationFilter === location
                  ? 'bg-primary-100 text-primary-800'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {location.charAt(0).toUpperCase() + location.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Callouts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCallouts.map((callout: Callout) => {
          const location = getLocationDisplay(callout);
          
          return (
            <div key={callout.id} className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
              {/* Callout Header */}
              <div className="p-6 border-b border-gray-100">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center">
                    <BoltIcon className="h-6 w-6 text-primary-600 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900">
                      {callout.challenger.first_name || callout.challenger.username} vs {callout.challenged.first_name || callout.challenged.username}
                    </h3>
                  </div>
                  <div className="flex items-center space-x-2">
                    {/* Privacy Indicator */}
                    {callout.is_private && (
                      <div className="flex items-center text-gray-500" title="Private Callout">
                        <EyeSlashIcon className="h-4 w-4" />
                      </div>
                    )}
                    {callout.is_invite_only && (
                      <div className="flex items-center text-gray-500" title="Invite Only">
                        <ShieldCheckIcon className="h-4 w-4" />
                      </div>
                    )}
                    {/* Status Badge */}
                    <span className={`px-2 py-1 text-xs rounded-full font-medium border ${getStatusColor(callout.status)} flex items-center`}>
                      {getStatusIcon(callout.status)}
                      <span className="ml-1">{callout.status}</span>
                    </span>
                  </div>
                </div>
                
                {/* Race Type */}
                <div className="flex items-center text-sm text-gray-600 mb-2">
                  <span className="mr-2">{getRaceTypeIcon(callout.race_type)}</span>
                  {callout.race_type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </div>
                
                {/* Location */}
                <div className="flex items-center text-sm text-gray-600 mb-2">
                  <span className="mr-2">{location.icon}</span>
                  <span className="truncate">{location.name}</span>
                </div>
                
                {/* Experience Level */}
                {callout.experience_level && (
                  <div className="mb-2">
                    <span className={`px-2 py-1 text-xs rounded-full font-medium ${getExperienceLevelColor(callout.experience_level)}`}>
                      {callout.experience_level.charAt(0).toUpperCase() + callout.experience_level.slice(1)}
                    </span>
                  </div>
                )}
              </div>

              {/* Callout Details */}
              <div className="p-6 space-y-3">
                {/* Horsepower Range */}
                {(callout.min_horsepower || callout.max_horsepower) && (
                  <div className="flex items-center text-sm text-gray-600">
                    <BoltIcon className="h-4 w-4 mr-2 text-gray-400" />
                    <span>
                      {callout.min_horsepower && callout.max_horsepower 
                        ? `${callout.min_horsepower}-${callout.max_horsepower} HP`
                        : callout.min_horsepower 
                          ? `Min ${callout.min_horsepower} HP`
                          : `Max ${callout.max_horsepower} HP`
                      }
                    </span>
                  </div>
                )}
                
                {/* Tire Requirement */}
                {callout.tire_requirement && (
                  <div className="text-sm text-gray-600">
                    <span className="font-medium">Tires:</span> {callout.tire_requirement}
                  </div>
                )}
                
                {/* Wager Amount */}
                {callout.wager_amount > 0 && (
                  <div className="flex items-center text-sm">
                    <CurrencyDollarIcon className="h-4 w-4 mr-2 text-green-600" />
                    <span className="font-semibold text-green-600">${callout.wager_amount}</span>
                    <span className="text-gray-600 ml-1">wager</span>
                  </div>
                )}
                
                {/* Scheduled Date */}
                {callout.scheduled_date && (
                  <div className="flex items-center text-sm text-gray-600">
                    <CalendarIcon className="h-4 w-4 mr-2" />
                    {new Date(callout.scheduled_date).toLocaleDateString()}
                  </div>
                )}
                
                {/* Message */}
                {callout.message && (
                  <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded-lg">
                    "{callout.message}"
                  </p>
                )}
                
                {/* Rules */}
                {callout.rules && (
                  <div className="text-sm text-gray-600">
                    <span className="font-medium">Rules:</span> {callout.rules}
                  </div>
                )}
                
                <div className="text-xs text-gray-500 pt-2 border-t border-gray-100">
                  Created: {formatDate(callout.created_at)}
                </div>
              </div>
              
              {/* Action Buttons */}
              <div className="p-6 pt-0">
                <div className="flex items-center justify-between">
                  <Link
                    to={`/app/callouts/${callout.id}`}
                    className="text-primary-600 hover:text-primary-700 font-medium text-sm flex items-center"
                  >
                    <UserIcon className="h-4 w-4 mr-1" />
                    View Details
                  </Link>
                  
                  {canManageCallout(callout) && (
                    <div className="flex space-x-2">
                      {canAcceptDecline(callout) && (
                        <>
                          <button
                            onClick={() => handleAcceptCallout(callout.id)}
                            disabled={acceptMutation.isPending}
                            className="bg-green-600 text-white p-2 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            title="Accept Callout"
                          >
                            <CheckIcon className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleDeclineCallout(callout.id)}
                            disabled={declineMutation.isPending}
                            className="bg-red-600 text-white p-2 rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            title="Decline Callout"
                          >
                            <XMarkIcon className="h-4 w-4" />
                          </button>
                        </>
                      )}
                      
                      {canDelete(callout) && (
                        <button
                          onClick={() => setShowDeleteConfirm(callout.id)}
                          className="bg-gray-600 text-white p-2 rounded-lg hover:bg-gray-700 transition-colors"
                          title="Delete Callout"
                        >
                          <TrashIcon className="h-4 w-4" />
                        </button>
                      )}
                      
                      {callout.challenger.id === authUser?.id && callout.status === 'pending' && (
                        <Link
                          to={`/app/callouts/${callout.id}/edit`}
                          className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 transition-colors"
                          title="Edit Callout"
                        >
                          <PencilIcon className="h-4 w-4" />
                        </Link>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Empty State */}
      {filteredCallouts.length === 0 && (
        <div className="text-center py-12">
          <BoltIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Callouts Found</h3>
          <p className="text-gray-600 mb-6">
            {statusFilter === 'all' && locationFilter === 'all'
              ? "No callouts have been created yet. Be the first to challenge someone!"
              : `No ${statusFilter !== 'all' ? statusFilter : ''} ${locationFilter !== 'all' ? locationFilter : ''} callouts found.`
            }
          </p>
          {statusFilter === 'all' && locationFilter === 'all' && (
            <Link
              to="/app/callouts/create"
              className="btn-primary inline-flex items-center"
            >
              <PlusIcon className="h-4 w-4 mr-2" />
              Create First Callout
            </Link>
          )}
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Delete Callout</h3>
            <p className="text-gray-600 mb-6">Are you sure you want to delete this callout? This action cannot be undone.</p>
            <div className="flex space-x-3">
              <button
                onClick={() => handleDeleteCallout(showDeleteConfirm)}
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