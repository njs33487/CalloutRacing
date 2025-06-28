import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { calloutAPI, userAPI, trackAPI } from '../services/api';
import { User, Track } from '../types';

export default function CreateCallout() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [users, setUsers] = useState<User[]>([]);
  const [tracks, setTracks] = useState<Track[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [showUserResults, setShowUserResults] = useState(false);

  const [formData, setFormData] = useState({
    challenged: '',
    challenged_id: null as number | null,
    race_type: 'quarter_mile',
    location_type: 'track',
    track: '',
    track_id: null as number | null,
    street_location: '',
    wager_amount: '',
    scheduled_date: '',
    message: ''
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

  const searchUsers = async (query: string) => {
    if (query.length < 2) {
      setUsers([]);
      setShowUserResults(false);
      return;
    }

    try {
      const response = await userAPI.searchUsers(query);
      setUsers(response.data);
      setShowUserResults(true);
    } catch (err) {
      console.error('Error searching users:', err);
    }
  };

  const handleUserSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);
    setFormData(prev => ({ ...prev, challenged: query, challenged_id: null }));
    searchUsers(query);
  };

  const selectUser = (user: User) => {
    setFormData(prev => ({ 
      ...prev, 
      challenged: user.username, 
      challenged_id: user.id 
    }));
    setSearchQuery(user.username);
    setShowUserResults(false);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear track_id when location type changes
    if (name === 'location_type') {
      setFormData(prev => ({ 
        ...prev, 
        location_type: value as 'track' | 'street',
        track_id: null,
        track: ''
      }));
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
      if (!formData.challenged_id) {
        throw new Error('Please select a user to challenge');
      }

      if (formData.location_type === 'track' && !formData.track_id) {
        throw new Error('Please select a track');
      }

      if (formData.location_type === 'street' && !formData.street_location.trim()) {
        throw new Error('Please enter a street location');
      }

      // Prepare data for API
      const calloutData = {
        challenged: formData.challenged_id,
        race_type: formData.race_type,
        location_type: formData.location_type,
        track: formData.track_id,
        street_location: formData.street_location,
        wager_amount: formData.wager_amount ? parseFloat(formData.wager_amount) : 0,
        scheduled_date: formData.scheduled_date || null,
        message: formData.message
      };

      await calloutAPI.create(calloutData);
      setSuccess('Callout created successfully!');
      
      // Redirect to callouts page after a short delay
      setTimeout(() => {
        navigate('/callouts');
      }, 1500);

    } catch (err: any) {
      setError(err.response?.data?.message || err.message || 'Failed to create callout');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/callouts');
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Create Callout</h1>
      
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
          {/* User Search */}
          <div className="relative">
            <label htmlFor="challenged" className="block mb-2 font-medium">
              Challenge User *
            </label>
            <input
              type="text"
              id="challenged"
              name="challenged"
              value={searchQuery}
              onChange={handleUserSearch}
              className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Search for a user to challenge..."
              required
            />
            {showUserResults && users.length > 0 && (
              <div className="absolute z-10 w-full bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-y-auto">
                {users.map(user => (
                  <div
                    key={user.id}
                    onClick={() => selectUser(user)}
                    className="px-4 py-2 hover:bg-gray-100 cursor-pointer border-b last:border-b-0"
                  >
                    <div className="font-medium">{user.username}</div>
                    <div className="text-sm text-gray-600">
                      {user.first_name} {user.last_name}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Race Type */}
          <div>
            <label htmlFor="race_type" className="block mb-2 font-medium">
              Race Type
            </label>
            <select
              id="race_type"
              name="race_type"
              value={formData.race_type}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="quarter_mile">Quarter Mile</option>
              <option value="eighth_mile">Eighth Mile</option>
              <option value="roll_race">Roll Race</option>
              <option value="dig_race">Dig Race</option>
            </select>
          </div>

          {/* Location Type */}
          <div>
            <label htmlFor="location_type" className="block mb-2 font-medium">
              Location Type
            </label>
            <select
              id="location_type"
              name="location_type"
              value={formData.location_type}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="track">Track</option>
              <option value="street">Street</option>
            </select>
          </div>

          {/* Track or Street Location */}
          {formData.location_type === 'track' ? (
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
          ) : (
            <div>
              <label htmlFor="street_location" className="block mb-2 font-medium">
                Street Location *
              </label>
              <input
                type="text"
                id="street_location"
                name="street_location"
                value={formData.street_location}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter street address or location"
                required
              />
            </div>
          )}

          {/* Wager Amount */}
          <div>
            <label htmlFor="wager_amount" className="block mb-2 font-medium">
              Wager Amount (Optional)
            </label>
            <input
              type="number"
              id="wager_amount"
              name="wager_amount"
              value={formData.wager_amount}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              min="0"
              step="0.01"
              placeholder="0.00"
            />
          </div>

          {/* Scheduled Date */}
          <div>
            <label htmlFor="scheduled_date" className="block mb-2 font-medium">
              Scheduled Date & Time (Optional)
            </label>
            <input
              type="datetime-local"
              id="scheduled_date"
              name="scheduled_date"
              value={formData.scheduled_date}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Message */}
          <div>
            <label htmlFor="message" className="block mb-2 font-medium">
              Message *
            </label>
            <textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={4}
              placeholder="What's your challenge message?"
              required
            />
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
              {loading ? 'Creating...' : 'Create Callout'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
} 