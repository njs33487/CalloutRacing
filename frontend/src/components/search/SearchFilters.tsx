import { useState } from 'react';
import { AdjustmentsHorizontalIcon, XMarkIcon } from '@heroicons/react/24/outline';

interface SearchFilters {
  category: string;
  location: string;
  dateRange: string;
  priceRange: string;
  horsepowerRange: string;
  status: string;
}

interface SearchFiltersProps {
  filters: SearchFilters;
  setFilters: (filters: SearchFilters) => void;
  showFilters: boolean;
  setShowFilters: (show: boolean) => void;
  onClearFilters: () => void;
  hasActiveFilters: boolean;
}

export default function SearchFilters({
  filters,
  setFilters,
  showFilters,
  setShowFilters,
  onClearFilters,
  hasActiveFilters
}: SearchFiltersProps) {
  const updateFilter = (key: keyof SearchFilters, value: string) => {
    setFilters({ ...filters, [key]: value });
  };

  return (
    <div className="mb-6">
      {/* Filter Toggle Button */}
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <AdjustmentsHorizontalIcon className="w-4 h-4" />
          Filters
          {hasActiveFilters && (
            <span className="inline-flex items-center justify-center w-5 h-5 text-xs font-medium text-white bg-blue-600 rounded-full">
              !
            </span>
          )}
        </button>
        
        {hasActiveFilters && (
          <button
            onClick={onClearFilters}
            className="text-sm text-gray-500 hover:text-gray-700"
          >
            Clear all
          </button>
        )}
      </div>

      {/* Filter Panel */}
      {showFilters && (
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Category Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Category
              </label>
              <select
                value={filters.category}
                onChange={(e) => updateFilter('category', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Categories</option>
                <option value="user">Users</option>
                <option value="event">Events</option>
                <option value="marketplace">Marketplace</option>
                <option value="track">Tracks</option>
                <option value="callout">Callouts</option>
              </select>
            </div>

            {/* Location Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Location
              </label>
              <input
                type="text"
                value={filters.location}
                onChange={(e) => updateFilter('location', e.target.value)}
                placeholder="Enter location..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Date Range Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Date Range
              </label>
              <select
                value={filters.dateRange}
                onChange={(e) => updateFilter('dateRange', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Any Time</option>
                <option value="today">Today</option>
                <option value="week">This Week</option>
                <option value="month">This Month</option>
                <option value="year">This Year</option>
              </select>
            </div>

            {/* Price Range Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Price Range
              </label>
              <select
                value={filters.priceRange}
                onChange={(e) => updateFilter('priceRange', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Any Price</option>
                <option value="0-1000">$0 - $1,000</option>
                <option value="1000-5000">$1,000 - $5,000</option>
                <option value="5000-10000">$5,000 - $10,000</option>
                <option value="10000+">$10,000+</option>
              </select>
            </div>

            {/* Horsepower Range Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Horsepower Range
              </label>
              <select
                value={filters.horsepowerRange}
                onChange={(e) => updateFilter('horsepowerRange', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Any HP</option>
                <option value="0-200">0 - 200 HP</option>
                <option value="200-400">200 - 400 HP</option>
                <option value="400-600">400 - 600 HP</option>
                <option value="600+">600+ HP</option>
              </select>
            </div>

            {/* Status Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                value={filters.status}
                onChange={(e) => updateFilter('status', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Any Status</option>
                <option value="active">Active</option>
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 