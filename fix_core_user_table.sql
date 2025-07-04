-- =====================================================
-- FIX MISSING CORE_USER TABLE
-- This script creates the missing core_user table
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

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_core_user_username ON core_user(username);
CREATE INDEX IF NOT EXISTS idx_core_user_email ON core_user(email);
CREATE INDEX IF NOT EXISTS idx_core_user_email_verified ON core_user(email_verified);

-- Insert a default superuser if needed (optional)
-- INSERT INTO core_user (username, email, password, is_superuser, is_staff, is_active, date_joined)
-- VALUES ('admin', 'admin@calloutracing.com', 'pbkdf2_sha256$600000$...', TRUE, TRUE, TRUE, NOW())
-- ON CONFLICT (username) DO NOTHING;

COMMIT; 