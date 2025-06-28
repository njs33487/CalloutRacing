import { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { MagnifyingGlassIcon, UserIcon, CalendarIcon, MapPinIcon, ShoppingBagIcon, BoltIcon } from '@heroicons/react/24/outline';
import { searchAPI } from '../services/api';
import { User, Event, MarketplaceItem, Track, Callout } from '../types';

interface SearchResult {
  type: 'user' | 'event' | 'marketplace' | 'track' | 'callout';
  data: User | Event | MarketplaceItem | Track | Callout;
  relevance: number;
}

interface GlobalSearchResponse {
  users: User[];
  events: Event[];
  marketplace: MarketplaceItem[];
  tracks: Track[];
  callouts: Callout[];
  total_results: number;
}

export default function GlobalSearchBar() {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const searchRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  // Debounced search effect
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchQuery.trim().length >= 2) {
        performSearch();
      } else {
        setResults([]);
        setShowResults(false);
      }
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [searchQuery]);

  // Handle click outside to close results
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowResults(false);
        setSelectedIndex(-1);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Handle keyboard navigation
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (!showResults) return;

      switch (event.key) {
        case 'ArrowDown':
          event.preventDefault();
          setSelectedIndex(prev => 
            prev < results.length - 1 ? prev + 1 : prev
          );
          break;
        case 'ArrowUp':
          event.preventDefault();
          setSelectedIndex(prev => prev > 0 ? prev - 1 : -1);
          break;
        case 'Enter':
          event.preventDefault();
          if (selectedIndex >= 0 && selectedIndex < results.length) {
            handleResultClick(results[selectedIndex]);
          }
          break;
        case 'Escape':
          setShowResults(false);
          setSelectedIndex(-1);
          break;
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [showResults, results, selectedIndex]);

  const performSearch = async () => {
    setIsLoading(true);
    try {
      const query = searchQuery.trim();
      const response = await searchAPI.globalSearch(query, undefined, 8);
      const data: GlobalSearchResponse = response.data;
      
      // Convert the response to SearchResult format
      const searchResults: SearchResult[] = [
        ...data.users.slice(0, 3).map(user => ({
          type: 'user' as const,
          data: user,
          relevance: calculateRelevance(query, user.username + ' ' + user.first_name + ' ' + user.last_name)
        })),
        ...data.events.slice(0, 2).map(event => ({
          type: 'event' as const,
          data: event,
          relevance: calculateRelevance(query, event.title + ' ' + event.description)
        })),
        ...data.marketplace.slice(0, 2).map(item => ({
          type: 'marketplace' as const,
          data: item,
          relevance: calculateRelevance(query, item.title + ' ' + item.description)
        })),
        ...data.tracks.slice(0, 1).map(track => ({
          type: 'track' as const,
          data: track,
          relevance: calculateRelevance(query, track.name + ' ' + track.location)
        }))
      ];
      
      // Sort by relevance
      searchResults.sort((a, b) => b.relevance - a.relevance);
      
      setResults(searchResults);
      setShowResults(searchResults.length > 0);
      setSelectedIndex(-1);
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
      setShowResults(false);
    } finally {
      setIsLoading(false);
    }
  };

  const calculateRelevance = (query: string, text: string): number => {
    const queryLower = query.toLowerCase();
    const textLower = text.toLowerCase();
    
    if (textLower.startsWith(queryLower)) return 100;
    if (textLower.includes(queryLower)) return 50;
    
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

  const getResultIcon = (type: string) => {
    switch (type) {
      case 'user':
        return <UserIcon className="w-4 h-4" />;
      case 'event':
        return <CalendarIcon className="w-4 h-4" />;
      case 'marketplace':
        return <ShoppingBagIcon className="w-4 h-4" />;
      case 'track':
        return <MapPinIcon className="w-4 h-4" />;
      case 'callout':
        return <BoltIcon className="w-4 h-4" />;
      default:
        return <MagnifyingGlassIcon className="w-4 h-4" />;
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
        return `${user.first_name} ${user.last_name}`;
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
        const user = result.data as User;
        return `@${user.username}`;
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

  const handleResultClick = (result: SearchResult) => {
    navigate(getResultLink(result));
    setShowResults(false);
    setSearchQuery('');
    setResults([]);
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/app/search?q=${encodeURIComponent(searchQuery.trim())}`);
      setShowResults(false);
      setSearchQuery('');
      setResults([]);
    }
  };

  return (
    <div ref={searchRef} className="relative flex-1 max-w-lg mx-4">
      <form onSubmit={handleSearchSubmit}>
        <div className="relative">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search racers, events, tracks, marketplace..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
          />
          {isLoading && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
            </div>
          )}
        </div>
      </form>

      {/* Search Results Dropdown */}
      {showResults && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white rounded-lg shadow-lg border border-gray-200 z-50 max-h-96 overflow-y-auto">
          {results.length === 0 ? (
            <div className="p-4 text-center text-gray-500 text-sm">
              No results found
            </div>
          ) : (
            <>
              {results.map((result, index) => (
                <button
                  key={`${result.type}-${result.data.id}`}
                  onClick={() => handleResultClick(result)}
                  className={`w-full p-3 text-left hover:bg-gray-50 flex items-center space-x-3 ${
                    index === selectedIndex ? 'bg-gray-50' : ''
                  } ${index === results.length - 1 ? '' : 'border-b border-gray-100'}`}
                >
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
                      {getResultIcon(result.type)}
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-gray-900 truncate">
                      {getResultTitle(result)}
                    </div>
                    <div className="text-xs text-gray-500 truncate">
                      {getResultSubtitle(result)}
                    </div>
                  </div>
                  <div className="flex-shrink-0">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                      {result.type.charAt(0).toUpperCase() + result.type.slice(1)}
                    </span>
                  </div>
                </button>
              ))}
              
              {/* View All Results Link */}
              <div className="p-3 border-t border-gray-100">
                <Link
                  to={`/app/search?q=${encodeURIComponent(searchQuery.trim())}`}
                  className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                  onClick={() => {
                    setShowResults(false);
                    setSearchQuery('');
                    setResults([]);
                  }}
                >
                  View all results →
                </Link>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
} 