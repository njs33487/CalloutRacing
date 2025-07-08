#!/usr/bin/env python
"""
Detailed database diagnostic script
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
from django.core.exceptions import FieldError

def debug_database():
    """Detailed database debugging"""
    print("🔍 Detailed Database Diagnostic")
    print("=" * 50)
    
    # Check database connection and type
    try:
        with connection.cursor() as cursor:
            # Try PostgreSQL version first
            try:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                print(f"✅ PostgreSQL connected: {version[0]}")
                db_type = "postgresql"
            except:
                # Try SQLite version
                try:
                    cursor.execute("SELECT sqlite_version();")
                    version = cursor.fetchone()
                    print(f"✅ SQLite connected: {version[0]}")
                    db_type = "sqlite"
                except:
                    print("❌ Unknown database type")
                    db_type = "unknown"
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    # Check table structure
    print("\n📋 Checking table structure...")
    tables_to_check = [
        'core_event',
        'core_track', 
        'core_callout',
        'core_raceresult',
        'core_sponsoredcontent',
        'core_userpost',
        'core_user'
    ]
    
    with connection.cursor() as cursor:
        for table in tables_to_check:
            try:
                if db_type == "postgresql":
                    cursor.execute(f"SELECT COUNT(*) FROM {table};")
                else:
                    cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count} records")
            except Exception as e:
                print(f"  ❌ {table}: {e}")
    
    # Check specific columns that were missing
    print("\n🔍 Checking problematic columns...")
    with connection.cursor() as cursor:
        try:
            if db_type == "postgresql":
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'core_event' 
                    AND column_name IN ('is_sponsored', 'sponsor_name', 'sponsor_logo_url', 'sponsor_website_url')
                """)
            else:
                cursor.execute("PRAGMA table_info(core_event);")
                columns = cursor.fetchall()
                event_columns = [col[1] for col in columns if col[1] in ['is_sponsored', 'sponsor_name', 'sponsor_logo_url', 'sponsor_website_url']]
                for col in event_columns:
                    print(f"  ✅ core_event.{col}: exists")
                return
            
            columns = cursor.fetchall()
            for col in columns:
                print(f"  ✅ core_event.{col[0]}: {col[1]}")
        except Exception as e:
            print(f"  ❌ Error checking Event columns: {e}")
        
        try:
            if db_type == "postgresql":
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'core_raceresult' 
                    AND column_name = 'callout_id'
                """)
            else:
                cursor.execute("PRAGMA table_info(core_raceresult);")
                columns = cursor.fetchall()
                race_result_columns = [col[1] for col in columns if col[1] == 'callout_id']
                for col in race_result_columns:
                    print(f"  ✅ core_raceresult.{col}: exists")
                return
            
            columns = cursor.fetchall()
            for col in columns:
                print(f"  ✅ core_raceresult.{col[0]}: {col[1]}")
        except Exception as e:
            print(f"  ❌ Error checking RaceResult columns: {e}")
    
    # Test Django ORM queries
    print("\n🐍 Testing Django ORM queries...")
    
    try:
        events = Event.objects.all()
        print(f"  ✅ Event.objects.all(): {events.count()} records")
        
        # Test the specific query that was failing
        from django.utils import timezone
        upcoming_events = Event.objects.filter(
            start_date__gte=timezone.now(),
            is_active=True
        ).order_by('start_date')[:10]
        print(f"  ✅ Upcoming events query: {upcoming_events.count()} records")
        
    except Exception as e:
        print(f"  ❌ Event query failed: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        callouts = Callout.objects.all()
        print(f"  ✅ Callout.objects.all(): {callouts.count()} records")
        
        # Test the specific query that was failing
        pending_callouts = Callout.objects.filter(status='pending')
        print(f"  ✅ Pending callouts query: {pending_callouts.count()} records")
        
    except Exception as e:
        print(f"  ❌ Callout query failed: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        sponsored_content = SponsoredContent.objects.filter(is_active=True)
        print(f"  ✅ SponsoredContent.objects.filter(is_active=True): {sponsored_content.count()} records")
        
    except Exception as e:
        print(f"  ❌ SponsoredContent query failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Check for foreign key issues
    print("\n🔗 Checking foreign key relationships...")
    
    try:
        # Check if events have valid track references
        events_without_track = Event.objects.filter(track__isnull=True).count()
        print(f"  Events without track: {events_without_track}")
        
        # Check if events have valid organizer references
        events_without_organizer = Event.objects.filter(organizer__isnull=True).count()
        print(f"  Events without organizer: {events_without_organizer}")
        
    except Exception as e:
        print(f"  ❌ Foreign key check failed: {e}")
    
    # Test serializers
    print("\n📝 Testing serializers...")
    
    try:
        from api.serializers import EventSerializer, CalloutSerializer, SponsoredContentSerializer
        
        # Test Event serializer
        events = Event.objects.all()[:1]
        if events:
            serializer = EventSerializer(events[0])
            print(f"  ✅ Event serializer works")
        else:
            print(f"  ⚠️  No events to test serializer")
            
    except Exception as e:
        print(f"  ❌ Serializer test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_database() 