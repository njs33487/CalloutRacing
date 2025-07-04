-- =====================================================
-- POPULATE SAMPLE DATA - CalloutRacing
-- This script populates the database with realistic sample data
-- =====================================================

-- First, let's fix the django_content_type table
ALTER TABLE django_content_type ADD COLUMN IF NOT EXISTS name VARCHAR(100);
UPDATE django_content_type SET name = CONCAT(app_label, '.', model) WHERE name IS NULL;
ALTER TABLE django_content_type ALTER COLUMN name SET NOT NULL;

-- =====================
-- POPULATE USERS
-- =====================

-- Create sample users
INSERT INTO core_user (username, email, password, is_superuser, is_staff, is_active, date_joined, email_verified) VALUES
('admin', 'admin@calloutracing.com', 'pbkdf2_sha256$600000$dummy_hash_for_demo', TRUE, TRUE, TRUE, NOW(), TRUE),
('john_racer', 'john@example.com', 'pbkdf2_sha256$600000$dummy_hash_for_demo', FALSE, FALSE, TRUE, NOW(), TRUE),
('sarah_speed', 'sarah@example.com', 'pbkdf2_sha256$600000$dummy_hash_for_demo', FALSE, FALSE, TRUE, NOW(), TRUE),
('mike_drag', 'mike@example.com', 'pbkdf2_sha256$600000$dummy_hash_for_demo', FALSE, FALSE, TRUE, NOW(), TRUE),
('lisa_turbo', 'lisa@example.com', 'pbkdf2_sha256$600000$dummy_hash_for_demo', FALSE, FALSE, TRUE, NOW(), TRUE),
('david_burnout', 'david@example.com', 'pbkdf2_sha256$600000$dummy_hash_for_demo', FALSE, FALSE, TRUE, NOW(), TRUE),
('emma_nitro', 'emma@example.com', 'pbkdf2_sha256$600000$dummy_hash_for_demo', FALSE, FALSE, TRUE, NOW(), TRUE),
('alex_shift', 'alex@example.com', 'pbkdf2_sha256$600000$dummy_hash_for_demo', FALSE, FALSE, TRUE, NOW(), TRUE),
('jessica_boost', 'jessica@example.com', 'pbkdf2_sha256$600000$dummy_hash_for_demo', FALSE, FALSE, TRUE, NOW(), TRUE),
('ryan_race', 'ryan@example.com', 'pbkdf2_sha256$600000$dummy_hash_for_demo', FALSE, FALSE, TRUE, NOW(), TRUE)
ON CONFLICT (username) DO NOTHING;

-- Create user profiles
INSERT INTO core_userprofile (user_id, bio, location, phone, car_make, car_model, year, wins, losses, total_races, email_verified, is_verified) VALUES
(2, 'Street racing enthusiast with 10 years experience. Love drag racing and car meets.', 'Los Angeles, CA', '555-0101', 'Ford', 'Mustang', 2018, 45, 12, 57, TRUE, TRUE),
(3, 'Professional drag racer. Multiple track records holder. Available for coaching.', 'Houston, TX', '555-0102', 'Chevrolet', 'Camaro', 2020, 78, 8, 86, TRUE, TRUE),
(4, 'Car enthusiast and mechanic. Specialize in engine modifications and tuning.', 'Phoenix, AZ', '555-0103', 'Dodge', 'Challenger', 2019, 32, 15, 47, TRUE, TRUE),
(5, 'Racing photographer and car enthusiast. Love capturing the action on and off track.', 'Miami, FL', '555-0104', 'Nissan', 'GT-R', 2021, 28, 20, 48, TRUE, TRUE),
(6, 'Street racer turned track racer. Safety first, speed second.', 'Dallas, TX', '555-0105', 'Toyota', 'Supra', 2020, 55, 18, 73, TRUE, TRUE),
(7, 'Engine builder and racer. Custom turbo setups are my specialty.', 'Las Vegas, NV', '555-0106', 'BMW', 'M3', 2019, 42, 25, 67, TRUE, TRUE),
(8, 'Young racer with big dreams. Learning from the best in the community.', 'San Diego, CA', '555-0107', 'Honda', 'Civic', 2017, 15, 30, 45, TRUE, FALSE),
(9, 'Car show organizer and racer. Bringing the community together.', 'Austin, TX', '555-0108', 'Subaru', 'WRX STI', 2020, 38, 22, 60, TRUE, TRUE),
(10, 'Professional tuner and racer. ECU mapping and dyno tuning services.', 'Orlando, FL', '555-0109', 'Mitsubishi', 'Lancer Evo', 2018, 65, 12, 77, TRUE, TRUE),
(11, 'New to racing but passionate about cars. Looking to learn and grow.', 'Tampa, FL', '555-0110', 'Volkswagen', 'Golf GTI', 2019, 8, 35, 43, TRUE, FALSE)
ON CONFLICT (user_id) DO NOTHING;

