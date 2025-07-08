#!/usr/bin/env python
"""
Script to check for database issues that might be causing 500 errors
"""
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from core.models.racing import Event, Track, Callout, RaceResult
from core.models.social import SponsoredContent, UserPost
from core.models.auth import User
from django.db import connection

def check_database_issues():
    """Check for common database issues"""
    print("Checking database for potential issues...")
    print("=" * 50)
    
    # Check if tables exist and have data
    try:
        track_count = Track.objects.count()
        print(f"✅ Tracks: {track_count} records")
    except Exception as e:
        print(f"❌ Tracks table error: {e}")
    
    try:
        event_count = Event.objects.count()
        print(f"✅ Events: {event_count} records")
    except Exception as e:
        print(f"❌ Events table error: {e}")
    
    try:
        callout_count = Callout.objects.count()
        print(f"✅ Callouts: {callout_count} records")
    except Exception as e:
        print(f"❌ Callouts table error: {e}")
    
    try:
        race_result_count = RaceResult.objects.count()
        print(f"✅ Race Results: {race_result_count} records")
    except Exception as e:
        print(f"❌ Race Results table error: {e}")
    
    try:
        sponsored_content_count = SponsoredContent.objects.count()
        print(f"✅ Sponsored Content: {sponsored_content_count} records")
    except Exception as e:
        print(f"❌ Sponsored Content table error: {e}")
    
    try:
        user_post_count = UserPost.objects.count()
        print(f"✅ User Posts: {user_post_count} records")
    except Exception as e:
        print(f"❌ User Posts table error: {e}")
    
    try:
        user_count = User.objects.count()
        print(f"✅ Users: {user_count} records")
    except Exception as e:
        print(f"❌ Users table error: {e}")
    
    # Check for foreign key issues
    print("\nChecking for foreign key issues...")
    print("=" * 50)
    
    try:
        # Check if events have valid track references
        events_without_track = Event.objects.filter(track__isnull=True).count()
        print(f"Events without track: {events_without_track}")
        
        # Check if events have valid organizer references
        events_without_organizer = Event.objects.filter(organizer__isnull=True).count()
        print(f"Events without organizer: {events_without_organizer}")
        
    except Exception as e:
        print(f"❌ Foreign key check error: {e}")
    
    try:
        # Check if callouts have valid user references
        callouts_without_challenger = Callout.objects.filter(challenger__isnull=True).count()
        print(f"Callouts without challenger: {callouts_without_challenger}")
        
        callouts_without_challenged = Callout.objects.filter(challenged__isnull=True).count()
        print(f"Callouts without challenged: {callouts_without_challenged}")
        
    except Exception as e:
        print(f"❌ Callout foreign key check error: {e}")
    
    # Check database schema
    print("\nChecking database schema...")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        try:
            # Check if Event table has is_sponsored column
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'core_event' 
                AND column_name = 'is_sponsored'
            """)
            result = cursor.fetchone()
            if result:
                print("✅ Event table has is_sponsored column")
            else:
                print("❌ Event table missing is_sponsored column")
        except Exception as e:
            print(f"❌ Schema check error: {e}")
        
        try:
            # Check if RaceResult table has callout_id column
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'core_raceresult' 
                AND column_name = 'callout_id'
            """)
            result = cursor.fetchone()
            if result:
                print("✅ RaceResult table has callout_id column")
            else:
                print("❌ RaceResult table missing callout_id column")
        except Exception as e:
            print(f"❌ Schema check error: {e}")

if __name__ == "__main__":
    check_database_issues() 