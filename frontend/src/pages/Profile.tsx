import { useState } from 'react'
import { UserIcon, TruckIcon } from '@heroicons/react/24/outline'

export default function Profile() {
  const [profile] = useState({
    username: 'SpeedDemon',
    email: 'speed@example.com',
    location: 'Los Angeles, CA',
    bio: 'Professional drag racer with 10+ years of experience. Love quarter-mile racing and building fast cars.',
    stats: {
      races: 156,
      wins: 89,
      losses: 67,
      winRate: 57.1
    },
    cars: [
      {
        id: 1,
        name: '2018 Mustang GT',
        model: 'Ford Mustang',
        year: 2018,
        mods: ['Turbo', 'Exhaust', 'Suspension']
      }
    ]
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center">
          <UserIcon className="h-10 w-10 text-primary-600" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{profile.username}</h1>
          <p className="text-gray-600">{profile.location}</p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="card text-center">
          <div className="text-2xl font-bold text-primary-600">{profile.stats.races}</div>
          <div className="text-sm text-gray-600">Total Races</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-green-600">{profile.stats.wins}</div>
          <div className="text-sm text-gray-600">Wins</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-red-600">{profile.stats.losses}</div>
          <div className="text-sm text-gray-600">Losses</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-blue-600">{profile.stats.winRate}%</div>
          <div className="text-sm text-gray-600">Win Rate</div>
        </div>
      </div>

      {/* Bio */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">About</h2>
        <p className="text-gray-700">{profile.bio}</p>
      </div>

      {/* Cars */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">My Cars</h2>
          <button className="btn-secondary text-sm">
            Add Car
          </button>
        </div>
        
        <div className="space-y-4">
          {profile.cars.map((car) => (
            <div key={car.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <TruckIcon className="h-6 w-6 text-primary-600 mr-3" />
                  <div>
                    <h3 className="font-semibold text-gray-900">{car.name}</h3>
                    <p className="text-sm text-gray-600">{car.year} {car.model}</p>
                  </div>
                </div>
                <button className="btn-secondary text-sm">
                  Edit
                </button>
              </div>
              
              <div className="mt-3">
                <div className="text-sm text-gray-600 mb-1">Modifications:</div>
                <div className="flex flex-wrap gap-2">
                  {car.mods.map((mod, index) => (
                    <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                      {mod}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
} 