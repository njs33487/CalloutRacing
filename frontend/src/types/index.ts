// TypeScript type definitions for the CalloutRacing application

// ============================================================================
// USER & PROFILE TYPES
// ============================================================================

// Basic user information from Django auth
export interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  date_joined: string;
}

// Extended user profile with racing stats and personal info
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

// ============================================================================
// CALLOUT (RACE CHALLENGE) TYPES
// ============================================================================

// Race challenge between two users
export interface Callout {
  id: number;
  challenger: User;
  challenged: User;
  event: Event | null;
  track: Track | null;
  hot_spot: HotSpot | null;
  crew: RacingCrew | null;
  location_type: 'track' | 'street' | 'hot_spot';
  street_location: string;
  race_type: 'quarter_mile' | 'eighth_mile' | 'roll_race' | 'dig_race' | 'heads_up' | 'bracket';
  max_horsepower: number | null;
  min_horsepower: number | null;
  tire_requirement: string;
  rules: string;
  experience_level: 'beginner' | 'intermediate' | 'experienced' | 'pro';
  is_private: boolean;
  is_invite_only: boolean;
  wager_amount: number;
  message: string;
  status: 'pending' | 'accepted' | 'declined' | 'completed' | 'cancelled';
  scheduled_date: string | null;
  winner: User | null;
  images?: CalloutImage[];
  created_at: string;
  updated_at: string;
}

// Images associated with a callout
export interface CalloutImage {
  id: number;
  image: string;
  is_primary: boolean;
}

// ============================================================================
// EVENT TYPES
// ============================================================================

// Racing event organized by a user
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
  images?: EventImage[];
  created_at: string;
  updated_at: string;
}

// Images associated with an event
export interface EventImage {
  id: number;
  image: string;
  is_primary: boolean;
}

// ============================================================================
// TRACK TYPES
// ============================================================================

// Racing track information
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

// ============================================================================
// MARKETPLACE TYPES
// ============================================================================

// Item for sale in the marketplace
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

// Images associated with a marketplace item
export interface MarketplaceImage {
  id: number;
  image: string;
  is_primary: boolean;
}

// ============================================================================
// CAR PROFILE TYPES
// ============================================================================

// Detailed car information and specifications
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

// Car modification/upgrade information
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

// Images associated with a car
export interface CarImage {
  id: number;
  image: string;
  caption: string;
  is_primary: boolean;
}

// ============================================================================
// SOCIAL POST TYPES
// ============================================================================

// User social media post
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

// Comment on a social post
export interface PostComment {
  id: number;
  content: string;
  user: User;
  created_at: string;
}

// ============================================================================
// API RESPONSE TYPES
// ============================================================================

// Standard paginated API response
export interface ApiResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

// Application statistics for dashboard
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

// ============================================================================
// FORM TYPES
// ============================================================================

// Form data for creating a new callout
export interface CreateCalloutForm {
  challenged: string;
  race_type: string;
  location_type: string;
  track: string;
  street_location: string;
  wager_amount: string;
  message: string;
}

// Form data for creating a new event
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

// Form data for creating a new marketplace listing
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

// Add these new interfaces after the existing interfaces

export interface HotSpot {
  id: number;
  name: string;
  description: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  latitude: number;
  longitude: number;
  spot_type: 'track' | 'street_meet' | 'parking_lot' | 'industrial' | 'other';
  rules: string;
  amenities: string;
  peak_hours: string;
  is_verified: boolean;
  is_active: boolean;
  created_by: User;
  total_races: number;
  last_activity: string | null;
  created_at: string;
  updated_at: string;
}

export interface RacingCrew {
  id: number;
  name: string;
  description: string;
  crew_type: 'car_club' | 'racing_crew' | 'friend_group' | 'team';
  is_private: boolean;
  is_invite_only: boolean;
  owner: User;
  admins: User[];
  members: User[];
  member_count: number;
  total_races: number;
  created_at: string;
  updated_at: string;
}

export interface CrewMembership {
  id: number;
  crew: RacingCrew;
  user: User;
  status: 'pending' | 'active' | 'banned';
  joined_at: string;
  invited_by: User | null;
}

export interface LocationBroadcast {
  id: number;
  user: User;
  hot_spot: HotSpot | null;
  latitude: number;
  longitude: number;
  address: string;
  message: string;
  is_active: boolean;
  expires_at: string;
  created_at: string;
}

export interface ReputationRating {
  id: number;
  rater: User;
  rated_user: User;
  punctuality: number;
  rule_adherence: number;
  sportsmanship: number;
  overall: number;
  comment: string;
  created_at: string;
}

export interface OpenChallenge {
  id: number;
  challenger: User;
  title: string;
  description: string;
  challenge_type: 'street' | 'track' | 'roll_race' | 'dig_race' | 'meetup';
  max_horsepower: number | null;
  min_horsepower: number | null;
  tire_requirement: string;
  location: string;
  hot_spot: HotSpot | null;
  scheduled_date: string | null;
  rules: string;
  stakes: string;
  is_active: boolean;
  max_participants: number | null;
  responses_count: number;
  created_at: string;
  updated_at: string;
}

export interface ChallengeResponse {
  id: number;
  responder: User;
  status: 'interested' | 'accepted' | 'declined';
  message: string;
  created_at: string;
} 