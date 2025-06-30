import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  MapPinIcon, 
  CalendarIcon, 
  UserIcon, 
  BoltIcon, 
  ShieldCheckIcon,
  CurrencyDollarIcon,
  ExclamationTriangleIcon,
  ArrowLeftIcon
} from '@heroicons/react/24/outline';
import { calloutAPI, userAPI, trackAPI } from '../services/api';
import { User, Track } from '../types';
import ConfirmationDialog from '../components/ConfirmationDialog';
import ErrorBoundary from '../components/ErrorBoundary';
import { PageLoadingFallback } from '../components/LoadingFallback';
import SecurityWrapper from '../components/SecurityWrapper';

export default function CreateCallout() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [users, setUsers] = useState<User[]>([]);
  const [tracks, setTracks] = useState<Track[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [showUserResults, setShowUserResults] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [confirmationData, setConfirmationData] = useState<any>(null);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [recoveryData, setRecoveryData] = useState<any>(null);

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
    message: '',
    is_private: false,
    is_invite_only: false,
    max_horsepower: '',
    min_horsepower: '',
    tire_requirement: '',
    rules: '',
    experience_level: 'intermediate'
  });

  // Load tracks on component mount with error handling
  useEffect(() => {
    loadTracks();
  }, []);

  // Recovery mechanism - save form data to localStorage
  useEffect(() => {
    const savedData = localStorage.getItem('createCalloutFormData');
    if (savedData) {
      try {
        const parsed = JSON.parse(savedData);
        setFormData(parsed);
        setRecoveryData(parsed);
        setHasUnsavedChanges(true);
      } catch (err) {
        console.error('Failed to parse saved form data:', err);
        localStorage.removeItem('createCalloutFormData');
      }
    }
  }, []);

  // Auto-save form data
  useEffect(() => {
    const saveFormData = () => {
      try {
        localStorage.setItem('createCalloutFormData', JSON.stringify(formData));
        setHasUnsavedChanges(true);
      } catch (err) {
        console.error('Failed to save form data:', err);
      }
    };

    const debounceTimer = setTimeout(saveFormData, 1000);
    return () => clearTimeout(debounceTimer);
  }, [formData]);

  // Clear saved data on successful submission
  const clearSavedData = useCallback(() => {
    localStorage.removeItem('createCalloutFormData');
    setHasUnsavedChanges(false);
    setRecoveryData(null);
  }, []);

  const loadTracks = async () => {
    try {
      setInitialLoading(true);
      const response = await trackAPI.list();
      setTracks(response.data || []);
    } catch (err: any) {
      console.error('Error loading tracks:', err);
      setError('Failed to load tracks. Please refresh the page or try again later.');
    } finally {
      setInitialLoading(false);
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
      setUsers(response.data || []);
      setShowUserResults(true);
    } catch (err: any) {
      console.error('Error searching users:', err);
      setError('Failed to search users. Please try again.');
      setUsers([]);
      setShowUserResults(false);
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
    const { name, value, type } = e.target;
    
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
    
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

  const validateForm = () => {
    if (!formData.challenged_id) {
      throw new Error('Please select a user to challenge');
    }

    if (formData.location_type === 'track' && !formData.track_id) {
      throw new Error('Please select a track');
    }

    if (formData.location_type === 'street' && !formData.street_location.trim()) {
      throw new Error('Please enter a street location');
    }

    if (formData.max_horsepower && formData.min_horsepower) {
      const max = parseInt(formData.max_horsepower);
      const min = parseInt(formData.min_horsepower);
      if (max < min) {
        throw new Error('Maximum horsepower cannot be less than minimum horsepower');
      }
    }

    // Security validation
    if (formData.wager_amount && parseFloat(formData.wager_amount) > 10000) {
      throw new Error('Wager amount cannot exceed $10,000 for security reasons');
    }
  };

  const prepareCalloutData = () => {
    return {
      challenged: formData.challenged_id,
      race_type: formData.race_type,
      location_type: formData.location_type,
      track: formData.track_id,
      street_location: formData.street_location,
      wager_amount: formData.wager_amount ? parseFloat(formData.wager_amount) : 0,
      scheduled_date: formData.scheduled_date || null,
      message: formData.message,
      is_private: formData.is_private,
      is_invite_only: formData.is_invite_only,
      max_horsepower: formData.max_horsepower ? parseInt(formData.max_horsepower) : null,
      min_horsepower: formData.min_horsepower ? parseInt(formData.min_horsepower) : null,
      tire_requirement: formData.tire_requirement,
      rules: formData.rules,
      experience_level: formData.experience_level
    };
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      validateForm();
      
      // Prepare data for confirmation dialog
      const selectedUser = users.find(u => u.id === formData.challenged_id);
      const selectedTrack = tracks.find(t => t.id === formData.track_id);
      
      const confirmationData = {
        'Challenged User': selectedUser ? `${selectedUser.first_name} ${selectedUser.last_name} (@${selectedUser.username})` : 'Not selected',
        'Race Type': formData.race_type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
        'Location Type': formData.location_type.charAt(0).toUpperCase() + formData.location_type.slice(1),
        'Location': formData.location_type === 'track' 
          ? (selectedTrack ? selectedTrack.name : 'Not selected')
          : formData.street_location || 'Not specified',
        'Privacy': formData.is_private ? 'Private' : (formData.is_invite_only ? 'Invite Only' : 'Public'),
        'Experience Level': formData.experience_level.charAt(0).toUpperCase() + formData.experience_level.slice(1),
        'Wager Amount': formData.wager_amount ? `$${formData.wager_amount}` : 'No wager',
        'Scheduled Date': formData.scheduled_date ? new Date(formData.scheduled_date).toLocaleDateString() : 'Not scheduled',
        'Message': formData.message || 'No message'
      };

      setConfirmationData(confirmationData);
      setShowConfirmation(true);
    } catch (err: any) {
      setError(err.message || 'Please check your form inputs');
    }
  };

  const handleConfirmCreate = async () => {
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const calloutData = prepareCalloutData();
      await calloutAPI.create(calloutData);
      setSuccess('Callout created successfully!');
      setShowConfirmation(false);
      clearSavedData();
      
      // Redirect to callouts page after a short delay
      setTimeout(() => {
        navigate('/app/callouts');
      }, 1500);

    } catch (err: any) {
      const errorMessage = err.response?.data?.message || err.message || 'Failed to create callout';
      setError(errorMessage);
      
      // Log error for debugging
      console.error('Callout creation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    if (hasUnsavedChanges) {
      if (window.confirm('You have unsaved changes. Are you sure you want to leave?')) {
        clearSavedData();
        navigate('/app/callouts');
      }
    } else {
      navigate('/app/callouts');
    }
  };

  const handleRecovery = () => {
    if (recoveryData) {
      setFormData(recoveryData);
      setRecoveryData(null);
      setHasUnsavedChanges(true);
    }
  };

  const handleClearForm = () => {
    if (window.confirm('Are you sure you want to clear all form data?')) {
      setFormData({
        challenged: '',
        challenged_id: null,
        race_type: 'quarter_mile',
        location_type: 'track',
        track: '',
        track_id: null,
        street_location: '',
        wager_amount: '',
        scheduled_date: '',
        message: '',
        is_private: false,
        is_invite_only: false,
        max_horsepower: '',
        min_horsepower: '',
        tire_requirement: '',
        rules: '',
        experience_level: 'intermediate'
      });
      clearSavedData();
    }
  };

  // Show loading state while initializing
  if (initialLoading) {
    return <PageLoadingFallback />;
  }

  return (
    <ErrorBoundary>
      <SecurityWrapper>
        <div className="max-w-4xl mx-auto p-6">
          {/* Recovery Banner */}
          {recoveryData && (
            <div className="bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded-lg mb-6 flex items-center justify-between">
              <div className="flex items-center">
                <ExclamationTriangleIcon className="h-5 w-5 mr-2" />
                <span>We found unsaved form data. Would you like to restore it?</span>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={handleRecovery}
                  className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
                >
                  Restore
                </button>
                <button
                  onClick={() => setRecoveryData(null)}
                  className="bg-gray-600 text-white px-3 py-1 rounded text-sm hover:bg-gray-700"
                >
                  Dismiss
                </button>
              </div>
            </div>
          )}

          {/* Header with back button */}
          <div className="mb-8">
            <div className="flex items-center mb-4">
              <button
                onClick={handleCancel}
                className="mr-4 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ArrowLeftIcon className="h-5 w-5" />
              </button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">Create Callout</h1>
                <p className="text-gray-600">Challenge another racer to a head-to-head competition</p>
              </div>
            </div>

            {/* Form Actions */}
            <div className="flex justify-between items-center">
              <div className="flex space-x-2">
                {hasUnsavedChanges && (
                  <span className="text-sm text-gray-500 flex items-center">
                    <div className="w-2 h-2 bg-yellow-500 rounded-full mr-2"></div>
                    Unsaved changes
                  </span>
                )}
              </div>
              <button
                onClick={handleClearForm}
                className="text-sm text-gray-500 hover:text-red-600 transition-colors"
              >
                Clear Form
              </button>
            </div>
          </div>
          
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6 flex items-center">
              <BoltIcon className="h-5 w-5 mr-2" />
              {error}
            </div>
          )}
          
          {success && (
            <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-6 flex items-center">
              <BoltIcon className="h-5 w-5 mr-2" />
              {success}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Basic Information Section */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                <UserIcon className="h-5 w-5 mr-2 text-primary-600" />
                Basic Information
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* User Search */}
                <div className="relative md:col-span-2">
                  <label htmlFor="challenged" className="block mb-2 font-medium text-gray-700">
                    Challenge User *
                  </label>
                  <div className="relative">
                    <input
                      type="text"
                      id="challenged"
                      name="challenged"
                      value={searchQuery}
                      onChange={handleUserSearch}
                      className="w-full border border-gray-300 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                      placeholder="Search for a user to challenge..."
                      required
                    />
                    <UserIcon className="absolute right-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  </div>
                  {showUserResults && users.length > 0 && (
                    <div className="absolute z-10 w-full bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto mt-1">
                      {users.map(user => (
                        <div
                          key={user.id}
                          onClick={() => selectUser(user)}
                          className="px-4 py-3 hover:bg-gray-50 cursor-pointer border-b last:border-b-0 flex items-center"
                        >
                          <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center mr-3">
                            <span className="text-primary-600 font-medium text-sm">
                              {user.first_name?.[0] || user.username[0].toUpperCase()}
                            </span>
                          </div>
                          <div>
                            <div className="font-medium text-gray-900">{user.username}</div>
                            <div className="text-sm text-gray-600">
                              {user.first_name} {user.last_name}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Race Type */}
                <div>
                  <label htmlFor="race_type" className="block mb-2 font-medium text-gray-700">
                    Race Type *
                  </label>
                  <select
                    id="race_type"
                    name="race_type"
                    value={formData.race_type}
                    onChange={handleChange}
                    className="w-full border border-gray-300 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    required
                  >
                    <option value="quarter_mile">🏁 Quarter Mile</option>
                    <option value="eighth_mile">⚡ Eighth Mile</option>
                    <option value="roll_race">🔄 Roll Race</option>
                    <option value="dig_race">🚀 Dig Race</option>
                    <option value="heads_up">👥 Heads Up</option>
                    <option value="bracket">🎯 Bracket Racing</option>
                  </select>
                </div>

                {/* Experience Level */}
                <div>
                  <label htmlFor="experience_level" className="block mb-2 font-medium text-gray-700">
                    Experience Level
                  </label>
                  <select
                    id="experience_level"
                    name="experience_level"
                    value={formData.experience_level}
                    onChange={handleChange}
                    className="w-full border border-gray-300 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  >
                    <option value="beginner">🟢 Beginner</option>
                    <option value="intermediate">🟡 Intermediate</option>
                    <option value="experienced">🟠 Experienced</option>
                    <option value="pro">🔴 Pro</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Location Section */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                <MapPinIcon className="h-5 w-5 mr-2 text-primary-600" />
                Location & Schedule
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Location Type */}
                <div>
                  <label htmlFor="location_type" className="block mb-2 font-medium text-gray-700">
                    Location Type *
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    <label className={`relative cursor-pointer rounded-lg border-2 p-4 text-center transition-colors ${
                      formData.location_type === 'track' 
                        ? 'border-primary-500 bg-primary-50' 
                        : 'border-gray-300 hover:border-gray-400'
                    }`}>
                      <input
                        type="radio"
                        name="location_type"
                        value="track"
                        checked={formData.location_type === 'track'}
                        onChange={handleChange}
                        className="sr-only"
                      />
                      <div className="text-2xl mb-2">🏁</div>
                      <div className="font-medium text-gray-900">Track</div>
                      <div className="text-sm text-gray-600">Official racing facility</div>
                    </label>
                    
                    <label className={`relative cursor-pointer rounded-lg border-2 p-4 text-center transition-colors ${
                      formData.location_type === 'street' 
                        ? 'border-primary-500 bg-primary-50' 
                        : 'border-gray-300 hover:border-gray-400'
                    }`}>
                      <input
                        type="radio"
                        name="location_type"
                        value="street"
                        checked={formData.location_type === 'street'}
                        onChange={handleChange}
                        className="sr-only"
                      />
                      <div className="text-2xl mb-2">🛣️</div>
                      <div className="font-medium text-gray-900">Street</div>
                      <div className="text-sm text-gray-600">Street location</div>
                    </label>
                  </div>
                </div>

                {/* Track Selection (if location type is track) */}
                {formData.location_type === 'track' && (
                  <div>
                    <label htmlFor="track" className="block mb-2 font-medium text-gray-700">
                      Select Track *
                    </label>
                    <select
                      id="track"
                      name="track"
                      value={formData.track}
                      onChange={(e) => {
                        const track = tracks.find(t => t.name === e.target.value);
                        if (track) selectTrack(track);
                      }}
                      className="w-full border border-gray-300 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                      required
                    >
                      <option value="">Select a track...</option>
                      {tracks.map(track => (
                        <option key={track.id} value={track.name}>
                          {track.name} - {track.location}
                        </option>
                      ))}
                    </select>
                  </div>
                )}

                {/* Street Location (if location type is street) */}
                {formData.location_type === 'street' && (
                  <div>
                    <label htmlFor="street_location" className="block mb-2 font-medium text-gray-700">
                      Street Location *
                    </label>
                    <input
                      type="text"
                      id="street_location"
                      name="street_location"
                      value={formData.street_location}
                      onChange={handleChange}
                      className="w-full border border-gray-300 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                      placeholder="Enter street address or location..."
                      required
                    />
                  </div>
                )}

                {/* Scheduled Date */}
                <div>
                  <label htmlFor="scheduled_date" className="block mb-2 font-medium text-gray-700">
                    Scheduled Date (Optional)
                  </label>
                  <div className="relative">
                    <input
                      type="datetime-local"
                      id="scheduled_date"
                      name="scheduled_date"
                      value={formData.scheduled_date}
                      onChange={handleChange}
                      className="w-full border border-gray-300 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                    <CalendarIcon className="absolute right-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  </div>
                </div>
              </div>
            </div>

            {/* Racing Requirements Section */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                <BoltIcon className="h-5 w-5 mr-2 text-primary-600" />
                Racing Requirements
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Horsepower Range */}
                <div className="md:col-span-2">
                  <label className="block mb-2 font-medium text-gray-700">Horsepower Range (Optional)</label>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label htmlFor="min_horsepower" className="block text-sm text-gray-600 mb-1">Minimum HP</label>
                      <input
                        type="number"
                        id="min_horsepower"
                        name="min_horsepower"
                        value={formData.min_horsepower}
                        onChange={handleChange}
                        className="w-full border border-gray-300 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                        placeholder="Min HP"
                        min="0"
                      />
                    </div>
                    <div>
                      <label htmlFor="max_horsepower" className="block text-sm text-gray-600 mb-1">Maximum HP</label>
                      <input
                        type="number"
                        id="max_horsepower"
                        name="max_horsepower"
                        value={formData.max_horsepower}
                        onChange={handleChange}
                        className="w-full border border-gray-300 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                        placeholder="Max HP"
                        min="0"
                      />
                    </div>
                  </div>
                </div>

                {/* Tire Requirement */}
                <div>
                  <label htmlFor="tire_requirement" className="block mb-2 font-medium text-gray-700">
                    Tire Requirement (Optional)
                  </label>
                  <input
                    type="text"
                    id="tire_requirement"
                    name="tire_requirement"
                    value={formData.tire_requirement}
                    onChange={handleChange}
                    className="w-full border border-gray-300 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="e.g., Drag radials only, Street tires allowed"
                  />
                </div>

                {/* Wager Amount */}
                <div>
                  <label htmlFor="wager_amount" className="block mb-2 font-medium text-gray-700">
                    Wager Amount (Optional)
                  </label>
                  <div className="relative">
                    <input
                      type="number"
                      id="wager_amount"
                      name="wager_amount"
                      value={formData.wager_amount}
                      onChange={handleChange}
                      className="w-full border border-gray-300 px-4 py-3 pl-10 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                      placeholder="Enter wager amount..."
                      min="0"
                      max="10000"
                      step="0.01"
                    />
                    <CurrencyDollarIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Maximum wager: $10,000</p>
                </div>
              </div>

              {/* Rules */}
              <div className="mt-6">
                <label htmlFor="rules" className="block mb-2 font-medium text-gray-700">
                  Special Rules (Optional)
                </label>
                <textarea
                  id="rules"
                  name="rules"
                  value={formData.rules}
                  onChange={handleChange}
                  className="w-full border border-gray-300 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  rows={3}
                  placeholder="Any special rules or conditions for this race..."
                />
              </div>
            </div>

            {/* Privacy & Message Section */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                <ShieldCheckIcon className="h-5 w-5 mr-2 text-primary-600" />
                Privacy & Communication
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Privacy Settings */}
                <div>
                  <label className="block mb-3 font-medium text-gray-700">Privacy Settings</label>
                  <div className="space-y-3">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        name="is_private"
                        checked={formData.is_private}
                        onChange={handleChange}
                        className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                      />
                      <span className="ml-2 text-sm text-gray-700">Private callout (only visible to participants)</span>
                    </label>
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        name="is_invite_only"
                        checked={formData.is_invite_only}
                        onChange={handleChange}
                        className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                      />
                      <span className="ml-2 text-sm text-gray-700">Invite only (requires approval)</span>
                    </label>
                  </div>
                </div>

                {/* Message */}
                <div>
                  <label htmlFor="message" className="block mb-2 font-medium text-gray-700">
                    Message (Optional)
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    className="w-full border border-gray-300 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    rows={4}
                    placeholder="Add a message to your callout..."
                  />
                </div>
              </div>
            </div>

            {/* Form Actions */}
            <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
              <button
                type="button"
                onClick={handleCancel}
                className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors font-medium"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium flex items-center"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Creating...
                  </>
                ) : (
                  <>
                    <BoltIcon className="h-4 w-4 mr-2" />
                    Create Callout
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Confirmation Dialog */}
          <ConfirmationDialog
            isOpen={showConfirmation}
            onClose={() => setShowConfirmation(false)}
            onConfirm={handleConfirmCreate}
            title="Confirm Callout Creation"
            message="Please review the callout details below before creating. This action cannot be undone."
            confirmText="Create Callout"
            cancelText="Go Back"
            type="warning"
            loading={loading}
            data={confirmationData}
          />
        </div>
      </SecurityWrapper>
    </ErrorBoundary>
  );
} 