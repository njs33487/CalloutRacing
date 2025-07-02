from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from core.models import Track, Event, Callout, HotSpot, MarketplaceListing
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate Railway database with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput',
            action='store_true',
            help='Do not prompt for user input',
        )

    def handle(self, *args, **options):
        self.stdout.write("🚀 Starting Railway data population...")
        
        # 1. Create Admin User
        self.stdout.write("👤 Creating admin user...")
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@calloutracing.com',
                'password': make_password('admin123'),
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        
        if not created:
            admin_user.set_password('admin123')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
        
        self.stdout.write(f"✅ Admin user: {admin_user.email}")
        
        # 2. Create Sample Tracks
        self.stdout.write("🏁 Creating sample tracks...")
        
        tracks_data = [
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
                'name': 'Atlanta Dragway',
                'location': 'Commerce, Georgia',
                'description': 'NHRA Camping World Drag Racing Series venue.',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Bandimere Speedway',
                'location': 'Morrison, Colorado',
                'description': 'NHRA Camping World Drag Racing Series venue.',
                'track_type': 'drag',
                'surface_type': 'concrete',
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
                'description': 'NHRA Camping World Drag Racing Series venue.',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.25,
                'is_active': True
            }
        ]
        
        created_tracks = []
        for track_data in tracks_data:
            track, created = Track.objects.get_or_create(
                name=track_data['name'],
                defaults=track_data
            )
            if created:
                created_tracks.append(track)
                self.stdout.write(f"   ✅ Created: {track.name}")
        
        self.stdout.write(f"✅ Created {len(created_tracks)} tracks")
        
        # 3. Create Sample Events
        self.stdout.write("📅 Creating sample events...")
        
        event_data = [
            {
                'title': 'Friday Night Drags',
                'description': 'Weekly drag racing event for all skill levels',
                'event_type': 'drag',
                'start_time': timezone.now() + timedelta(days=7),
                'end_time': timezone.now() + timedelta(days=7, hours=4),
                'location': 'Atlanta Dragway',
                'is_active': True
            },
            {
                'title': 'Test & Tune Session',
                'description': 'Open track time for testing and tuning',
                'event_type': 'test_tune',
                'start_time': timezone.now() + timedelta(days=14),
                'end_time': timezone.now() + timedelta(days=14, hours=6),
                'location': 'Bristol Dragway',
                'is_active': True
            }
        ]
        
        created_events = []
        for event_info in event_data:
            track = Track.objects.filter(name=event_info['location']).first()
            if track:
                event, created = Event.objects.get_or_create(
                    title=event_info['title'],
                    defaults={
                        **event_info,
                        'track': track,
                        'created_by': admin_user
                    }
                )
                if created:
                    created_events.append(event)
                    self.stdout.write(f"   ✅ Created: {event.title}")
        
        self.stdout.write(f"✅ Created {len(created_events)} events")
        
        # 4. Create Sample Callouts
        self.stdout.write("🏎️ Creating sample callouts...")
        
        callout_data = [
            {
                'title': 'Looking for Competition',
                'description': 'Anyone want to race? Stock vs Stock',
                'callout_type': 'open',
                'experience_level': 'beginner',
                'is_invite_only': False
            },
            {
                'title': 'Pro Challenge',
                'description': 'Pro racers only. Serious competition.',
                'callout_type': 'challenge',
                'experience_level': 'expert',
                'is_invite_only': True
            }
        ]
        
        created_callouts = []
        for callout_info in callout_data:
            track = Track.objects.first()
            if track:
                callout, created = Callout.objects.get_or_create(
                    title=callout_info['title'],
                    defaults={
                        **callout_info,
                        'track': track,
                        'created_by': admin_user
                    }
                )
                if created:
                    created_callouts.append(callout)
                    self.stdout.write(f"   ✅ Created: {callout.title}")
        
        self.stdout.write(f"✅ Created {len(created_callouts)} callouts")
        
        # 5. Create Sample HotSpots
        self.stdout.write("🔥 Creating sample hotspots...")
        
        hotspot_data = [
            {
                'name': 'Pit Area',
                'description': 'Main pit area for racers',
                'hotspot_type': 'meeting',
                'is_active': True
            },
            {
                'name': 'Starting Line',
                'description': 'Where the action begins',
                'hotspot_type': 'racing',
                'is_active': True
            }
        ]
        
        created_hotspots = []
        for hotspot_info in hotspot_data:
            track = Track.objects.first()
            if track:
                hotspot, created = HotSpot.objects.get_or_create(
                    name=hotspot_info['name'],
                    track=track,
                    defaults={
                        **hotspot_info,
                        'created_by': admin_user
                    }
                )
                if created:
                    created_hotspots.append(hotspot)
                    self.stdout.write(f"   ✅ Created: {hotspot.name}")
        
        self.stdout.write(f"✅ Created {len(created_hotspots)} hotspots")
        
        # Summary
        self.stdout.write("\n📊 Data Population Summary:")
        self.stdout.write(f"   Users: {User.objects.count()}")
        self.stdout.write(f"   Tracks: {Track.objects.count()}")
        self.stdout.write(f"   Events: {Event.objects.count()}")
        self.stdout.write(f"   Callouts: {Callout.objects.count()}")
        self.stdout.write(f"   HotSpots: {HotSpot.objects.count()}")
        self.stdout.write(f"   Marketplace Listings: {MarketplaceListing.objects.count()}")
        
        self.stdout.write("\n✅ Railway data population completed successfully!")
        self.stdout.write("🔑 Admin credentials: admin / admin123") 