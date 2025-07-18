 // API Service - centralizes all backend API calls and handles authentication
import axios from 'axios'
import { HotSpot, RacingCrew, CrewMembership, LocationBroadcast, ReputationRating, OpenChallenge, ChallengeResponse, Callout } from '../types';
import Cookies from 'js-cookie';

// Get API URL from environment variable or use default
const API_URL = (import.meta as any).env?.VITE_API_URL || 
                (window.location.hostname === 'localhost' ? 'http://localhost:8000/api' : 'https://calloutracing-backend-production.up.railway.app/api')

console.log('API URL configured as:', API_URL)

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for session authentication
})

// Utility to fetch CSRF token from cookie
export function getCSRFToken() {
  const token = Cookies.get('csrftoken');
  console.log('CSRF Token from cookie:', token);
  return token;
}

// Add a request interceptor to set X-CSRFToken header for all POST, PUT, PATCH, DELETE requests
api.interceptors.request.use((config) => {
  const method = config.method?.toLowerCase();
  if (["post", "put", "patch", "delete"].includes(method || "")) {
    const csrfToken = getCSRFToken();
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
      console.log('Setting X-CSRFToken header:', csrfToken);
    } else {
      console.warn('No CSRF token found for', method, 'request to', config.url);
    }
  }
  return config;
})

// Response interceptor - handles authentication errors and redirects to login
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear any stored user data and redirect to login
      localStorage.removeItem('user')
      window.location.href = '/login'
    } else if (error.response?.status === 403) {
      // Forbidden - user is not authenticated, but don't redirect
      // This is expected for unauthenticated users accessing protected endpoints
      console.log('Access forbidden - user not authenticated')
    }
    return Promise.reject(error)
  }
)

// Utility to ensure CSRF cookie is set before making POST requests
export async function ensureCSRFToken() {
  try {
    console.log('Fetching CSRF token...');
    const response = await api.get('/auth/csrf/');
    console.log('CSRF token response:', response.status);
    
    // Check if CSRF token is now available
    const token = getCSRFToken();
    if (token) {
      console.log('CSRF token successfully set:', token);
    } else {
      console.warn('CSRF token not found after fetch attempt');
    }
    
    return response;
  } catch (error) {
    console.error('Failed to fetch CSRF token:', error);
    throw error;
  }
}

// Authentication API endpoints
export const authAPI = {
  register: (data: any) => api.post('/auth/register/', data),
  login: (data: any) => api.post('/auth/login/', data),
  logout: () => api.post('/auth/logout/'),
  refresh: () => api.post('/auth/refresh/'),
  verifyEmail: (token: string) => api.post('/auth/verify-email/', { token }),
  resendVerification: () => api.post('/auth/resend-verification/'),
  forgotPassword: (email: string) => api.post('/auth/forgot-password/', { email }),
  resetPassword: (token: string, password: string) => api.post('/auth/reset-password/', { token, password }),
  changePassword: (oldPassword: string, newPassword: string) => api.post('/auth/change-password/', { old_password: oldPassword, new_password: newPassword }),
  profile: () => api.get('/auth/profile/'),
  updateProfile: (data: any) => api.patch('/auth/profile/', data),
  deleteAccount: () => api.delete('/auth/delete-account/'),
  testAuth: () => api.get('/auth/test-auth/'),
  googleSSO: (idToken: string) => api.post('/auth/google/', { id_token: idToken }),
  facebookSSO: (accessToken: string) => api.post('/auth/facebook/', { access_token: accessToken }),
  getSSOConfig: () => api.get('/auth/sso-config/'),
  checkUserExists: (data: { username?: string; email?: string }) => api.post('/auth/check-user/', data),
  requestPasswordReset: (email: string) => api.post('/auth/request-password-reset/', { email }),
  // OTP methods
  sendOtp: (identifier: string, method: 'email' | 'phone') => api.post('/auth/otp/send/', { identifier, method }),
  verifyOtp: (identifier: string, otp: string, type: 'email' | 'phone') => api.post('/auth/otp/verify/', { identifier, otp_code: otp, type }),
  otpLogin: (identifier: string, otp: string) => api.post('/auth/otp-login/', { identifier, otp }),
  emailLogin: (email: string) => api.post('/auth/email-login/', { email }),
  // Subscription methods
  getSubscriptionPlans: () => api.get('/subscriptions/plans/'),
  createSubscriptionCheckout: (data: { price_id: string }) => api.post('/subscriptions/create-checkout-session/', data),
  createCustomerPortalSession: () => api.post('/subscriptions/create-portal-session/'),
  getSubscriptionStatus: () => api.get('/subscriptions/status/'),
  // Marketplace methods
  getMarketplaceItem: (itemId: string) => api.get(`/marketplace/items/${itemId}/`),
  createMarketplacePaymentIntent: (itemId: string) => api.post(`/marketplace/items/${itemId}/create-payment-intent/`),
}

