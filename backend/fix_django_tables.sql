-- =====================================================
-- FIX DJANGO SYSTEM TABLES
-- This script fixes the Django system tables to match Django's expectations
-- =====================================================

-- Add missing 'name' column to django_content_type
ALTER TABLE django_content_type ADD COLUMN IF NOT EXISTS name VARCHAR(100);

-- Update existing records to have a default name
UPDATE django_content_type SET name = CONCAT(app_label, '.', model) WHERE name IS NULL;

-- Make name column NOT NULL after updating
ALTER TABLE django_content_type ALTER COLUMN name SET NOT NULL;

-- Add unique constraint on (app_label, model) if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'django_content_type_app_label_model_76bd3d3b_uniq'
    ) THEN
        ALTER TABLE django_content_type ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
    END IF;
END $$;

COMMIT; 