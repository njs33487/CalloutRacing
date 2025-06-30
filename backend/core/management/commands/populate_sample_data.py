from django.core.management.base import BaseCommand
from django.db import models
from django.contrib.auth.hashers import make_password
from core.models import User, Track, Event, Callout, UserProfile, HotSpot, MarketplaceListing
from django.utils import timezone
from datetime import timedelta
import random
from typing import List
from core.models.marketplace import ListingCategory


class Command(BaseCommand):
    help = 'Populate the database with comprehensive sample data including staff profile, tracks, and dummy data'

    def handle(self, *args, **options):
        # Create staff profile first
        self.create_staff_profile()
        
        # Create tracks
        self.create_tracks()
        
        # Create sample users
        self.create_sample_users()
        
        # Create sample events
        self.create_sample_events()
        
        # Create sample callouts
        self.create_sample_callouts()
        
        # Create sample hotspots
        self.create_sample_hotspots()
        
        # Create sample marketplace listings
        self.create_sample_marketplace_listings()
        
        self.stdout.write(self.style.SUCCESS('Successfully created comprehensive sample data!'))  # type: ignore

    def create_staff_profile(self):
        """Create the staff profile for digibin@digitalbinarysolutionsllc.com"""
        email = 'digibin@digitalbinarysolutionsllc.com'
        password = '123qweQWE$$'
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():  # type: ignore
            self.stdout.write(f'Staff user {email} already exists, updating...')
            user = User.objects.get(email=email)  # type: ignore
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.email_verified = True
            user.save()
        else:
            user = User.objects.create(  # type: ignore
                username='digibin',
                email=email,
                password=make_password(password),
                first_name='Digital',
                last_name='Binary',
                is_staff=True,
                is_superuser=True,
                email_verified=True,
                is_active=True
            )
            self.stdout.write(f'Created staff user: {email}')
        
        # Create or update user profile
        profile, created = UserProfile.objects.get_or_create(  # type: ignore
            user=user,
            defaults={
                'bio': 'Founder and Lead Developer at Digital Binary Solutions LLC. Racing enthusiast and tech innovator.',
                'location': 'United States',
                'car_make': 'Tesla',
                'car_model': 'Model S Plaid',
                'car_year': 2023,
                'wins': 15,
                'losses': 8,
                'total_races': 23
            }
        )
        
        if not created:
            profile.bio = 'Founder and Lead Developer at Digital Binary Solutions LLC. Racing enthusiast and tech innovator.'
            profile.location = 'United States'
            profile.car_make = 'Tesla'
            profile.car_model = 'Model S Plaid'
            profile.car_year = 2023
            profile.wins = 15
            profile.losses = 8
            profile.total_races = 23
            profile.save()
        
        self.stdout.write(f'Staff profile created/updated for {user.username}')

    def create_tracks(self):
        """Create comprehensive track data for the US"""
        tracks_data = [
            # Major Drag Strips
            {
                'name': 'Pomona Raceway',
                'location': 'Pomona, California',
                'description': 'Home of the NHRA Winternationals and Finals. Historic quarter-mile drag strip.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Gainesville Raceway',
                'location': 'Gainesville, Florida',
                'description': 'NHRA Gatornationals venue. Premier drag racing facility.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'zMAX Dragway',
                'location': 'Concord, North Carolina',
                'description': 'Four-lane drag strip at Charlotte Motor Speedway. NHRA Four-Wide Nationals.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Texas Motorplex',
                'location': 'Ennis, Texas',
                'description': 'NHRA FallNationals venue. State-of-the-art drag racing facility.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Las Vegas Motor Speedway Drag Strip',
                'location': 'Las Vegas, Nevada',
                'description': 'NHRA Nationals venue. High-altitude racing challenges.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            
            # Major Road Courses
            {
                'name': 'Circuit of the Americas',
                'location': 'Austin, Texas',
                'description': 'F1 US Grand Prix venue. 3.426-mile world-class road course.',
                'track_type': 'road_course',
                'surface_type': 'asphalt',
                'length': 3.426,
                'is_active': True
            },
            {
                'name': 'Laguna Seca Raceway',
                'location': 'Monterey, California',
                'description': 'Famous for the Corkscrew. 2.238-mile technical road course.',
                'track_type': 'road_course',
                'surface_type': 'asphalt',
                'length': 2.238,
                'is_active': True
            },
            {
                'name': 'Road America',
                'location': 'Elkhart Lake, Wisconsin',
                'description': '4.048-mile natural terrain road course. IMSA and IndyCar venue.',
                'track_type': 'road_course',
                'surface_type': 'asphalt',
                'length': 4.048,
                'is_active': True
            },
            {
                'name': 'Sebring International Raceway',
                'location': 'Sebring, Florida',
                'description': '12 Hours of Sebring venue. 3.74-mile historic road course.',
                'track_type': 'road_course',
                'surface_type': 'asphalt',
                'length': 3.74,
                'is_active': True
            },
            {
                'name': 'Watkins Glen International',
                'location': 'Watkins Glen, New York',
                'description': '3.4-mile road course. NASCAR and IMSA venue.',
                'track_type': 'road_course',
                'surface_type': 'asphalt',
                'length': 3.4,
                'is_active': True
            },
            
            # Major Oval Tracks
            {
                'name': 'Daytona International Speedway',
                'location': 'Daytona Beach, Florida',
                'description': 'Daytona 500 venue. 2.5-mile high-banked oval.',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 2.5,
                'is_active': True
            },
            {
                'name': 'Indianapolis Motor Speedway',
                'location': 'Indianapolis, Indiana',
                'description': 'Indy 500 venue. 2.5-mile historic oval.',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 2.5,
                'is_active': True
            },
            {
                'name': 'Talladega Superspeedway',
                'location': 'Talladega, Alabama',
                'description': '2.66-mile high-banked superspeedway. NASCAR venue.',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 2.66,
                'is_active': True
            },
            {
                'name': 'Bristol Motor Speedway',
                'location': 'Bristol, Tennessee',
                'description': '0.533-mile high-banked concrete oval. NASCAR short track.',
                'track_type': 'oval',
                'surface_type': 'concrete',
                'length': 0.533,
                'is_active': True
            },
            {
                'name': 'Charlotte Motor Speedway',
                'location': 'Concord, North Carolina',
                'description': '1.5-mile quad-oval. NASCAR All-Star Race venue.',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 1.5,
                'is_active': True
            }
        ]
        
        # Clear existing tracks and create new ones
        Track.objects.all().delete()  # type: ignore
        
        created_tracks = []
        for track_data in tracks_data:
            track = Track.objects.create(**track_data)  # type: ignore
            created_tracks.append(track)
        
        self.stdout.write(f'Created {len(created_tracks)} tracks')

    def create_sample_users(self):
        """Create sample users for testing"""
        sample_users = [
            {
                'username': 'speeddemon',
                'email': 'speeddemon@example.com',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'bio': 'Drag racing enthusiast with a passion for quarter-mile runs.',
                'car_make': 'Chevrolet',
                'car_model': 'Camaro SS',
                'car_year': 2022,
                'wins': 25,
                'losses': 12,
                'total_races': 37
            },
            {
                'username': 'trackmaster',
                'email': 'trackmaster@example.com',
                'first_name': 'Sarah',
                'last_name': 'Williams',
                'bio': 'Road course specialist. Love the technical challenges.',
                'car_make': 'BMW',
                'car_model': 'M3',
                'car_year': 2021,
                'wins': 18,
                'losses': 15,
                'total_races': 33
            },
            {
                'username': 'ovalracer',
                'email': 'ovalracer@example.com',
                'first_name': 'Tom',
                'last_name': 'Davis',
                'bio': 'Oval track specialist. NASCAR fan and weekend warrior.',
                'car_make': 'Ford',
                'car_model': 'Mustang GT',
                'car_year': 2023,
                'wins': 30,
                'losses': 8,
                'total_races': 38
            },
            {
                'username': 'importking',
                'email': 'importking@example.com',
                'first_name': 'Alex',
                'last_name': 'Chen',
                'bio': 'Import tuner specialist. JDM all the way!',
                'car_make': 'Nissan',
                'car_model': 'Skyline GT-R',
                'car_year': 1999,
                'wins': 22,
                'losses': 18,
                'total_races': 40
            },
            {
                'username': 'musclequeen',
                'email': 'musclequeen@example.com',
                'first_name': 'Jessica',
                'last_name': 'Rodriguez',
                'bio': 'American muscle car enthusiast. Nothing beats raw power!',
                'car_make': 'Dodge',
                'car_model': 'Challenger Hellcat',
                'car_year': 2023,
                'wins': 28,
                'losses': 10,
                'total_races': 38
            }
        ]
        
        created_users = []
        for user_data in sample_users:
            # Check if user exists
            user = User.objects.filter(username=user_data['username']).first()  # type: ignore
            if user:
                self.stdout.write(f"User {user_data['username']} already exists, skipping creation.")
            else:
                user = User.objects.create(  # type: ignore
                    username=user_data['username'],
                    email=user_data['email'],
                    password=make_password('password123'),
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email_verified=True,
                    is_active=True
                )
                self.stdout.write(f"Created user: {user_data['username']}")
            # Create or update profile
            profile, created = UserProfile.objects.get_or_create(  # type: ignore
                user=user,
                defaults={
                    'bio': user_data['bio'],
                    'location': 'United States',
                    'car_make': user_data['car_make'],
                    'car_model': user_data['car_model'],
                    'car_year': user_data['car_year'],
                    'wins': user_data['wins'],
                    'losses': user_data['losses'],
                    'total_races': user_data['total_races']
                }
            )
            if not created:
                profile.bio = user_data['bio']
                profile.location = 'United States'
                profile.car_make = user_data['car_make']
                profile.car_model = user_data['car_model']
                profile.car_year = user_data['car_year']
                profile.wins = user_data['wins']
                profile.losses = user_data['losses']
                profile.total_races = user_data['total_races']
                profile.save()
            created_users.append(user)
        
        self.stdout.write(f'Created or updated {len(created_users)} sample users')

    def create_sample_events(self):
        """Create sample events"""
        users = list(User.objects.all())  # type: ignore
        tracks = list(Track.objects.all())  # type: ignore
        
        if not users or not tracks:
            self.stdout.write('Skipping events - need users and tracks')
            return
        
        event_types = ['race', 'meet', 'show', 'practice']
        event_titles = [
            'Friday Night Drags',
            'Weekend Warriors',
            'Street Car Showdown',
            'Test & Tune Night',
            'Import vs Domestic',
            'Muscle Car Madness',
            'Tuner Tuesday',
            'Weekend Race Series',
            'Car Show & Shine',
            'Drag Racing Championship',
            'Road Course Challenge',
            'Oval Track Spectacular',
            'Drift Competition',
            'Time Attack Event',
            'Car Meet & Cruise'
        ]
        
        events_created = 0
        
        for i in range(15):
            organizer = random.choice(users)
            track = random.choice(tracks)
            event_type = random.choice(event_types)
            title = random.choice(event_titles)
            
            # Create event with random future date
            start_date = timezone.now() + timedelta(days=random.randint(1, 60))
            end_date = start_date + timedelta(hours=random.randint(2, 12))
            
            event = Event.objects.create(  # type: ignore
                title=f"{title} #{i+1}",
                description=f"Join us for an exciting {event_type} event at {track.name}! This is a sample event for testing purposes.",
                event_type=event_type,
                track=track,
                organizer=organizer,
                start_date=start_date,
                end_date=end_date,
                max_participants=random.randint(20, 200),
                entry_fee=random.choice([0, 25, 50, 75, 100, 150]),
                is_public=True,
                is_active=True
            )
            events_created += 1
            
        self.stdout.write(f'Created {events_created} sample events')

    def create_sample_callouts(self):
        """Create sample callouts"""
        users = list(User.objects.all())  # type: ignore
        tracks = list(Track.objects.filter(track_type='drag'))  # type: ignore
        
        if len(users) < 2 or not tracks:
            self.stdout.write('Skipping callouts - need at least 2 users and drag tracks')
            return
        
        race_types = ['quarter_mile', 'eighth_mile', 'roll_race', 'dig_race']
        experience_levels = ['beginner', 'intermediate', 'experienced', 'pro']
        
        callouts_created = 0
        
        for i in range(min(20, len(users) * (len(users) - 1))):
            challenger = random.choice(users)
            other_users = [u for u in users if u != challenger]
            
            if not other_users:
                break
                
            challenged = random.choice(other_users)
            track = random.choice(tracks)
            race_type = random.choice(race_types)
            experience_level = random.choice(experience_levels)
            
            # Create callout with random future date
            scheduled_date = timezone.now() + timedelta(days=random.randint(1, 30))
            
            messages = [
                "Ready to race? Let's see who's faster!",
                "Think you can handle this challenge?",
                "Time to settle this on the track!",
                "Your car vs mine. Let's do this!",
                "Ready to put your money where your mouth is?",
                "Show me what you've got!",
                "Time to prove who's the real deal!",
                "Let's see if you can back up that talk!"
            ]
            
            callout = Callout.objects.create(  # type: ignore
                challenger=challenger,
                challenged=challenged,
                race_type=race_type,
                location_type='track',
                track=track,
                scheduled_date=scheduled_date,
                message=random.choice(messages),
                is_private=False,
                is_invite_only=False,
                experience_level=experience_level,
                status='pending',
                wager_amount=random.choice([0, 50, 100, 200, 500])
            )
            callouts_created += 1
            
        self.stdout.write(f'Created {callouts_created} sample callouts')

    def create_sample_hotspots(self):
        """Create sample hotspots"""
        users = list(User.objects.all())  # type: ignore
        
        if not users:
            self.stdout.write('Skipping hotspots - need users')
            return
        
        hotspots_data = [
            {
                'name': 'Downtown Car Meet Spot',
                'description': 'Popular downtown location for car meets and street racing.',
                'address': '123 Main Street',
                'city': 'Los Angeles',
                'state': 'California',
                'zip_code': '90210',
                'latitude': 34.0522,
                'longitude': -118.2437,
                'spot_type': 'street_meet',
                'rules': 'No burnouts, respect the community, keep it clean.',
                'amenities': 'Parking, lighting, food trucks nearby',
                'peak_hours': 'Friday 8PM-12AM, Saturday 7PM-1AM'
            },
            {
                'name': 'Industrial District Racing',
                'description': 'Abandoned industrial area popular for late-night racing.',
                'address': '456 Industrial Blvd',
                'city': 'Houston',
                'state': 'Texas',
                'zip_code': '77001',
                'latitude': 29.7604,
                'longitude': -95.3698,
                'spot_type': 'industrial',
                'rules': 'Be careful, watch for security, no spectators',
                'amenities': 'Long straightaways, minimal traffic',
                'peak_hours': 'Saturday 10PM-3AM'
            },
            {
                'name': 'Mall Parking Lot Meet',
                'description': 'Large mall parking lot for car shows and meets.',
                'address': '789 Shopping Center Dr',
                'city': 'Miami',
                'state': 'Florida',
                'zip_code': '33101',
                'latitude': 25.7617,
                'longitude': -80.1918,
                'spot_type': 'parking_lot',
                'rules': 'No racing, display only, respect mall property',
                'amenities': 'Large parking area, food court, restrooms',
                'peak_hours': 'Sunday 2PM-8PM'
            }
        ]
        
        hotspots_created = 0
        for hotspot_data in hotspots_data:
            creator = random.choice(users)
            
            hotspot = HotSpot.objects.create(  # type: ignore
                created_by=creator,
                **hotspot_data
            )
            hotspots_created += 1
            
        self.stdout.write(f'Created {hotspots_created} sample hotspots')

    def create_sample_marketplace_listings(self):
        """Create sample marketplace listings"""
        users = list(User.objects.all())  # type: ignore
        
        if not users:
            self.stdout.write('Skipping marketplace listings - need users')
            return
        
        listings_data = [
            {
                'title': 'Turbocharger Kit - Brand New',
                'description': 'Complete turbo kit for Honda Civic. Includes everything needed for installation.',
                'price': 2500.00,
                'category': 'performance',
                'condition': 'new'
            },
            {
                'title': 'Used Racing Seats',
                'description': 'Pair of Sparco racing seats. Good condition, includes mounting brackets.',
                'price': 800.00,
                'category': 'interior',
                'condition': 'used'
            },
            {
                'title': 'ECU Tune Service',
                'description': 'Professional ECU tuning service. Dyno tuning available.',
                'price': 500.00,
                'category': 'services',
                'condition': 'new'
            },
            {
                'title': 'Carbon Fiber Hood',
                'description': 'Lightweight carbon fiber hood for Subaru WRX. Perfect fit.',
                'price': 1200.00,
                'category': 'exterior',
                'condition': 'new'
            },
            {
                'title': 'Racing Tires - Set of 4',
                'description': 'Bridgestone Potenza RE-71R. 245/40R18. 80% tread remaining.',
                'price': 600.00,
                'category': 'tires',
                'condition': 'used'
            }
        ]
        
        # Create ListingCategory objects for each unique category
        category_names = set(listing['category'] for listing in listings_data)
        category_objs = {}
        for name in category_names:
            obj, _ = ListingCategory.objects.get_or_create(name=name.capitalize())  # type: ignore
            category_objs[name] = obj
        
        listings_created = 0
        for listing_data in listings_data:
            seller = random.choice(users)
            category_obj = category_objs[listing_data['category']]
            listing = MarketplaceListing.objects.create(  # type: ignore
                seller=seller,
                title=listing_data['title'],
                description=listing_data['description'],
                price=listing_data['price'],
                category=category_obj,
                condition=listing_data['condition']
            )
            listings_created += 1
        
        self.stdout.write(f'Created {listings_created} sample marketplace listings') 