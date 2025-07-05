import React from 'react';

interface Event {
  id: number;
  name: string;
  date: string;
  location: string;
  is_sponsored: boolean;
  sponsor_name?: string;
  sponsor_logo_url?: string;
  sponsor_website_url?: string;
}

interface EventCardProps {
  event: Event;
}

const EventCard: React.FC<EventCardProps> = ({ event }) => {
  return (
    <div className="event-card bg-white rounded-lg shadow-md p-6 border border-gray-200">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{event.name}</h3>
      <p className="text-gray-600 mb-3">{event.date} - {event.location}</p>
      
      {event.is_sponsored && event.sponsor_name && (
        <div className="sponsor-info bg-blue-50 border border-blue-200 rounded-md p-3 mb-4">
          <p className="text-sm text-blue-700 mb-2">Sponsored by:</p>
          <div className="flex items-center space-x-3">
            {event.sponsor_logo_url && (
              <a 
                href={event.sponsor_website_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex-shrink-0"
              >
                <img 
                  src={event.sponsor_logo_url} 
                  alt={event.sponsor_name} 
                  className="h-8 w-auto object-contain"
                />
              </a>
            )}
            {event.sponsor_website_url && (
              <a 
                href={event.sponsor_website_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 font-medium"
              >
                {event.sponsor_name}
              </a>
            )}
            {!event.sponsor_logo_url && !event.sponsor_website_url && (
              <span className="text-blue-700 font-medium">{event.sponsor_name}</span>
            )}
          </div>
        </div>
      )}
      
      <div className="flex justify-between items-center">
        <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors">
          View Details
        </button>
        <span className="text-sm text-gray-500">
          {event.is_sponsored ? 'Sponsored Event' : 'Community Event'}
        </span>
      </div>
    </div>
  );
};

export default EventCard; 