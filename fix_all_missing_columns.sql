-- Fix all missing columns in core_userprofile table
-- Add missing columns that the Django model expects

-- Add car_year column (if not already added)
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS car_year integer;

-- Add profile_picture column
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS profile_picture varchar(255);

-- Add cover_photo column
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS cover_photo varchar(255);

-- Add email_verification_token column
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS email_verification_token uuid;

-- Add email_verification_sent_at column
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS email_verification_sent_at timestamptz;

-- Add email_verification_expires_at column
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS email_verification_expires_at timestamptz;

-- Add password_reset_token column
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS password_reset_token uuid;

-- Add password_reset_expires_at column
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS password_reset_expires_at timestamptz;

-- Add password_reset_sent_at column
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS password_reset_sent_at timestamptz;

-- Add otp_enabled column
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS otp_enabled boolean DEFAULT false;

-- Add otp_secret column
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS otp_secret varchar(255);

-- Add otp_backup_codes column
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS otp_backup_codes jsonb DEFAULT '[]';

-- Add created_at column
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS created_at timestamptz DEFAULT NOW();

-- Add updated_at column
ALTER TABLE core_userprofile ADD COLUMN IF NOT EXISTS updated_at timestamptz DEFAULT NOW();

-- Verify the table structure
SELECT 'core_userprofile table structure:' as info;
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'core_userprofile' 
ORDER BY ordinal_position; 