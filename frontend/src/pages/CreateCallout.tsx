import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { BoltIcon } from '@heroicons/react/24/outline'

export default function CreateCallout() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    challenged: '',
    raceType: 'quarter-mile',
    location: '',
    wager: '',
    message: ''
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle form submission
    console.log('Creating callout:', formData)
    navigate('/app/callouts')
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
        <BoltIcon className="h-8 w-8 text-primary-600 mr-3" />
        <h1 className="text-3xl font-bold text-gray-900">Create Callout</h1>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="challenged" className="block text-sm font-medium text-gray-700 mb-2">
            Challenge User
          </label>
          <input
            type="text"
            id="challenged"
            name="challenged"
            value={formData.challenged}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="Enter username to challenge"
            required
          />
        </div>

        <div>
          <label htmlFor="raceType" className="block text-sm font-medium text-gray-700 mb-2">
            Race Type
          </label>
          <select
            id="raceType"
            name="raceType"
            value={formData.raceType}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="quarter-mile">Quarter Mile</option>
            <option value="eighth-mile">Eighth Mile</option>
            <option value="roll-race">Roll Race</option>
            <option value="dig-race">Dig Race</option>
          </select>
        </div>

        <div>
          <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
            Location
          </label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="Drag strip, highway, etc."
            required
          />
        </div>

        <div>
          <label htmlFor="wager" className="block text-sm font-medium text-gray-700 mb-2">
            Wager (Optional)
          </label>
          <input
            type="number"
            id="wager"
            name="wager"
            value={formData.wager}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="Enter amount in dollars"
            min="0"
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

        <div className="flex space-x-4">
          <button
            type="button"
            onClick={() => navigate('/app/callouts')}
            className="btn-secondary flex-1"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn-primary flex-1"
          >
            Create Callout
          </button>
        </div>
      </form>
    </div>
  )
} 