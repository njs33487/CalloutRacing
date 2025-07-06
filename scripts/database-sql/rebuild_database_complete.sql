-- =====================================================
-- COMPLETE DATABASE REBUILD AND POPULATION SCRIPT
-- CalloutRacing - Social & Marketplace Features
-- =====================================================

-- Drop all existing tables (if they exist)
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;

-- =====================================================
-- STEP 1: Create Django System Tables
-- =====================================================

-- Django content types
CREATE TABLE django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE(app_label, model)
);

-- Django migrations
CREATE TABLE django_migrations (
    id SERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Django sessions
CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Django admin log
CREATE TABLE django_admin_log (
    id SERIAL PRIMARY KEY,
    action_time TIMESTAMP WITH TIME ZONE NOT NULL,
    object_id TEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT NOT NULL,
    change_message TEXT NOT NULL,
    content_type_id INTEGER REFERENCES django_content_type(id),
    user_id INTEGER
);

-- =====================================================
-- STEP 2: Create Authentication Tables
-- =====================================================

-- Auth permissions
CREATE TABLE auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL REFERENCES django_content_type(id),
    codename VARCHAR(100) NOT NULL,
    UNIQUE(content_type_id, codename)
);

-- Auth groups
CREATE TABLE auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

-- Auth group permissions
CREATE TABLE auth_group_permissions (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES auth_group(id),
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
    UNIQUE(group_id, permission_id)
);

-- Auth users
CREATE TABLE auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Auth user groups
CREATE TABLE auth_user_groups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    group_id INTEGER NOT NULL REFERENCES auth_group(id),
    UNIQUE(user_id, group_id)
);

-- Auth user permissions
CREATE TABLE auth_user_user_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
    UNIQUE(user_id, permission_id)
);

-- Authtoken tables
CREATE TABLE authtoken_token (
    key VARCHAR(40) PRIMARY KEY,
    created TIMESTAMP WITH TIME ZONE NOT NULL,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id)
);

CREATE TABLE authtoken_tokenproxy (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id)
);

-- =====================================================
-- STEP 3: Create Core Application Tables
-- =====================================================

-- User profiles
CREATE TABLE core_userprofile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id),
    bio TEXT,
    location VARCHAR(200),
    car_make VARCHAR(100),
    car_model VARCHAR(100),
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    total_races INTEGER DEFAULT 0,
    profile_picture VARCHAR(255),
    email_verified BOOLEAN DEFAULT FALSE,
    phone_number VARCHAR(20),
    date_of_birth DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tracks
