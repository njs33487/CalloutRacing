import { useState } from 'react'
import { MapPinIcon, PhoneIcon, GlobeAltIcon } from '@heroicons/react/24/outline'

export default function Tracks() {
  const [tracks] = useState([
    {
      id: 1,
      name: 'Speedway International',
      location: 'Los Angeles, CA',
      type: 'Drag Strip',
      surface: 'Asphalt',
      length: '1/4 Mile',
      phone: '(555) 123-4567',
      website: 'www.speedwayinternational.com',
      description: 'Professional drag racing facility with state-of-the-art timing equipment.'
    },
    {
      id: 2,
      name: 'Thunder Valley Raceway',
      location: 'Miami, FL',
      type: 'Drag Strip',
      surface: 'Concrete',
      length: '1/4 Mile',
      phone: '(555) 987-6543',
      website: 'www.thundervalleyraceway.com',
      description: 'Premier racing facility with multiple lanes and professional staff.'
    }
  ])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Racing Tracks</h1>
        <p className="text-gray-600">Find tracks and facilities near you</p>
      </div>

      {/* Tracks Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {tracks.map((track) => (
          <div key={track.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <MapPinIcon className="h-6 w-6 text-primary-600 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">
                  {track.name}
                </h3>
              </div>
              <span className="px-2 py-1 text-xs rounded-full font-medium bg-blue-100 text-blue-800">
                {track.type}
              </span>
            </div>
            
            <div className="space-y-3">
              <div className="text-sm text-gray-600">
                📍 {track.location}
              </div>
              
              <div className="text-sm">
                <span className="text-gray-600">Surface: </span>
                <span className="font-medium">{track.surface}</span>
              </div>
              
              <div className="text-sm">
                <span className="text-gray-600">Length: </span>
                <span className="font-medium">{track.length}</span>
              </div>
              
              <div className="flex items-center text-sm text-gray-600">
                <PhoneIcon className="h-4 w-4 mr-2" />
                {track.phone}
              </div>
              
              <div className="flex items-center text-sm text-gray-600">
                <GlobeAltIcon className="h-4 w-4 mr-2" />
                <a href={`https://${track.website}`} className="text-primary-600 hover:underline">
                  {track.website}
                </a>
              </div>
              
              <p className="text-sm text-gray-700">{track.description}</p>
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
      {tracks.length === 0 && (
        <div className="text-center py-12">
          <MapPinIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No tracks found</h3>
          <p className="text-gray-600 mb-6">We're working on adding more tracks to our database!</p>
        </div>
      )}
    </div>
  )
} 