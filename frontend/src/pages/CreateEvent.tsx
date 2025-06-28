import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { eventAPI, trackAPI } from '../services/api';
import { Track } from '../types';

export default function CreateEvent() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [tracks, setTracks] = useState<Track[]>([]);

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    event_type: 'race',
    track: '',
    track_id: null as number | null,
    start_date: '',
    end_date: '',
    max_participants: '',
    entry_fee: '',
    is_public: true
  });

  // Load tracks on component mount
  useEffect(() => {
    loadTracks();
  }, []);

  const loadTracks = async () => {
    try {
      const response = await trackAPI.list();
      setTracks(response.data);
    } catch (err) {
      console.error('Error loading tracks:', err);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const selectTrack = (track: Track) => {
    setFormData(prev => ({ 
      ...prev, 
      track: track.name, 
      track_id: track.id 
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      // Validate required fields
      if (!formData.title.trim()) {
        throw new Error('Event title is required');
      }

      if (!formData.description.trim()) {
        throw new Error('Event description is required');
      }

      if (!formData.track_id) {
        throw new Error('Please select a track');
      }

      if (!formData.start_date) {
        throw new Error('Start date is required');
      }

      if (!formData.end_date) {
        throw new Error('End date is required');
      }

      // Validate dates
      const startDate = new Date(formData.start_date);
      const endDate = new Date(formData.end_date);
      const now = new Date();

      if (startDate < now) {
        throw new Error('Start date cannot be in the past');
      }

      if (endDate <= startDate) {
        throw new Error('End date must be after start date');
      }

      // Prepare data for API
      const eventData = {
        title: formData.title.trim(),
        description: formData.description.trim(),
        event_type: formData.event_type,
        track: formData.track_id,
        start_date: formData.start_date,
        end_date: formData.end_date,
        max_participants: formData.max_participants ? parseInt(formData.max_participants) : null,
        entry_fee: formData.entry_fee ? parseFloat(formData.entry_fee) : 0,
        is_public: formData.is_public
      };

      await eventAPI.create(eventData);
      setSuccess('Event created successfully!');
      
      // Redirect to events page after a short delay
      setTimeout(() => {
        navigate('/events');
      }, 1500);

    } catch (err: any) {
      setError(err.response?.data?.message || err.message || 'Failed to create event');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/events');
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Create Event</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-6">
          {/* Event Title */}
          <div>
            <label htmlFor="title" className="block mb-2 font-medium">
              Event Title *
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter event title"
              required
            />
          </div>

          {/* Description */}
          <div>
            <label htmlFor="description" className="block mb-2 font-medium">
              Description *
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={4}
              placeholder="Describe your event..."
              required
            />
          </div>

          {/* Event Type */}
          <div>
            <label htmlFor="event_type" className="block mb-2 font-medium">
              Event Type *
            </label>
            <select
              id="event_type"
              name="event_type"
              value={formData.event_type}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="race">Race Event</option>
              <option value="meet">Car Meet</option>
              <option value="show">Car Show</option>
              <option value="test">Test & Tune</option>
            </select>
          </div>

          {/* Track Selection */}
          <div>
            <label htmlFor="track" className="block mb-2 font-medium">
              Track *
            </label>
            <select
              id="track"
              name="track"
              value={formData.track}
              onChange={(e) => {
                const track = tracks.find(t => t.name === e.target.value);
                if (track) {
                  selectTrack(track);
                }
              }}
              className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="">Select a track</option>
              {tracks.map(track => (
                <option key={track.id} value={track.name}>
                  {track.name} - {track.location}
                </option>
              ))}
            </select>
          </div>

          {/* Date & Time */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="start_date" className="block mb-2 font-medium">
                Start Date & Time *
              </label>
              <input
                type="datetime-local"
                id="start_date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label htmlFor="end_date" className="block mb-2 font-medium">
                End Date & Time *
              </label>
              <input
                type="datetime-local"
                id="end_date"
                name="end_date"
                value={formData.end_date}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
          </div>

          {/* Optional Fields */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="max_participants" className="block mb-2 font-medium">
                Max Participants (Optional)
              </label>
              <input
                type="number"
                id="max_participants"
                name="max_participants"
                value={formData.max_participants}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                min="1"
                placeholder="No limit"
              />
            </div>
            <div>
              <label htmlFor="entry_fee" className="block mb-2 font-medium">
                Entry Fee (Optional)
              </label>
              <input
                type="number"
                id="entry_fee"
                name="entry_fee"
                value={formData.entry_fee}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                min="0"
                step="0.01"
                placeholder="0.00"
              />
            </div>
          </div>

          {/* Public/Private Toggle */}
          <div className="flex items-center">
            <input
              type="checkbox"
              id="is_public"
              name="is_public"
              checked={formData.is_public}
              onChange={handleChange}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="is_public" className="ml-2 block text-sm font-medium">
              Make this event public
            </label>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-4 pt-4">
            <button
              type="button"
              onClick={handleCancel}
              className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 py-2 px-4 rounded font-medium transition-colors"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading}
            >
              {loading ? 'Creating...' : 'Create Event'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
} 