# Database Setup for Railway Deployment

## Step 1: Add PostgreSQL Database to Railway

1. **Go to Railway Dashboard**
   - Navigate to your CalloutRacing project
   - Click "New" button
   - Select "Database" → "PostgreSQL"

2. **Configure Database**
   - Railway will automatically create a PostgreSQL database
   - Note the database name and credentials

## Step 2: Link Database to Backend Service

1. **Connect Database to Backend**
   - In your backend service, go to "Variables" tab
   - Railway should automatically add `DATABASE_URL` environment variable
   - If not, manually add: `DATABASE_URL=postgresql://username:password@host:port/database`

2. **Alternative Database URL Format**
   - If Railway uses a different format, you can also set:
   - `Postgres.DATABASE_URL=postgresql://username:password@host:port/database`

## Step 3: Verify Database Connection

After adding the database:

1. **Redeploy your application**
2. **Check the health endpoint**: `https://calloutracing.up.railway.app/health/`
3. **Look for database status**: Should show "connected" instead of "disconnected"

## Step 4: Run Migrations

The application will automatically run migrations on startup, but you can also:

1. **Check Railway logs** for migration output
2. **Look for**: "Running database migrations..." and "Operations to perform:"
3. **Verify**: No more "21 unapplied migration(s)" warnings

## Troubleshooting

### If Database Shows "disconnected":
1. Check that `DATABASE_URL` is set in environment variables
2. Verify the database is running in Railway
3. Check that the backend service is linked to the database

### If Migrations Don't Run:
1. Check Railway logs for any database connection errors
2. Verify the database URL format is correct
3. Make sure the database user has proper permissions

### Common Database URL Format:
```
postgresql://username:password@host:port/database_name
```

## Testing Database Connection

Once set up, test these endpoints:

1. **Health Check**: `https://calloutracing.up.railway.app/health/`
   - Should show `"database": "connected"`

2. **Admin Interface**: `https://calloutracing.up.railway.app/admin/`
   - Should load without database errors

3. **API Endpoints**: `https://calloutracing.up.railway.app/api/`
   - Should work with database operations 