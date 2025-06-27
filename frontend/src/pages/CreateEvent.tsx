import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'
import { CalendarIcon } from '@heroicons/react/24/outline'
import { api } from '../services/api'
import { Track } from '../types'

export default function CreateEvent() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    title: '',
    event_type: 'race',
    track: '',
    start_date: '',
    end_date: '',
    max_participants: '',
    entry_fee: '',
    description: '',
    is_public: true
  })

  // Fetch tracks for dropdown
  const { data: tracksData } = useQuery({
    queryKey: ['tracks'],
    queryFn: () => api.get('/tracks/').then(res => res.data)
  })

  const tracks = tracksData?.results || []

  // Create event mutation
  const createEvent = useMutation({
    mutationFn: (data: any) => api.post('/events/', data),
    onSuccess: () => {
      navigate('/app/events')
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    const submitData = {
      ...formData,
      track: parseInt(formData.track),
      max_participants: formData.max_participants ? parseInt(formData.max_participants) : null,
      entry_fee: parseFloat(formData.entry_fee) || 0,
      is_public: formData.is_public
    }

    createEvent.mutate(submitData)
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center mb-6">
        <CalendarIcon className="h-8 w-8 text-primary-600 mr-3" />
        <h1 className="text-3xl font-bold text-gray-900">Create Event</h1>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
            Event Title
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="Enter event title"
            required
          />
        </div>

        <div>
          <label htmlFor="event_type" className="block text-sm font-medium text-gray-700 mb-2">
            Event Type
          </label>
          <select
            id="event_type"
            name="event_type"
            value={formData.event_type}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="race">Race Event</option>
            <option value="test">Test & Tune</option>
            <option value="meet">Car Meet</option>
            <option value="show">Car Show</option>
          </select>
        </div>

        <div>
          <label htmlFor="track" className="block text-sm font-medium text-gray-700 mb-2">
            Track/Facility
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
            {tracks.map((track: Track) => (
              <option key={track.id} value={track.id}>
                {`${track.name} - ${track.location}`}
              </option>
            ))}
          </select>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label htmlFor="start_date" className="block text-sm font-medium text-gray-700 mb-2">
              Start Date
            </label>
            <input
              type="date"
              id="start_date"
              name="start_date"
              value={formData.start_date}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            />
          </div>
          <div>
            <label htmlFor="end_date" className="block text-sm font-medium text-gray-700 mb-2">
              End Date
            </label>
            <input
              type="date"
              id="end_date"
              name="end_date"
              value={formData.end_date}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label htmlFor="max_participants" className="block text-sm font-medium text-gray-700 mb-2">
              Max Participants
            </label>
            <input
              type="number"
              id="max_participants"
              name="max_participants"
              value={formData.max_participants}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter max participants"
              min="1"
            />
          </div>
          <div>
            <label htmlFor="entry_fee" className="block text-sm font-medium text-gray-700 mb-2">
              Entry Fee ($)
            </label>
            <input
              type="number"
              id="entry_fee"
              name="entry_fee"
              value={formData.entry_fee}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter entry fee"
              min="0"
              step="0.01"
            />
          </div>
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="Describe your event..."
            required
          />
        </div>

        {createEvent.error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-800">
              {(createEvent.error as any)?.response?.data?.error || 'Failed to create event. Please try again.'}
            </p>
          </div>
        )}

        <div className="flex space-x-4">
          <button
            type="button"
            onClick={() => navigate('/app/events')}
            className="btn-secondary flex-1"
            disabled={createEvent.isPending}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn-primary flex-1"
            disabled={createEvent.isPending}
          >
            {createEvent.isPending ? 'Creating...' : 'Create Event'}
          </button>
        </div>
      </form>
    </div>
  )
} 