-- =====================
-- POPULATE TRACKS
-- =====================

INSERT INTO core_track (name, location, description, track_type, surface_type, length, is_active) VALUES
('Los Angeles Raceway', 'Los Angeles, CA', 'Premier drag racing facility with multiple lanes and professional timing systems.', 'drag_strip', 'asphalt', 1320.00, TRUE),
('Houston Motorsports Park', 'Houston, TX', 'State-of-the-art racing complex with both drag and road course options.', 'drag_strip', 'concrete', 1320.00, TRUE),
('Phoenix International Raceway', 'Phoenix, AZ', 'Historic track known for high-speed racing and excellent facilities.', 'drag_strip', 'asphalt', 1320.00, TRUE),
('Miami Speedway', 'Miami, FL', 'Coastal racing venue with beautiful views and challenging conditions.', 'drag_strip', 'concrete', 1320.00, TRUE),
('Dallas Raceway', 'Dallas, TX', 'Modern facility with advanced timing and safety systems.', 'drag_strip', 'asphalt', 1320.00, TRUE),
('Las Vegas Motor Speedway', 'Las Vegas, NV', 'World-class facility hosting major racing events.', 'drag_strip', 'concrete', 1320.00, TRUE),
('San Diego Raceway', 'San Diego, CA', 'Community-focused track perfect for beginners and pros alike.', 'drag_strip', 'asphalt', 1320.00, TRUE),
('Austin Motorsports Complex', 'Austin, TX', 'Multi-purpose racing facility with drag strip and road course.', 'drag_strip', 'concrete', 1320.00, TRUE),
('Orlando Speedway', 'Orlando, FL', 'Family-friendly racing venue with excellent spectator facilities.', 'drag_strip', 'asphalt', 1320.00, TRUE),
('Tampa Bay Raceway', 'Tampa, FL', 'Coastal track known for its challenging weather conditions.', 'drag_strip', 'concrete', 1320.00, TRUE)
ON CONFLICT (name) DO NOTHING;

-- =====================
-- POPULATE EVENTS
-- =====================

