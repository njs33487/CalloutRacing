# Events Slice Documentation

## Overview

The Events Slice provides comprehensive state management for all event-related functionality in the CalloutRacing application. It handles events, user events, featured events, upcoming events, and event statistics.

## Features

### **State Management**
- **Events**: All events with pagination and filtering
- **User Events**: Events where user is organizer or participant
- **Featured Events**: Highlighted events for promotion
- **Upcoming Events**: Future events for quick access
- **Current Event**: Currently viewed event details
- **Event Statistics**: Analytics and metrics

### **Advanced Filtering**
- Event type filtering (race, meet, show, competition, track_day, drift_event)
- Date range filtering
- Location-based filtering
- Price range filtering
- Public/private event filtering
- Featured event filtering
- Organizer filtering

### **CRUD Operations**
- Create, read, update, delete events
- Join/leave events
- Real-time participant count updates
- Event statistics calculation

## State Structure

```typescript
interface EventsState {
  events: Event[];
  userEvents: Event[];
  featuredEvents: Event[];
  upcomingEvents: Event[];
  pastEvents: Event[];
  currentEvent: Event | null;
  filters: EventFilters;
  stats: EventStats | null;
  pagination: {
    page: number;
    hasMore: boolean;
    loading: boolean;
  };
  loading: boolean;
  error: string | null;
}
```

## Event Interface

```typescript
interface Event {
  id: number;
  title: string;
  description: string;
  event_type: 'race' | 'meet' | 'show' | 'competition' | 'track_day' | 'drift_event';
  location: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  latitude: number;
  longitude: number;
  start_date: string;
  end_date: string;
  start_time: string;
  end_time: string;
  organizer: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
  };
  participants: Array<{
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    joined_at: string;
  }>;
  max_participants: number;
  current_participants: number;
  entry_fee: number;
  is_public: boolean;
  is_active: boolean;
  is_featured: boolean;
  rules: string;
  requirements: string;
  prizes: string;
  images: string[];
  tags: string[];
  created_at: string;
  updated_at: string;
}
```

## Async Thunks

### **Fetch Events**
```typescript
export const fetchEvents = createAsyncThunk(
  'events/fetchEvents',
  async ({ page = 1, refresh = false }, { getState, rejectWithValue }) => {
    // Fetches events with current filters and pagination
  }
);
```

### **Fetch User Events**
```typescript
export const fetchUserEvents = createAsyncThunk(
  'events/fetchUserEvents',
  async (_, { rejectWithValue }) => {
    // Fetches events where user is organizer or participant
  }
);
```

### **Fetch Featured Events**
```typescript
export const fetchFeaturedEvents = createAsyncThunk(
  'events/fetchFeaturedEvents',
  async (_, { rejectWithValue }) => {
    // Fetches events marked as featured
  }
);
```

### **Fetch Upcoming Events**
```typescript
export const fetchUpcomingEvents = createAsyncThunk(
  'events/fetchUpcomingEvents',
  async (_, { rejectWithValue }) => {
    // Fetches future events
  }
);
```

### **Event CRUD Operations**
```typescript
export const createEvent = createAsyncThunk(...);
export const updateEvent = createAsyncThunk(...);
export const deleteEvent = createAsyncThunk(...);
export const fetchEventById = createAsyncThunk(...);
```

### **Event Participation**
```typescript
export const joinEvent = createAsyncThunk(...);
export const leaveEvent = createAsyncThunk(...);
```

### **Event Statistics**
```typescript
export const fetchEventStats = createAsyncThunk(
  'events/fetchEventStats',
  async (_, { rejectWithValue }) => {
    // Calculates and returns event statistics
  }
);
```

## Actions

### **Filter Actions**
```typescript
setEventTypeFilter: (eventType: string) => void;
setDateRangeFilter: (dateRange: [Date | null, Date | null]) => void;
setLocationFilter: (location: string) => void;
setPriceRangeFilter: (priceRange: [number, number]) => void;
setPublicFilter: (isPublic: boolean | null) => void;
setFeaturedFilter: (isFeatured: boolean | null) => void;
setOrganizerFilter: (organizerId: number | null) => void;
clearFilters: () => void;
```

### **State Actions**
```typescript
setCurrentEvent: (event: Event | null) => void;
clearError: () => void;
updateEventParticipantCount: (eventId: number, count: number) => void;
```

## Usage Examples

### **1. Fetch Events with Filters**
```typescript
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { fetchEvents, setEventTypeFilter } from '../store/slices/eventsSlice';

const EventsComponent = () => {
  const dispatch = useAppDispatch();
  const { events, loading, pagination } = useAppSelector(state => state.events);

  useEffect(() => {
    dispatch(fetchEvents({ page: 1, refresh: true }));
  }, [dispatch]);

  const handleFilterChange = (eventType: string) => {
    dispatch(setEventTypeFilter(eventType));
    dispatch(fetchEvents({ page: 1, refresh: true }));
  };

  return (
    <div>
      {loading ? <LoadingSpinner /> : (
        <div>
          {events.map(event => (
            <EventCard key={event.id} event={event} />
          ))}
        </div>
      )}
    </div>
  );
};
```

### **2. Create New Event**
```typescript
import { createEvent } from '../store/slices/eventsSlice';

const CreateEventForm = () => {
  const dispatch = useAppDispatch();

  const handleSubmit = async (eventData: Partial<Event>) => {
    try {
      await dispatch(createEvent(eventData)).unwrap();
      // Navigate to events list or show success message
    } catch (error) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
    </form>
  );
};
```

