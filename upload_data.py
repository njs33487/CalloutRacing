#!/usr/bin/env python
import os
import sys
import django
import psycopg2
from urllib.parse import urlparse

# Add the backend directory to the Python path
sys.path.append('backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

# Import models
from core.models import Track, User, Event, Callout, HotSpot, MarketplaceListing
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
import random
import uuid

def upload_comprehensive_data():
    """Upload comprehensive data to the database"""
    print("🚀 Starting comprehensive data upload...")
    
    # 1. Create/Update Admin User
    print("👤 Creating admin user...")
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@calloutracing.com',
            'password': make_password('admin123'),
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
            'email_verified': True,
            'is_active': True,
            'email_verification_token': uuid.uuid4()
        }
    )
    
    if not created:
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.email_verified = True
        admin_user.save()
    
    print(f"✅ Admin user: {admin_user.email}")
    
    # 2. Upload Comprehensive Dragstrip Data
    print("\n🏁 Uploading comprehensive dragstrip data...")
    
    dragstrips_data = [
        {
            'name': 'Alabama International Dragway',
            'location': 'Steele, Alabama',
            'description': 'Quarter-mile asphalt dragstrip opened in 1994.',
            'track_type': 'drag',
            'surface_type': 'asphalt',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Alaska Raceway Park',
            'location': 'Palmer, Alaska',
            'description': 'Quarter-mile concrete dragstrip opened in 1964.',
            'track_type': 'drag',
            'surface_type': 'concrete',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Arroyo Seco Raceway',
            'location': 'Deming, New Mexico',
            'description': 'Quarter-mile asphalt dragstrip opened in 1998.',
            'track_type': 'drag',
            'surface_type': 'asphalt',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Atco Dragway',
            'location': 'Atco, New Jersey',
            'description': 'Quarter-mile asphalt dragstrip opened in 1960.',
            'track_type': 'drag',
            'surface_type': 'asphalt',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Atlanta Dragway',
            'location': 'Commerce, Georgia',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile concrete dragstrip opened in 1975.',
            'track_type': 'drag',
            'surface_type': 'concrete',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Bandimere Speedway',
            'location': 'Morrison, Colorado',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile concrete dragstrip opened in 1958.',
            'track_type': 'drag',
            'surface_type': 'concrete',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Bradenton Motorsports Park',
            'location': 'Bradenton, Florida',
            'description': 'Quarter-mile concrete dragstrip opened in 1974.',
            'track_type': 'drag',
            'surface_type': 'concrete',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Brainerd International Raceway',
            'location': 'Brainerd, Minnesota',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile asphalt dragstrip opened in 1969.',
            'track_type': 'drag',
            'surface_type': 'asphalt',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Bristol Dragway',
            'location': 'Bristol, Tennessee',
            'description': 'Quarter-mile concrete dragstrip opened in 1965.',
            'track_type': 'drag',
            'surface_type': 'concrete',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Gainesville Raceway',
            'location': 'Gainesville, Florida',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile concrete dragstrip opened in 1969.',
            'track_type': 'drag',
            'surface_type': 'concrete',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Houston Raceway Park',
            'location': 'Baytown, Texas',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile asphalt dragstrip opened in 1988.',
            'track_type': 'drag',
            'surface_type': 'asphalt',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'In-N-Out Burger Pomona Dragstrip',
            'location': 'Pomona, California',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile concrete dragstrip opened in 1951.',
            'track_type': 'drag',
            'surface_type': 'concrete',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Las Vegas Motor Speedway',
            'location': 'Las Vegas, Nevada',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile asphalt dragstrip opened in 1995.',
            'track_type': 'drag',
            'surface_type': 'asphalt',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Lucas Oil Raceway',
            'location': 'Brownsburg, Indiana',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile asphalt dragstrip opened in 1960.',
            'track_type': 'drag',
            'surface_type': 'asphalt',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Maple Grove Raceway',
            'location': 'Mohnton, Pennsylvania',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile asphalt dragstrip opened in 1962.',
            'track_type': 'drag',
            'surface_type': 'asphalt',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'New England Dragway',
            'location': 'Epping, New Hampshire',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile asphalt dragstrip opened in 1966.',
            'track_type': 'drag',
            'surface_type': 'asphalt',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Pacific Raceways',
            'location': 'Kent, Washington',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile asphalt dragstrip opened in 1960.',
            'track_type': 'drag',
            'surface_type': 'asphalt',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Sonoma Raceway',
            'location': 'Sonoma, California',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile asphalt dragstrip opened in 1968.',
            'track_type': 'drag',
            'surface_type': 'asphalt',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Summit Motorsports Park',
            'location': 'Norwalk, Ohio',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile asphalt dragstrip opened in 1974.',
            'track_type': 'drag',
            'surface_type': 'asphalt',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Texas Motorplex',
            'location': 'Ennis, Texas',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile concrete dragstrip opened in 1986.',
            'track_type': 'drag',
            'surface_type': 'concrete',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Virginia Motorsports Park',
            'location': 'Petersburg, Virginia',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile asphalt dragstrip opened in 1994.',
            'track_type': 'drag',
            'surface_type': 'asphalt',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'Wild Horse Pass Motorsports Park',
            'location': 'Chandler, Arizona',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile concrete dragstrip opened in 1983.',
            'track_type': 'drag',
            'surface_type': 'concrete',
            'length': 0.25,
            'is_active': True
        },
        {
            'name': 'zMAX Dragway at Charlotte Motor Speedway',
            'location': 'Concord, North Carolina',
            'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile concrete dragstrip opened in 2008.',
            'track_type': 'drag',
            'surface_type': 'concrete',
            'length': 0.25,
            'is_active': True
        }
    ]
    
    created_tracks = 0
    updated_tracks = 0
    
    for track_data in dragstrips_data:
        track, created = Track.objects.get_or_create(
            name=track_data['name'],
            defaults=track_data
        )
        
        if created:
            created_tracks += 1
            print(f"✅ Created: {track_data['name']}")
        else:
            # Update existing track
            for key, value in track_data.items():
                setattr(track, key, value)
            track.save()
            updated_tracks += 1
            print(f"🔄 Updated: {track_data['name']}")
    
    print(f"\n🏁 Dragstrips: {created_tracks} created, {updated_tracks} updated")
    
    # 3. Create Sample Users
    print("\n👥 Creating sample users...")
    
    sample_users = [
        {
            'username': 'speeddemon',
            'email': 'speed@example.com',
            'first_name': 'Speed',
            'last_name': 'Demon',
            'password': 'password123'
        },
        {
            'username': 'trackmaster',
            'email': 'track@example.com',
            'first_name': 'Track',
            'last_name': 'Master',
            'password': 'password123'
        },
        {
            'username': 'ovalracer',
            'email': 'oval@example.com',
            'first_name': 'Oval',
            'last_name': 'Racer',
            'password': 'password123'
        },
        {
            'username': 'importking',
            'email': 'import@example.com',
            'first_name': 'Import',
            'last_name': 'King',
            'password': 'password123'
        },
        {
            'username': 'musclequeen',
            'email': 'muscle@example.com',
            'first_name': 'Muscle',
            'last_name': 'Queen',
            'password': 'password123'
        }
    ]
    
    for user_data in sample_users:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'password': make_password(user_data['password']),
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email_verified': True,
                'is_active': True,
                'email_verification_token': uuid.uuid4()
            }
        )
        
        if created:
            print(f"✅ Created user: {user_data['username']}")
        else:
            print(f"🔄 User exists: {user_data['username']}")
    
    # 4. Create Sample Events
    print("\n🎪 Creating sample events...")
    
    event_names = [
        'Friday Night Drags',
        'Weekend Warriors',
        'Street Legal Drags',
        'Import vs Domestic',
        'Muscle Car Showdown',
        'Tuner Tuesday',
        'Classic Car Night',
        'Pro Street Challenge',
        'Junior Dragster Series',
        'Bracket Racing Championship'
    ]
    
    for i, event_name in enumerate(event_names):
        event, created = Event.objects.get_or_create(
            title=event_name,
            defaults={
                'description': f'Exciting {event_name.lower()} event with great prizes!',
                'location': f'Track {i+1}',
                'date': timezone.now() + timedelta(days=i*7),
                'start_time': '18:00:00',
                'end_time': '22:00:00',
                'max_participants': 50,
                'entry_fee': random.randint(25, 100),
                'prize_pool': random.randint(500, 2000),
                'is_active': True,
                'created_by': admin_user
            }
        )
        
        if created:
            print(f"✅ Created event: {event_name}")
    
    # 5. Create Sample Callouts
    print("\n🏆 Creating sample callouts...")
    
    callout_titles = [
        'Street Racing Challenge',
        'Drag Strip Showdown',
        'Quarter Mile Battle',
        'Import vs Domestic',
        'Muscle Car Challenge',
        'Tuner vs Stock',
        'Pro Street Race',
        'Bracket Racing',
        'Heads Up Racing',
        'Index Racing'
    ]
    
    for i, title in enumerate(callout_titles):
        callout, created = Callout.objects.get_or_create(
            title=title,
            defaults={
                'description': f'Exciting {title.lower()} for serious racers!',
                'location': f'Location {i+1}',
                'date': timezone.now() + timedelta(days=i*3),
                'start_time': '20:00:00',
                'max_participants': 20,
                'entry_fee': random.randint(10, 50),
                'prize_pool': random.randint(200, 1000),
                'is_active': True,
                'created_by': admin_user,
                'experience_level': random.choice(['beginner', 'intermediate', 'advanced']),
                'is_invite_only': False
            }
        )
        
        if created:
            print(f"✅ Created callout: {title}")
    
    # 6. Create Sample HotSpots
    print("\n🔥 Creating sample hotspots...")
    
    hotspot_names = [
        'Downtown Racing District',
        'Industrial Zone Drag Strip',
        'Highway 1 Racing Spot',
        'Mountain Pass Racing',
        'Coastal Highway Racing',
        'Desert Racing Oasis',
        'Urban Racing Circuit',
        'Suburban Racing Zone',
        'Rural Racing Road',
        'Bridge Racing Spot'
    ]
    
    for i, name in enumerate(hotspot_names):
        hotspot, created = HotSpot.objects.get_or_create(
            name=name,
            defaults={
                'description': f'Popular racing location: {name}',
                'location': f'Location {i+1}',
                'is_active': True,
                'created_by': admin_user
            }
        )
        
        if created:
            print(f"✅ Created hotspot: {name}")
    
    # 7. Create Sample Marketplace Listings
    print("\n🛒 Creating sample marketplace listings...")
    
    listing_titles = [
        'Turbocharger Kit',
        'Performance Exhaust',
        'Racing Tires',
        'ECU Tune',
        'Suspension Kit',
        'Brake Upgrade',
        'Intake System',
        'Fuel Injectors',
        'Racing Seat',
        'Roll Cage'
    ]
    
    for i, title in enumerate(listing_titles):
        listing, created = MarketplaceListing.objects.get_or_create(
            title=title,
            defaults={
                'description': f'High-quality {title.lower()} for racing enthusiasts',
                'price': random.randint(100, 2000),
                'category': 'parts',
                'condition': 'new',
                'is_active': True,
                'created_by': admin_user
            }
        )
        
        if created:
            print(f"✅ Created listing: {title}")
    
    # Final Summary
    print("\n" + "="*50)
    print("🎉 DATA UPLOAD COMPLETE! 🎉")
    print("="*50)
    print(f"📊 Total Tracks: {Track.objects.count()}")
    print(f"🏁 Drag Strips: {Track.objects.filter(track_type='drag').count()}")
    print(f"👥 Users: {User.objects.count()}")
    print(f"🎪 Events: {Event.objects.count()}")
    print(f"🏆 Callouts: {Callout.objects.count()}")
    print(f"🔥 HotSpots: {HotSpot.objects.count()}")
    print(f"🛒 Marketplace Listings: {MarketplaceListing.objects.count()}")
    print("="*50)

if __name__ == "__main__":
    upload_comprehensive_data() 