INSERT INTO core_event (title, description, track_id, start_date, end_date, event_type, max_participants, entry_fee, is_public, is_active, organizer_id, created_by) VALUES
('Spring Drag Championship', 'Annual spring drag racing championship with cash prizes and trophies.', 1, NOW() + INTERVAL '30 days', NOW() + INTERVAL '30 days' + INTERVAL '8 hours', 'championship', 64, 150.00, TRUE, TRUE, 2, 2),
('Street Legal Drag Night', 'Monthly street legal drag racing event. All cars welcome.', 2, NOW() + INTERVAL '7 days', NOW() + INTERVAL '7 days' + INTERVAL '6 hours', 'street_legal', 32, 50.00, TRUE, TRUE, 3, 3),
('Import vs Domestic Showdown', 'Epic battle between import and domestic cars. Separate classes for each.', 3, NOW() + INTERVAL '14 days', NOW() + INTERVAL '14 days' + INTERVAL '10 hours', 'showdown', 48, 75.00, TRUE, TRUE, 4, 4),
('Tuner Car Meet & Race', 'Car show followed by drag racing. Best of both worlds.', 4, NOW() + INTERVAL '21 days', NOW() + INTERVAL '21 days' + INTERVAL '12 hours', 'meet_and_race', 40, 60.00, TRUE, TRUE, 5, 5),
('Pro-Am Racing Series', 'Professional and amateur racers compete in separate classes.', 5, NOW() + INTERVAL '45 days', NOW() + INTERVAL '45 days' + INTERVAL '8 hours', 'pro_am', 56, 100.00, TRUE, TRUE, 6, 6),
('Night Racing Spectacular', 'Under the lights racing with special effects and entertainment.', 6, NOW() + INTERVAL '60 days', NOW() + INTERVAL '60 days' + INTERVAL '6 hours', 'night_racing', 36, 80.00, TRUE, TRUE, 7, 7),
('Beginner Friendly Race Day', 'Perfect for new racers. Instruction and guidance provided.', 7, NOW() + INTERVAL '10 days', NOW() + INTERVAL '10 days' + INTERVAL '4 hours', 'beginner', 24, 25.00, TRUE, TRUE, 8, 8),
('Car Show & Drag Racing', 'Show your car and race it too. Multiple categories.', 8, NOW() + INTERVAL '35 days', NOW() + INTERVAL '35 days' + INTERVAL '10 hours', 'show_and_race', 44, 70.00, TRUE, TRUE, 9, 9),
('Tuner Challenge', 'Modified car competition with dyno testing and drag racing.', 9, NOW() + INTERVAL '50 days', NOW() + INTERVAL '50 days' + INTERVAL '8 hours', 'tuner_challenge', 32, 90.00, TRUE, TRUE, 10, 10),
('Community Race Day', 'Bring the community together for friendly competition.', 10, NOW() + INTERVAL '15 days', NOW() + INTERVAL '15 days' + INTERVAL '6 hours', 'community', 28, 40.00, TRUE, TRUE, 11, 11)
ON CONFLICT DO NOTHING;

-- =====================
-- POPULATE CALLOUTS
-- =====================

INSERT INTO core_callout (challenger_id, challenged_id, event_id, location_type, track_id, street_location, city, state, race_type, wager_amount, message, experience_level, min_horsepower, max_horsepower, status, scheduled_date) VALUES
(2, 3, 1, 'track', 1, NULL, 'Los Angeles', 'CA', 'drag_race', 500.00, 'Ready to see what your Camaro can do against my Mustang!', 'intermediate', 400, 600, 'accepted', NOW() + INTERVAL '5 days'),
(4, 5, 2, 'track', 2, NULL, 'Houston', 'TX', 'drag_race', 300.00, 'Challenger vs GT-R, let''s see who''s faster!', 'advanced', 450, 700, 'pending', NOW() + INTERVAL '3 days'),
(6, 7, 3, 'track', 3, NULL, 'Phoenix', 'AZ', 'drag_race', 200.00, 'Supra vs M3, classic battle!', 'intermediate', 350, 550, 'accepted', NOW() + INTERVAL '7 days'),
(8, 9, 4, 'track', 4, NULL, 'Miami', 'FL', 'drag_race', 150.00, 'Civic vs WRX, import showdown!', 'beginner', 200, 400, 'pending', NOW() + INTERVAL '2 days'),
(10, 11, 5, 'track', 5, NULL, 'Dallas', 'TX', 'drag_race', 400.00, 'Evo vs GTI, turbo battle!', 'advanced', 300, 500, 'accepted', NOW() + INTERVAL '4 days')
ON CONFLICT DO NOTHING;

-- =====================
-- POPULATE SOCIAL FEATURES
-- =====================

-- Follow relationships
INSERT INTO core_follow (follower_id, following_id) VALUES
(2, 3), (2, 4), (2, 5),
(3, 2), (3, 6), (3, 7),
(4, 2), (4, 3), (4, 8),
(5, 2), (5, 4), (5, 9),
(6, 3), (6, 4), (6, 10),
(7, 2), (7, 5), (7, 11),
(8, 4), (8, 6), (8, 9),
(9, 5), (9, 7), (9, 10),
(10, 6), (10, 8), (10, 11),
(11, 7), (11, 9), (11, 10)
ON CONFLICT DO NOTHING;

