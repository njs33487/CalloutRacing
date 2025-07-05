import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { eventAPI } from '../../services/api';

// Interfaces
export interface Event {
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

export interface EventFilters {
  event_type: string;
  date_range: [Date | null, Date | null];
  location: string;
  price_range: [number, number];
  is_public: boolean | null;
  is_featured: boolean | null;
  organizer_id: number | null;
}

export interface EventStats {
  total_events: number;
  upcoming_events: number;
  past_events: number;
  events_this_month: number;
  average_participants: number;
  total_participants: number;
}

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

const initialState: EventsState = {
  events: [],
  userEvents: [],
  featuredEvents: [],
  upcomingEvents: [],
  pastEvents: [],
  currentEvent: null,
  filters: {
    event_type: 'all',
    date_range: [null, null],
    location: '',
    price_range: [0, 1000],
    is_public: null,
    is_featured: null,
    organizer_id: null,
  },
  stats: null,
  pagination: {
    page: 1,
    hasMore: true,
    loading: false,
  },
  loading: false,
  error: null,
};

// Async thunks
export const fetchEvents = createAsyncThunk(
  'events/fetchEvents',
  async ({ page = 1, refresh = false }: { page?: number; refresh?: boolean }, { getState, rejectWithValue }) => {
    try {
      const state = getState() as any;
      const { filters } = state.events;
      
      const params = new URLSearchParams({
        page: page.toString(),
        ...(filters.event_type !== 'all' && { event_type: filters.event_type }),
        ...(filters.location && { location: filters.location }),
        ...(filters.price_range[0] > 0 && { min_fee: filters.price_range[0].toString() }),
        ...(filters.price_range[1] < 1000 && { max_fee: filters.price_range[1].toString() }),
        ...(filters.is_public !== null && { is_public: filters.is_public.toString() }),
        ...(filters.is_featured !== null && { is_featured: filters.is_featured.toString() }),
        ...(filters.organizer_id && { organizer_id: filters.organizer_id.toString() }),
      });

      const response = await eventAPI.list();
      const events = response.data.results || response.data;
      
      return {
        events,
        page,
        refresh,
        hasMore: events.length === 20, // Assuming page size is 20
      };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch events');
    }
  }
);

export const fetchUserEvents = createAsyncThunk(
  'events/fetchUserEvents',
  async (_, { rejectWithValue }) => {
    try {
      const response = await eventAPI.list();
      // Filter events where user is organizer or participant
      const events = response.data.results || response.data;
      return events.filter((event: Event) => 
        event.organizer.id === 1 || // Replace with actual user ID from auth
        event.participants.some(p => p.id === 1) // Replace with actual user ID from auth
      );
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch user events');
    }
  }
);

export const fetchFeaturedEvents = createAsyncThunk(
  'events/fetchFeaturedEvents',
  async (_, { rejectWithValue }) => {
    try {
      const response = await eventAPI.list();
      const events = response.data.results || response.data;
      return events.filter((event: Event) => event.is_featured);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch featured events');
    }
  }
);

export const fetchUpcomingEvents = createAsyncThunk(
  'events/fetchUpcomingEvents',
  async (_, { rejectWithValue }) => {
    try {
      const response = await eventAPI.list();
      const events = response.data.results || response.data;
      const now = new Date();
      return events.filter((event: Event) => new Date(event.start_date) > now);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch upcoming events');
    }
  }
);

export const fetchEventById = createAsyncThunk(
  'events/fetchEventById',
  async (eventId: number, { rejectWithValue }) => {
    try {
      const response = await eventAPI.get(eventId);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch event');
    }
  }
);

export const createEvent = createAsyncThunk(
  'events/createEvent',
  async (eventData: Partial<Event>, { rejectWithValue }) => {
    try {
      const response = await eventAPI.create(eventData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to create event');
    }
  }
);

export const updateEvent = createAsyncThunk(
  'events/updateEvent',
  async ({ id, data }: { id: number; data: Partial<Event> }, { rejectWithValue }) => {
    try {
      const response = await eventAPI.update(id, data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to update event');
    }
  }
);

export const deleteEvent = createAsyncThunk(
  'events/deleteEvent',
  async (eventId: number, { rejectWithValue }) => {
    try {
      await eventAPI.delete(eventId);
      return eventId;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to delete event');
    }
  }
);

export const joinEvent = createAsyncThunk(
  'events/joinEvent',
  async (eventId: number, { rejectWithValue }) => {
    try {
      await eventAPI.join(eventId);
      return eventId;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to join event');
    }
  }
);

export const leaveEvent = createAsyncThunk(
  'events/leaveEvent',
  async (eventId: number, { rejectWithValue }) => {
    try {
      await eventAPI.leave(eventId);
      return eventId;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to leave event');
    }
  }
);

export const fetchEventStats = createAsyncThunk(
  'events/fetchEventStats',
  async (_, { rejectWithValue }) => {
    try {
      // This would be a custom API endpoint for event statistics
      const response = await eventAPI.list();
      const events = response.data.results || response.data;
      
      const now = new Date();
      const thisMonth = new Date(now.getFullYear(), now.getMonth(), 1);
      
      const stats: EventStats = {
        total_events: events.length,
        upcoming_events: events.filter((e: Event) => new Date(e.start_date) > now).length,
        past_events: events.filter((e: Event) => new Date(e.start_date) < now).length,
        events_this_month: events.filter((e: Event) => new Date(e.start_date) >= thisMonth).length,
        average_participants: events.length > 0 
          ? events.reduce((sum: number, e: Event) => sum + e.current_participants, 0) / events.length 
          : 0,
        total_participants: events.reduce((sum: number, e: Event) => sum + e.current_participants, 0),
      };
      
      return stats;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch event stats');
    }
  }
);

// Events slice
const eventsSlice = createSlice({
  name: 'events',
  initialState,
  reducers: {
    setEventTypeFilter: (state, action: PayloadAction<string>) => {
      state.filters.event_type = action.payload;
      state.pagination.page = 1;
      state.events = [];
    },
    setDateRangeFilter: (state, action: PayloadAction<[Date | null, Date | null]>) => {
      state.filters.date_range = action.payload;
      state.pagination.page = 1;
      state.events = [];
    },
    setLocationFilter: (state, action: PayloadAction<string>) => {
      state.filters.location = action.payload;
      state.pagination.page = 1;
      state.events = [];
    },
    setPriceRangeFilter: (state, action: PayloadAction<[number, number]>) => {
      state.filters.price_range = action.payload;
      state.pagination.page = 1;
      state.events = [];
    },
    setPublicFilter: (state, action: PayloadAction<boolean | null>) => {
      state.filters.is_public = action.payload;
      state.pagination.page = 1;
      state.events = [];
    },
    setFeaturedFilter: (state, action: PayloadAction<boolean | null>) => {
      state.filters.is_featured = action.payload;
      state.pagination.page = 1;
      state.events = [];
    },
    setOrganizerFilter: (state, action: PayloadAction<number | null>) => {
      state.filters.organizer_id = action.payload;
      state.pagination.page = 1;
      state.events = [];
    },
    clearFilters: (state) => {
      state.filters = initialState.filters;
      state.pagination.page = 1;
      state.events = [];
    },
    setCurrentEvent: (state, action: PayloadAction<Event | null>) => {
      state.currentEvent = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    updateEventParticipantCount: (state, action: PayloadAction<{ eventId: number; count: number }>) => {
      const { eventId, count } = action.payload;
      const event = state.events.find(e => e.id === eventId);
      if (event) {
        event.current_participants = count;
      }
      if (state.currentEvent?.id === eventId) {
        state.currentEvent.current_participants = count;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch events
      .addCase(fetchEvents.pending, (state, action) => {
        const { refresh } = action.meta.arg;
        if (refresh) {
          state.loading = true;
        } else {
          state.pagination.loading = true;
        }
        state.error = null;
      })
      .addCase(fetchEvents.fulfilled, (state, action) => {
        const { events, page, refresh, hasMore } = action.payload;
        
        if (refresh || page === 1) {
          state.events = events;
        } else {
          state.events = [...state.events, ...events];
        }
        
        state.pagination.page = page;
        state.pagination.hasMore = hasMore;
        state.pagination.loading = false;
        state.loading = false;
        state.error = null;
      })
      .addCase(fetchEvents.rejected, (state, action) => {
        state.pagination.loading = false;
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch user events
      .addCase(fetchUserEvents.fulfilled, (state, action) => {
        state.userEvents = action.payload;
      })
      // Fetch featured events
      .addCase(fetchFeaturedEvents.fulfilled, (state, action) => {
        state.featuredEvents = action.payload;
      })
      // Fetch upcoming events
      .addCase(fetchUpcomingEvents.fulfilled, (state, action) => {
        state.upcomingEvents = action.payload;
      })
      // Fetch event by ID
      .addCase(fetchEventById.fulfilled, (state, action) => {
        state.currentEvent = action.payload;
      })
      // Create event
      .addCase(createEvent.fulfilled, (state, action) => {
        state.events.unshift(action.payload);
        state.userEvents.unshift(action.payload);
      })
      // Update event
      .addCase(updateEvent.fulfilled, (state, action) => {
        const updatedEvent = action.payload;
        
        // Update in events array
        const eventIndex = state.events.findIndex(event => event.id === updatedEvent.id);
        if (eventIndex !== -1) {
          state.events[eventIndex] = updatedEvent;
        }
        
        // Update in userEvents array
        const userEventIndex = state.userEvents.findIndex(event => event.id === updatedEvent.id);
        if (userEventIndex !== -1) {
          state.userEvents[userEventIndex] = updatedEvent;
        }
        
        // Update current event if it's the same
        if (state.currentEvent?.id === updatedEvent.id) {
          state.currentEvent = updatedEvent;
        }
      })
      // Delete event
      .addCase(deleteEvent.fulfilled, (state, action) => {
        const deletedEventId = action.payload;
        
        // Remove from events array
        state.events = state.events.filter(event => event.id !== deletedEventId);
        
        // Remove from userEvents array
        state.userEvents = state.userEvents.filter(event => event.id !== deletedEventId);
        
        // Clear current event if it's the deleted one
        if (state.currentEvent?.id === deletedEventId) {
          state.currentEvent = null;
        }
      })
      // Join event
      .addCase(joinEvent.fulfilled, (state, action) => {
        const eventId = action.payload;
        const event = state.events.find(e => e.id === eventId);
        if (event) {
          event.current_participants += 1;
        }
        if (state.currentEvent?.id === eventId) {
          state.currentEvent.current_participants += 1;
        }
      })
      // Leave event
      .addCase(leaveEvent.fulfilled, (state, action) => {
        const eventId = action.payload;
        const event = state.events.find(e => e.id === eventId);
        if (event) {
          event.current_participants = Math.max(0, event.current_participants - 1);
        }
        if (state.currentEvent?.id === eventId) {
          state.currentEvent.current_participants = Math.max(0, state.currentEvent.current_participants - 1);
        }
      })
      // Fetch event stats
      .addCase(fetchEventStats.fulfilled, (state, action) => {
        state.stats = action.payload;
      });
  },
});

export const {
  setEventTypeFilter,
  setDateRangeFilter,
  setLocationFilter,
  setPriceRangeFilter,
  setPublicFilter,
  setFeaturedFilter,
  setOrganizerFilter,
  clearFilters,
  setCurrentEvent,
  clearError,
  updateEventParticipantCount,
} = eventsSlice.actions;

export default eventsSlice.reducer; 