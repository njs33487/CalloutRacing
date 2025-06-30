from django.core.management.base import BaseCommand
from core.models import User, Track, Event, Callout, UserProfile
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Populate the database with sample events and callouts for testing'

    def handle(self, *args, **options):
        # Get existing users and tracks
        users = list(User.objects.all())
        tracks = list(Track.objects.filter(is_active=True))
        
        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please create users first.'))
            return
            
        if not tracks:
            self.stdout.write(self.style.ERROR('No tracks found. Please run populate_tracks first.'))
            return

        # Create sample events
        self.create_sample_events(users, tracks)
        
        # Create sample callouts only if we have multiple users
        if len(users) >= 2:
            self.create_sample_callouts(users, tracks)
        else:
            self.stdout.write('Skipping callouts - need at least 2 users')
        
        self.stdout.write(self.style.SUCCESS('Successfully created sample data!'))

    def create_sample_events(self, users, tracks):
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
            'Drag Racing Championship'
        ]
        
        events_created = 0
        
        for i in range(10):
            organizer = random.choice(users)
            track = random.choice(tracks)
            event_type = random.choice(event_types)
            title = random.choice(event_titles)
            
            # Create event with random future date
            start_date = timezone.now() + timedelta(days=random.randint(1, 30))
            end_date = start_date + timedelta(hours=random.randint(2, 8))
            
            event = Event.objects.create(
                title=f"{title} #{i+1}",
                description=f"Join us for an exciting {event_type} event at {track.name}!",
                event_type=event_type,
                track=track,
                organizer=organizer,
                start_date=start_date,
                end_date=end_date,
                max_participants=random.randint(20, 100),
                entry_fee=random.choice([0, 25, 50, 75, 100]),
                is_public=True,
                is_active=True
            )
            events_created += 1
            
        self.stdout.write(f'Created {events_created} sample events')

    def create_sample_callouts(self, users, tracks):
        race_types = ['quarter_mile', 'eighth_mile', 'roll_race', 'dig_race', 'heads_up']
        experience_levels = ['beginner', 'intermediate', 'experienced', 'pro']
        
        callouts_created = 0
        
        for i in range(min(15, len(users) * (len(users) - 1))):  # Limit based on available users
            challenger = random.choice(users)
            other_users = [u for u in users if u != challenger]
            
            if not other_users:
                break
                
            challenged = random.choice(other_users)
            track = random.choice(tracks)
            race_type = random.choice(race_types)
            experience_level = random.choice(experience_levels)
            
            # Create callout with random future date
            scheduled_date = timezone.now() + timedelta(days=random.randint(1, 14))
            
            callout = Callout.objects.create(
                challenger=challenger,
                challenged=challenged,
                race_type=race_type,
                location_type='track',
                track=track,
                scheduled_date=scheduled_date,
                message=f"Ready to race? Let's see who's faster!",
                is_private=False,
                is_invite_only=False,
                experience_level=experience_level,
                status='pending'
            )
            callouts_created += 1
            
        self.stdout.write(f'Created {callouts_created} sample callouts') 