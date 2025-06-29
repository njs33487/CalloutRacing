-- Create the missing core_user table
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

-- Create indexes
CREATE INDEX IF NOT EXISTS core_user_username_idx ON core_user(username);
CREATE INDEX IF NOT EXISTS core_user_email_idx ON core_user(email);

-- Insert migration record
INSERT INTO django_migrations (app, name, applied) 
VALUES ('core', '0001_initial', NOW())
ON CONFLICT (app, name) DO NOTHING;

-- Verify the table was created
SELECT 'core_user table created successfully' as status;
SELECT COUNT(*) as user_count FROM core_user; 