-- Fix django_content_type table - update null name values
UPDATE django_content_type 
SET name = CONCAT(app_label, '.', model) 
WHERE name IS NULL;

-- Verify the fix
SELECT 'django_content_type after fix:' as info;
SELECT id, app_label, model, name FROM django_content_type WHERE name IS NULL; 