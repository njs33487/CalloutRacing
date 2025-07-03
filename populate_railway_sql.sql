-- Populate Railway PostgreSQL Database with Sample Data
-- Connect using: psql "postgresql://postgres:QfGzdLFMYTfqmSAiohnrWGJGMMrQEMnK@postgres.railway.internal:5432/railway"

-- First, let's check what tables exist
\dt

-- Check if we have any existing data
SELECT COUNT(*) FROM auth_user;
SELECT COUNT(*) FROM core_userprofile;
SELECT COUNT(*) FROM core_hotspot;
SELECT COUNT(*) FROM core_track;
SELECT COUNT(*) FROM core_event;
SELECT COUNT(*) FROM core_callout;
SELECT COUNT(*) FROM core_userpost;
SELECT COUNT(*) FROM core_marketplace;
SELECT COUNT(*) FROM core_listingcategory;
SELECT COUNT(*) FROM core_marketplacelisting;

-- Create admin user if it doesn't exist
INSERT INTO auth_user (username, email, password, is_staff, is_superuser, is_active, date_joined)
VALUES (
    'admin',
    'admin@calloutracing.com',
    'pbkdf2_sha256$600000$dummy$dummy', -- This will be replaced by Django's password hashing
    true,
    true,
    true,
    NOW()
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
    
    -- Create sample hotspots
    INSERT INTO core_hotspot (name, description, address, city, state, zip_code, latitude, longitude, spot_type, rules, amenities, peak_hours, is_verified, is_active, total_races, created_by_id, created_at, updated_at)
    VALUES 
        ('LA Raceway', 'Premier racing facility in Los Angeles', '123 Racing Blvd', 'Los Angeles', 'CA', '90210', 34.0522, -118.2437, 'track', 'Safety first, no reckless driving', 'Restrooms, food, parking', 'Friday 6PM-12AM', true, true, 150, admin_user_id, NOW(), NOW()),
        ('NY Speedway', 'High-speed oval track', '456 Speed Ave', 'New York', 'NY', '10001', 40.7128, -74.0060, 'track', 'Helmets required, follow flag signals', 'Pit area, timing system', 'Saturday 2PM-10PM', true, true, 200, admin_user_id, NOW(), NOW()),
        ('Miami Drag Strip', 'Quarter mile drag racing', '789 Drag Rd', 'Miami', 'FL', '33101', 25.7617, -80.1918, 'track', 'NHRA rules apply', 'Tech inspection, timing lights', 'Sunday 10AM-6PM', true, true, 300, admin_user_id, NOW(), NOW()),
        ('Chicago Industrial Zone', 'Popular street meet location', '321 Industrial St', 'Chicago', 'IL', '60601', 41.8781, -87.6298, 'industrial', 'Be respectful, clean up after', 'Large parking area', 'Friday 8PM-2AM', false, true, 75, admin_user_id, NOW(), NOW()),
        ('Houston Parking Lot', 'Weekend car meet spot', '654 Meet Ave', 'Houston', 'TX', '77001', 29.7604, -95.3698, 'parking_lot', 'No racing, display only', 'Food trucks, music', 'Saturday 6PM-11PM', false, true, 50, admin_user_id, NOW(), NOW());
    
    -- Create sample tracks
    INSERT INTO core_track (name, location, description, track_type, surface_type, length, is_active, created_at, updated_at)
    VALUES 
        ('LA Raceway', 'Los Angeles, CA', 'Premier road course with multiple configurations', 'road_course', 'asphalt', 2.5, true, NOW(), NOW()),
        ('NY Speedway', 'New York, NY', 'High-speed oval track for stock car racing', 'oval', 'asphalt', 1.5, true, NOW(), NOW()),
        ('Miami Circuit', 'Miami, FL', 'Technical road course with elevation changes', 'road_course', 'asphalt', 3.2, true, NOW(), NOW()),
        ('Chicago Track', 'Chicago, IL', 'Multi-purpose racing facility', 'oval', 'concrete', 1.0, true, NOW(), NOW()),
        ('Houston Dragway', 'Houston, TX', 'Quarter mile drag strip', 'drag', 'asphalt', 0.25, true, NOW(), NOW());
    
    -- Get track IDs for events
    DECLARE
        la_track_id INTEGER;
        miami_track_id INTEGER;
        ny_track_id INTEGER;
    BEGIN
        SELECT id INTO la_track_id FROM core_track WHERE name = 'LA Raceway';
        SELECT id INTO miami_track_id FROM core_track WHERE name = 'Miami Circuit';
        SELECT id INTO ny_track_id FROM core_track WHERE name = 'NY Speedway';
        
        -- Create sample events
        INSERT INTO core_event (title, description, event_type, start_date, end_date, max_participants, entry_fee, is_public, is_active, organizer_id, track_id, created_at, updated_at)
        VALUES 
            ('Spring Racing Championship', 'Annual spring racing event with multiple classes', 'race', '2024-04-15 09:00:00', '2024-04-17 18:00:00', 100, 150.00, true, true, admin_user_id, la_track_id, NOW(), NOW()),
            ('Summer Drag Racing Series', 'Weekly drag racing series throughout summer', 'race', '2024-06-01 10:00:00', '2024-08-31 22:00:00', 50, 75.00, true, true, admin_user_id, miami_track_id, NOW(), NOW()),
            ('Fall Track Day', 'Open track day for all skill levels', 'meet', '2024-10-20 08:00:00', '2024-10-20 17:00:00', 75, 50.00, true, true, admin_user_id, ny_track_id, NOW(), NOW());
    END;
    
    -- Create sample callouts
    INSERT INTO core_callout (challenger_id, challenged_id, location_type, track_id, street_location, city, state, race_type, wager_amount, message, experience_level, min_horsepower, max_horsepower, tire_requirement, rules, is_private, is_invite_only, status, scheduled_date, created_at, updated_at)
    VALUES 
        (admin_user_id, admin_user_id, 'street', NULL, 'Downtown LA', 'Los Angeles', 'CA', 'quarter_mile', 100.00, 'Looking for challengers in the LA area', 'intermediate', 300, 800, 'Street legal tires only', 'No nitrous, street legal cars only', false, false, 'pending', '2024-04-20 20:00:00', NOW(), NOW()),
        (admin_user_id, admin_user_id, 'track', miami_track_id, '', 'Miami', 'FL', 'quarter_mile', 200.00, 'Quarter mile challenge at Miami Speedway', 'advanced', 400, 1000, 'Drag radials allowed', 'NHRA rules apply', false, true, 'pending', '2024-05-15 19:00:00', NOW(), NOW());
    
    -- Create sample listing categories
    INSERT INTO core_listingcategory (name, description, parent_id)
    VALUES 
        ('Cars', 'Complete vehicles for sale', NULL),
        ('Parts', 'Car parts and components', NULL),
        ('Services', 'Racing and automotive services', NULL),
        ('Equipment', 'Racing equipment and tools', NULL);
    
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
            (admin_user_id, 'Professional Tuning Service', 'ECU tuning and dyno services', services_cat_id, 500.00, 'new', 'Miami, FL', false, NOW(), NOW());
    END;
    
    -- Create sample social posts
    INSERT INTO core_userpost (author_id, content, post_type, likes_count, comments_count, is_public, created_at, updated_at)
    VALUES 
        (admin_user_id, 'Just finished a great race at LA Raceway! The new setup is working perfectly.', 'text', 0, 0, true, NOW(), NOW()),
        (admin_user_id, 'Looking for recommendations on the best drag racing tires for street use.', 'text', 0, 0, true, NOW(), NOW()),
        (admin_user_id, 'Spring Championship registration is now open! Don''t miss out on this amazing event.', 'text', 0, 0, true, NOW(), NOW());
    
    -- Get post IDs for comments
    DECLARE
        post1_id INTEGER;
        post2_id INTEGER;
        post3_id INTEGER;
    BEGIN
        SELECT id INTO post1_id FROM core_userpost WHERE content LIKE 'Just finished a great race%' LIMIT 1;
        SELECT id INTO post2_id FROM core_userpost WHERE content LIKE 'Looking for recommendations%' LIMIT 1;
        SELECT id INTO post3_id FROM core_userpost WHERE content LIKE 'Spring Championship registration%' LIMIT 1;
        
        -- Create sample comments
        INSERT INTO core_postcomment (post_id, author_id, content, likes_count, created_at)
        VALUES 
            (post1_id, admin_user_id, 'Great job! What was your time?', 0, NOW()),
            (post2_id, admin_user_id, 'I recommend Michelin Pilot Sport tires', 0, NOW()),
            (post3_id, admin_user_id, 'Count me in! Can''t wait for the championship', 0, NOW());
    END;
    
END $$;

-- Display summary of created data
SELECT 'Users' as table_name, COUNT(*) as count FROM auth_user
UNION ALL
SELECT 'User Profiles', COUNT(*) FROM core_userprofile
UNION ALL
SELECT 'Hotspots', COUNT(*) FROM core_hotspot
UNION ALL
SELECT 'Tracks', COUNT(*) FROM core_track
UNION ALL
SELECT 'Events', COUNT(*) FROM core_event
UNION ALL
SELECT 'Callouts', COUNT(*) FROM core_callout
UNION ALL
SELECT 'Listing Categories', COUNT(*) FROM core_listingcategory
UNION ALL
SELECT 'Marketplace Listings', COUNT(*) FROM core_marketplacelisting
UNION ALL
SELECT 'Social Posts', COUNT(*) FROM core_userpost
UNION ALL
SELECT 'Comments', COUNT(*) FROM core_postcomment;

-- Show admin user details
SELECT username, email, is_superuser, date_joined FROM auth_user WHERE username = 'admin'; 