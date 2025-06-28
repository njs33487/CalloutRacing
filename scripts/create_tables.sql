-- SQL script to create essential tables for CalloutRacing
-- This can be run directly in the Railway PostgreSQL console

-- Create core_user table
CREATE TABLE IF NOT EXISTS core_user (
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

-- Create django_migrations table if it doesn't exist
CREATE TABLE IF NOT EXISTS django_migrations (
    id SERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Insert the initial migration record
INSERT INTO django_migrations (app, name, applied) 
VALUES ('core', '0001_initial', NOW())
ON CONFLICT (app, name) DO NOTHING;

-- Create auth_group table if it doesn't exist
CREATE TABLE IF NOT EXISTS auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

-- Create auth_permission table if it doesn't exist
CREATE TABLE IF NOT EXISTS auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL
);

-- Create core_userprofile table
CREATE TABLE IF NOT EXISTS core_userprofile (
    id BIGSERIAL PRIMARY KEY,
    bio TEXT NOT NULL DEFAULT '',
    location VARCHAR(200) NOT NULL DEFAULT '',
    car_make VARCHAR(50) NOT NULL DEFAULT '',
    car_model VARCHAR(50) NOT NULL DEFAULT '',
    car_year INTEGER,
    profile_picture VARCHAR(100),
    cover_photo VARCHAR(100),
    wins INTEGER NOT NULL DEFAULT 0,
    losses INTEGER NOT NULL DEFAULT 0,
    total_races INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    user_id BIGINT NOT NULL UNIQUE REFERENCES core_user(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS core_user_username_idx ON core_user(username);
CREATE INDEX IF NOT EXISTS core_user_email_idx ON core_user(email);
CREATE INDEX IF NOT EXISTS core_userprofile_user_id_idx ON core_userprofile(user_id);

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO current_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO current_user; 