-- Friendships
INSERT INTO core_friendship (sender_id, receiver_id, status) VALUES
(2, 3, 'accepted'), (2, 4, 'accepted'), (2, 5, 'pending'),
(3, 6, 'accepted'), (3, 7, 'accepted'), (3, 8, 'pending'),
(4, 9, 'accepted'), (4, 10, 'accepted'), (4, 11, 'pending'),
(5, 6, 'accepted'), (5, 7, 'pending'), (5, 8, 'accepted'),
(6, 9, 'accepted'), (6, 10, 'accepted'), (6, 11, 'pending')
ON CONFLICT DO NOTHING;

-- User posts
INSERT INTO core_userpost (author_id, content, post_type, likes_count, comments_count, is_public) VALUES
(2, 'Just finished installing my new turbo setup. Can''t wait to test it at the track this weekend! #turbo #racing', 'text', 15, 8, TRUE),
(3, 'New personal best at the track today! 10.2 seconds in the quarter mile. The Camaro is running strong! 🏁', 'text', 23, 12, TRUE),
(4, 'Check out my latest engine build. 600+ horsepower and still street legal! #enginebuild #horsepower', 'text', 31, 18, TRUE),
(5, 'Amazing shots from today''s race meet. The GT-R community never disappoints! 📸', 'text', 19, 9, TRUE),
(6, 'Safety first, speed second. Always wear your helmet and safety gear! #safety #racing', 'text', 27, 14, TRUE),
(7, 'Custom turbo setup complete. Dyno results coming soon! #turbo #dyno', 'text', 22, 11, TRUE),
(8, 'First time at the track today. Learned so much from the experienced racers! #beginner #learning', 'text', 13, 7, TRUE),
(9, 'Organizing the biggest car meet of the year. Save the date! #carmeet #community', 'text', 35, 20, TRUE),
(10, 'ECU tuning session today. Gained 50+ horsepower on the dyno! #tuning #horsepower', 'text', 28, 16, TRUE),
(11, 'New to racing but loving every minute of it! Thanks to everyone for the support! #newracer #community', 'text', 17, 10, TRUE)
ON CONFLICT DO NOTHING;

-- Post comments
INSERT INTO core_postcomment (post_id, author_id, content) VALUES
(1, 3, 'Looking good! What turbo did you go with?'),
(1, 4, 'Can''t wait to see the dyno numbers!'),
(2, 2, 'Impressive time! What mods do you have?'),
(2, 6, 'Great run! The Camaro is a beast!'),
(3, 5, '600+ HP is insane! Street legal too?'),
(3, 7, 'Love the build! What''s next?'),
(4, 2, 'Amazing photos! GT-Rs are beautiful!'),
(4, 8, 'Great shots! What camera do you use?'),
(5, 3, 'Safety is always priority! Good reminder!'),
(5, 9, 'Couldn''t agree more! Safety first!'),
(6, 4, 'Custom turbo setups are the best!'),
(6, 10, 'Can''t wait to see the dyno results!'),
(7, 5, 'Welcome to the racing community!'),
(7, 11, 'Everyone starts somewhere! Keep it up!'),
(8, 6, 'Count me in! When and where?'),
(8, 7, 'Sounds like a great event!'),
(9, 8, '50+ HP gain is huge! What tune?'),
(9, 9, 'Dyno numbers don''t lie!'),
(10, 10, 'Welcome to the family!'),
(10, 2, 'We''re all here to help!')
ON CONFLICT DO NOTHING;

-- =====================
-- POPULATE MARKETPLACE
-- =====================

-- Listing categories
INSERT INTO core_listingcategory (name, description) VALUES
('Performance Parts', 'Engine, transmission, and drivetrain components'),
('Exterior Parts', 'Body kits, spoilers, and exterior modifications'),
('Interior Parts', 'Seats, steering wheels, and interior accessories'),
('Wheels & Tires', 'Wheels, tires, and suspension components'),
('Electronics', 'ECUs, gauges, and electronic components'),
('Tools & Equipment', 'Tools, diagnostic equipment, and shop supplies'),
('Complete Cars', 'Full vehicles for sale'),
('Services', 'Tuning, installation, and repair services')
ON CONFLICT (name) DO NOTHING;

