import { useState } from 'react'
import { Link } from 'react-router-dom'
import { CalendarIcon, PlusIcon, MapPinIcon, UserGroupIcon } from '@heroicons/react/24/outline'

export default function Events() {
  const [events] = useState([
    {
      id: 1,
      title: 'Spring Drag Racing Championship',
      type: 'Race Event',
      track: 'Speedway International',
      startDate: '2024-03-15',
      endDate: '2024-03-17',
      participants: 45,
      maxParticipants: 100,
      entryFee: 150,
      description: 'The biggest drag racing event of the spring season!'
    },
    {
      id: 2,
      title: 'Friday Night Test & Tune',
      type: 'Test & Tune',
      track: 'Local Drag Strip',
      startDate: '2024-01-19',
      endDate: '2024-01-19',
      participants: 28,
      maxParticipants: 50,
      entryFee: 25,
      description: 'Weekly test and tune session for all racers.'
    }
  ])

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

      {/* Events Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {events.map((event) => (
          <div key={event.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <CalendarIcon className="h-6 w-6 text-primary-600 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">
                  {event.title}
                </h3>
              </div>
              <span className="px-2 py-1 text-xs rounded-full font-medium bg-blue-100 text-blue-800">
                {event.type}
              </span>
            </div>
            
            <div className="space-y-3">
              <div className="flex items-center text-sm text-gray-600">
                <MapPinIcon className="h-4 w-4 mr-2" />
                {event.track}
              </div>
              
              <div className="flex items-center text-sm text-gray-600">
                <CalendarIcon className="h-4 w-4 mr-2" />
                {event.startDate} - {event.endDate}
              </div>
              
              <div className="flex items-center text-sm text-gray-600">
                <UserGroupIcon className="h-4 w-4 mr-2" />
                {event.participants}/{event.maxParticipants} participants
              </div>
              
              <div className="text-sm">
                <span className="text-gray-600">Entry Fee: </span>
                <span className="font-semibold text-green-600">${event.entryFee}</span>
              </div>
              
              <p className="text-sm text-gray-700">{event.description}</p>
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
      {events.length === 0 && (
        <div className="text-center py-12">
          <CalendarIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No events yet</h3>
          <p className="text-gray-600 mb-6">Be the first to create an event and bring the racing community together!</p>
          <Link
            to="/app/events/create"
            className="btn-primary inline-flex items-center"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            Create Your First Event
          </Link>
        </div>
      )}
    </div>
  )
} 