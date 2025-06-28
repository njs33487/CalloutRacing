import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { BoltIcon, PlusIcon, MapPinIcon, CalendarIcon, CheckIcon, XMarkIcon, TrashIcon, PencilIcon } from '@heroicons/react/24/outline'
import { calloutAPI } from '../services/api'
import { Callout } from '../types'
import { useAuth } from '../contexts/AuthContext'

export default function Callouts() {
  const { user: authUser } = useAuth();
  const queryClient = useQueryClient();
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [selectedCallout, setSelectedCallout] = useState<Callout | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Fetch callouts from API
  const { data: calloutsData, isLoading, error: fetchError } = useQuery({
    queryKey: ['callouts', statusFilter],
    queryFn: () => calloutAPI.list().then(res => res.data)
  });

  const callouts = calloutsData?.results || [];

  // Filter callouts by status on the frontend
  const filteredCallouts = statusFilter === 'all' 
    ? callouts 
    : callouts.filter((callout: Callout) => callout.status === statusFilter);

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
        {filteredCallouts.map((callout: Callout) => (
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
            
            {/* Action Buttons */}
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex items-center justify-between">
                <Link
                  to={`/app/callouts/${callout.id}`}
                  className="text-primary-600 hover:text-primary-700 font-medium text-sm"
                >
                  View Details
                </Link>
                
                {canManageCallout(callout) && (
                  <div className="flex space-x-2">
                    {canAcceptDecline(callout) && (
                      <>
                        <button
                          onClick={() => handleAcceptCallout(callout.id)}
                          disabled={acceptMutation.isPending}
                          className="bg-green-600 text-white p-2 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                          title="Accept Callout"
                        >
                          <CheckIcon className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDeclineCallout(callout.id)}
                          disabled={declineMutation.isPending}
                          className="bg-red-600 text-white p-2 rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
                          title="Decline Callout"
                        >
                          <XMarkIcon className="h-4 w-4" />
                        </button>
                      </>
                    )}
                    
                    {canDelete(callout) && (
                      <button
                        onClick={() => setShowDeleteConfirm(callout.id)}
                        className="bg-gray-600 text-white p-2 rounded-lg hover:bg-gray-700"
                        title="Delete Callout"
                      >
                        <TrashIcon className="h-4 w-4" />
                      </button>
                    )}
                    
                    {callout.challenger.id === authUser?.id && callout.status === 'pending' && (
                      <Link
                        to={`/app/callouts/${callout.id}/edit`}
                        className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700"
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
        ))}
      </div>

      {/* Empty State */}
      {filteredCallouts.length === 0 && (
        <div className="text-center py-12">
          <BoltIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Callouts Found</h3>
          <p className="text-gray-600 mb-6">
            {statusFilter === 'all' 
              ? "No callouts have been created yet. Be the first to challenge someone!"
              : `No ${statusFilter} callouts found.`
            }
          </p>
          {statusFilter === 'all' && (
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