-- Marketplace listings
INSERT INTO core_marketplace (seller_id, title, description, category, condition, price, is_negotiable, trade_offered, location, contact_phone, contact_email, is_active) VALUES
(2, 'Garrett GTX3582R Turbo', 'Brand new Garrett GTX3582R turbocharger. Perfect for high horsepower builds. Never installed.', 'Performance Parts', 'new', 2500.00, TRUE, TRUE, 'Los Angeles, CA', '555-0101', 'john@example.com', TRUE),
(3, 'HRE Wheels Set', 'Set of 4 HRE P101 wheels. 19x10 front, 19x11 rear. Perfect condition.', 'Wheels & Tires', 'excellent', 3500.00, TRUE, FALSE, 'Houston, TX', '555-0102', 'sarah@example.com', TRUE),
(4, 'Cobb Accessport V3', 'Cobb Accessport V3 for Subaru WRX/STI. Unmarried and ready to use.', 'Electronics', 'excellent', 500.00, FALSE, TRUE, 'Phoenix, AZ', '555-0103', 'mike@example.com', TRUE),
(5, 'Recaro Sportster CS', 'Pair of Recaro Sportster CS seats. Black with red stitching. Excellent condition.', 'Interior Parts', 'excellent', 1200.00, TRUE, TRUE, 'Miami, FL', '555-0104', 'lisa@example.com', TRUE),
(6, 'Tein Flex Z Coilovers', 'Tein Flex Z coilovers for Toyota Supra. Used for 5000 miles. Great condition.', 'Wheels & Tires', 'good', 800.00, TRUE, FALSE, 'Dallas, TX', '555-0105', 'david@example.com', TRUE),
(7, 'AEM Infinity ECU', 'AEM Infinity 8 ECU with harness. Perfect for standalone engine management.', 'Electronics', 'excellent', 1800.00, TRUE, TRUE, 'Las Vegas, NV', '555-0106', 'emma@example.com', TRUE),
(8, 'Honda Civic Type R', '2018 Honda Civic Type R. 15,000 miles. Stock with minor modifications.', 'Complete Cars', 'excellent', 35000.00, TRUE, FALSE, 'San Diego, CA', '555-0107', 'alex@example.com', TRUE),
(9, 'ECU Tuning Service', 'Professional ECU tuning service. Dyno tuning and street tuning available.', 'Services', 'new', 400.00, FALSE, FALSE, 'Austin, TX', '555-0108', 'jessica@example.com', TRUE),
(10, 'Mishimoto Intercooler', 'Mishimoto intercooler for Mitsubishi Lancer Evo. Brand new in box.', 'Performance Parts', 'new', 600.00, TRUE, TRUE, 'Orlando, FL', '555-0109', 'ryan@example.com', TRUE),
(11, 'Snap-on Tool Set', 'Complete Snap-on tool set. Professional grade tools. Excellent condition.', 'Tools & Equipment', 'excellent', 2500.00, TRUE, FALSE, 'Tampa, FL', '555-0110', 'ryan@example.com', TRUE)
ON CONFLICT DO NOTHING;

-- =====================
-- POPULATE CAR PROFILES
-- =====================

