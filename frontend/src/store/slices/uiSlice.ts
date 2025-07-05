import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// UI state interface
interface UIState {
  modals: {
    createPost: boolean;
    createCallout: boolean;
    createEvent: boolean;
    createListing: boolean;
    deleteConfirm: { show: boolean; itemId: number | null; itemType: string | null };
    profileEdit: boolean;
    settings: boolean;
  };
  filters: {
    marketplace: {
      category: string;
      priceRange: [number, number];
      condition: string;
      location: string;
    };
    social: {
      postType: string;
      timeFilter: string;
      author: string;
    };
    events: {
      eventType: string;
      dateRange: [Date | null, Date | null];
      location: string;
    };
    racing: {
      calloutType: string;
      status: string;
      location: string;
    };
  };
  notifications: {
    success: string | null;
    error: string | null;
    info: string | null;
    warning: string | null;
  };
  sidebar: {
    isOpen: boolean;
    activeSection: string;
  };
  search: {
    isOpen: boolean;
    query: string;
    results: any[];
    isLoading: boolean;
  };
}

// Initial state
const initialState: UIState = {
  modals: {
    createPost: false,
    createCallout: false,
    createEvent: false,
    createListing: false,
    deleteConfirm: { show: false, itemId: null, itemType: null },
    profileEdit: false,
    settings: false,
  },
  filters: {
    marketplace: {
      category: 'all',
      priceRange: [0, 100000],
      condition: 'all',
      location: '',
    },
    social: {
      postType: '',
      timeFilter: '',
      author: '',
    },
    events: {
      eventType: 'all',
      dateRange: [null, null],
      location: '',
    },
    racing: {
      calloutType: 'all',
      status: 'all',
      location: '',
    },
  },
  notifications: {
    success: null,
    error: null,
    info: null,
    warning: null,
  },
  sidebar: {
    isOpen: false,
    activeSection: 'dashboard',
  },
  search: {
    isOpen: false,
    query: '',
    results: [],
    isLoading: false,
  },
};

// UI slice
const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    // Modal actions
    openModal: (state, action: PayloadAction<keyof UIState['modals']>) => {
      const modalKey = action.payload;
      if (modalKey !== 'deleteConfirm') {
        (state.modals as any)[modalKey] = true;
      }
    },
    closeModal: (state, action: PayloadAction<keyof UIState['modals']>) => {
      const modalKey = action.payload;
      if (modalKey !== 'deleteConfirm') {
        (state.modals as any)[modalKey] = false;
      }
    },
    openDeleteConfirm: (state, action: PayloadAction<{ itemId: number; itemType: string }>) => {
      state.modals.deleteConfirm = {
        show: true,
        itemId: action.payload.itemId,
        itemType: action.payload.itemType,
      };
    },
    closeDeleteConfirm: (state) => {
      state.modals.deleteConfirm = { show: false, itemId: null, itemType: null };
    },
    closeAllModals: (state) => {
      Object.keys(state.modals).forEach((key) => {
        if (key === 'deleteConfirm') {
          state.modals.deleteConfirm = { show: false, itemId: null, itemType: null };
        } else {
          (state.modals as any)[key] = false;
        }
      });
    },

    // Filter actions
    setMarketplaceFilter: (state, action: PayloadAction<Partial<UIState['filters']['marketplace']>>) => {
      state.filters.marketplace = { ...state.filters.marketplace, ...action.payload };
    },
    setSocialFilter: (state, action: PayloadAction<Partial<UIState['filters']['social']>>) => {
      state.filters.social = { ...state.filters.social, ...action.payload };
    },
    setEventsFilter: (state, action: PayloadAction<Partial<UIState['filters']['events']>>) => {
      state.filters.events = { ...state.filters.events, ...action.payload };
    },
    setRacingFilter: (state, action: PayloadAction<Partial<UIState['filters']['racing']>>) => {
      state.filters.racing = { ...state.filters.racing, ...action.payload };
    },
    clearFilters: (state, action: PayloadAction<keyof UIState['filters']>) => {
      const filterType = action.payload;
      if (filterType === 'marketplace') {
        state.filters.marketplace = initialState.filters.marketplace;
      } else if (filterType === 'social') {
        state.filters.social = initialState.filters.social;
      } else if (filterType === 'events') {
        state.filters.events = initialState.filters.events;
      } else if (filterType === 'racing') {
        state.filters.racing = initialState.filters.racing;
      }
    },

    // Notification actions
    showSuccess: (state, action: PayloadAction<string>) => {
      state.notifications.success = action.payload;
      state.notifications.error = null;
      state.notifications.info = null;
      state.notifications.warning = null;
    },
    showError: (state, action: PayloadAction<string>) => {
      state.notifications.error = action.payload;
      state.notifications.success = null;
      state.notifications.info = null;
      state.notifications.warning = null;
    },
    showInfo: (state, action: PayloadAction<string>) => {
      state.notifications.info = action.payload;
      state.notifications.success = null;
      state.notifications.error = null;
      state.notifications.warning = null;
    },
    showWarning: (state, action: PayloadAction<string>) => {
      state.notifications.warning = action.payload;
      state.notifications.success = null;
      state.notifications.error = null;
      state.notifications.info = null;
    },
    clearNotifications: (state) => {
      state.notifications = initialState.notifications;
    },
    clearNotification: (state, action: PayloadAction<keyof UIState['notifications']>) => {
      state.notifications[action.payload] = null;
    },

    // Sidebar actions
    toggleSidebar: (state) => {
      state.sidebar.isOpen = !state.sidebar.isOpen;
    },
    openSidebar: (state) => {
      state.sidebar.isOpen = true;
    },
    closeSidebar: (state) => {
      state.sidebar.isOpen = false;
    },
    setActiveSection: (state, action: PayloadAction<string>) => {
      state.sidebar.activeSection = action.payload;
    },

    // Search actions
    openSearch: (state) => {
      state.search.isOpen = true;
    },
    closeSearch: (state) => {
      state.search.isOpen = false;
      state.search.query = '';
      state.search.results = [];
    },
    setSearchQuery: (state, action: PayloadAction<string>) => {
      state.search.query = action.payload;
    },
    setSearchResults: (state, action: PayloadAction<any[]>) => {
      state.search.results = action.payload;
    },
    setSearchLoading: (state, action: PayloadAction<boolean>) => {
      state.search.isLoading = action.payload;
    },
  },
});

export const {
  openModal,
  closeModal,
  openDeleteConfirm,
  closeDeleteConfirm,
  closeAllModals,
  setMarketplaceFilter,
  setSocialFilter,
  setEventsFilter,
  setRacingFilter,
  clearFilters,
  showSuccess,
  showError,
  showInfo,
  showWarning,
  clearNotifications,
  clearNotification,
  toggleSidebar,
  openSidebar,
  closeSidebar,
  setActiveSection,
  openSearch,
  closeSearch,
  setSearchQuery,
  setSearchResults,
  setSearchLoading,
} = uiSlice.actions;

export default uiSlice.reducer; 