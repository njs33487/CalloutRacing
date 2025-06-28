import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { userAPI, eventAPI, marketplaceAPI, trackAPI, calloutAPI } from '../services/api';
import { User, Event, MarketplaceItem, Track, Callout } from '../types';
import SearchFilters from './search/SearchFilters';
import SearchResults from './search/SearchResults';
import SearchTabs from './search/SearchTabs';

interface SearchFilters {
  category: string;
  location: string;
  dateRange: string;
  priceRange: string;
  horsepowerRange: string;
  status: string;
}

interface SearchResult {
  type: 'user' | 'event' | 'marketplace' | 'track' | 'callout';
  data: User | Event | MarketplaceItem | Track | Callout;
  relevance: number;
}

export default function AdvancedSearch() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialQuery = searchParams.get('q') || '';
  
  const [searchQuery, setSearchQuery] = useState(initialQuery);
  const [filters, setFilters] = useState<SearchFilters>({
    category: '',
    location: '',
    dateRange: '',
    priceRange: '',
    horsepowerRange: '',
    status: ''
  });
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [activeTab, setActiveTab] = useState<'all' | 'users' | 'events' | 'marketplace' | 'tracks' | 'callouts'>('all');

  // Initialize search if there's a query parameter
  useEffect(() => {
    if (initialQuery) {
      performSearch();
    }
  }, []);

  // Debounced search effect
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchQuery.trim().length >= 2) {
        performSearch();
        // Update URL with search query
        setSearchParams({ q: searchQuery.trim() });
      } else {
        setResults([]);
        // Clear URL parameter if no search query
        if (searchQuery.trim() === '') {
          setSearchParams({});
        }
      }
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [searchQuery, filters, setSearchParams]);

  const performSearch = async () => {
    setIsLoading(true);
    try {
      const searchPromises = [];
      const query = searchQuery.trim();

      // Search users
      if (activeTab === 'all' || activeTab === 'users') {
        searchPromises.push(
          userAPI.searchUsers(query).then(response => 
            response.data.map((user: User) => ({
              type: 'user' as const,
              data: user,
              relevance: calculateRelevance(query, user.username + ' ' + user.first_name + ' ' + user.last_name)
            }))
          ).catch(() => [])
        );
      }

      // Search events
      if (activeTab === 'all' || activeTab === 'events') {
        searchPromises.push(
          eventAPI.list().then(response => 
            response.data
              .filter((event: Event) => 
                event.title.toLowerCase().includes(query.toLowerCase()) ||
                event.description.toLowerCase().includes(query.toLowerCase())
              )
              .map((event: Event) => ({
                type: 'event' as const,
                data: event,
                relevance: calculateRelevance(query, event.title + ' ' + event.description)
              }))
          ).catch(() => [])
        );
      }

      // Search marketplace
      if (activeTab === 'all' || activeTab === 'marketplace') {
        searchPromises.push(
          marketplaceAPI.list().then(response => 
            response.data
              .filter((item: MarketplaceItem) => 
                item.title.toLowerCase().includes(query.toLowerCase()) ||
                item.description.toLowerCase().includes(query.toLowerCase())
              )
              .map((item: MarketplaceItem) => ({
                type: 'marketplace' as const,
                data: item,
                relevance: calculateRelevance(query, item.title + ' ' + item.description)
              }))
          ).catch(() => [])
        );
      }

      // Search tracks
      if (activeTab === 'all' || activeTab === 'tracks') {
        searchPromises.push(
          trackAPI.list().then(response => 
            response.data
              .filter((track: Track) => 
                track.name.toLowerCase().includes(query.toLowerCase()) ||
                track.location.toLowerCase().includes(query.toLowerCase()) ||
                (track.description && track.description.toLowerCase().includes(query.toLowerCase()))
              )
              .map((track: Track) => ({
                type: 'track' as const,
                data: track,
                relevance: calculateRelevance(query, track.name + ' ' + track.location + ' ' + (track.description || ''))
              }))
          ).catch(() => [])
        );
      }

      // Search callouts
      if (activeTab === 'all' || activeTab === 'callouts') {
        searchPromises.push(
          calloutAPI.list().then(response => 
            response.data
              .filter((callout: Callout) => 
                callout.message.toLowerCase().includes(query.toLowerCase())
              )
              .map((callout: Callout) => ({
                type: 'callout' as const,
                data: callout,
                relevance: calculateRelevance(query, callout.message)
              }))
          ).catch(() => [])
        );
      }

      const searchResults = await Promise.all(searchPromises);
      const allResults = searchResults.flat().sort((a, b) => b.relevance - a.relevance);
      
      // Apply additional filters
      const filteredResults = applyFilters(allResults);
      setResults(filteredResults);
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const calculateRelevance = (query: string, text: string): number => {
    const queryLower = query.toLowerCase();
    const textLower = text.toLowerCase();
    
    if (textLower.startsWith(queryLower)) return 100;
    if (textLower.includes(queryLower)) return 50;
    
    // Check for partial matches
    const queryWords = queryLower.split(' ');
    const textWords = textLower.split(' ');
    let matches = 0;
    
    queryWords.forEach(word => {
      if (textWords.some(textWord => textWord.includes(word))) {
        matches++;
      }
    });
    
    return (matches / queryWords.length) * 30;
  };

  const applyFilters = (results: SearchResult[]): SearchResult[] => {
    return results.filter(result => {
      // Category filter
      if (filters.category && result.type !== filters.category) {
        return false;
      }

      // Location filter
      if (filters.location) {
        const location = getLocation(result).toLowerCase();
        if (!location.includes(filters.location.toLowerCase())) {
          return false;
        }
      }

      // Price range filter (for marketplace items)
      if (filters.priceRange && result.type === 'marketplace') {
        const item = result.data as MarketplaceItem;
        const price = parseFloat(item.price.toString());
        
        switch (filters.priceRange) {
          case '0-1000':
            if (price > 1000) return false;
            break;
          case '1000-5000':
            if (price < 1000 || price > 5000) return false;
            break;
          case '5000-10000':
            if (price < 5000 || price > 10000) return false;
            break;
          case '10000+':
            if (price < 10000) return false;
            break;
        }
      }

      // Horsepower range filter (for users with cars)
      if (filters.horsepowerRange && result.type === 'user') {
        // This would need to be implemented based on user's car profile
        // For now, we'll skip this filter
      }

      // Status filter
      if (filters.status) {
        // This would need to be implemented based on the specific model
        // For now, we'll skip this filter
      }

      return true;
    });
  };

  const getLocation = (result: SearchResult): string => {
    switch (result.type) {
      case 'user':
        return (result.data as any).profile?.location || 'Location not specified';
      case 'event':
        return (result.data as Event).track?.location || 'Location not specified';
      case 'marketplace':
        return (result.data as MarketplaceItem).location;
      case 'track':
        return (result.data as Track).location;
      case 'callout':
        return (result.data as Callout).street_location || 'Location not specified';
      default:
        return 'Location not specified';
    }
  };

  const clearFilters = () => {
    setFilters({
      category: '',
      location: '',
      dateRange: '',
      priceRange: '',
      horsepowerRange: '',
      status: ''
    });
  };

  const hasActiveFilters = () => {
    return Object.values(filters).some(value => value !== '');
  };

  // Calculate result counts for tabs
  const resultCounts = {
    all: results.length,
    users: results.filter(r => r.type === 'user').length,
    events: results.filter(r => r.type === 'event').length,
    marketplace: results.filter(r => r.type === 'marketplace').length,
    tracks: results.filter(r => r.type === 'track').length,
    callouts: results.filter(r => r.type === 'callout').length,
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Advanced Search</h1>
        <p className="text-gray-600">
          Search across users, events, marketplace items, tracks, and callouts
        </p>
      </div>

      {/* Search Input */}
      <div className="relative mb-6">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search for users, events, marketplace items, tracks, callouts..."
          className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      {/* Search Filters */}
      <SearchFilters
        filters={filters}
        setFilters={setFilters}
        showFilters={showFilters}
        setShowFilters={setShowFilters}
        onClearFilters={clearFilters}
        hasActiveFilters={hasActiveFilters()}
      />

      {/* Search Tabs */}
      <SearchTabs
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        resultCounts={resultCounts}
      />

      {/* Search Results */}
      <SearchResults
        results={results}
        isLoading={isLoading}
        searchQuery={searchQuery}
      />
    </div>
  );
} 