CREATE TABLE core_track (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    location VARCHAR(200),
    description TEXT,
    surface_type VARCHAR(50),
    length DECIMAL(8,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Events
CREATE TABLE core_event (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    track_id INTEGER REFERENCES core_track(id),
    start_date TIMESTAMP WITH TIME ZONE,
    end_date TIMESTAMP WITH TIME ZONE,
    event_type VARCHAR(50),
    max_participants INTEGER,
    entry_fee DECIMAL(10,2),
    created_by INTEGER REFERENCES auth_user(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Event participants
CREATE TABLE core_eventparticipant (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES core_event(id),
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    car_id INTEGER,
    registration_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'registered',
    UNIQUE(event_id, user_id)
);

-- Callouts
CREATE TABLE core_callout (
    id SERIAL PRIMARY KEY,
    challenger_id INTEGER NOT NULL REFERENCES auth_user(id),
    challenged_id INTEGER NOT NULL REFERENCES auth_user(id),
    event_id INTEGER REFERENCES core_event(id),
    message TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Race results
CREATE TABLE core_raceresult (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES core_event(id),
    winner_id INTEGER REFERENCES auth_user(id),
    loser_id INTEGER REFERENCES auth_user(id),
    winner_time DECIMAL(8,3),
    loser_time DECIMAL(8,3),
    race_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    notes TEXT
);

-- =====================================================
-- STEP 4: Create Social Features Tables
-- =====================================================

-- Follow relationships
CREATE TABLE core_follow (
    id SERIAL PRIMARY KEY,
    follower_id INTEGER NOT NULL REFERENCES auth_user(id),
    following_id INTEGER NOT NULL REFERENCES auth_user(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(follower_id, following_id)
);

-- Block relationships
CREATE TABLE core_block (
    id SERIAL PRIMARY KEY,
    blocker_id INTEGER NOT NULL REFERENCES auth_user(id),
    blocked_id INTEGER NOT NULL REFERENCES auth_user(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(blocker_id, blocked_id)
);

-- Friendships
CREATE TABLE core_friendship (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL REFERENCES auth_user(id),
    receiver_id INTEGER NOT NULL REFERENCES auth_user(id),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(sender_id, receiver_id)
);

-- Messages
CREATE TABLE core_message (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL REFERENCES auth_user(id),
    recipient_id INTEGER NOT NULL REFERENCES auth_user(id),
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User posts
CREATE TABLE core_userpost (
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES auth_user(id),
    content TEXT NOT NULL,
    post_type VARCHAR(20) DEFAULT 'text',
    image VARCHAR(255),
    video VARCHAR(255),
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Post comments
CREATE TABLE core_postcomment (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES core_userpost(id) ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES auth_user(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Notifications
CREATE TABLE core_notification (
    id SERIAL PRIMARY KEY,
    recipient_id INTEGER NOT NULL REFERENCES auth_user(id),
    sender_id INTEGER REFERENCES auth_user(id),
    notification_type VARCHAR(50),
    title VARCHAR(200),
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    related_object_id INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Racing crews
CREATE TABLE core_racingcrew (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    owner_id INTEGER NOT NULL REFERENCES auth_user(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crew memberships
CREATE TABLE core_crewmembership (
    id SERIAL PRIMARY KEY,
    crew_id INTEGER NOT NULL REFERENCES core_racingcrew(id),
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    role VARCHAR(50) DEFAULT 'member',
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(crew_id, user_id)
);

-- Reputation ratings
CREATE TABLE core_reputationrating (
    id SERIAL PRIMARY KEY,
    rater_id INTEGER NOT NULL REFERENCES auth_user(id),
    rated_user_id INTEGER NOT NULL REFERENCES auth_user(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(rater_id, rated_user_id)
);

-- =====================================================
-- STEP 5: Create Marketplace Features Tables
-- =====================================================

-- Listing categories
CREATE TABLE core_listingcategory (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    parent_id INTEGER REFERENCES core_listingcategory(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Marketplace listings
CREATE TABLE core_marketplace (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES auth_user(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    condition VARCHAR(20),
    price DECIMAL(10,2) NOT NULL,
    is_negotiable BOOLEAN DEFAULT TRUE,
    trade_offered BOOLEAN DEFAULT FALSE,
    trade_description TEXT,
    location VARCHAR(200),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(254),
    is_active BOOLEAN DEFAULT TRUE,
    views INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Marketplace images
CREATE TABLE core_marketplaceimage (
    id SERIAL PRIMARY KEY,
    listing_id INTEGER NOT NULL REFERENCES core_marketplace(id) ON DELETE CASCADE,
    image VARCHAR(255) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Marketplace orders
CREATE TABLE core_marketplaceorder (
    id SERIAL PRIMARY KEY,
    listing_id INTEGER NOT NULL REFERENCES core_marketplace(id),
    buyer_id INTEGER NOT NULL REFERENCES auth_user(id),
    seller_id INTEGER NOT NULL REFERENCES auth_user(id),
    status VARCHAR(20) DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Marketplace reviews
CREATE TABLE core_marketplacereview (
    id SERIAL PRIMARY KEY,
    listing_id INTEGER NOT NULL REFERENCES core_marketplace(id),
    reviewer_id INTEGER NOT NULL REFERENCES auth_user(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(200),
    content TEXT,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User wallets
CREATE TABLE core_userwallet (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id),
    balance DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Payment transactions
CREATE TABLE core_paymenttransaction (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    transaction_type VARCHAR(50),
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    reference_id VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Orders
CREATE TABLE core_order (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER NOT NULL REFERENCES auth_user(id),
    seller_id INTEGER NOT NULL REFERENCES auth_user(id),
    status VARCHAR(20) DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    shipping_address_id INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Order items
CREATE TABLE core_orderitem (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES core_order(id),
    listing_id INTEGER NOT NULL REFERENCES core_marketplace(id),
    quantity INTEGER DEFAULT 1,
    unit_price DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Shipping addresses
CREATE TABLE core_shippingaddress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    street VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100),
    zip_code VARCHAR(20),
    country VARCHAR(100),
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Reviews
CREATE TABLE core_review (
    id SERIAL PRIMARY KEY,
    reviewer_id INTEGER NOT NULL REFERENCES auth_user(id),
    listing_id INTEGER NOT NULL REFERENCES core_marketplace(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(200),
    content TEXT,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Ratings
CREATE TABLE core_rating (
    id SERIAL PRIMARY KEY,
    rater_id INTEGER NOT NULL REFERENCES auth_user(id),
    rated_user_id INTEGER NOT NULL REFERENCES auth_user(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(rater_id, rated_user_id)
);

-- =====================================================
-- STEP 6: Create Car and Racing Features Tables
-- =====================================================

-- Car profiles
CREATE TABLE core_carprofile (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES auth_user(id),
    make VARCHAR(100),
    model VARCHAR(100),
    year INTEGER,
    engine VARCHAR(100),
    transmission VARCHAR(50),
    color VARCHAR(50),
    mileage INTEGER,
    description TEXT,
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Car images
CREATE TABLE core_carimage (
    id SERIAL PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES core_carprofile(id) ON DELETE CASCADE,
    image VARCHAR(255) NOT NULL,
    caption VARCHAR(200),
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Car modifications
CREATE TABLE core_carmodification (
    id SERIAL PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES core_carprofile(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    cost DECIMAL(10,2),
    installation_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Build logs
CREATE TABLE core_buildlog (
    id SERIAL PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES core_carprofile(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    likes_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Build milestones
CREATE TABLE core_buildmilestone (
    id SERIAL PRIMARY KEY,
    build_log_id INTEGER NOT NULL REFERENCES core_buildlog(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completion_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Build media
CREATE TABLE core_buildmedia (
    id SERIAL PRIMARY KEY,
    build_log_id INTEGER NOT NULL REFERENCES core_buildlog(id) ON DELETE CASCADE,
    media_type VARCHAR(20),
    file_path VARCHAR(255),
    caption VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Car tours
CREATE TABLE core_cartour (
    id SERIAL PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES core_carprofile(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    likes_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Performance data
CREATE TABLE core_performancedata (
    id SERIAL PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES core_carprofile(id) ON DELETE CASCADE,
    quarter_mile_time DECIMAL(6,3),
    quarter_mile_speed DECIMAL(6,2),
    zero_to_sixty DECIMAL(5,2),
    horsepower INTEGER,
    torque INTEGER,
    dyno_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Build wishlists
CREATE TABLE core_buildwishlist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    car_id INTEGER REFERENCES core_carprofile(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Wishlist suggestions
CREATE TABLE core_wishlistsuggestion (
    id SERIAL PRIMARY KEY,
    wishlist_id INTEGER NOT NULL REFERENCES core_buildwishlist(id) ON DELETE CASCADE,
    suggestion_text TEXT,
    priority INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Build ratings
CREATE TABLE core_buildrating (
    id SERIAL PRIMARY KEY,
    build_log_id INTEGER NOT NULL REFERENCES core_buildlog(id) ON DELETE CASCADE,
    rater_id INTEGER NOT NULL REFERENCES auth_user(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(build_log_id, rater_id)
);

-- Build comments
CREATE TABLE core_buildcomment (
    id SERIAL PRIMARY KEY,
    build_log_id INTEGER NOT NULL REFERENCES core_buildlog(id) ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES auth_user(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Build badges
CREATE TABLE core_buildbadge (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Build badge awards
CREATE TABLE core_buildbadgeaward (
    id SERIAL PRIMARY KEY,
    badge_id INTEGER NOT NULL REFERENCES core_buildbadge(id),
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    awarded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(badge_id, user_id)
);

-- Car listings
CREATE TABLE core_carlisting (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES auth_user(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    make VARCHAR(100),
    model VARCHAR(100),
    year INTEGER,
    price DECIMAL(10,2) NOT NULL,
    mileage INTEGER,
    condition VARCHAR(50),
    location VARCHAR(200),
    is_negotiable BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Listing images
CREATE TABLE core_listingimage (
    id SERIAL PRIMARY KEY,
    listing_id INTEGER NOT NULL REFERENCES core_carlisting(id) ON DELETE CASCADE,
    image VARCHAR(255) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- STEP 7: Create Additional Features Tables
-- =====================================================

-- Hot spots
CREATE TABLE core_hotspot (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    location VARCHAR(200),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    created_by INTEGER REFERENCES auth_user(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Location broadcasts
CREATE TABLE core_locationbroadcast (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    location VARCHAR(200),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    message TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Open challenges
CREATE TABLE core_openchallenge (
    id SERIAL PRIMARY KEY,
    challenger_id INTEGER NOT NULL REFERENCES auth_user(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    location VARCHAR(200),
    challenge_date TIMESTAMP WITH TIME ZONE,
    max_participants INTEGER,
    status VARCHAR(20) DEFAULT 'open',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Challenge responses
CREATE TABLE core_challengeresponse (
    id SERIAL PRIMARY KEY,
    challenge_id INTEGER NOT NULL REFERENCES core_openchallenge(id),
    responder_id INTEGER NOT NULL REFERENCES auth_user(id),
    message TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(challenge_id, responder_id)
);

-- Subscriptions
CREATE TABLE core_subscription (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    subscription_type VARCHAR(50),
    start_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    end_date TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Payments
CREATE TABLE core_payment (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    transaction_id VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);



-- Contact submissions
CREATE TABLE core_contactsubmission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(254) NOT NULL,
    subject VARCHAR(200),
    message TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- STEP 8: Create Indexes for Performance
-- =====================================================

-- User indexes
CREATE INDEX idx_auth_user_username ON auth_user(username);
CREATE INDEX idx_auth_user_email ON auth_user(email);

-- Social indexes
CREATE INDEX idx_core_userpost_author ON core_userpost(author_id);
CREATE INDEX idx_core_userpost_created ON core_userpost(created_at);
CREATE INDEX idx_core_friendship_sender ON core_friendship(sender_id);
CREATE INDEX idx_core_friendship_receiver ON core_friendship(receiver_id);
CREATE INDEX idx_core_message_sender ON core_message(sender_id);
CREATE INDEX idx_core_message_recipient ON core_message(recipient_id);

-- Marketplace indexes
CREATE INDEX idx_core_marketplace_seller ON core_marketplace(seller_id);
CREATE INDEX idx_core_marketplace_category ON core_marketplace(category);
CREATE INDEX idx_core_marketplace_price ON core_marketplace(price);
CREATE INDEX idx_core_marketplace_created ON core_marketplace(created_at);

-- Racing indexes
CREATE INDEX idx_core_event_start_date ON core_event(start_date);
CREATE INDEX idx_core_callout_challenger ON core_callout(challenger_id);
CREATE INDEX idx_core_callout_challenged ON core_callout(challenged_id);

-- =====================================================
-- STEP 9: Insert Sample Data
-- =====================================================

-- Insert Django content types
INSERT INTO django_content_type (app_label, model) VALUES
('auth', 'user'),
('auth', 'group'),
('auth', 'permission'),
('core', 'userprofile'),
('core', 'track'),
('core', 'event'),
('core', 'callout'),
('core', 'userpost'),
('core', 'marketplace'),
('core', 'friendship');

-- Insert permissions
INSERT INTO auth_permission (name, content_type_id, codename) VALUES
('Can add user', 1, 'add_user'),
('Can change user', 1, 'change_user'),
('Can delete user', 1, 'delete_user'),
('Can view user', 1, 'view_user'),
('Can add user profile', 4, 'add_userprofile'),
('Can change user profile', 4, 'change_userprofile'),
('Can delete user profile', 4, 'delete_userprofile'),
('Can view user profile', 4, 'view_userprofile');

-- Insert sample users
INSERT INTO auth_user (username, first_name, last_name, email, password, is_staff, is_active, is_superuser, date_joined) VALUES
('admin', 'Admin', 'User', 'admin@calloutracing.com', 'pbkdf2_sha256$600000$hash_here', true, true, true, NOW()),
('racer1', 'John', 'Doe', 'john@example.com', 'pbkdf2_sha256$600000$hash_here', false, true, false, NOW()),
('racer2', 'Jane', 'Smith', 'jane@example.com', 'pbkdf2_sha256$600000$hash_here', false, true, false, NOW()),
('seller1', 'Mike', 'Johnson', 'mike@example.com', 'pbkdf2_sha256$600000$hash_here', false, true, false, NOW()),
('buyer1', 'Sarah', 'Wilson', 'sarah@example.com', 'pbkdf2_sha256$600000$hash_here', false, true, false, NOW());

-- Insert user profiles
INSERT INTO core_userprofile (user_id, bio, location, car_make, car_model, wins, losses, total_races, email_verified) VALUES
(1, 'System Administrator', 'Los Angeles, CA', 'Chevrolet', 'Camaro', 0, 0, 0, true),
(2, 'Professional drag racer with 10 years experience', 'Los Angeles, CA', 'Chevrolet', 'Camaro', 15, 5, 20, true),
(3, 'Weekend warrior racer', 'Miami, FL', 'Ford', 'Mustang', 8, 12, 20, true),
(4, 'Car parts dealer and enthusiast', 'New York, NY', 'Dodge', 'Challenger', 5, 8, 13, true),
(5, 'Looking for my first race car', 'Chicago, IL', 'Honda', 'Civic', 0, 0, 0, true);

-- Insert tracks
INSERT INTO core_track (name, location, description, surface_type, length) VALUES
('Alabama International Dragway', 'Steele, AL', 'Premier drag racing facility', 'asphalt', 1320.00),
('LA Raceway', 'Los Angeles, CA', 'Local racing venue', 'concrete', 1320.00),
('Miami Speedway', 'Miami, FL', 'High-performance racing track', 'asphalt', 1320.00);

-- Insert listing categories
INSERT INTO core_listingcategory (name, description) VALUES
('Cars', 'Complete vehicles for sale'),
('Parts', 'Car parts and components'),
('Services', 'Racing and automotive services'),
('Equipment', 'Racing equipment and tools');

-- Insert sample marketplace listings
INSERT INTO core_marketplace (seller_id, title, description, category, condition, price, location, is_negotiable) VALUES
(4, '2018 Mustang GT', 'Well-maintained Mustang GT, perfect for racing', 'car', 'used', 35000.00, 'Los Angeles, CA', true),
(4, 'Turbo Kit for Honda Civic', 'Complete turbo kit, barely used', 'parts', 'used', 2500.00, 'New York, NY', true),
(4, 'Professional Tuning Service', 'ECU tuning and dyno services', 'services', 'new', 500.00, 'Miami, FL', false);

-- Insert sample social posts
INSERT INTO core_userpost (author_id, content, post_type, likes_count, comments_count, is_public) VALUES
(2, 'Just finished a great race at Alabama International Dragway! The new setup is working perfectly.', 'text', 0, 0, true),
(2, 'Looking for recommendations on the best drag racing tires for street use.', 'text', 0, 0, true),
(3, 'Friday Night Drags registration is now open! Don''t miss out on this amazing event.', 'text', 0, 0, true);

-- Insert sample friendships
INSERT INTO core_friendship (sender_id, receiver_id, status) VALUES
(2, 3, 'accepted'),
(2, 4, 'pending'),
(3, 4, 'accepted');

-- Insert sample events
INSERT INTO core_event (title, description, track_id, start_date, end_date, event_type, max_participants, entry_fee, created_by) VALUES
('Spring Championship', 'Annual spring drag racing championship', 1, '2024-04-15 09:00:00', '2024-04-15 18:00:00', 'championship', 50, 100.00, 1),
('Friday Night Drags', 'Weekly Friday night racing', 2, '2024-03-22 19:00:00', '2024-03-22 23:00:00', 'weekly', 30, 25.00, 1);

-- Insert sample callouts
INSERT INTO core_callout (challenger_id, challenged_id, event_id, message, status) VALUES
(2, 3, 1, 'Ready to race this weekend?', 'pending'),
(3, 2, 2, 'Let''s settle this on the track!', 'accepted');

-- Insert user wallets
INSERT INTO core_userwallet (user_id, balance) VALUES
(1, 1000.00),
(2, 500.00),
(3, 750.00),
(4, 2000.00),
(5, 100.00);

-- Insert sample notifications
INSERT INTO core_notification (recipient_id, sender_id, notification_type, title, message) VALUES
(3, 2, 'friend_request', 'New Friend Request', 'John Doe sent you a friend request'),
(4, 2, 'post_like', 'Post Liked', 'John Doe liked your post'),
(5, 4, 'marketplace_contact', 'New Message', 'You have a new message about your listing');

-- =====================================================
-- STEP 10: Create Sequences for Auto-incrementing IDs
-- =====================================================

-- Update sequences to start after the inserted data
SELECT setval('auth_user_id_seq', (SELECT MAX(id) FROM auth_user));
SELECT setval('core_userprofile_id_seq', (SELECT MAX(id) FROM core_userprofile));
SELECT setval('core_marketplace_id_seq', (SELECT MAX(id) FROM core_marketplace));
SELECT setval('core_userpost_id_seq', (SELECT MAX(id) FROM core_userpost));
SELECT setval('core_event_id_seq', (SELECT MAX(id) FROM core_event));

-- =====================================================
-- COMPLETION MESSAGE
-- =====================================================

DO $$
BEGIN
    RAISE NOTICE 'Database rebuild complete!';
    RAISE NOTICE 'Created % tables', (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public');
    RAISE NOTICE 'Inserted % users', (SELECT COUNT(*) FROM auth_user);
    RAISE NOTICE 'Inserted % marketplace listings', (SELECT COUNT(*) FROM core_marketplace);
    RAISE NOTICE 'Inserted % social posts', (SELECT COUNT(*) FROM core_userpost);
    RAISE NOTICE 'Database is ready for production use!';
END $$; 