import { useState } from 'react'
import { Link } from 'react-router-dom'
import { BoltIcon, PlusIcon, MapPinIcon, CalendarIcon } from '@heroicons/react/24/outline'

export default function Callouts() {
  const [callouts] = useState([
    {
      id: 1,
      challenger: 'SpeedDemon',
      challenged: 'RacingKing',
      raceType: 'Quarter Mile',
      location: 'Drag Strip',
      status: 'pending',
      wager: 500,
      message: 'Think you can handle this? Let\'s see what you got!',
      createdAt: '2024-01-15'
    },
    {
      id: 2,
      challenger: 'TurboBoost',
      challenged: 'NitrousQueen',
      raceType: 'Roll Race',
      location: 'Highway',
      status: 'accepted',
      wager: 1000,
      message: 'Ready to prove who\'s the fastest on the street!',
      createdAt: '2024-01-14'
    }
  ])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800'
      case 'accepted':
        return 'bg-green-100 text-green-800'
      case 'completed':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
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

      {/* Callouts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {callouts.map((callout) => (
          <div key={callout.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <BoltIcon className="h-6 w-6 text-primary-600 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">
                  {callout.challenger} vs {callout.challenged}
                </h3>
              </div>
              <span className={`px-2 py-1 text-xs rounded-full font-medium ${getStatusColor(callout.status)}`}>
                {callout.status}
              </span>
            </div>
            
            <div className="space-y-3">
              <div className="flex items-center text-sm text-gray-600">
                <CalendarIcon className="h-4 w-4 mr-2" />
                {callout.raceType}
              </div>
              
              <div className="flex items-center text-sm text-gray-600">
                <MapPinIcon className="h-4 w-4 mr-2" />
                {callout.location}
              </div>
              
              {callout.wager > 0 && (
                <div className="text-sm">
                  <span className="text-gray-600">Wager: </span>
                  <span className="font-semibold text-green-600">${callout.wager}</span>
                </div>
              )}
              
              <p className="text-sm text-gray-700">{callout.message}</p>
              
              <div className="text-xs text-gray-500">
                Created: {callout.createdAt}
              </div>
            </div>
            
            <div className="mt-4 pt-4 border-t border-gray-200">
              <button className="w-full btn-secondary text-sm">
                View Details
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {callouts.length === 0 && (
        <div className="text-center py-12">
          <BoltIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No callouts yet</h3>
          <p className="text-gray-600 mb-6">Be the first to create a callout and challenge other racers!</p>
          <Link
            to="/app/callouts/create"
            className="btn-primary inline-flex items-center"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            Create Your First Callout
          </Link>
        </div>
      )}
    </div>
  )
} 