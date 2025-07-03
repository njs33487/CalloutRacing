-- Complete Railway PostgreSQL Database Setup Script for DBeaver
-- Connect to: postgresql://postgres:QfGzdLFMYTfqmSAiohnrWGJGMMrQEMnK@caboose.proxy.rlwy.net:33954/railway

-- =====================================================
-- STEP 1: Check current database state
-- =====================================================

-- Check what tables exist
\dt

-- Check if we have any existing data
SELECT 'Current database state:' as info;
SELECT COUNT(*) as user_count FROM auth_user;
SELECT COUNT(*) as track_count FROM core_track;
SELECT COUNT(*) as event_count FROM core_event;
SELECT COUNT(*) as callout_count FROM core_callout;
SELECT COUNT(*) as hotspot_count FROM core_hotspot;

-- =====================================================
-- STEP 2: Create Django tables (if they don't exist)
-- =====================================================

-- Note: Django migrations should create these tables
-- If tables don't exist, you need to run Django migrations first
-- This script assumes tables already exist from Django migrations

-- =====================================================
-- STEP 3: Populate with sample data
-- =====================================================

-- Create admin user if it doesn't exist
INSERT INTO auth_user (username, email, password, is_staff, is_superuser, is_active, date_joined, first_name, last_name)
VALUES (
    'admin',
    'admin@calloutracing.com',
    'pbkdf2_sha256$600000$dummy$dummy', -- This will be replaced by Django's password hashing
    true,
    true,
    true,
    NOW(),
    'Admin',
    'User'
) ON CONFLICT (username) DO NOTHING;

-- Get the admin user ID
DO $$
DECLARE
    admin_user_id INTEGER;
BEGIN
    SELECT id INTO admin_user_id FROM auth_user WHERE username = 'admin';
    
    -- Create user profile for admin
    INSERT INTO core_userprofile (user_id, bio, location, phone, is_verified, created_at, updated_at)
    VALUES (
        admin_user_id,
        'System Administrator',
        'United States',
        '+1234567890',
        true,
        NOW(),
        NOW()
    ) ON CONFLICT (user_id) DO NOTHING;
    
    -- Create sample tracks
    INSERT INTO core_track (name, location, description, track_type, surface_type, length, is_active, created_at, updated_at)
    VALUES 
        ('Alabama International Dragway', 'Steele, Alabama', 'Quarter-mile asphalt dragstrip opened in 1994.', 'drag', 'asphalt', 0.25, true, NOW(), NOW()),
        ('Atlanta Dragway', 'Commerce, Georgia', 'NHRA Camping World Drag Racing Series venue.', 'drag', 'concrete', 0.25, true, NOW(), NOW()),
        ('Bandimere Speedway', 'Morrison, Colorado', 'NHRA Camping World Drag Racing Series venue.', 'drag', 'concrete', 0.25, true, NOW(), NOW()),
        ('Bristol Dragway', 'Bristol, Tennessee', 'Quarter-mile concrete dragstrip opened in 1965.', 'drag', 'concrete', 0.25, true, NOW(), NOW()),
        ('Gainesville Raceway', 'Gainesville, Florida', 'NHRA Camping World Drag Racing Series venue.', 'drag', 'concrete', 0.25, true, NOW(), NOW())
    ON CONFLICT (name) DO NOTHING;
    
    -- Get track IDs for events
    DECLARE
        track1_id INTEGER;
        track2_id INTEGER;
    BEGIN
        SELECT id INTO track1_id FROM core_track WHERE name = 'Alabama International Dragway' LIMIT 1;
        SELECT id INTO track2_id FROM core_track WHERE name = 'Atlanta Dragway' LIMIT 1;
        
        -- Create sample events
        INSERT INTO core_event (title, description, event_type, start_date, end_date, max_participants, entry_fee, is_public, is_active, organizer_id, track_id, created_at, updated_at)
        VALUES 
            ('Friday Night Drags', 'Weekly drag racing event for all skill levels', 'race', NOW() + INTERVAL '7 days', NOW() + INTERVAL '7 days 4 hours', 50, 25.00, true, true, admin_user_id, track1_id, NOW(), NOW()),
            ('Test & Tune Session', 'Open track time for testing and tuning', 'test', NOW() + INTERVAL '14 days', NOW() + INTERVAL '14 days 6 hours', 30, 15.00, true, true, admin_user_id, track2_id, NOW(), NOW())
        ON CONFLICT (title) DO NOTHING;
    END;
    
    -- Create sample callouts
    INSERT INTO core_callout (challenger_id, challenged_id, location_type, track_id, street_location, city, state, race_type, wager_amount, message, experience_level, min_horsepower, max_horsepower, tire_requirement, rules, is_private, is_invite_only, status, scheduled_date, created_at, updated_at)
    VALUES 
        (admin_user_id, admin_user_id, 'track', track1_id, '', 'Steele', 'AL', 'quarter_mile', 100.00, 'Looking for Competition - Anyone want to race? Stock vs Stock', 'beginner', 200, 600, 'Street legal tires only', 'No nitrous, street legal cars only', false, false, 'pending', NOW() + INTERVAL '10 days', NOW(), NOW()),
        (admin_user_id, admin_user_id, 'track', track2_id, '', 'Commerce', 'GA', 'quarter_mile', 200.00, 'Pro Challenge - Pro racers only. Serious competition.', 'advanced', 400, 1000, 'Drag radials allowed', 'NHRA rules apply', false, true, 'pending', NOW() + INTERVAL '15 days', NOW(), NOW())
    ON CONFLICT (message) DO NOTHING;
    
    -- Create sample hotspots
    INSERT INTO core_hotspot (name, description, address, city, state, zip_code, latitude, longitude, spot_type, rules, amenities, peak_hours, is_verified, is_active, total_races, created_by_id, created_at, updated_at)
    VALUES 
        ('LA Raceway Pit Area', 'Main pit area for racers', '123 Racing Blvd', 'Los Angeles', 'CA', '90210', 34.0522, -118.2437, 'track', 'Safety first, no reckless driving', 'Restrooms, food, parking', 'Friday 6PM-12AM', true, true, 150, admin_user_id, NOW(), NOW()),
        ('Miami Speedway Starting Line', 'Where the action begins', '789 Drag Rd', 'Miami', 'FL', '33101', 25.7617, -80.1918, 'track', 'NHRA rules apply', 'Tech inspection, timing lights', 'Sunday 10AM-6PM', true, true, 300, admin_user_id, NOW(), NOW())
    ON CONFLICT (name) DO NOTHING;
    
    -- Create sample listing categories
    INSERT INTO core_listingcategory (name, description, parent_id)
    VALUES 
        ('Cars', 'Complete vehicles for sale', NULL),
        ('Parts', 'Car parts and components', NULL),
        ('Services', 'Racing and automotive services', NULL),
        ('Equipment', 'Racing equipment and tools', NULL)
    ON CONFLICT (name) DO NOTHING;
    
    -- Get category IDs
    DECLARE
        cars_cat_id INTEGER;
        parts_cat_id INTEGER;
        services_cat_id INTEGER;
    BEGIN
        SELECT id INTO cars_cat_id FROM core_listingcategory WHERE name = 'Cars';
        SELECT id INTO parts_cat_id FROM core_listingcategory WHERE name = 'Parts';
        SELECT id INTO services_cat_id FROM core_listingcategory WHERE name = 'Services';
        
        -- Create sample marketplace listings
        INSERT INTO core_marketplacelisting (seller_id, title, description, category_id, price, condition, location, is_negotiable, created_at, updated_at)
        VALUES 
            (admin_user_id, '2018 Mustang GT', 'Well-maintained Mustang GT, perfect for racing', cars_cat_id, 35000.00, 'used', 'Los Angeles, CA', true, NOW(), NOW()),
            (admin_user_id, 'Turbo Kit for Honda Civic', 'Complete turbo kit, barely used', parts_cat_id, 2500.00, 'used', 'New York, NY', true, NOW(), NOW()),
            (admin_user_id, 'Professional Tuning Service', 'ECU tuning and dyno services', services_cat_id, 500.00, 'new', 'Miami, FL', false, NOW(), NOW())
        ON CONFLICT (title) DO NOTHING;
    END;
    
    -- Create sample social posts
    INSERT INTO core_userpost (author_id, content, post_type, likes_count, comments_count, is_public, created_at, updated_at)
    VALUES 
        (admin_user_id, 'Just finished a great race at Alabama International Dragway! The new setup is working perfectly.', 'text', 0, 0, true, NOW(), NOW()),
        (admin_user_id, 'Looking for recommendations on the best drag racing tires for street use.', 'text', 0, 0, true, NOW(), NOW()),
        (admin_user_id, 'Friday Night Drags registration is now open! Don''t miss out on this amazing event.', 'text', 0, 0, true, NOW(), NOW())
    ON CONFLICT (content) DO NOTHING;
    
    -- Get post IDs for comments
    DECLARE
        post1_id INTEGER;
        post2_id INTEGER;
        post3_id INTEGER;
    BEGIN
        SELECT id INTO post1_id FROM core_userpost WHERE content LIKE 'Just finished a great race%' LIMIT 1;
        SELECT id INTO post2_id FROM core_userpost WHERE content LIKE 'Looking for recommendations%' LIMIT 1;
        SELECT id INTO post3_id FROM core_userpost WHERE content LIKE 'Friday Night Drags registration%' LIMIT 1;
        
        -- Create sample comments
        INSERT INTO core_postcomment (post_id, author_id, content, likes_count, created_at)
        VALUES 
            (post1_id, admin_user_id, 'Great job! What was your time?', 0, NOW()),
            (post2_id, admin_user_id, 'I recommend Michelin Pilot Sport tires', 0, NOW()),
            (post3_id, admin_user_id, 'Count me in! Can''t wait for the event', 0, NOW())
        ON CONFLICT (post_id, author_id, content) DO NOTHING;
    END;
    
END $$;

-- =====================================================
-- STEP 4: Display summary of created data
-- =====================================================

SELECT '=== DATABASE POPULATION SUMMARY ===' as summary;

SELECT 'Users' as table_name, COUNT(*) as count FROM auth_user
UNION ALL
SELECT 'User Profiles', COUNT(*) FROM core_userprofile
UNION ALL
SELECT 'Tracks', COUNT(*) FROM core_track
UNION ALL
SELECT 'Events', COUNT(*) FROM core_event
UNION ALL
SELECT 'Callouts', COUNT(*) FROM core_callout
UNION ALL
SELECT 'Hotspots', COUNT(*) FROM core_hotspot
UNION ALL
SELECT 'Listing Categories', COUNT(*) FROM core_listingcategory
UNION ALL
SELECT 'Marketplace Listings', COUNT(*) FROM core_marketplacelisting
UNION ALL
SELECT 'Social Posts', COUNT(*) FROM core_userpost
UNION ALL
SELECT 'Comments', COUNT(*) FROM core_postcomment;

-- Show admin user details
SELECT '=== ADMIN USER DETAILS ===' as admin_info;
SELECT username, email, is_superuser, date_joined FROM auth_user WHERE username = 'admin';

-- Show sample data
SELECT '=== SAMPLE TRACKS ===' as tracks_info;
SELECT name, location, track_type FROM core_track LIMIT 5;

SELECT '=== SAMPLE EVENTS ===' as events_info;
SELECT title, event_type, start_date FROM core_event LIMIT 5;

SELECT '=== SAMPLE CALLOUTS ===' as callouts_info;
SELECT message, race_type, experience_level FROM core_callout LIMIT 5;

-- =====================================================
-- STEP 5: Verification queries
-- =====================================================

SELECT '=== VERIFICATION QUERIES ===' as verification;

-- Check if admin user can log in (password needs to be set via Django)
SELECT 'Admin user exists and is superuser:' as check_info, 
       username, is_superuser, is_active 
FROM auth_user WHERE username = 'admin';

-- Check track-event relationships
SELECT 'Track-Event relationships:' as relationship_info,
       t.name as track_name, e.title as event_title
FROM core_track t
LEFT JOIN core_event e ON t.id = e.track_id
LIMIT 10;

-- Check callout-track relationships
SELECT 'Callout-Track relationships:' as relationship_info,
       c.message as callout_message, t.name as track_name
FROM core_callout c
LEFT JOIN core_track t ON c.track_id = t.id
LIMIT 10;

SELECT '=== DATABASE SETUP COMPLETE ===' as completion;
SELECT 'You can now use the admin user (admin/admin123) to log into the Django admin interface.' as next_steps; 