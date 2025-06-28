import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { 
  MagnifyingGlassIcon, 
  MapPinIcon, 
  CalendarIcon, 
  UserIcon, 
  BoltIcon, 
  ShoppingBagIcon,
  AdjustmentsHorizontalIcon
} from '@heroicons/react/24/outline';
import { userAPI, eventAPI, marketplaceAPI, trackAPI, calloutAPI } from '../services/api';
import { User, Event, MarketplaceItem, Track, Callout } from '../types';

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
      // Location filter
      if (filters.location && result.type !== 'user') {
        const location = getLocation(result);
        if (!location.toLowerCase().includes(filters.location.toLowerCase())) {
          return false;
        }
      }

      // Price range filter (for marketplace items)
      if (filters.priceRange && result.type === 'marketplace') {
        const item = result.data as MarketplaceItem;
        const [min, max] = filters.priceRange.split('-').map(Number);
        if (item.price < min || (max && item.price > max)) {
          return false;
        }
      }

      // Horsepower range filter (for cars in marketplace)
      if (filters.horsepowerRange && result.type === 'marketplace') {
        const item = result.data as MarketplaceItem;
        if (item.category === 'car') {
          // This would need to be implemented based on car data structure
          // For now, we'll skip this filter
        }
      }

      // Status filter
      if (filters.status && result.type === 'callout') {
        const callout = result.data as Callout;
        if (callout.status !== filters.status) {
          return false;
        }
      }

      return true;
    });
  };

  const getLocation = (result: SearchResult): string => {
    switch (result.type) {
      case 'event':
        return (result.data as Event).track.location;
      case 'marketplace':
        return (result.data as MarketplaceItem).location;
      case 'track':
        return (result.data as Track).location;
      case 'callout':
        const callout = result.data as Callout;
        return callout.track?.location || callout.street_location || '';
      default:
        return '';
    }
  };

  const getResultIcon = (type: string) => {
    switch (type) {
      case 'user':
        return <UserIcon className="w-5 h-5" />;
      case 'event':
        return <CalendarIcon className="w-5 h-5" />;
      case 'marketplace':
        return <ShoppingBagIcon className="w-5 h-5" />;
      case 'track':
        return <MapPinIcon className="w-5 h-5" />;
      case 'callout':
        return <BoltIcon className="w-5 h-5" />;
      default:
        return <MagnifyingGlassIcon className="w-5 h-5" />;
    }
  };

  const getResultLink = (result: SearchResult): string => {
    switch (result.type) {
      case 'user':
        return `/app/profile/${result.data.id}`;
      case 'event':
        return `/app/events/${result.data.id}`;
      case 'marketplace':
        return `/app/marketplace/${result.data.id}`;
      case 'track':
        return `/app/tracks/${result.data.id}`;
      case 'callout':
        return `/app/callouts/${result.data.id}`;
      default:
        return '#';
    }
  };

  const getResultTitle = (result: SearchResult): string => {
    switch (result.type) {
      case 'user':
        const user = result.data as User;
        return `${user.first_name} ${user.last_name} (@${user.username})`;
      case 'event':
        return (result.data as Event).title;
      case 'marketplace':
        return (result.data as MarketplaceItem).title;
      case 'track':
        return (result.data as Track).name;
      case 'callout':
        const callout = result.data as Callout;
        return `Callout: ${callout.challenger.username} vs ${callout.challenged.username}`;
      default:
        return '';
    }
  };

  const getResultSubtitle = (result: SearchResult): string => {
    switch (result.type) {
      case 'user':
        return 'Racer';
      case 'event':
        const event = result.data as Event;
        return `${event.event_type} • ${new Date(event.start_date).toLocaleDateString()}`;
      case 'marketplace':
        const item = result.data as MarketplaceItem;
        return `${item.category} • $${item.price}`;
      case 'track':
        return (result.data as Track).location;
      case 'callout':
        const callout = result.data as Callout;
        return `${callout.race_type} • ${callout.status}`;
      default:
        return '';
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

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Advanced Search</h1>
        <p className="text-gray-600">Find racers, events, tracks, marketplace items, and more</p>
      </div>

      {/* Search Bar */}
      <div className="mb-6">
        <div className="relative">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for racers, events, tracks, marketplace items, callouts..."
            className="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 p-1"
          >
            <AdjustmentsHorizontalIcon className="w-5 h-5 text-gray-400" />
          </button>
        </div>
      </div>

      {/* Filters */}
      {showFilters && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
            {hasActiveFilters() && (
              <button
                onClick={clearFilters}
                className="text-sm text-primary-600 hover:text-primary-700"
              >
                Clear all
              </button>
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
              <select
                value={filters.category}
                onChange={(e) => setFilters({ ...filters, category: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">All Categories</option>
                <option value="user">Racers</option>
                <option value="event">Events</option>
                <option value="marketplace">Marketplace</option>
                <option value="track">Tracks</option>
                <option value="callout">Callouts</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
              <input
                type="text"
                value={filters.location}
                onChange={(e) => setFilters({ ...filters, location: e.target.value })}
                placeholder="City, State"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Price Range</label>
              <select
                value={filters.priceRange}
                onChange={(e) => setFilters({ ...filters, priceRange: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Any Price</option>
                <option value="0-1000">Under $1,000</option>
                <option value="1000-5000">$1,000 - $5,000</option>
                <option value="5000-10000">$5,000 - $10,000</option>
                <option value="10000-50000">$10,000 - $50,000</option>
                <option value="50000-999999">$50,000+</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select
                value={filters.status}
                onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Any Status</option>
                <option value="pending">Pending</option>
                <option value="accepted">Accepted</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'all', label: 'All Results', count: results.length },
              { id: 'users', label: 'Racers', count: results.filter(r => r.type === 'user').length },
              { id: 'events', label: 'Events', count: results.filter(r => r.type === 'event').length },
              { id: 'marketplace', label: 'Marketplace', count: results.filter(r => r.type === 'marketplace').length },
              { id: 'tracks', label: 'Tracks', count: results.filter(r => r.type === 'track').length },
              { id: 'callouts', label: 'Callouts', count: results.filter(r => r.type === 'callout').length },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label} ({tab.count})
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Results */}
      <div className="space-y-4">
        {isLoading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          </div>
        ) : results.length === 0 ? (
          <div className="text-center py-12">
            <MagnifyingGlassIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {searchQuery ? 'No results found' : 'Start searching to find what you need'}
            </h3>
            <p className="text-gray-600">
              {searchQuery 
                ? 'Try adjusting your search terms or filters'
                : 'Search for racers, events, tracks, marketplace items, and callouts'
              }
            </p>
          </div>
        ) : (
          results
            .filter(result => activeTab === 'all' || result.type === activeTab)
            .map((result) => (
              <Link
                key={`${result.type}-${result.data.id}`}
                to={getResultLink(result)}
                className="block bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                      {getResultIcon(result.type)}
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-lg font-medium text-gray-900 truncate">
                      {getResultTitle(result)}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {getResultSubtitle(result)}
                    </p>
                    {result.type === 'marketplace' && (
                      <p className="text-sm text-gray-500 mt-1">
                        Location: {(result.data as MarketplaceItem).location}
                      </p>
                    )}
                  </div>
                  <div className="flex-shrink-0">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                      {result.type.charAt(0).toUpperCase() + result.type.slice(1)}
                    </span>
                  </div>
                </div>
              </Link>
            ))
        )}
      </div>
    </div>
  );
} 