INSERT INTO core_carprofile (owner_id, make, model, year, engine, transmission, color, mileage, description, is_public) VALUES
(2, 'Ford', 'Mustang GT', 2018, '5.0L V8', 'Manual', 'Race Red', 25000, 'Heavily modified Mustang with turbo setup. 600+ horsepower.', TRUE),
(3, 'Chevrolet', 'Camaro SS', 2020, '6.2L V8', 'Manual', 'Black', 15000, 'Pro-built Camaro with extensive modifications. Track ready.', TRUE),
(4, 'Dodge', 'Challenger Hellcat', 2019, '6.2L Supercharged V8', 'Automatic', 'White', 12000, 'Hellcat with custom tune and exhaust. 800+ horsepower.', TRUE),
(5, 'Nissan', 'GT-R', 2021, '3.8L Twin-Turbo V6', 'Automatic', 'Pearl White', 8000, 'Godzilla in its natural habitat. Track monster.', TRUE),
(6, 'Toyota', 'Supra', 2020, '3.0L Turbo I6', 'Manual', 'Phantom Matte Gray', 18000, 'MK5 Supra with custom turbo setup. Drift and drag ready.', TRUE),
(7, 'BMW', 'M3', 2019, '3.0L Twin-Turbo I6', 'Manual', 'Alpine White', 22000, 'F80 M3 with extensive modifications. Pure performance.', TRUE),
(8, 'Honda', 'Civic Type R', 2017, '2.0L Turbo I4', 'Manual', 'Championship White', 35000, 'FK8 Type R with bolt-ons. Daily driver and weekend warrior.', TRUE),
(9, 'Subaru', 'WRX STI', 2020, '2.5L Turbo H4', 'Manual', 'World Rally Blue', 16000, 'STI with custom tune and suspension. Rally inspired.', TRUE),
(10, 'Mitsubishi', 'Lancer Evolution X', 2018, '2.0L Turbo I4', 'Manual', 'Rally Red', 28000, 'Evo X with custom turbo and AWD setup. Rally heritage.', TRUE),
(11, 'Volkswagen', 'Golf GTI', 2019, '2.0L Turbo I4', 'Manual', 'Pure White', 24000, 'MK7.5 GTI with stage 2 tune. Hot hatch perfection.', TRUE)
ON CONFLICT DO NOTHING;

-- =====================
-- POPULATE RACE RESULTS
-- =====================

INSERT INTO core_raceresult (event_id, winner_id, loser_id, winner_time, loser_time, race_date, notes) VALUES
(1, 2, 3, 10.5, 10.8, NOW() - INTERVAL '5 days', 'Great race! Both cars performed well.'),
(1, 4, 5, 9.8, 10.2, NOW() - INTERVAL '5 days', 'Hellcat dominated the GT-R in this matchup.'),
(2, 6, 7, 11.2, 11.5, NOW() - INTERVAL '3 days', 'Supra vs M3, close race!'),
(2, 8, 9, 12.1, 12.3, NOW() - INTERVAL '3 days', 'Type R vs STI, import battle!'),
(3, 10, 11, 11.8, 12.2, NOW() - INTERVAL '7 days', 'Evo vs GTI, AWD advantage!'),
(4, 2, 4, 10.3, 10.6, NOW() - INTERVAL '2 days', 'Mustang vs Hellcat, V8 battle!'),
(5, 3, 5, 10.7, 11.0, NOW() - INTERVAL '4 days', 'Camaro vs GT-R, American vs Japanese!'),
(6, 6, 8, 11.5, 12.0, NOW() - INTERVAL '1 day', 'Supra vs Type R, different approaches!'),
(7, 7, 9, 11.3, 11.8, NOW() - INTERVAL '6 days', 'M3 vs STI, luxury vs rally!'),
(8, 10, 2, 11.9, 10.4, NOW() - INTERVAL '8 days', 'Evo vs Mustang, underdog story!')
ON CONFLICT DO NOTHING;

-- =====================
-- POPULATE NOTIFICATIONS
-- =====================

INSERT INTO core_notification (recipient_id, sender_id, notification_type, title, message, is_read) VALUES
(2, 3, 'callout', 'New Callout Challenge', 'Sarah has challenged you to a race!', FALSE),
(3, 4, 'follow', 'New Follower', 'Mike is now following you!', FALSE),
(4, 5, 'comment', 'New Comment', 'Lisa commented on your post!', FALSE),
(5, 6, 'like', 'New Like', 'David liked your post!', FALSE),
(6, 7, 'message', 'New Message', 'Emma sent you a message!', FALSE),
(7, 8, 'event', 'Event Reminder', 'Your race is tomorrow!', FALSE),
(8, 9, 'friend_request', 'Friend Request', 'Jessica wants to be your friend!', FALSE),
(9, 10, 'marketplace', 'New Listing', 'Ryan posted a new marketplace listing!', FALSE),
(10, 11, 'race_result', 'Race Result', 'Your race result has been posted!', FALSE),
(11, 2, 'welcome', 'Welcome to CalloutRacing', 'Welcome to the community!', FALSE)
ON CONFLICT DO NOTHING;

