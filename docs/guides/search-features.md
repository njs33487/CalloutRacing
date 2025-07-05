# Advanced Search and Find Features

## Overview

CalloutRacing provides comprehensive search functionality across all major entities in the application. The search system includes both a global search bar in the header and a dedicated advanced search page with filtering capabilities.

## Features

### 1. Global Search Bar

**Location**: Header of the main application layout
**Purpose**: Quick search with instant results

#### Features:
- **Real-time search**: Results appear as you type (debounced at 300ms)
- **Keyboard navigation**: Use arrow keys to navigate results, Enter to select, Escape to close
- **Click outside to close**: Automatically closes when clicking outside the search area
- **Quick results**: Shows up to 8 most relevant results across all categories
- **Direct navigation**: Click any result to go directly to that item

#### Search Categories:
- **Racers**: Search by username, first name, or last name
- **Events**: Search by title, description, or event type
- **Marketplace**: Search by title, description, or category
- **Tracks**: Search by name, location, or description
- **Callouts**: Search by message content or race type

### 2. Advanced Search Page

**Location**: `/app/search`
**Purpose**: Comprehensive search with advanced filtering

#### Features:
- **Full search results**: Shows all matching results with pagination
- **Advanced filters**: Filter by category, location, price range, status, etc.
- **Tabbed results**: View results by category (All, Racers, Events, Marketplace, Tracks, Callouts)
- **URL persistence**: Search queries are saved in the URL for sharing and bookmarking
- **Relevance scoring**: Results are sorted by relevance to the search query

#### Available Filters:
- **Category**: Filter by specific content type
- **Location**: Filter by city, state, or location
- **Price Range**: Filter marketplace items by price
- **Status**: Filter callouts by status (pending, accepted, completed, cancelled)
- **Date Range**: Filter events by date (coming soon)

### 3. Backend Search API

**Endpoint**: `/api/search/`
**Method**: GET
**Authentication**: Required

#### Query Parameters:
- `q` (required): Search query string (minimum 2 characters)
- `category` (optional): Filter by category (users, events, marketplace, tracks, callouts)
- `limit` (optional): Maximum results per category (default: 10)

#### Response Format:
```json
{
  "users": [...],
  "events": [...],
  "marketplace": [...],
  "tracks": [...],
  "callouts": [...],
  "total_results": 25
}
```

## Search Algorithm

### Relevance Scoring

The search system uses a multi-factor relevance scoring algorithm:

1. **Exact match**: 100 points for exact string matches
2. **Contains match**: 50 points for partial string matches
3. **Word matching**: 30 points for matching individual words
4. **Category weighting**: Different weights for different content types

### Search Fields by Entity

#### Users
- Username
- First name
- Last name

#### Events
- Title
- Description
- Event type

#### Marketplace Items
- Title
- Description
- Category

#### Tracks
- Name
- Location
- Description

#### Callouts
- Message content
- Race type

## Usage Examples

### Basic Search
1. Type in the global search bar: "drag race"
2. Results will show events, tracks, and callouts related to drag racing
3. Click on any result to navigate directly

### Advanced Search
1. Navigate to `/app/search`
2. Enter search query: "mustang"
3. Use filters to narrow results:
   - Category: Marketplace
   - Price Range: $10,000 - $50,000
4. View results in the Marketplace tab

### URL-based Search
- Direct link: `/app/search?q=quarter%20mile`
- Shareable search results
- Bookmarkable searches

## Performance Optimizations

### Frontend
- **Debounced search**: Prevents excessive API calls while typing
- **Cached results**: Recent search results are cached
- **Lazy loading**: Results load progressively
- **Virtual scrolling**: For large result sets (coming soon)

### Backend
- **Database indexing**: Optimized indexes on search fields
- **Query optimization**: Efficient SQL queries with proper joins
- **Result limiting**: Configurable limits to prevent performance issues
- **Caching**: Redis caching for frequent searches (coming soon)

## Future Enhancements

### Planned Features
1. **Full-text search**: PostgreSQL full-text search integration
2. **Search suggestions**: Autocomplete and search suggestions
3. **Search analytics**: Track popular searches and improve relevance
4. **Advanced filters**: More granular filtering options
5. **Search history**: Save and manage search history
6. **Saved searches**: Save frequently used search queries
7. **Search alerts**: Get notified when new items match saved searches

### Technical Improvements
1. **Elasticsearch integration**: For better search performance and features
2. **Fuzzy matching**: Handle typos and similar terms
3. **Semantic search**: Understand search intent and context
4. **Search ranking**: Machine learning-based result ranking
5. **Multi-language support**: Search in multiple languages

## API Documentation

### Global Search Endpoint

```http
GET /api/search/?q={query}&category={category}&limit={limit}
```

#### Example Request:
```http
GET /api/search/?q=drag%20race&category=events&limit=5
```

#### Example Response:
```json
{
  "users": [],
  "events": [
    {
      "id": 1,
      "title": "Drag Racing Championship",
      "description": "Quarter mile drag racing event",
      "event_type": "championship",
      "start_date": "2024-06-15T18:00:00Z",
      "track": {
        "id": 1,
        "name": "Speedway Drag Strip",
        "location": "Daytona, FL"
      }
    }
  ],
  "marketplace": [],
  "tracks": [],
  "callouts": [],
  "total_results": 1
}
```

### Error Handling

The search API returns appropriate HTTP status codes:

- `200 OK`: Successful search with results
- `400 Bad Request`: Invalid search parameters
- `401 Unauthorized`: Authentication required
- `500 Internal Server Error`: Server error

## Troubleshooting

### Common Issues

1. **No results found**
   - Check spelling and try different keywords
   - Use broader search terms
   - Check if the content exists in the system

2. **Slow search performance**
   - Reduce search query length
   - Use more specific terms
   - Check network connection

3. **Search not working**
   - Ensure you're authenticated
   - Check browser console for errors
   - Verify API endpoint is accessible

### Debug Mode

Enable debug mode to see search queries and performance metrics:

```javascript
// In browser console
localStorage.setItem('debug_search', 'true');
```

## Contributing

To contribute to the search functionality:

1. Follow the existing code patterns
2. Add appropriate tests for new features
3. Update documentation for any changes
4. Consider performance implications
5. Test with various search scenarios

## Support

For issues or questions about the search functionality:

1. Check this documentation first
2. Review the troubleshooting section
3. Contact the development team
4. Create an issue in the project repository 