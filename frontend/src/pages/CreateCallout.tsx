import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'
import { BoltIcon, MagnifyingGlassIcon, PhotoIcon, XMarkIcon } from '@heroicons/react/24/outline'
import { api } from '../services/api'
import { User, Track } from '../types'

interface ImageFile {
  file: File;
  preview: string;
  id: string;
}

export default function CreateCallout() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    challenged: '',
    message: '',
    location_type: 'street',
    race_type: 'roll_race',
    track: '',
    street_location: '',
    scheduled_date: '',
    wager_amount: '',
    car_details: ''
  })
  const [searchQuery, setSearchQuery] = useState('')
  const [showUserSearch, setShowUserSearch] = useState(false)
  const [images, setImages] = useState<ImageFile[]>([])

  // Search users
  const { data: usersData } = useQuery({
    queryKey: ['users', searchQuery],
    queryFn: () => api.get(`/users/?search=${searchQuery}`).then(res => res.data),
    enabled: searchQuery.length > 2
  })

  const users = usersData?.results || []

  // Fetch tracks for dropdown
  const { data: tracks = [] } = useQuery<Track[]>({
    queryKey: ['tracks'],
    queryFn: () => api.get('/tracks/').then(res => res.data)
  })

  // Create callout mutation
  const createCallout = useMutation({
    mutationFn: async (data: any) => {
      const formDataToSend = new FormData()
      
      // Add form fields
      Object.keys(data).forEach(key => {
        if (key !== 'images') {
          formDataToSend.append(key, data[key])
        }
      })
      
      // Add images
      images.forEach((imageFile, index) => {
        formDataToSend.append('images', imageFile.file)
        if (index === 0) {
          formDataToSend.append('primary_image', 'true')
        }
      })
      
      return api.post('/callouts/', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
    },
    onSuccess: () => {
      navigate('/app/callouts')
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    const submitData = {
      ...formData,
      track: formData.track ? parseInt(formData.track) : null,
      wager_amount: parseFloat(formData.wager_amount) || 0,
      scheduled_date: formData.scheduled_date || null,
      images
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

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    
    files.forEach(file => {
      if (file.type.startsWith('image/')) {
        const reader = new FileReader()
        reader.onload = (e) => {
          const imageFile: ImageFile = {
            file,
            preview: e.target?.result as string,
            id: Math.random().toString(36).substr(2, 9)
          }
          setImages(prev => [...prev, imageFile])
        }
        reader.readAsDataURL(file)
      }
    })
  }

  const removeImage = (id: string) => {
    setImages(prev => prev.filter(img => img.id !== id))
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
              className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Search for a user to challenge"
              required
            />
            <div className="absolute right-3 top-2.5">
              <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
            </div>
            
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
                    <div>
                      <div className="font-medium">{user.username}</div>
                      <div className="text-sm text-gray-600">{user.first_name} {user.last_name}</div>
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
              {tracks.map((track: Track) => (
                <option key={track.id} value={track.id.toString()}>{track.name}</option>
              ))}
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
          <label htmlFor="scheduled_date" className="block text-sm font-medium text-gray-700 mb-2">
            Scheduled Date (Optional)
          </label>
          <input
            type="datetime-local"
            id="scheduled_date"
            name="scheduled_date"
            value={formData.scheduled_date}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div>
          <label htmlFor="car_details" className="block text-sm font-medium text-gray-700 mb-2">
            Car Details (Optional)
          </label>
          <textarea
            id="car_details"
            name="car_details"
            value={formData.car_details}
            onChange={handleChange}
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            placeholder="Enter car details"
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

        <div>
          <label htmlFor="images" className="block text-sm font-medium text-gray-700 mb-2">
            Images (Optional)
          </label>
          <div className="space-y-4">
            {/* Image Upload Input */}
            <div className="flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-primary-400 transition-colors">
              <div className="space-y-1 text-center">
                <PhotoIcon className="mx-auto h-12 w-12 text-gray-400" />
                <div className="flex text-sm text-gray-600">
                  <label
                    htmlFor="image-upload"
                    className="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500"
                  >
                    <span>Upload images</span>
                  </label>
                  <input
                    id="image-upload"
                    name="image-upload"
                    type="file"
                    className="sr-only"
                    multiple
                    accept="image/*"
                    onChange={handleImageUpload}
                  />
                  <p className="pl-1">or drag and drop</p>
                </div>
                <p className="text-xs text-gray-500">PNG, JPG, GIF up to 10MB each</p>
              </div>
            </div>

            {/* Image Previews */}
            {images.length > 0 && (
              <div>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {images.map((image, index) => (
                    <div key={image.id} className="relative group">
                      <img
                        src={image.preview}
                        alt={`Preview ${index + 1}`}
                        className="w-full h-32 object-cover rounded-lg border border-gray-200"
                      />
                      <button
                        type="button"
                        onClick={() => removeImage(image.id)}
                        className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        <XMarkIcon className="h-4 w-4" />
                      </button>
                      {index === 0 && (
                        <div className="absolute top-2 left-2 bg-primary-600 text-white text-xs px-2 py-1 rounded">
                          Primary
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
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