### **3. Join/Leave Event**
```typescript
import { joinEvent, leaveEvent } from '../store/slices/eventsSlice';

const EventCard = ({ event }: { event: Event }) => {
  const dispatch = useAppDispatch();
  const { user } = useAppSelector(state => state.auth);

  const isParticipant = event.participants.some(p => p.id === user?.id);

  const handleJoin = async () => {
    try {
      await dispatch(joinEvent(event.id)).unwrap();
      // Show success message
    } catch (error) {
      // Handle error
    }
  };

  const handleLeave = async () => {
    try {
      await dispatch(leaveEvent(event.id)).unwrap();
      // Show success message
    } catch (error) {
      // Handle error
    }
  };

  return (
    <div>
      <h3>{event.title}</h3>
      <p>{event.description}</p>
      <p>Participants: {event.current_participants}/{event.max_participants}</p>
      {!isParticipant ? (
        <button onClick={handleJoin}>Join Event</button>
      ) : (
        <button onClick={handleLeave}>Leave Event</button>
      )}
    </div>
  );
};
```

### **4. Event Statistics Dashboard**
```typescript
import { fetchEventStats } from '../store/slices/eventsSlice';

const EventStatsDashboard = () => {
  const dispatch = useAppDispatch();
  const { stats } = useAppSelector(state => state.events);

  useEffect(() => {
    dispatch(fetchEventStats());
  }, [dispatch]);

  return (
    <div className="stats-dashboard">
      <div className="stat-card">
        <h3>Total Events</h3>
        <p>{stats?.total_events || 0}</p>
      </div>
      <div className="stat-card">
        <h3>Upcoming Events</h3>
        <p>{stats?.upcoming_events || 0}</p>
      </div>
      <div className="stat-card">
        <h3>Events This Month</h3>
        <p>{stats?.events_this_month || 0}</p>
      </div>
      <div className="stat-card">
        <h3>Average Participants</h3>
        <p>{stats?.average_participants?.toFixed(1) || 0}</p>
      </div>
    </div>
  );
};
```

### **5. Advanced Filtering**
```typescript
import { 
  setEventTypeFilter, 
  setDateRangeFilter, 
  setLocationFilter,
  clearFilters 
} from '../store/slices/eventsSlice';

const EventFilters = () => {
  const dispatch = useAppDispatch();
  const { filters } = useAppSelector(state => state.events);

  const handleEventTypeChange = (eventType: string) => {
    dispatch(setEventTypeFilter(eventType));
  };

  const handleDateRangeChange = (startDate: Date | null, endDate: Date | null) => {
    dispatch(setDateRangeFilter([startDate, endDate]));
  };

  const handleLocationChange = (location: string) => {
    dispatch(setLocationFilter(location));
  };

  const handleClearFilters = () => {
    dispatch(clearFilters());
  };

  return (
    <div className="filters">
      <select 
        value={filters.event_type} 
        onChange={(e) => handleEventTypeChange(e.target.value)}
      >
        <option value="all">All Types</option>
        <option value="race">Race</option>
        <option value="meet">Meet</option>
        <option value="show">Show</option>
        <option value="competition">Competition</option>
        <option value="track_day">Track Day</option>
        <option value="drift_event">Drift Event</option>
      </select>

      <input 
        type="text" 
        placeholder="Location"
        value={filters.location}
        onChange={(e) => handleLocationChange(e.target.value)}
      />

      <button onClick={handleClearFilters}>Clear Filters</button>
    </div>
  );
};
```

## Benefits

### **1. Centralized Event Management**
- All event-related state in one place
- Consistent data structure across components
- Easy to maintain and debug

### **2. Advanced Filtering**
- Multiple filter types for precise event discovery
- Real-time filter updates
- Persistent filter state

### **3. Performance Optimization**
- Pagination for large event lists
- Selective re-rendering with useSelector
- Memoized selectors for expensive computations

### **4. Real-time Updates**
- Automatic participant count updates
- Live event status changes
- Instant UI feedback

### **5. Comprehensive Statistics**
- Event analytics and metrics
- Dashboard-ready data
- Performance insights

## Integration with Other Slices

### **Auth Slice Integration**
```typescript
// Use user ID from auth state for user-specific operations
const { user } = useAppSelector(state => state.auth);
const userEvents = events.filter(event => 
  event.organizer.id === user?.id || 
  event.participants.some(p => p.id === user?.id)
);
```

### **UI Slice Integration**
```typescript
// Use UI state for modals and notifications
const dispatch = useAppDispatch();
const { showSuccess, showError } = useAppSelector(state => state.ui);

const handleCreateEvent = async (eventData) => {
  try {
    await dispatch(createEvent(eventData)).unwrap();
    dispatch(showSuccess('Event created successfully!'));
  } catch (error) {
    dispatch(showError('Failed to create event'));
  }
};
```

## Best Practices

1. **Use Typed Hooks**: Always use `useAppDispatch` and `useAppSelector`
2. **Handle Loading States**: Check loading state before rendering
3. **Error Handling**: Implement proper error handling for async operations
4. **Optimistic Updates**: Update UI immediately for better UX
5. **Pagination**: Use pagination for large datasets
6. **Filter Persistence**: Consider persisting filters in localStorage

## Future Enhancements

1. **Real-time Updates**: WebSocket integration for live event updates
2. **Offline Support**: Cache events for offline viewing
3. **Advanced Analytics**: More detailed event statistics
4. **Event Recommendations**: AI-powered event suggestions
5. **Social Features**: Event sharing and social interactions 