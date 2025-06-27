// User and Profile types
export interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  date_joined: string;
}

export interface UserProfile {
  id: number;
  user: User;
  bio?: string;
  location?: string;
  wins: number;
  losses: number;
  total_races: number;
  win_rate?: number;
  profile_picture?: string;
  cover_photo?: string;
  created_at: string;
  updated_at: string;
}

// Callout types
export interface Callout {
  id: number;
  challenger: User;
  challenged: User;
  race_type: string;
  location_type: string;
  street_location?: string;
  track?: Track;
  status: 'pending' | 'accepted' | 'declined' | 'completed' | 'cancelled';
  wager_amount: number;
  message: string;
  scheduled_date?: string;
  winner?: User;
  created_at: string;
  updated_at: string;
}

// Event types
export interface Event {
  id: number;
  title: string;
  description: string;
  event_type: string;
  track: Track;
  organizer: User;
  start_date: string;
  end_date: string;
  max_participants?: number;
  entry_fee: number;
  is_public: boolean;
  is_active: boolean;
  participants_count?: number;
  created_at: string;
  updated_at: string;
}

// Track types
export interface Track {
  id: number;
  name: string;
  location: string;
  description?: string;
  track_type: string;
  surface_type: string;
  is_active: boolean;
  created_at: string;
}

// Marketplace types
export interface MarketplaceItem {
  id: number;
  title: string;
  description: string;
  category: string;
  condition: string;
  price: number;
  is_negotiable: boolean;
  trade_offered: boolean;
  trade_description?: string;
  location: string;
  contact_phone?: string;
  contact_email?: string;
  is_active: boolean;
  views: number;
  created_at: string;
  seller: User;
  images?: MarketplaceImage[];
}

export interface MarketplaceImage {
  id: number;
  image: string;
  is_primary: boolean;
}

// Car Profile types
export interface CarProfile {
  id: number;
  name: string;
  make: string;
  model: string;
  year: number;
  trim: string;
  color: string;
  engine_size: number;
  engine_type: string;
  horsepower: number;
  torque: number;
  weight: number;
  transmission: string;
  drivetrain: string;
  best_quarter_mile: number;
  best_eighth_mile: number;
  best_trap_speed: number;
  description: string;
  is_primary: boolean;
  is_active: boolean;
  user: User;
  modifications: CarModification[];
  images: CarImage[];
  created_at: string;
}

export interface CarModification {
  id: number;
  category: string;
  name: string;
  brand: string;
  description: string;
  cost: number;
  installed_date: string;
  is_installed: boolean;
}

export interface CarImage {
  id: number;
  image: string;
  caption: string;
  is_primary: boolean;
}

// Post types
export interface UserPost {
  id: number;
  content: string;
  image?: string;
  like_count: number;
  is_liked: boolean;
  created_at: string;
  user: User;
  car?: CarProfile;
  comments: PostComment[];
}

export interface PostComment {
  id: number;
  content: string;
  user: User;
  created_at: string;
}

// API Response types
export interface ApiResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

export interface Stats {
  total_users: number;
  total_tracks: number;
  total_events: number;
  total_callouts: number;
  total_marketplace_items: number;
  active_callouts: number;
  upcoming_events: number;
  marketplace_items: number;
  total_racers: number;
}

// Form types
export interface CreateCalloutForm {
  challenged: string;
  race_type: string;
  location_type: string;
  track: string;
  street_location: string;
  wager_amount: string;
  message: string;
}

export interface CreateEventForm {
  title: string;
  event_type: string;
  track: string;
  start_date: string;
  end_date: string;
  max_participants: string;
  entry_fee: string;
  description: string;
  is_public: boolean;
}

export interface CreateListingForm {
  title: string;
  category: string;
  price: string;
  condition: string;
  location: string;
  description: string;
  is_negotiable: boolean;
  trade_offered: boolean;
  trade_description: string;
} 