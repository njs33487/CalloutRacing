-- =====================================================
-- FIX PRODUCTION DATABASE - CORE_USER TABLE
-- This script creates the missing core_user table and essential related tables
-- Run this in DBeaver connected to your Railway PostgreSQL database
-- =====================================================

-- Create the core_user table that Django expects
CREATE TABLE IF NOT EXISTS core_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL UNIQUE,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    reset_token VARCHAR(255),
    reset_token_expires TIMESTAMP WITH TIME ZONE
);

-- Create essential Django system tables if they don't exist
CREATE TABLE IF NOT EXISTS django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE(app_label, model)
);

CREATE TABLE IF NOT EXISTS django_migrations (
    id SERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS django_admin_log (
    id SERIAL PRIMARY KEY,
    action_time TIMESTAMP WITH TIME ZONE NOT NULL,
    object_id TEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT NOT NULL,
    change_message TEXT NOT NULL,
    content_type_id INTEGER REFERENCES django_content_type(id),
    user_id INTEGER
);

-- Create auth tables
CREATE TABLE IF NOT EXISTS auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL REFERENCES django_content_type(id),
    codename VARCHAR(100) NOT NULL,
    UNIQUE(content_type_id, codename)
);

CREATE TABLE IF NOT EXISTS auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS auth_group_permissions (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES auth_group(id),
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
    UNIQUE(group_id, permission_id)
);

-- Create auth_user for compatibility
CREATE TABLE IF NOT EXISTS auth_user (
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

CREATE TABLE IF NOT EXISTS auth_user_groups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    group_id INTEGER NOT NULL REFERENCES auth_group(id),
    UNIQUE(user_id, group_id)
);

CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
    UNIQUE(user_id, permission_id)
);

-- Create authtoken tables
CREATE TABLE IF NOT EXISTS authtoken_token (
    key VARCHAR(40) PRIMARY KEY,
    created TIMESTAMP WITH TIME ZONE NOT NULL,
    user_id INTEGER NOT NULL UNIQUE REFERENCES core_user(id)
);

CREATE TABLE IF NOT EXISTS authtoken_tokenproxy (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES core_user(id)
);

-- Create core_userprofile table
CREATE TABLE IF NOT EXISTS core_userprofile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES core_user(id),
    bio TEXT,
    location VARCHAR(200),
    phone VARCHAR(20),
    car_make VARCHAR(100),
    car_model VARCHAR(100),
    year INTEGER,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    total_races INTEGER DEFAULT 0,
    profile_picture VARCHAR(255),
    email_verified BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    date_of_birth DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_core_user_username ON core_user(username);
CREATE INDEX IF NOT EXISTS idx_core_user_email ON core_user(email);
CREATE INDEX IF NOT EXISTS idx_core_user_email_verified ON core_user(email_verified);
CREATE INDEX IF NOT EXISTS idx_auth_user_username ON auth_user(username);
CREATE INDEX IF NOT EXISTS idx_auth_user_email ON auth_user(email);

COMMIT; 