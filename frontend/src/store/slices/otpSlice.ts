import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { authAPI } from '../../services/api';

interface OtpState {
  loading: boolean;
  error: string | null;
  step: 'input' | 'otp' | 'success';
  identifier: string;
  type: 'phone' | 'email';
  user: any | null;
}

const initialState: OtpState = {
  loading: false,
  error: null,
  step: 'input',
  identifier: '',
  type: 'phone',
  user: null,
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
  async ({ identifier, otp_code }: { identifier: string; otp_code: string; type: 'phone' | 'email' }) => {
    const response = await authAPI.verifyOtp(identifier, otp_code);
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
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Send OTP
      .addCase(sendOtpAsync.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendOtpAsync.fulfilled, (state) => {
        state.loading = false;
        state.step = 'otp';
      })
      .addCase(sendOtpAsync.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to send OTP';
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
      })
      .addCase(verifyOtpAsync.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to verify OTP';
      });
  },
});

export const { setIdentifier, setType, resetOtp, clearError } = otpSlice.actions;
export default otpSlice.reducer;