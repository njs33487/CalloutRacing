-- Drop all tables and recreate database
-- WARNING: This will delete all data!

-- Drop all tables in the correct order (respecting foreign keys)
DROP TABLE IF EXISTS core_userpost_likes CASCADE;
DROP TABLE IF EXISTS core_userpost CASCADE;
DROP TABLE IF EXISTS core_userprofile CASCADE;
DROP TABLE IF EXISTS core_userwallet CASCADE;
DROP TABLE IF EXISTS core_user CASCADE;
DROP TABLE IF EXISTS core_track CASCADE;
DROP TABLE IF EXISTS core_subscription CASCADE;
DROP TABLE IF EXISTS core_reputationrating CASCADE;
DROP TABLE IF EXISTS core_racingcrew_members CASCADE;
DROP TABLE IF EXISTS core_racingcrew_admins CASCADE;
DROP TABLE IF EXISTS core_racingcrew CASCADE;
DROP TABLE IF EXISTS core_raceresult CASCADE;
DROP TABLE IF EXISTS core_postcomment CASCADE;
DROP TABLE IF EXISTS core_payment CASCADE;
DROP TABLE IF EXISTS core_openchallenge CASCADE;
DROP TABLE IF EXISTS core_notification CASCADE;
DROP TABLE IF EXISTS core_message CASCADE;
DROP TABLE IF EXISTS core_marketplacereview CASCADE;
DROP TABLE IF EXISTS core_marketplaceorder CASCADE;
DROP TABLE IF EXISTS core_marketplaceimage CASCADE;
DROP TABLE IF EXISTS core_marketplace CASCADE;
DROP TABLE IF EXISTS core_locationbroadcast CASCADE;
DROP TABLE IF EXISTS core_hotspot CASCADE;
DROP TABLE IF EXISTS core_friendship CASCADE;
DROP TABLE IF EXISTS core_eventparticipant CASCADE;
DROP TABLE IF EXISTS core_event CASCADE;
DROP TABLE IF EXISTS core_contactsubmission CASCADE;
DROP TABLE IF EXISTS core_challengeresponse CASCADE;
DROP TABLE IF EXISTS core_carmodification CASCADE;
DROP TABLE IF EXISTS core_carimage CASCADE;
DROP TABLE IF EXISTS core_carprofile CASCADE;
DROP TABLE IF EXISTS core_callout CASCADE;
DROP TABLE IF EXISTS core_bettingpool CASCADE;
DROP TABLE IF EXISTS core_bet CASCADE;

-- Drop Django system tables
DROP TABLE IF EXISTS django_session CASCADE;
DROP TABLE IF EXISTS django_migrations CASCADE;
DROP TABLE IF EXISTS django_content_type CASCADE;
DROP TABLE IF EXISTS django_admin_log CASCADE;
DROP TABLE IF EXISTS authtoken_token CASCADE;
DROP TABLE IF EXISTS auth_user_user_permissions CASCADE;
DROP TABLE IF EXISTS auth_user_groups CASCADE;
DROP TABLE IF EXISTS auth_user CASCADE;
DROP TABLE IF EXISTS auth_permission CASCADE;
DROP TABLE IF EXISTS auth_group_permissions CASCADE;
DROP TABLE IF EXISTS auth_group CASCADE;

-- Recreate django_migrations table
CREATE TABLE django_migrations (
    id SERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE(app, name)
);

-- Recreate django_content_type table
CREATE TABLE django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE(app_label, model)
);

-- Recreate auth_group table
CREATE TABLE auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

-- Recreate auth_permission table
CREATE TABLE auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL REFERENCES django_content_type(id),
    codename VARCHAR(100) NOT NULL,
    UNIQUE(content_type_id, codename)
);

-- Recreate auth_group_permissions table
CREATE TABLE auth_group_permissions (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES auth_group(id),
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
    UNIQUE(group_id, permission_id)
);

-- Recreate core_user table with complete schema
CREATE TABLE core_user (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    email_verification_token UUID DEFAULT gen_random_uuid(),
    email_verification_sent_at TIMESTAMP WITH TIME ZONE,
    email_verification_expires_at TIMESTAMP WITH TIME ZONE,
    email VARCHAR(254) NOT NULL UNIQUE,
    username VARCHAR(150) NOT NULL UNIQUE
);

-- Create indexes for core_user
CREATE INDEX core_user_username_idx ON core_user(username);
CREATE INDEX core_user_email_idx ON core_user(email);

-- Recreate auth_user table (Django's default user table)
CREATE TABLE auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    username VARCHAR(150) NOT NULL UNIQUE
);

-- Recreate auth_user_groups table
CREATE TABLE auth_user_groups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    group_id INTEGER NOT NULL REFERENCES auth_group(id),
    UNIQUE(user_id, group_id)
);

-- Recreate auth_user_user_permissions table
CREATE TABLE auth_user_user_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
    UNIQUE(user_id, permission_id)
);

-- Recreate authtoken_token table
CREATE TABLE authtoken_token (
    key VARCHAR(40) PRIMARY KEY,
    created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id)
);

-- Recreate django_session table
CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Recreate django_admin_log table
CREATE TABLE django_admin_log (
    id SERIAL PRIMARY KEY,
    action_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    object_id TEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT NOT NULL,
    change_message TEXT NOT NULL,
    content_type_id INTEGER REFERENCES django_content_type(id),
    user_id INTEGER NOT NULL REFERENCES auth_user(id)
);

-- Insert initial migration record
INSERT INTO django_migrations (app, name, applied) 
VALUES ('core', '0001_initial', NOW())
ON CONFLICT (app, name) DO NOTHING;

-- Verify the core_user table was created correctly
SELECT 'Database recreated successfully' as status;
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'core_user' ORDER BY ordinal_position; 