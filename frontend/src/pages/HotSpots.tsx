import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getHotSpots, createHotSpot } from '../services/api';
import { MapPin, Clock, Users, Star, Plus, Filter } from 'lucide-react';

const HotSpots: React.FC = () => {
  const [filters, setFilters] = useState({
    spot_type: '',
    city: '',
    state: '',
    is_verified: false
  });
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [createForm, setCreateForm] = useState({
    name: '',
    description: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    latitude: '',
    longitude: '',
    spot_type: 'street_meet' as const,
    rules: '',
    amenities: '',
    peak_hours: ''
  });

  const { data: hotSpots, isLoading, refetch } = useQuery({
    queryKey: ['hotspots', filters],
    queryFn: () => getHotSpots(filters)
  });

  const handleCreateHotSpot = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createHotSpot({
        ...createForm,
        latitude: parseFloat(createForm.latitude),
        longitude: parseFloat(createForm.longitude)
      });
      setShowCreateForm(false);
      setCreateForm({
        name: '', description: '', address: '', city: '', state: '', zip_code: '',
        latitude: '', longitude: '', spot_type: 'street_meet', rules: '', amenities: '', peak_hours: ''
      });
      refetch();
    } catch (error) {
      console.error('Error creating hot spot:', error);
    }
  };

  const getSpotTypeIcon = (type: string) => {
    switch (type) {
      case 'track': return '🏁';
      case 'street_meet': return '🛣️';
      case 'parking_lot': return '🅿️';
      case 'industrial': return '🏭';
      default: return '📍';
    }
  };

  const getSpotTypeLabel = (type: string) => {
    switch (type) {
      case 'track': return 'Official Track';
      case 'street_meet': return 'Street Meet Point';
      case 'parking_lot': return 'Parking Lot';
      case 'industrial': return 'Industrial Area';
      default: return 'Other';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-white rounded-lg shadow p-6">
                  <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
                  <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Racing Hot Spots</h1>
            <p className="text-gray-600 mt-2">Find and discover racing locations near you</p>
          </div>
          <button
            onClick={() => setShowCreateForm(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-4 h-4" />
            Add Hot Spot
          </button>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Filter className="w-5 h-5 text-gray-500" />
            <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <select
              value={filters.spot_type}
              onChange={(e) => setFilters({ ...filters, spot_type: e.target.value })}
              className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Types</option>
              <option value="track">Official Track</option>
              <option value="street_meet">Street Meet Point</option>
              <option value="parking_lot">Parking Lot</option>
              <option value="industrial">Industrial Area</option>
              <option value="other">Other</option>
            </select>
            <input
              type="text"
              placeholder="City"
              value={filters.city}
              onChange={(e) => setFilters({ ...filters, city: e.target.value })}
              className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="text"
              placeholder="State"
              value={filters.state}
              onChange={(e) => setFilters({ ...filters, state: e.target.value })}
              className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={filters.is_verified}
                onChange={(e) => setFilters({ ...filters, is_verified: e.target.checked })}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">Verified Only</span>
            </label>
          </div>
        </div>

        {/* Hot Spots Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {hotSpots?.map((hotSpot) => (
            <div key={hotSpot.id} className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{getSpotTypeIcon(hotSpot.spot_type)}</span>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{hotSpot.name}</h3>
                      <p className="text-sm text-gray-500">{getSpotTypeLabel(hotSpot.spot_type)}</p>
                    </div>
                  </div>
                  {hotSpot.is_verified && (
                    <Star className="w-5 h-5 text-yellow-500 fill-current" />
                  )}
                </div>

                <div className="space-y-3 mb-4">
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <MapPin className="w-4 h-4" />
                    <span>{hotSpot.city}, {hotSpot.state}</span>
                  </div>
                  {hotSpot.peak_hours && (
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <Clock className="w-4 h-4" />
                      <span>{hotSpot.peak_hours}</span>
                    </div>
                  )}
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <Users className="w-4 h-4" />
                    <span>{hotSpot.total_races} races held here</span>
                  </div>
                </div>

                {hotSpot.description && (
                  <p className="text-gray-700 text-sm mb-4 line-clamp-3">{hotSpot.description}</p>
                )}

                {hotSpot.rules && (
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold text-gray-900 mb-2">Rules</h4>
                    <p className="text-sm text-gray-600 line-clamp-2">{hotSpot.rules}</p>
                  </div>
                )}

                {hotSpot.amenities && (
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold text-gray-900 mb-2">Amenities</h4>
                    <p className="text-sm text-gray-600 line-clamp-2">{hotSpot.amenities}</p>
                  </div>
                )}

                <div className="flex justify-between items-center pt-4 border-t border-gray-100">
                  <span className="text-xs text-gray-500">
                    Created by {hotSpot.created_by.username}
                  </span>
                  <button className="text-blue-600 text-sm font-medium hover:text-blue-700">
                    View Details
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {hotSpots?.length === 0 && (
          <div className="text-center py-12">
            <MapPin className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No hot spots found</h3>
            <p className="text-gray-600">Try adjusting your filters or add a new hot spot.</p>
          </div>
        )}
      </div>

      {/* Create Hot Spot Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold text-gray-900">Add New Hot Spot</h2>
                <button
                  onClick={() => setShowCreateForm(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleCreateHotSpot} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                    <input
                      type="text"
                      required
                      value={createForm.name}
                      onChange={(e) => setCreateForm({ ...createForm, name: e.target.value })}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
                    <select
                      required
                      value={createForm.spot_type}
                      onChange={(e) => setCreateForm({ ...createForm, spot_type: e.target.value as any })}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="street_meet">Street Meet Point</option>
                      <option value="parking_lot">Parking Lot</option>
                      <option value="industrial">Industrial Area</option>
                      <option value="track">Official Track</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    value={createForm.description}
                    onChange={(e) => setCreateForm({ ...createForm, description: e.target.value })}
                    rows={3}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                  <input
                    type="text"
                    required
                    value={createForm.address}
                    onChange={(e) => setCreateForm({ ...createForm, address: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
                    <input
                      type="text"
                      required
                      value={createForm.city}
                      onChange={(e) => setCreateForm({ ...createForm, city: e.target.value })}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
                    <input
                      type="text"
                      required
                      value={createForm.state}
                      onChange={(e) => setCreateForm({ ...createForm, state: e.target.value })}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">ZIP Code</label>
                    <input
                      type="text"
                      required
                      value={createForm.zip_code}
                      onChange={(e) => setCreateForm({ ...createForm, zip_code: e.target.value })}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Latitude</label>
                    <input
                      type="number"
                      step="any"
                      required
                      value={createForm.latitude}
                      onChange={(e) => setCreateForm({ ...createForm, latitude: e.target.value })}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Longitude</label>
                    <input
                      type="number"
                      step="any"
                      required
                      value={createForm.longitude}
                      onChange={(e) => setCreateForm({ ...createForm, longitude: e.target.value })}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Peak Hours</label>
                  <input
                    type="text"
                    placeholder="e.g., Friday 8PM-12AM"
                    value={createForm.peak_hours}
                    onChange={(e) => setCreateForm({ ...createForm, peak_hours: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Rules</label>
                  <textarea
                    value={createForm.rules}
                    onChange={(e) => setCreateForm({ ...createForm, rules: e.target.value })}
                    rows={3}
                    placeholder="Specific rules for this location..."
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Amenities</label>
                  <textarea
                    value={createForm.amenities}
                    onChange={(e) => setCreateForm({ ...createForm, amenities: e.target.value })}
                    rows={3}
                    placeholder="Available amenities..."
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div className="flex justify-end gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowCreateForm(false)}
                    className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Create Hot Spot
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HotSpots; 