-- Railway PostgreSQL Database Setup - Step by Step
-- Connect to: postgresql://postgres:QfGzdLFMYTfqmSAiohnrWGJGMMrQEMnK@caboose.proxy.rlwy.net:33954/railway

-- IMPORTANT: Django migrations must be run first!
-- If you get "table not found" errors, run Django migrations on Railway:
-- 1. Go to Railway dashboard
-- 2. Open shell for your backend service
-- 3. Run: python manage.py migrate
-- 4. Then run this script

-- =====================================================
-- STEP 1: Check what tables exist (run this first)
-- =====================================================

-- List all tables in the database (DBeaver compatible)
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Check current data counts (only if tables exist)
SELECT 'Current data counts:' as info;
SELECT 'auth_user' as table_name, COUNT(*) as count FROM auth_user
UNION ALL
SELECT 'core_track', COUNT(*) FROM core_track
UNION ALL
SELECT 'core_event', COUNT(*) FROM core_event
UNION ALL
SELECT 'core_callout', COUNT(*) FROM core_callout
UNION ALL
SELECT 'core_hotspot', COUNT(*) FROM core_hotspot;

-- =====================================================
-- STEP 2: Create admin user (run this second)
-- =====================================================

-- Create admin user
INSERT INTO auth_user (username, email, password, is_staff, is_superuser, is_active, date_joined, first_name, last_name)
VALUES (
    'admin',
    'admin@calloutracing.com',
    'pbkdf2_sha256$600000$dummy$dummy',
    true,
    true,
    true,
    NOW(),
    'Admin',
    'User'
) ON CONFLICT (username) DO NOTHING;

-- Create user profile for admin
INSERT INTO core_userprofile (user_id, bio, location, phone, is_verified, created_at, updated_at)
SELECT 
    id,
    'System Administrator',
    'United States',
    '+1234567890',
    true,
    NOW(),
    NOW()
FROM auth_user 
WHERE username = 'admin'
ON CONFLICT (user_id) DO NOTHING;

-- =====================================================
-- STEP 3: Create sample tracks (run this third)
-- =====================================================

-- Create sample tracks
INSERT INTO core_track (name, location, description, track_type, surface_type, length, is_active, created_at, updated_at)
VALUES 
    ('Alabama International Dragway', 'Steele, Alabama', 'Quarter-mile asphalt dragstrip opened in 1994.', 'drag', 'asphalt', 0.25, true, NOW(), NOW()),
    ('Atlanta Dragway', 'Commerce, Georgia', 'NHRA Camping World Drag Racing Series venue.', 'drag', 'concrete', 0.25, true, NOW(), NOW()),
    ('Bandimere Speedway', 'Morrison, Colorado', 'NHRA Camping World Drag Racing Series venue.', 'drag', 'concrete', 0.25, true, NOW(), NOW()),
    ('Bristol Dragway', 'Bristol, Tennessee', 'Quarter-mile concrete dragstrip opened in 1965.', 'drag', 'concrete', 0.25, true, NOW(), NOW()),
    ('Gainesville Raceway', 'Gainesville, Florida', 'NHRA Camping World Drag Racing Series venue.', 'drag', 'concrete', 0.25, true, NOW(), NOW())
ON CONFLICT (name) DO NOTHING;

-- =====================================================
-- STEP 4: Create sample events (run this fourth)
-- =====================================================

-- Create sample events
INSERT INTO core_event (title, description, event_type, start_date, end_date, max_participants, entry_fee, is_public, is_active, organizer_id, track_id, created_at, updated_at)
SELECT 
    'Friday Night Drags',
    'Weekly drag racing event for all skill levels',
    'race',
    NOW() + INTERVAL '7 days',
    NOW() + INTERVAL '7 days 4 hours',
    50,
    25.00,
    true,
    true,
    u.id,
    t.id,
    NOW(),
    NOW()
FROM auth_user u, core_track t
WHERE u.username = 'admin' AND t.name = 'Alabama International Dragway'
ON CONFLICT (title) DO NOTHING;

INSERT INTO core_event (title, description, event_type, start_date, end_date, max_participants, entry_fee, is_public, is_active, organizer_id, track_id, created_at, updated_at)
SELECT 
    'Test & Tune Session',
    'Open track time for testing and tuning',
    'test',
    NOW() + INTERVAL '14 days',
    NOW() + INTERVAL '14 days 6 hours',
    30,
    15.00,
    true,
    true,
    u.id,
    t.id,
    NOW(),
    NOW()
FROM auth_user u, core_track t
WHERE u.username = 'admin' AND t.name = 'Atlanta Dragway'
ON CONFLICT (title) DO NOTHING;

-- =====================================================
-- STEP 5: Create sample callouts (run this fifth)
-- =====================================================

-- Create sample callouts
INSERT INTO core_callout (challenger_id, challenged_id, location_type, track_id, street_location, city, state, race_type, wager_amount, message, experience_level, min_horsepower, max_horsepower, tire_requirement, rules, is_private, is_invite_only, status, scheduled_date, created_at, updated_at)
SELECT 
    u.id,
    u.id,
    'track',
    t.id,
    '',
    'Steele',
    'AL',
    'quarter_mile',
    100.00,
    'Looking for Competition - Anyone want to race? Stock vs Stock',
    'beginner',
    200,
    600,
    'Street legal tires only',
    'No nitrous, street legal cars only',
    false,
    false,
    'pending',
    NOW() + INTERVAL '10 days',
    NOW(),
    NOW()
FROM auth_user u, core_track t
WHERE u.username = 'admin' AND t.name = 'Alabama International Dragway'
ON CONFLICT (message) DO NOTHING;

