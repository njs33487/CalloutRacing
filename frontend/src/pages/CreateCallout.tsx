import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'
import { BoltIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline'
import { api } from '../services/api'

interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
}

export default function CreateCallout() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    challenged: '',
    race_type: 'quarter_mile',
    location_type: 'track',
    track: '',
    street_location: '',
    wager_amount: '',
    message: ''
  })
  const [searchQuery, setSearchQuery] = useState('')
  const [showUserSearch, setShowUserSearch] = useState(false)

  // Search users
  const { data: usersData } = useQuery({
    queryKey: ['users', searchQuery],
    queryFn: () => api.get(`/api/users/?search=${searchQuery}`).then(res => res.data),
    enabled: searchQuery.length > 2
  })

  const users = usersData?.results || []

  // Create callout mutation
  const createCallout = useMutation({
    mutationFn: (data: any) => api.post('/api/callouts/', data),
    onSuccess: () => {
      navigate('/app/callouts')
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    const submitData: any = {
      challenged: parseInt(formData.challenged),
      race_type: formData.race_type,
      location_type: formData.location_type,
      wager_amount: formData.wager_amount ? parseFloat(formData.wager_amount) : 0,
      message: formData.message
    }

    if (formData.location_type === 'track' && formData.track) {
      submitData.track = parseInt(formData.track)
    } else if (formData.location_type === 'street' && formData.street_location) {
      submitData.street_location = formData.street_location
    }

    createCallout.mutate(submitData)
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleUserSelect = (user: User) => {
    setFormData({
      ...formData,
      challenged: user.id.toString()
    })
    setSearchQuery(user.username)
    setShowUserSearch(false)
  }

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value)
    setShowUserSearch(true)
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center mb-6">
        <BoltIcon className="h-8 w-8 text-primary-600 mr-3" />
        <h1 className="text-3xl font-bold text-gray-900">Create Callout</h1>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="challenged" className="block text-sm font-medium text-gray-700 mb-2">
            Challenge User
          </label>
          <div className="relative">
            <input
              type="text"
              id="challenged"
              name="challenged"
              value={searchQuery}
              onChange={handleSearchChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Search for a user to challenge"
              required
            />
            <MagnifyingGlassIcon className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
            
            {/* User search dropdown */}
            {showUserSearch && users.length > 0 && (
              <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
                {users.map((user: User) => (
                  <button
                    key={user.id}
                    type="button"
                    onClick={() => handleUserSelect(user)}
                    className="w-full px-4 py-2 text-left hover:bg-gray-100 focus:bg-gray-100"
                  >
                    <div className="font-medium">{user.username}</div>
                    <div className="text-sm text-gray-600">
                      {user.first_name} {user.last_name}
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        <div>
          <label htmlFor="race_type" className="block text-sm font-medium text-gray-700 mb-2">
            Race Type
          </label>
          <select
            id="race_type"
            name="race_type"
            value={formData.race_type}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="quarter_mile">Quarter Mile</option>
            <option value="eighth_mile">Eighth Mile</option>
            <option value="roll_race">Roll Race</option>
            <option value="dig_race">Dig Race</option>
          </select>
        </div>

        <div>
          <label htmlFor="location_type" className="block text-sm font-medium text-gray-700 mb-2">
            Location Type
          </label>
          <select
            id="location_type"
            name="location_type"
            value={formData.location_type}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="track">Track</option>
            <option value="street">Street</option>
          </select>
        </div>

        {formData.location_type === 'track' ? (
          <div>
            <label htmlFor="track" className="block text-sm font-medium text-gray-700 mb-2">
              Track
            </label>
            <select
              id="track"
              name="track"
              value={formData.track}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            >
              <option value="">Select a track</option>
              <option value="1">Speedway International</option>
              <option value="2">Local Drag Strip</option>
              <option value="3">Raceway Park</option>
            </select>
          </div>
        ) : (
          <div>
            <label htmlFor="street_location" className="block text-sm font-medium text-gray-700 mb-2">
              Street Location
            </label>
            <input
              type="text"
              id="street_location"
              name="street_location"
              value={formData.street_location}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter street location"
              required
            />
          </div>
        )}

        <div>
          <label htmlFor="wager_amount" className="block text-sm font-medium text-gray-700 mb-2">
            Wager (Optional)
          </label>
          <input
            type="number"
            id="wager_amount"
            name="wager_amount"
            value={formData.wager_amount}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="Enter amount in dollars"
            min="0"
            step="0.01"
          />
        </div>

        <div>
          <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
            Message
          </label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="Add a message to your challenge..."
            required
          />
        </div>

        {createCallout.error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-800">
              {(createCallout.error as any)?.response?.data?.error || 'Failed to create callout. Please try again.'}
            </p>
          </div>
        )}

        <div className="flex space-x-4">
          <button
            type="button"
            onClick={() => navigate('/app/callouts')}
            className="btn-secondary flex-1"
            disabled={createCallout.isPending}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn-primary flex-1"
            disabled={createCallout.isPending}
          >
            {createCallout.isPending ? 'Creating...' : 'Create Callout'}
          </button>
        </div>
      </form>
    </div>
  )
} 