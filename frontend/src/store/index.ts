import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import uiReducer from './slices/uiSlice';
import socialReducer from './slices/socialSlice';
import marketplaceReducer from './slices/marketplaceSlice';
import racingReducer from './slices/racingSlice';
import eventsReducer from './slices/eventsSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    ui: uiReducer,
    social: socialReducer,
    marketplace: marketplaceReducer,
    racing: racingReducer,
    events: eventsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore these action types
        ignoredActions: ['persist/PERSIST'],
        // Ignore these field paths in all actions
        ignoredActionPaths: ['payload.timestamp'],
        // Ignore these paths in state
        ignoredPaths: ['ui.notifications'],
      },
    }),
  devTools: process.env.NODE_ENV !== 'production',
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch; 