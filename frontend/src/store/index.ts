import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import eventsReducer from './slices/eventsSlice';
import marketplaceReducer from './slices/marketplaceSlice';
import racingReducer from './slices/racingSlice';
import socialReducer from './slices/socialSlice';
import uiReducer from './slices/uiSlice';
import otpReducer from './slices/otpSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    events: eventsReducer,
    marketplace: marketplaceReducer,
    racing: racingReducer,
    social: socialReducer,
    ui: uiReducer,
    otp: otpReducer,
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