INSERT INTO core_callout (challenger_id, challenged_id, location_type, track_id, street_location, city, state, race_type, wager_amount, message, experience_level, min_horsepower, max_horsepower, tire_requirement, rules, is_private, is_invite_only, status, scheduled_date, created_at, updated_at)
SELECT 
    u.id,
    u.id,
    'track',
    t.id,
    '',
    'Commerce',
    'GA',
    'quarter_mile',
    200.00,
    'Pro Challenge - Pro racers only. Serious competition.',
    'advanced',
    400,
    1000,
    'Drag radials allowed',
    'NHRA rules apply',
    false,
    true,
    'pending',
    NOW() + INTERVAL '15 days',
    NOW(),
    NOW()
FROM auth_user u, core_track t
WHERE u.username = 'admin' AND t.name = 'Atlanta Dragway'
ON CONFLICT (message) DO NOTHING;

-- =====================================================
-- STEP 6: Create sample hotspots (run this sixth)
-- =====================================================

-- Create sample hotspots
INSERT INTO core_hotspot (name, description, address, city, state, zip_code, latitude, longitude, spot_type, rules, amenities, peak_hours, is_verified, is_active, total_races, created_by_id, created_at, updated_at)
SELECT 
    'LA Raceway Pit Area',
    'Main pit area for racers',
    '123 Racing Blvd',
    'Los Angeles',
    'CA',
    '90210',
    34.0522,
    -118.2437,
    'track',
    'Safety first, no reckless driving',
    'Restrooms, food, parking',
    'Friday 6PM-12AM',
    true,
    true,
    150,
    u.id,
    NOW(),
    NOW()
FROM auth_user u
WHERE u.username = 'admin'
ON CONFLICT (name) DO NOTHING;

INSERT INTO core_hotspot (name, description, address, city, state, zip_code, latitude, longitude, spot_type, rules, amenities, peak_hours, is_verified, is_active, total_races, created_by_id, created_at, updated_at)
SELECT 
    'Miami Speedway Starting Line',
    'Where the action begins',
    '789 Drag Rd',
    'Miami',
    'FL',
    '33101',
    25.7617,
    -80.1918,
    'track',
    'NHRA rules apply',
    'Tech inspection, timing lights',
    'Sunday 10AM-6PM',
    true,
    true,
    300,
    u.id,
    NOW(),
    NOW()
FROM auth_user u
WHERE u.username = 'admin'
ON CONFLICT (name) DO NOTHING;

-- =====================================================
-- STEP 7: Create marketplace data (run this seventh)
-- =====================================================

-- Create listing categories
INSERT INTO core_listingcategory (name, description, parent_id)
VALUES 
    ('Cars', 'Complete vehicles for sale', NULL),
    ('Parts', 'Car parts and components', NULL),
    ('Services', 'Racing and automotive services', NULL),
    ('Equipment', 'Racing equipment and tools', NULL)
ON CONFLICT (name) DO NOTHING;

-- Create marketplace listings
INSERT INTO core_marketplacelisting (seller_id, title, description, category_id, price, condition, location, is_negotiable, created_at, updated_at)
SELECT 
    u.id,
    '2018 Mustang GT',
    'Well-maintained Mustang GT, perfect for racing',
    c.id,
    35000.00,
    'used',
    'Los Angeles, CA',
    true,
    NOW(),
    NOW()
FROM auth_user u, core_listingcategory c
WHERE u.username = 'admin' AND c.name = 'Cars'
ON CONFLICT (title) DO NOTHING;

INSERT INTO core_marketplacelisting (seller_id, title, description, category_id, price, condition, location, is_negotiable, created_at, updated_at)
SELECT 
    u.id,
    'Turbo Kit for Honda Civic',
    'Complete turbo kit, barely used',
    c.id,
    2500.00,
    'used',
    'New York, NY',
    true,
    NOW(),
    NOW()
FROM auth_user u, core_listingcategory c
WHERE u.username = 'admin' AND c.name = 'Parts'
ON CONFLICT (title) DO NOTHING;

-- =====================================================
-- STEP 8: Create social posts (run this eighth)
-- =====================================================

-- Create sample social posts
INSERT INTO core_userpost (author_id, content, post_type, likes_count, comments_count, is_public, created_at, updated_at)
SELECT 
    u.id,
    'Just finished a great race at Alabama International Dragway! The new setup is working perfectly.',
    'text',
    0,
    0,
    true,
    NOW(),
    NOW()
FROM auth_user u
WHERE u.username = 'admin'
ON CONFLICT (content) DO NOTHING;

INSERT INTO core_userpost (author_id, content, post_type, likes_count, comments_count, is_public, created_at, updated_at)
SELECT 
    u.id,
    'Looking for recommendations on the best drag racing tires for street use.',
    'text',
    0,
    0,
    true,
    NOW(),
    NOW()
FROM auth_user u
WHERE u.username = 'admin'
ON CONFLICT (content) DO NOTHING;

-- =====================================================
-- STEP 9: Final verification (run this last)
-- =====================================================

-- Show final summary
SELECT '=== FINAL DATABASE SUMMARY ===' as summary;

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
SELECT 'Social Posts', COUNT(*) FROM core_userpost;

-- Show admin user
SELECT '=== ADMIN USER ===' as admin_info;
SELECT username, email, is_superuser, is_active FROM auth_user WHERE username = 'admin';

-- Show sample data
SELECT '=== SAMPLE DATA ===' as sample_info;
SELECT 'Tracks:' as data_type, name, location FROM core_track LIMIT 3;
SELECT 'Events:' as data_type, title, event_type FROM core_event LIMIT 3;
SELECT 'Callouts:' as data_type, message, race_type FROM core_callout LIMIT 3; 