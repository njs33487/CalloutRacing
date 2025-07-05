import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { calloutAPI, eventAPI, getHotSpots, createHotSpot } from '../../services/api';

// Interfaces
export interface Callout {
  id: number;
  challenger: {
    id: number;
    username: string;
  };
  opponent: {
    id: number;
    username: string;
  };
  status: 'pending' | 'accepted' | 'declined' | 'completed' | 'cancelled';
  location: string;
  scheduled_time: string;
  car_details: {
    make: string;
    model: string;
    year: number;
    horsepower: number;
  };
  winner?: {
    id: number;
    username: string;
  };
  created_at: string;
  updated_at: string;
}

export interface Event {
  id: number;
  title: string;
  description: string;
  event_type: 'race' | 'meet' | 'show' | 'competition';
  location: string;
  scheduled_time: string;
  organizer: {
    id: number;
    username: string;
  };
  participants: Array<{
    id: number;
    username: string;
  }>;
  max_participants: number;
  created_at: string;
  updated_at: string;
}

export interface HotSpot {
  id: number;
  name: string;
  spot_type: 'track' | 'street_meet' | 'parking_lot' | 'industrial' | 'other';
  description: string;
  address: string;
  city: string;
  state: string;
  latitude: number;
  longitude: number;
  is_verified: boolean;
  created_by: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    date_joined: string;
  };
  created_at: string;
}

export interface UserStats {
  total_races: number;
  wins: number;
  losses: number;
  win_rate: number;
  average_reaction_time: number;
  best_quarter_mile: number;
  reputation_score: number;
}

interface RacingState {
  callouts: Callout[];
  events: Event[];
  hotspots: HotSpot[];
  userStats: UserStats | null;
  filters: {
    calloutType: string;
    status: string;
    location: string;
    eventType: string;
  };
  loading: boolean;
  error: string | null;
}

const initialState: RacingState = {
  callouts: [],
  events: [],
  hotspots: [],
  userStats: null,
  filters: {
    calloutType: 'all',
    status: 'all',
    location: '',
    eventType: 'all',
  },
  loading: false,
  error: null,
};

// Async thunks
export const fetchCallouts = createAsyncThunk(
  'racing/fetchCallouts',
  async (_, { getState, rejectWithValue }) => {
    try {
      const state = getState() as any;
      const { filters } = state.racing;
      
      const params = new URLSearchParams({
        ...(filters.calloutType !== 'all' && { callout_type: filters.calloutType }),
        ...(filters.status !== 'all' && { status: filters.status }),
        ...(filters.location && { location: filters.location }),
      });

      const response = await calloutAPI.list();
      return response.data.results || response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch callouts');
    }
  }
);

export const fetchEvents = createAsyncThunk(
  'racing/fetchEvents',
  async (_, { getState, rejectWithValue }) => {
    try {
      const state = getState() as any;
      const { filters } = state.racing;
      
      const params = new URLSearchParams({
        ...(filters.eventType !== 'all' && { event_type: filters.eventType }),
        ...(filters.location && { location: filters.location }),
      });

      const response = await eventAPI.list();
      return response.data.results || response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch events');
    }
  }
);

export const fetchHotspots = createAsyncThunk(
  'racing/fetchHotspots',
  async (params: {
    spot_type?: string;
    city?: string;
    state?: string;
    is_verified?: boolean;
  } = {}, { rejectWithValue }) => {
    try {
      const hotspots = await getHotSpots(params);
      return hotspots;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch hotspots');
    }
  }
);

