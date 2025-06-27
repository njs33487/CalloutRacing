import axios from 'axios'

// Get API URL from environment variable or use default
const API_URL = (import.meta as any).env?.VITE_API_URL || 'https://calloutracing-backend.up.railway.app'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const authAPI = {
  register: (data: any) => api.post('/auth/register/', data),
  login: (data: any) => api.post('/auth/login/', data),
  logout: () => api.post('/auth/logout/'),
  profile: () => api.get('/auth/profile/'),
}

export const contactAPI = {
  send: (data: any) => api.post('/contact/', data),
}

export const userAPI = {
  list: () => api.get('/users/'),
  profile: (id: number) => api.get(`/profiles/${id}/`),
  updateProfile: (id: number, data: any) => api.patch(`/profiles/${id}/`, data),
}

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

export const eventAPI = {
  list: () => api.get('/events/'),
  create: (data: any) => api.post('/events/', data),
  get: (id: number) => api.get(`/events/${id}/`),
  update: (id: number, data: any) => api.patch(`/events/${id}/`, data),
  delete: (id: number) => api.delete(`/events/${id}/`),
  join: (id: number) => api.post(`/events/${id}/join_event/`),
  leave: (id: number) => api.post(`/events/${id}/leave_event/`),
}

export const marketplaceAPI = {
  list: () => api.get('/marketplace/'),
  create: (data: any) => api.post('/marketplace/', data),
  get: (id: number) => api.get(`/marketplace/${id}/`),
  update: (id: number, data: any) => api.patch(`/marketplace/${id}/`, data),
  delete: (id: number) => api.delete(`/marketplace/${id}/`),
  myListings: () => api.get('/marketplace/my_listings/'),
}

export const trackAPI = {
  list: () => api.get('/tracks/'),
  create: (data: any) => api.post('/tracks/', data),
  get: (id: number) => api.get(`/tracks/${id}/`),
  update: (id: number, data: any) => api.patch(`/tracks/${id}/`, data),
  delete: (id: number) => api.delete(`/tracks/${id}/`),
}

export const carAPI = {
  list: () => api.get('/cars/'),
  create: (data: any) => api.post('/cars/', data),
  get: (id: number) => api.get(`/cars/${id}/`),
  update: (id: number, data: any) => api.patch(`/cars/${id}/`, data),
  delete: (id: number) => api.delete(`/cars/${id}/`),
  myCars: () => api.get('/cars/my_cars/'),
}

export const postAPI = {
  list: () => api.get('/posts/'),
  create: (data: any) => api.post('/posts/', data),
  get: (id: number) => api.get(`/posts/${id}/`),
  update: (id: number, data: any) => api.patch(`/posts/${id}/`, data),
  delete: (id: number) => api.delete(`/posts/${id}/`),
  likePost: (id: number) => api.post(`/posts/${id}/like_post/`),
}

export { api } 