-- =====================
-- POPULATE MESSAGES
-- =====================

INSERT INTO core_message (sender_id, recipient_id, content, is_read) VALUES
(2, 3, 'Hey Sarah! Great race today. Your Camaro is really fast!', FALSE),
(3, 2, 'Thanks John! Your Mustang is no slouch either. Let''s race again soon!', FALSE),
(4, 5, 'Lisa, I saw your GT-R at the meet. Beautiful car!', FALSE),
(5, 4, 'Thanks Mike! Your Hellcat is a beast. Love the sound!', FALSE),
(6, 7, 'Emma, are you going to the track this weekend?', FALSE),
(7, 6, 'Yes David! Should be a great day for racing. See you there!', FALSE),
(8, 9, 'Jessica, thanks for organizing the car meet. It was awesome!', FALSE),
(9, 8, 'You''re welcome Alex! The community really came together.', FALSE),
(10, 11, 'Ryan, I''m interested in your ECU tuning service.', FALSE),
(11, 10, 'Great! I can help you with that. What car do you have?', FALSE)
ON CONFLICT DO NOTHING;

-- =====================
-- POPULATE WALLETS
-- =====================

INSERT INTO core_userwallet (user_id, balance) VALUES
(2, 2500.00),
(3, 1800.00),
(4, 3200.00),
(5, 1500.00),
(6, 2100.00),
(7, 2800.00),
(8, 900.00),
(9, 1900.00),
(10, 3500.00),
(11, 1200.00)
ON CONFLICT (user_id) DO NOTHING;

-- =====================
-- POPULATE PAYMENT TRANSACTIONS
-- =====================

INSERT INTO core_paymenttransaction (user_id, transaction_type, amount, status, reference_id) VALUES
(2, 'deposit', 500.00, 'completed', 'TXN001'),
(3, 'withdrawal', 200.00, 'completed', 'TXN002'),
(4, 'deposit', 1000.00, 'completed', 'TXN003'),
(5, 'payment', 150.00, 'completed', 'TXN004'),
(6, 'deposit', 750.00, 'completed', 'TXN005'),
(7, 'withdrawal', 300.00, 'completed', 'TXN006'),
(8, 'deposit', 250.00, 'completed', 'TXN007'),
(9, 'payment', 80.00, 'completed', 'TXN008'),
(10, 'deposit', 1200.00, 'completed', 'TXN009'),
(11, 'withdrawal', 100.00, 'completed', 'TXN010')
ON CONFLICT DO NOTHING;

-- =====================
-- COMPLETION MESSAGE
-- =====================

DO $$
DECLARE
    user_count INTEGER;
    event_count INTEGER;
    listing_count INTEGER;
    post_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO user_count FROM core_user;
    SELECT COUNT(*) INTO event_count FROM core_event;
    SELECT COUNT(*) INTO listing_count FROM core_marketplace;
    SELECT COUNT(*) INTO post_count FROM core_userpost;
    
    RAISE NOTICE '=====================================================';
    RAISE NOTICE 'SAMPLE DATA POPULATION COMPLETE!';
    RAISE NOTICE '=====================================================';
    RAISE NOTICE 'Users created: %', user_count;
    RAISE NOTICE 'Events created: %', event_count;
    RAISE NOTICE 'Marketplace listings: %', listing_count;
    RAISE NOTICE 'Social posts: %', post_count;
    RAISE NOTICE 'All features now have realistic sample data!';
    RAISE NOTICE 'Ready for testing and demonstration!';
    RAISE NOTICE '=====================================================';
END $$;

COMMIT; 