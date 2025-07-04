-- Fix core_callout table - add missing columns
-- Add winner_id column
ALTER TABLE core_callout ADD COLUMN IF NOT EXISTS winner_id integer;

-- Add created_at column
ALTER TABLE core_callout ADD COLUMN IF NOT EXISTS created_at timestamptz DEFAULT NOW();

-- Add updated_at column
ALTER TABLE core_callout ADD COLUMN IF NOT EXISTS updated_at timestamptz DEFAULT NOW();

-- Add tire_requirement column
ALTER TABLE core_callout ADD COLUMN IF NOT EXISTS tire_requirement varchar(255);

-- Add rules column
ALTER TABLE core_callout ADD COLUMN IF NOT EXISTS rules text;

-- Add is_private column
ALTER TABLE core_callout ADD COLUMN IF NOT EXISTS is_private boolean DEFAULT false;

-- Add is_invite_only column
ALTER TABLE core_callout ADD COLUMN IF NOT EXISTS is_invite_only boolean DEFAULT false;

-- Verify the table structure
SELECT 'core_callout table structure:' as info;
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'core_callout' 
ORDER BY ordinal_position; 