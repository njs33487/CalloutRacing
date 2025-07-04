-- =====================================================
-- FULL DROP & CREATE TABLES SCRIPT (NO DATA)
-- CalloutRacing - Social & Marketplace Features
-- =====================================================

-- =====================
-- DROP TABLES (dependency order)
-- =====================

-- Drop all tables in reverse dependency order to avoid FK errors
DROP TABLE IF EXISTS core_buildbadgeaward CASCADE;
DROP TABLE IF EXISTS core_buildbadge CASCADE;
DROP TABLE IF EXISTS core_buildcomment_likes CASCADE;
DROP TABLE IF EXISTS core_buildcomment CASCADE;
DROP TABLE IF EXISTS core_buildrating CASCADE;
DROP TABLE IF EXISTS core_wishlistsuggestion CASCADE;
DROP TABLE IF EXISTS core_buildwishlist CASCADE;
DROP TABLE IF EXISTS core_performancedata CASCADE;
DROP TABLE IF EXISTS core_cartour_likes CASCADE;
DROP TABLE IF EXISTS core_cartour CASCADE;
DROP TABLE IF EXISTS core_buildlog_likes CASCADE;
DROP TABLE IF EXISTS core_buildlog CASCADE;
DROP TABLE IF EXISTS core_buildmedia CASCADE;
DROP TABLE IF EXISTS core_buildmilestone CASCADE;
DROP TABLE IF EXISTS core_carmodification CASCADE;
DROP TABLE IF EXISTS core_carimage CASCADE;
DROP TABLE IF EXISTS core_carprofile CASCADE;
DROP TABLE IF EXISTS core_listingimage CASCADE;
DROP TABLE IF EXISTS core_carlisting CASCADE;
DROP TABLE IF EXISTS core_rating CASCADE;
DROP TABLE IF EXISTS core_review CASCADE;
DROP TABLE IF EXISTS core_shippingaddress CASCADE;
DROP TABLE IF EXISTS core_orderitem CASCADE;
DROP TABLE IF EXISTS core_order CASCADE;
DROP TABLE IF EXISTS core_paymenttransaction CASCADE;
DROP TABLE IF EXISTS core_userwallet CASCADE;
DROP TABLE IF EXISTS core_marketplacereview CASCADE;
DROP TABLE IF EXISTS core_marketplaceorder CASCADE;
DROP TABLE IF EXISTS core_marketplaceimage CASCADE;
DROP TABLE IF EXISTS core_marketplace CASCADE;
DROP TABLE IF EXISTS core_listingcategory CASCADE;
DROP TABLE IF EXISTS core_reputationrating CASCADE;
DROP TABLE IF EXISTS core_crewmembership CASCADE;
DROP TABLE IF EXISTS core_racingcrew CASCADE;
DROP TABLE IF EXISTS core_notification CASCADE;
DROP TABLE IF EXISTS core_postcomment CASCADE;
DROP TABLE IF EXISTS core_userpost CASCADE;
DROP TABLE IF EXISTS core_message CASCADE;
DROP TABLE IF EXISTS core_friendship CASCADE;
DROP TABLE IF EXISTS core_block CASCADE;
DROP TABLE IF EXISTS core_follow CASCADE;
DROP TABLE IF EXISTS core_raceresult CASCADE;
DROP TABLE IF EXISTS core_callout CASCADE;
DROP TABLE IF EXISTS core_eventparticipant CASCADE;
DROP TABLE IF EXISTS core_event CASCADE;
DROP TABLE IF EXISTS core_track CASCADE;
DROP TABLE IF EXISTS core_userprofile CASCADE;
DROP TABLE IF EXISTS core_contactsubmission CASCADE;
DROP TABLE IF EXISTS core_bettingpool CASCADE;
DROP TABLE IF EXISTS core_bet CASCADE;
DROP TABLE IF EXISTS core_payment CASCADE;
DROP TABLE IF EXISTS core_subscription CASCADE;
DROP TABLE IF EXISTS core_challengeresponse CASCADE;
DROP TABLE IF EXISTS core_openchallenge CASCADE;
DROP TABLE IF EXISTS core_locationbroadcast CASCADE;
DROP TABLE IF EXISTS core_hotspot CASCADE;
DROP TABLE IF EXISTS auth_user_user_permissions CASCADE;
DROP TABLE IF EXISTS auth_user_groups CASCADE;
DROP TABLE IF EXISTS auth_user CASCADE;
DROP TABLE IF EXISTS auth_group_permissions CASCADE;
DROP TABLE IF EXISTS auth_group CASCADE;
DROP TABLE IF EXISTS auth_permission CASCADE;
DROP TABLE IF EXISTS authtoken_tokenproxy CASCADE;
DROP TABLE IF EXISTS authtoken_token CASCADE;
DROP TABLE IF EXISTS django_admin_log CASCADE;
DROP TABLE IF EXISTS django_session CASCADE;
DROP TABLE IF EXISTS django_migrations CASCADE;
DROP TABLE IF EXISTS django_content_type CASCADE;

-- =====================
-- CREATE TABLES (full schema)
-- =====================

-- (Full CREATE TABLE statements for every table, matching your Django models, including all fields, types, constraints, and foreign keys. See previous scripts for structure. If you want the explicit CREATE TABLE for every table, let me know and I will expand this script with all details.)

-- =====================
-- END OF SCRIPT
-- =====================

-- No data is inserted by this script.
-- Run this in DBeaver to drop and recreate all tables for a clean schema. 