// Contact form API
export const contactAPI = {
  send: (data: any) => api.post('/contact/', data),
}

// User management API endpoints
export const userAPI = {
  list: () => api.get('/users/'),
  profile: (id: number) => api.get(`/profiles/${id}/`),
  updateProfile: (id: number, data: any) => api.patch(`/profiles/${id}/`, data),
  uploadProfilePicture: (id: number, imageFile: File) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    return api.post(`/profiles/${id}/upload_profile_picture/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  uploadCoverPhoto: (id: number, imageFile: File) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    return api.post(`/profiles/${id}/upload_cover_photo/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  removeProfilePicture: (id: number) => api.delete(`/profiles/${id}/remove_profile_picture/`),
  removeCoverPhoto: (id: number) => api.delete(`/profiles/${id}/remove_cover_photo/`),
  updateStats: (id: number, stats: any) => api.post(`/profiles/${id}/update_stats/`, stats),
  
  // Friend-related endpoints
  searchUsers: (query: string) => api.get(`/users/search/?q=${encodeURIComponent(query)}`),
  getFriends: () => api.get('/friendships/friends/'),
  getPendingRequests: () => api.get('/friendships/pending_requests/'),
  getSentRequests: () => api.get('/friendships/sent_requests/'),
  sendFriendRequest: (userId: number) => api.post('/friendships/send_request/', { receiver: userId }),
  acceptFriendRequest: (friendshipId: number) => api.post(`/friendships/${friendshipId}/accept/`),
  declineFriendRequest: (friendshipId: number) => api.post(`/friendships/${friendshipId}/decline/`),
  cancelFriendRequest: (friendshipId: number) => api.delete(`/friendships/${friendshipId}/`),
  removeFriend: (userId: number) => api.delete(`/friendships/remove_friend/${userId}/`),
}

// Callout (race challenge) API endpoints
export const calloutAPI = {
  list: () => api.get('/callouts/'),
  create: (data: any) => api.post('/callouts/', data),
  get: (id: number) => api.get(`/callouts/${id}/`),
  update: (id: number, data: any) => api.patch(`/callouts/${id}/`, data),
  delete: (id: number) => api.delete(`/callouts/${id}/`),
  accept: (id: number) => api.post(`/callouts/${id}/accept_callout/`),
  decline: (id: number) => api.post(`/callouts/${id}/decline_callout/`),
  complete: (id: number, data: any) => api.post(`/callouts/${id}/complete_race/`, data),
}

// Event management API endpoints
export const eventAPI = {
  list: () => api.get('/events/'),
  create: (data: any) => api.post('/events/', data),
  get: (id: number) => api.get(`/events/${id}/`),
  update: (id: number, data: any) => api.patch(`/events/${id}/`, data),
  delete: (id: number) => api.delete(`/events/${id}/`),
  join: (id: number) => api.post(`/events/${id}/join_event/`),
  leave: (id: number) => api.post(`/events/${id}/leave_event/`),
}

// Marketplace (buy/sell) API endpoints
export const marketplaceAPI = {
  list: () => api.get('/marketplace/'),
  create: (data: any) => api.post('/marketplace/', data),
  get: (id: number) => api.get(`/marketplace/${id}/`),
  update: (id: number, data: any) => api.patch(`/marketplace/${id}/`, data),
  delete: (id: number) => api.delete(`/marketplace/${id}/`),
  myListings: () => api.get('/marketplace/my_listings/'),
}

// Track management API endpoints
export const trackAPI = {
  list: () => api.get('/tracks/'),
  create: (data: any) => api.post('/tracks/', data),
  get: (id: number) => api.get(`/tracks/${id}/`),
  update: (id: number, data: any) => api.patch(`/tracks/${id}/`, data),
  delete: (id: number) => api.delete(`/tracks/${id}/`),
}

// Car management API endpoints
export const carAPI = {
  list: () => api.get('/cars/'),
  create: (data: any) => api.post('/cars/', data),
  get: (id: number) => api.get(`/cars/${id}/`),
  update: (id: number, data: any) => api.patch(`/cars/${id}/`, data),
  delete: (id: number) => api.delete(`/cars/${id}/`),
  myCars: () => api.get('/cars/my_cars/'),
}

// Social posts API endpoints
export const postAPI = {
  list: () => api.get('/posts/'),
  create: (data: any) => api.post('/posts/', data),
  get: (id: number) => api.get(`/posts/${id}/`),
  update: (id: number, data: any) => api.patch(`/posts/${id}/`, data),
  delete: (id: number) => api.delete(`/posts/${id}/`),
  likePost: (id: number) => api.post(`/posts/${id}/like_post/`),
}

// Hot Spots API
export const getHotSpots = async (params?: {
  spot_type?: string;
  city?: string;
  state?: string;
  is_verified?: boolean;
}): Promise<HotSpot[]> => {
  const queryParams = new URLSearchParams();
  if (params?.spot_type) queryParams.append('spot_type', params.spot_type);
  if (params?.city) queryParams.append('city', params.city);
  if (params?.state) queryParams.append('state', params.state);
  if (params?.is_verified !== undefined) queryParams.append('is_verified', params.is_verified.toString());
  
  const response = await api.get(`/hotspots/?${queryParams}`);
  return response.data;
};

export const createHotSpot = async (data: Partial<HotSpot>): Promise<HotSpot> => {
  const response = await api.post('/hotspots/', data);
  return response.data;
};

export const updateHotSpot = async (id: number, data: Partial<HotSpot>): Promise<HotSpot> => {
  const response = await api.put(`/hotspots/${id}/`, data);
  return response.data;
};

export const deleteHotSpot = async (id: number): Promise<void> => {
  await api.delete(`/hotspots/${id}/`);
};

// Racing Crews API
export const getRacingCrews = async (params?: {
  crew_type?: string;
}): Promise<RacingCrew[]> => {
  const queryParams = new URLSearchParams();
  if (params?.crew_type) queryParams.append('crew_type', params.crew_type);
  
  const response = await api.get(`/crews/?${queryParams}`);
  return response.data;
};

export const createRacingCrew = async (data: Partial<RacingCrew>): Promise<RacingCrew> => {
  const response = await api.post('/crews/', data);
  return response.data;
};

export const updateRacingCrew = async (id: number, data: Partial<RacingCrew>): Promise<RacingCrew> => {
  const response = await api.put(`/crews/${id}/`, data);
  return response.data;
};

export const deleteRacingCrew = async (id: number): Promise<void> => {
  await api.delete(`/crews/${id}/`);
};

// Crew Memberships API
export const getCrewMemberships = async (): Promise<CrewMembership[]> => {
  const response = await api.get('/crew-memberships/');
  return response.data;
};

export const acceptCrewInvitation = async (id: number): Promise<void> => {
  await api.post(`/crew-memberships/${id}/accept_invitation/`);
};

export const declineCrewInvitation = async (id: number): Promise<void> => {
  await api.post(`/crew-memberships/${id}/decline_invitation/`);
};

// Location Broadcasts API
export const getLocationBroadcasts = async (params?: {
  hot_spot?: number;
  lat?: number;
  lng?: number;
  radius?: number;
}): Promise<LocationBroadcast[]> => {
  const queryParams = new URLSearchParams();
  if (params?.hot_spot) queryParams.append('hot_spot', params.hot_spot.toString());
  if (params?.lat) queryParams.append('lat', params.lat.toString());
  if (params?.lng) queryParams.append('lng', params.lng.toString());
  if (params?.radius) queryParams.append('radius', params.radius.toString());
  
  const response = await api.get(`/location-broadcasts/?${queryParams}`);
  return response.data;
};

export const createLocationBroadcast = async (data: Partial<LocationBroadcast>): Promise<LocationBroadcast> => {
  const response = await api.post('/location-broadcasts/', data);
  return response.data;
};

export const deactivateAllBroadcasts = async (): Promise<void> => {
  await api.post('/location-broadcasts/deactivate_all/');
};

// Reputation Ratings API
export const getReputationRatings = async (): Promise<ReputationRating[]> => {
  const response = await api.get('/reputation-ratings/');
  return response.data;
};

export const createReputationRating = async (data: Partial<ReputationRating>): Promise<ReputationRating> => {
  const response = await api.post('/reputation-ratings/', data);
  return response.data;
};

export const getUserReputationStats = async (userId: number): Promise<{
  user_id: number;
  username: string;
  average_ratings: {
    punctuality: number;
    rule_adherence: number;
    sportsmanship: number;
    overall: number;
  };
  total_ratings: number;
}> => {
  const response = await api.get(`/reputation-ratings/user_stats/?user_id=${userId}`);
  return response.data;
};

// Open Challenges API
export const getOpenChallenges = async (params?: {
  challenge_type?: string;
  location?: string;
  min_horsepower?: number;
  max_horsepower?: number;
  scheduled_after?: string;
}): Promise<OpenChallenge[]> => {
  const queryParams = new URLSearchParams();
  if (params?.challenge_type) queryParams.append('challenge_type', params.challenge_type);
  if (params?.location) queryParams.append('location', params.location);
  if (params?.min_horsepower) queryParams.append('min_horsepower', params.min_horsepower.toString());
  if (params?.max_horsepower) queryParams.append('max_horsepower', params.max_horsepower.toString());
  if (params?.scheduled_after) queryParams.append('scheduled_after', params.scheduled_after);
  
  const response = await api.get(`/open-challenges/?${queryParams}`);
  return response.data;
};

export const createOpenChallenge = async (data: Partial<OpenChallenge>): Promise<OpenChallenge> => {
  const response = await api.post('/open-challenges/', data);
  return response.data;
};

export const updateOpenChallenge = async (id: number, data: Partial<OpenChallenge>): Promise<OpenChallenge> => {
  const response = await api.put(`/open-challenges/${id}/`, data);
  return response.data;
};

export const deleteOpenChallenge = async (id: number): Promise<void> => {
  await api.delete(`/open-challenges/${id}/`);
};

export const respondToChallenge = async (id: number, data: {
  status: 'interested' | 'accepted' | 'declined';
  message?: string;
}): Promise<void> => {
  await api.post(`/open-challenges/${id}/respond/`, data);
};

export const getChallengeResponsesForChallenge = async (id: number): Promise<ChallengeResponse[]> => {
  const response = await api.get(`/open-challenges/${id}/responses/`);
  return response.data;
};

// Challenge Responses API
export const getChallengeResponses = async (): Promise<ChallengeResponse[]> => {
  const response = await api.get('/challenge-responses/');
  return response.data;
};

export const createChallengeResponse = async (data: Partial<ChallengeResponse>): Promise<ChallengeResponse> => {
  const response = await api.post('/challenge-responses/', data);
  return response.data;
};

// Update existing Callout API functions to include new fields
export const createCallout = async (data: Partial<Callout>): Promise<Callout> => {
  const response = await api.post('/callouts/', data);
  return response.data;
};

export const updateCallout = async (id: number, data: Partial<Callout>): Promise<Callout> => {
  const response = await api.put(`/callouts/${id}/`, data);
  return response.data;
};

export const acceptCallout = async (id: number): Promise<void> => {
  await api.post(`/callouts/${id}/accept/`);
};

export const declineCallout = async (id: number): Promise<void> => {
  await api.post(`/callouts/${id}/decline/`);
};

export const completeCallout = async (id: number, winnerId: number): Promise<void> => {
  await api.post(`/callouts/${id}/complete/`, { winner_id: winnerId });
};

// Global search API
export const searchAPI = {
  globalSearch: (query: string, category?: string, limit?: number) => {
    const params = new URLSearchParams();
    params.append('q', query);
    if (category) params.append('category', category);
    if (limit) params.append('limit', limit.toString());
    return api.get(`/search/?${params}`);
  },
};

export { API_URL };
export { api } 