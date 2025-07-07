import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { authAPI } from '../../services/api';

interface OtpState {
  loading: boolean;
  error: string | null;
  step: 'input' | 'otp' | 'success';
  identifier: string;
  type: 'phone' | 'email';
  user: any | null;
  remainingAttempts: number | null;
  resendCooldownSeconds: number | null;
  expiresInMinutes: number | null;
}

const initialState: OtpState = {
  loading: false,
  error: null,
  step: 'input',
  identifier: '',
  type: 'phone',
  user: null,
  remainingAttempts: null,
  resendCooldownSeconds: null,
  expiresInMinutes: null,
};

// Async thunks
export const sendOtpAsync = createAsyncThunk(
  'otp/sendOtp',
  async ({ identifier, type }: { identifier: string; type: 'phone' | 'email' }) => {
    const response = await authAPI.sendOtp(identifier, type);
    return response.data;
  }
);

export const verifyOtpAsync = createAsyncThunk(
  'otp/verifyOtp',
  async ({ identifier, otp_code, type }: { identifier: string; otp_code: string; type: 'phone' | 'email' }) => {
    const response = await authAPI.verifyOtp(identifier, otp_code, type);
    return response.data;
  }
);

const otpSlice = createSlice({
  name: 'otp',
  initialState,
  reducers: {
    setIdentifier: (state, action: PayloadAction<string>) => {
      state.identifier = action.payload;
    },
    setType: (state, action: PayloadAction<'phone' | 'email'>) => {
      state.type = action.payload;
    },
    resetOtp: (state) => {
      state.loading = false;
      state.error = null;
      state.step = 'input';
      state.identifier = '';
      state.user = null;
      state.remainingAttempts = null;
      state.resendCooldownSeconds = null;
      state.expiresInMinutes = null;
    },
    clearError: (state) => {
      state.error = null;
    },
    updateRateLimitInfo: (state, action: PayloadAction<{
      remainingAttempts?: number;
      resendCooldownSeconds?: number;
      expiresInMinutes?: number;
    }>) => {
      if (action.payload.remainingAttempts !== undefined) {
        state.remainingAttempts = action.payload.remainingAttempts;
      }
      if (action.payload.resendCooldownSeconds !== undefined) {
        state.resendCooldownSeconds = action.payload.resendCooldownSeconds;
      }
      if (action.payload.expiresInMinutes !== undefined) {
        state.expiresInMinutes = action.payload.expiresInMinutes;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Send OTP
      .addCase(sendOtpAsync.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendOtpAsync.fulfilled, (state, action) => {
        state.loading = false;
        state.step = 'otp';
        state.error = null;
        
        // Extract rate limiting info from response
        if (action.payload.remaining_attempts !== undefined) {
          state.remainingAttempts = action.payload.remaining_attempts;
        }
        if (action.payload.resend_cooldown_seconds !== undefined) {
          state.resendCooldownSeconds = action.payload.resend_cooldown_seconds;
        }
        if (action.payload.expires_in_minutes !== undefined) {
          state.expiresInMinutes = action.payload.expires_in_minutes;
        }
      })
      .addCase(sendOtpAsync.rejected, (state, action) => {
        state.loading = false;
        // Extract error message from the rejected action
        let errorMessage = 'Failed to send verification code';
        if (action.error.message) {
          errorMessage = action.error.message;
        } else if (action.payload && typeof action.payload === 'object' && 'error' in action.payload) {
          errorMessage = (action.payload as any).error;
        }
        state.error = errorMessage;
      })
      // Verify OTP
      .addCase(verifyOtpAsync.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(verifyOtpAsync.fulfilled, (state, action) => {
        state.loading = false;
        state.step = 'success';
        state.user = action.payload.user;
        state.error = null;
      })
      .addCase(verifyOtpAsync.rejected, (state, action) => {
        state.loading = false;
        // Extract error message from the rejected action
        let errorMessage = 'Failed to verify code';
        if (action.error.message) {
          errorMessage = action.error.message;
        } else if (action.payload && typeof action.payload === 'object' && 'error' in action.payload) {
          errorMessage = (action.payload as any).error;
        }
        state.error = errorMessage;
      });
  },
});

export const { setIdentifier, setType, resetOtp, clearError, updateRateLimitInfo } = otpSlice.actions;
export default otpSlice.reducer;