import { Link } from 'react-router-dom';
import { 
  UserIcon, 
  CalendarIcon, 
  MapPinIcon, 
  BoltIcon, 
  ShoppingBagIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import { User, Event, MarketplaceItem, Track, Callout } from '../../types';

interface SearchResult {
  type: 'user' | 'event' | 'marketplace' | 'track' | 'callout';
  data: User | Event | MarketplaceItem | Track | Callout;
  relevance: number;
}

interface SearchResultsProps {
  results: SearchResult[];
  isLoading: boolean;
  searchQuery: string;
}

export default function SearchResults({ results, isLoading, searchQuery }: SearchResultsProps) {
  const getResultIcon = (type: string) => {
    switch (type) {
      case 'user':
        return <UserIcon className="w-5 h-5 text-blue-600" />;
      case 'event':
        return <CalendarIcon className="w-5 h-5 text-green-600" />;
      case 'marketplace':
        return <ShoppingBagIcon className="w-5 h-5 text-purple-600" />;
      case 'track':
        return <MapPinIcon className="w-5 h-5 text-red-600" />;
      case 'callout':
        return <BoltIcon className="w-5 h-5 text-yellow-600" />;
      default:
        return <ClockIcon className="w-5 h-5 text-gray-600" />;
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
        return (result.data as User).username;
      case 'event':
        return (result.data as Event).title;
      case 'marketplace':
        return (result.data as MarketplaceItem).title;
      case 'track':
        return (result.data as Track).name;
      case 'callout':
        return `Callout: ${(result.data as Callout).challenger} vs ${(result.data as Callout).challenged}`;
      default:
        return 'Unknown';
    }
  };

  const getResultSubtitle = (result: SearchResult): string => {
    switch (result.type) {
      case 'user':
        const user = result.data as User;
        return `${user.first_name} ${user.last_name}`;
      case 'event':
        const event = result.data as Event;
        return `${event.event_type} • ${new Date(event.start_date).toLocaleDateString()}`;
      case 'marketplace':
        const item = result.data as MarketplaceItem;
        return `${item.category} • $${item.price}`;
      case 'track':
        const track = result.data as Track;
        return `${track.track_type} • ${track.location}`;
      case 'callout':
        const callout = result.data as Callout;
        return `${callout.race_type} • ${callout.location_type}`;
      default:
        return '';
    }
  };

  const getLocation = (result: SearchResult): string => {
    switch (result.type) {
      case 'user':
        return (result.data as any).location || 'Location not specified';
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

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(6)].map((_, index) => (
          <div key={index} className="bg-white rounded-lg border border-gray-200 p-4 animate-pulse">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-gray-300 rounded-full"></div>
              <div className="flex-1">
                <div className="h-4 bg-gray-300 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-300 rounded w-1/2"></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (results.length === 0 && searchQuery.trim()) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 text-lg mb-2">No results found</div>
        <div className="text-gray-400 text-sm">
          Try adjusting your search terms or filters
        </div>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 text-lg mb-2">Start searching</div>
        <div className="text-gray-400 text-sm">
          Enter a search term to find users, events, marketplace items, tracks, and callouts
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {results.map((result, index) => (
        <Link
          key={`${result.type}-${result.data.id}-${index}`}
          to={getResultLink(result)}
          className="block bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow duration-200"
        >
          <div className="flex items-center space-x-4">
            <div className="flex-shrink-0">
              {getResultIcon(result.type)}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-medium text-gray-900 truncate">
                  {getResultTitle(result)}
                </h3>
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full capitalize">
                  {result.type}
                </span>
              </div>
              <p className="text-sm text-gray-600 mt-1">
                {getResultSubtitle(result)}
              </p>
              <div className="flex items-center mt-2 text-xs text-gray-500">
                <MapPinIcon className="w-3 h-3 mr-1" />
                <span className="truncate">{getLocation(result)}</span>
              </div>
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
} 