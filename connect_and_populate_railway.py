#!/usr/bin/env python3
"""
Script to connect to Railway PostgreSQL database and populate with sample data
"""
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')

# Configure database connection for Railway
os.environ['DATABASE_URL'] = 'postgresql://postgres:password@caboose.proxy.rlwy.net:33954/railway'

# Initialize Django
django.setup()

User = get_user_model()

def populate_database():
    """Populate the database with sample data"""
    print("Connecting to Railway PostgreSQL database...")
    print(f"Database URL: postgresql://postgres:***@caboose.proxy.rlwy.net:33954/railway")
    
    try:
        # Import models after Django setup
        from django.contrib.auth.models import User
        from core.models.auth import UserProfile
        from core.models.locations import HotSpot
        from core.models.racing import Track, Event, Callout
        from core.models.social import UserPost, PostComment, Follow
        from core.models.marketplace import ListingCategory, MarketplaceListing
        
        print("✓ Successfully connected to Railway database")
        
        # Check if data already exists
        if User.objects.filter(is_superuser=True).exists():
            print("✓ Admin user already exists")
            admin_user = User.objects.filter(is_superuser=True).first()
        else:
            # Create admin user
            print("Creating admin user...")
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@calloutracing.com',
                password='admin123'
            )
            print(f"✓ Created admin user: {admin_user.username}")
        
        # Create or get UserProfile for admin
        profile, created = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={
                'bio': 'System Administrator',
                'location': 'United States',
                'phone': '+1234567890',
                'is_verified': True
            }
        )
        if created:
            print(f"✓ Created user profile for admin")
        
        # Create sample locations
        locations_data = [
            {'name': 'Los Angeles', 'state': 'CA', 'country': 'USA'},
            {'name': 'New York', 'state': 'NY', 'country': 'USA'},
            {'name': 'Miami', 'state': 'FL', 'country': 'USA'},
            {'name': 'Chicago', 'state': 'IL', 'country': 'USA'},
            {'name': 'Houston', 'state': 'TX', 'country': 'USA'},
        ]
        
        locations = []
        for loc_data in locations_data:
            location, created = Location.objects.get_or_create(
                name=loc_data['name'],
                defaults=loc_data
            )
            if created:
                print(f"✓ Created location: {location.name}")
            locations.append(location)
        
        # Create sample tracks
        tracks_data = [
            {'name': 'LA Raceway', 'location': locations[0], 'type': 'road_course'},
            {'name': 'NY Speedway', 'location': locations[1], 'type': 'oval'},
            {'name': 'Miami Circuit', 'location': locations[2], 'type': 'road_course'},
            {'name': 'Chicago Track', 'location': locations[3], 'type': 'oval'},
            {'name': 'Houston Dragway', 'location': locations[4], 'type': 'drag_strip'},
        ]
        
        tracks = []
        for track_data in tracks_data:
            track, created = Track.objects.get_or_create(
                name=track_data['name'],
                defaults=track_data
            )
            if created:
                print(f"✓ Created track: {track.name}")
            tracks.append(track)
        
        # Create sample drag strips
        dragstrips_data = [
            {'name': 'LA Drag Strip', 'location': locations[0], 'length': '1320'},
            {'name': 'NY Dragway', 'location': locations[1], 'length': '1320'},
            {'name': 'Miami Speedway', 'location': locations[2], 'length': '1320'},
        ]
        
        dragstrips = []
        for strip_data in dragstrips_data:
            strip, created = DragStrip.objects.get_or_create(
                name=strip_data['name'],
                defaults=strip_data
            )
            if created:
                print(f"✓ Created drag strip: {strip.name}")
            dragstrips.append(strip)
        
        # Create sample events
        events_data = [
            {
                'title': 'Spring Racing Championship',
                'description': 'Annual spring racing event with multiple classes',
                'location': locations[0],
                'start_date': '2024-04-15',
                'end_date': '2024-04-17',
                'event_type': 'championship',
                'organizer': admin_user
            },
            {
                'title': 'Summer Drag Racing Series',
                'description': 'Weekly drag racing series throughout summer',
                'location': locations[2],
                'start_date': '2024-06-01',
                'end_date': '2024-08-31',
                'event_type': 'series',
                'organizer': admin_user
            },
            {
                'title': 'Fall Track Day',
                'description': 'Open track day for all skill levels',
                'location': locations[1],
                'start_date': '2024-10-20',
                'end_date': '2024-10-20',
                'event_type': 'track_day',
                'organizer': admin_user
            }
        ]
        
        events = []
        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults=event_data
            )
            if created:
                print(f"✓ Created event: {event.title}")
            events.append(event)
        
        # Create sample callouts
        callouts_data = [
            {
                'title': 'Street Racing Challenge',
                'description': 'Looking for challengers in the LA area',
                'location': locations[0],
                'challenger': admin_user,
                'experience_level': 'intermediate',
                'is_invite_only': False
            },
            {
                'title': 'Drag Strip Showdown',
                'description': 'Quarter mile challenge at Miami Speedway',
                'location': locations[2],
                'challenger': admin_user,
                'experience_level': 'advanced',
                'is_invite_only': True
            }
        ]
        
        callouts = []
        for callout_data in callouts_data:
            callout, created = Callout.objects.get_or_create(
                title=callout_data['title'],
                defaults=callout_data
            )
            if created:
                print(f"✓ Created callout: {callout.title}")
            callouts.append(callout)
        
        # Create sample listing categories
        categories_data = [
            {'name': 'Cars', 'description': 'Complete vehicles for sale'},
            {'name': 'Parts', 'description': 'Car parts and components'},
            {'name': 'Services', 'description': 'Racing and automotive services'},
            {'name': 'Equipment', 'description': 'Racing equipment and tools'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = ListingCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                print(f"✓ Created category: {category.name}")
            categories.append(category)
        
        # Create sample marketplace listings
        listings_data = [
            {
                'title': '2018 Mustang GT',
                'description': 'Well-maintained Mustang GT, perfect for racing',
                'price': 35000.00,
                'category': categories[0],
                'seller': admin_user,
                'location': locations[0]
            },
            {
                'title': 'Turbo Kit for Honda Civic',
                'description': 'Complete turbo kit, barely used',
                'price': 2500.00,
                'category': categories[1],
                'seller': admin_user,
                'location': locations[1]
            },
            {
                'title': 'Professional Tuning Service',
                'description': 'ECU tuning and dyno services',
                'price': 500.00,
                'category': categories[2],
                'seller': admin_user,
                'location': locations[2]
            }
        ]
        
        listings = []
        for listing_data in listings_data:
            listing, created = MarketplaceListing.objects.get_or_create(
                title=listing_data['title'],
                defaults=listing_data
            )
            if created:
                print(f"✓ Created listing: {listing.title}")
            listings.append(listing)
        
        # Create sample social posts
        posts_data = [
            {
                'content': 'Just finished a great race at LA Raceway! The new setup is working perfectly.',
                'author': admin_user,
                'location': locations[0]
            },
            {
                'content': 'Looking for recommendations on the best drag racing tires for street use.',
                'author': admin_user,
                'location': locations[2]
            },
            {
                'content': 'Spring Championship registration is now open! Don\'t miss out on this amazing event.',
                'author': admin_user,
                'location': locations[0]
            }
        ]
        
        posts = []
        for post_data in posts_data:
            post, created = Post.objects.get_or_create(
                content=post_data['content'][:50] + '...' if len(post_data['content']) > 50 else post_data['content'],
                defaults=post_data
            )
            if created:
                print(f"✓ Created post: {post.content[:30]}...")
            posts.append(post)
        
        # Create sample comments
        comments_data = [
            {'content': 'Great job! What was your time?', 'post': posts[0], 'author': admin_user},
            {'content': 'I recommend Michelin Pilot Sport tires', 'post': posts[1], 'author': admin_user},
            {'content': 'Count me in! Can\'t wait for the championship', 'post': posts[2], 'author': admin_user},
        ]
        
        for comment_data in comments_data:
            comment, created = Comment.objects.get_or_create(
                content=comment_data['content'],
                post=comment_data['post'],
                author=comment_data['author']
            )
            if created:
                print(f"✓ Created comment: {comment.content[:30]}...")
        
        # Create sample likes
        for post in posts:
            like, created = Like.objects.get_or_create(
                post=post,
                user=admin_user
            )
            if created:
                print(f"✓ Created like for post: {post.content[:30]}...")
        
        print("\n🎉 Database population completed successfully!")
        print(f"✓ Admin user: {admin_user.username} (password: admin123)")
        print(f"✓ Created {len(locations)} locations")
        print(f"✓ Created {len(tracks)} tracks")
        print(f"✓ Created {len(dragstrips)} drag strips")
        print(f"✓ Created {len(events)} events")
        print(f"✓ Created {len(callouts)} callouts")
        print(f"✓ Created {len(categories)} marketplace categories")
        print(f"✓ Created {len(listings)} marketplace listings")
        print(f"✓ Created {len(posts)} social posts")
        
        return True
        
    except Exception as e:
        print(f"❌ Error populating database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = populate_database()
    if success:
        print("\n✅ Database is ready for use!")
    else:
        print("\n❌ Failed to populate database")
        sys.exit(1) 