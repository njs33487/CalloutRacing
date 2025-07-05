-- Clean up authtoken tokens that are causing foreign key constraint issues
-- This removes any tokens that reference non-existent users

-- Check if authtoken_token table exists
SELECT 'Checking authtoken_token table:' as info;
SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'authtoken_token'
) as authtoken_token_exists;

-- If table exists, clean up orphaned tokens
DO $$
BEGIN
    IF EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'authtoken_token'
    ) THEN
        -- Delete tokens that reference non-existent users
        DELETE FROM authtoken_token 
        WHERE user_id NOT IN (SELECT id FROM core_user);
        
        RAISE NOTICE 'Cleaned up orphaned tokens';
    ELSE
        RAISE NOTICE 'authtoken_token table does not exist';
    END IF;
END $$;

-- Show remaining tokens (if any)
SELECT 'Remaining tokens:' as info;
SELECT COUNT(*) as token_count FROM authtoken_token;

-- Optional: Drop the authtoken_token table entirely since we're not using it
-- Uncomment the following lines if you want to completely remove the table:
/*
DROP TABLE IF EXISTS authtoken_token;
SELECT 'authtoken_token table dropped' as info;
*/ 