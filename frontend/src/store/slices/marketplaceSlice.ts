import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { marketplaceAPI } from '../../services/api';

// Interfaces
export interface MarketplaceItem {
  id: number;
  title: string;
  description: string;
  price: number;
  category: 'car' | 'parts' | 'wheels' | 'electronics' | 'tools' | 'other';
  condition: 'new' | 'like_new' | 'good' | 'fair' | 'poor';
  location: string;
  contact_phone?: string;
  contact_email?: string;
  images: string[];
  seller: {
    id: number;
    username: string;
    email: string;
  };
  created_at: string;
  updated_at: string;
}

interface MarketplaceState {
  items: MarketplaceItem[];
  userListings: MarketplaceItem[];
  filters: {
    category: string;
    priceRange: [number, number];
    condition: string;
    location: string;
  };
  pagination: {
    page: number;
    hasMore: boolean;
    loading: boolean;
  };
  loading: boolean;
  error: string | null;
}

const initialState: MarketplaceState = {
  items: [],
  userListings: [],
  filters: {
    category: 'all',
    priceRange: [0, 100000],
    condition: 'all',
    location: '',
  },
  pagination: {
    page: 1,
    hasMore: true,
    loading: false,
  },
  loading: false,
  error: null,
};

// Async thunks
export const fetchMarketplaceItems = createAsyncThunk(
  'marketplace/fetchItems',
  async ({ page = 1, refresh = false }: { page?: number; refresh?: boolean }, { getState, rejectWithValue }) => {
    try {
      const state = getState() as any;
      const { filters } = state.marketplace;
      
      const params = new URLSearchParams({
        page: page.toString(),
        ...(filters.category !== 'all' && { category: filters.category }),
        ...(filters.condition !== 'all' && { condition: filters.condition }),
        ...(filters.location && { location: filters.location }),
        ...(filters.priceRange[0] > 0 && { min_price: filters.priceRange[0].toString() }),
        ...(filters.priceRange[1] < 100000 && { max_price: filters.priceRange[1].toString() }),
      });

      const response = await marketplaceAPI.list();
      const items = response.data.results || response.data;
      
      return {
        items,
        page,
        refresh,
        hasMore: items.length === 20, // Assuming page size is 20
      };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch marketplace items');
    }
  }
);

export const fetchUserListings = createAsyncThunk(
  'marketplace/fetchUserListings',
  async (_, { rejectWithValue }) => {
    try {
      const response = await marketplaceAPI.myListings();
      return response.data.results || response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch user listings');
    }
  }
);

export const createMarketplaceItem = createAsyncThunk(
  'marketplace/createItem',
  async (itemData: Partial<MarketplaceItem>, { rejectWithValue }) => {
    try {
      const response = await marketplaceAPI.create(itemData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to create marketplace item');
    }
  }
);

export const updateMarketplaceItem = createAsyncThunk(
  'marketplace/updateItem',
  async ({ id, data }: { id: number; data: Partial<MarketplaceItem> }, { rejectWithValue }) => {
    try {
      const response = await marketplaceAPI.update(id, data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to update marketplace item');
    }
  }
);

export const deleteMarketplaceItem = createAsyncThunk(
  'marketplace/deleteItem',
  async (itemId: number, { rejectWithValue }) => {
    try {
      await marketplaceAPI.delete(itemId);
      return itemId;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to delete marketplace item');
    }
  }
);

// Marketplace slice
const marketplaceSlice = createSlice({
  name: 'marketplace',
  initialState,
  reducers: {
    setCategoryFilter: (state, action: PayloadAction<string>) => {
      state.filters.category = action.payload;
      state.pagination.page = 1;
      state.items = [];
    },
    setPriceRangeFilter: (state, action: PayloadAction<[number, number]>) => {
      state.filters.priceRange = action.payload;
      state.pagination.page = 1;
      state.items = [];
    },
    setConditionFilter: (state, action: PayloadAction<string>) => {
      state.filters.condition = action.payload;
      state.pagination.page = 1;
      state.items = [];
    },
    setLocationFilter: (state, action: PayloadAction<string>) => {
      state.filters.location = action.payload;
      state.pagination.page = 1;
      state.items = [];
    },
    clearFilters: (state) => {
      state.filters = initialState.filters;
      state.pagination.page = 1;
      state.items = [];
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch marketplace items
      .addCase(fetchMarketplaceItems.pending, (state, action) => {
        const { refresh } = action.meta.arg;
        if (refresh) {
          state.loading = true;
        } else {
          state.pagination.loading = true;
        }
        state.error = null;
      })
      .addCase(fetchMarketplaceItems.fulfilled, (state, action) => {
        const { items, page, refresh, hasMore } = action.payload;
        
        if (refresh || page === 1) {
          state.items = items;
        } else {
          state.items = [...state.items, ...items];
        }
        
        state.pagination.page = page;
        state.pagination.hasMore = hasMore;
        state.pagination.loading = false;
        state.loading = false;
        state.error = null;
      })
      .addCase(fetchMarketplaceItems.rejected, (state, action) => {
        state.pagination.loading = false;
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch user listings
      .addCase(fetchUserListings.fulfilled, (state, action) => {
        state.userListings = action.payload;
      })
      // Create marketplace item
      .addCase(createMarketplaceItem.fulfilled, (state, action) => {
        state.userListings.unshift(action.payload);
        state.items.unshift(action.payload);
      })
      // Update marketplace item
      .addCase(updateMarketplaceItem.fulfilled, (state, action) => {
        const updatedItem = action.payload;
        
        // Update in items array
        const itemIndex = state.items.findIndex(item => item.id === updatedItem.id);
        if (itemIndex !== -1) {
          state.items[itemIndex] = updatedItem;
        }
        
        // Update in userListings array
        const userListingIndex = state.userListings.findIndex(item => item.id === updatedItem.id);
        if (userListingIndex !== -1) {
          state.userListings[userListingIndex] = updatedItem;
        }
      })
      // Delete marketplace item
      .addCase(deleteMarketplaceItem.fulfilled, (state, action) => {
        const deletedItemId = action.payload;
        
        // Remove from items array
        state.items = state.items.filter(item => item.id !== deletedItemId);
        
        // Remove from userListings array
        state.userListings = state.userListings.filter(item => item.id !== deletedItemId);
      });
  },
});

export const {
  setCategoryFilter,
  setPriceRangeFilter,
  setConditionFilter,
  setLocationFilter,
  clearFilters,
  clearError,
} = marketplaceSlice.actions;

export default marketplaceSlice.reducer; 