export const createCallout = createAsyncThunk(
  'racing/createCallout',
  async (calloutData: Partial<Callout>, { rejectWithValue }) => {
    try {
      const response = await calloutAPI.create(calloutData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to create callout');
    }
  }
);

export const acceptCallout = createAsyncThunk(
  'racing/acceptCallout',
  async (calloutId: number, { rejectWithValue }) => {
    try {
      await calloutAPI.accept(calloutId);
      return calloutId;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to accept callout');
    }
  }
);

export const declineCallout = createAsyncThunk(
  'racing/declineCallout',
  async (calloutId: number, { rejectWithValue }) => {
    try {
      await calloutAPI.decline(calloutId);
      return calloutId;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to decline callout');
    }
  }
);

export const completeCallout = createAsyncThunk(
  'racing/completeCallout',
  async ({ calloutId, winnerId }: { calloutId: number; winnerId: number }, { rejectWithValue }) => {
    try {
      await calloutAPI.complete(calloutId, { winner_id: winnerId });
      return { calloutId, winnerId };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to complete callout');
    }
  }
);

export const createEvent = createAsyncThunk(
  'racing/createEvent',
  async (eventData: Partial<Event>, { rejectWithValue }) => {
    try {
      const response = await eventAPI.create(eventData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to create event');
    }
  }
);

export const joinEvent = createAsyncThunk(
  'racing/joinEvent',
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
  'racing/leaveEvent',
  async (eventId: number, { rejectWithValue }) => {
    try {
      await eventAPI.leave(eventId);
      return eventId;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to leave event');
    }
  }
);

export const createHotspot = createAsyncThunk(
  'racing/createHotspot',
  async (hotspotData: Partial<HotSpot>, { rejectWithValue }) => {
    try {
      const hotspot = await createHotSpot(hotspotData);
      return hotspot;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to create hotspot');
    }
  }
);

// Racing slice
const racingSlice = createSlice({
  name: 'racing',
  initialState,
  reducers: {
    setCalloutTypeFilter: (state, action: PayloadAction<string>) => {
      state.filters.calloutType = action.payload;
    },
    setStatusFilter: (state, action: PayloadAction<string>) => {
      state.filters.status = action.payload;
    },
    setLocationFilter: (state, action: PayloadAction<string>) => {
      state.filters.location = action.payload;
    },
    setEventTypeFilter: (state, action: PayloadAction<string>) => {
      state.filters.eventType = action.payload;
    },
    clearFilters: (state) => {
      state.filters = initialState.filters;
    },
    clearError: (state) => {
      state.error = null;
    },
    updateCalloutStatus: (state, action: PayloadAction<{ id: number; status: Callout['status'] }>) => {
      const { id, status } = action.payload;
      const callout = state.callouts.find(c => c.id === id);
      if (callout) {
        callout.status = status;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch callouts
      .addCase(fetchCallouts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCallouts.fulfilled, (state, action) => {
        state.callouts = action.payload;
        state.loading = false;
        state.error = null;
      })
      .addCase(fetchCallouts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch events
      .addCase(fetchEvents.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchEvents.fulfilled, (state, action) => {
        state.events = action.payload;
        state.loading = false;
        state.error = null;
      })
      .addCase(fetchEvents.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch hotspots
      .addCase(fetchHotspots.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchHotspots.fulfilled, (state, action) => {
        state.hotspots = action.payload;
        state.loading = false;
        state.error = null;
      })
      .addCase(fetchHotspots.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Create callout
      .addCase(createCallout.fulfilled, (state, action) => {
        state.callouts.unshift(action.payload);
      })
      // Accept callout
      .addCase(acceptCallout.fulfilled, (state, action) => {
        const calloutId = action.payload;
        const callout = state.callouts.find(c => c.id === calloutId);
        if (callout) {
          callout.status = 'accepted';
        }
      })
      // Decline callout
      .addCase(declineCallout.fulfilled, (state, action) => {
        const calloutId = action.payload;
        const callout = state.callouts.find(c => c.id === calloutId);
        if (callout) {
          callout.status = 'declined';
        }
      })
      // Complete callout
      .addCase(completeCallout.fulfilled, (state, action) => {
        const { calloutId, winnerId } = action.payload;
        const callout = state.callouts.find(c => c.id === calloutId);
        if (callout) {
          callout.status = 'completed';
          callout.winner = { id: winnerId, username: '' }; // Username would be fetched separately
        }
      })
      // Create event
      .addCase(createEvent.fulfilled, (state, action) => {
        state.events.unshift(action.payload);
      })
      // Join event
      .addCase(joinEvent.fulfilled, (state, action) => {
        const eventId = action.payload;
        const event = state.events.find(e => e.id === eventId);
        if (event) {
          // Add current user to participants (user ID would be from auth state)
          // This is a simplified version
        }
      })
      // Leave event
      .addCase(leaveEvent.fulfilled, (state, action) => {
        const eventId = action.payload;
        const event = state.events.find(e => e.id === eventId);
        if (event) {
          // Remove current user from participants
          // This is a simplified version
        }
      })
      // Create hotspot
      .addCase(createHotspot.fulfilled, (state, action) => {
        state.hotspots.unshift(action.payload);
      });
  },
});

export const {
  setCalloutTypeFilter,
  setStatusFilter,
  setLocationFilter,
  setEventTypeFilter,
  clearFilters,
  clearError,
  updateCalloutStatus,
} = racingSlice.actions;

export default racingSlice.reducer; 