from django.core.management.base import BaseCommand
from core.models import Track
from django.db import transaction


class Command(BaseCommand):
    help = 'Populate the database with real racing tracks from the United States'

    def handle(self, *args, **options):
        tracks_data = [
            # Drag Strips
            {
                'name': 'Alabama International Dragway',
                'location': 'Steele, Alabama',
                'description': 'Quarter mile drag strip with asphalt surface',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Alaska Raceway Park',
                'location': 'Palmer, Alaska',
                'description': 'Quarter mile drag strip with concrete surface',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Atco Dragway',
                'location': 'Atco, New Jersey',
                'description': 'Quarter mile drag strip with asphalt surface',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Atlanta Dragway',
                'location': 'Commerce, Georgia',
                'description': 'Quarter mile drag strip with concrete surface',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Bandimere Speedway',
                'location': 'Morrison, Colorado',
                'description': 'Quarter mile drag strip with asphalt surface',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Beech Bend Raceway Park',
                'location': 'Bowling Green, Kentucky',
                'description': 'Quarter mile drag strip with asphalt surface',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Bristol Dragway',
                'location': 'Bristol, Tennessee',
                'description': 'Quarter mile drag strip with concrete surface',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Charlotte Motor Speedway Dragway',
                'location': 'Concord, North Carolina',
                'description': 'Quarter mile drag strip with asphalt surface',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Gainesville Raceway',
                'location': 'Gainesville, Florida',
                'description': 'Quarter mile drag strip with asphalt surface',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Houston Raceway Park',
                'location': 'Baytown, Texas',
                'description': 'Quarter mile drag strip with asphalt surface',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Las Vegas Motor Speedway Drag Strip',
                'location': 'Las Vegas, Nevada',
                'description': 'Quarter mile drag strip with asphalt surface',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Maple Grove Raceway',
                'location': 'Mohnton, Pennsylvania',
                'description': 'Quarter mile drag strip with asphalt surface',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Pomona Raceway',
                'location': 'Pomona, California',
                'description': 'Quarter mile drag strip with asphalt surface',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Sonoma Raceway',
                'location': 'Sonoma, California',
                'description': 'Quarter mile drag strip with asphalt surface',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Texas Motorplex',
                'location': 'Ennis, Texas',
                'description': 'Quarter mile drag strip with asphalt surface',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'zMAX Dragway',
                'location': 'Concord, North Carolina',
                'description': 'Quarter mile drag strip with asphalt surface',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },

            # Road Courses
            {
                'name': 'Barber Motorsports Park',
                'location': 'Birmingham, Alabama',
                'description': '2.38-mile road course with asphalt surface',
                'track_type': 'road',
                'surface_type': 'asphalt',
                'length': 2.38,
                'is_active': True
            },
            {
                'name': 'Circuit of the Americas',
                'location': 'Austin, Texas',
                'description': '3.426-mile road course with asphalt surface',
                'track_type': 'road',
                'surface_type': 'asphalt',
                'length': 3.426,
                'is_active': True
            },
            {
                'name': 'Daytona International Speedway Road Course',
                'location': 'Daytona Beach, Florida',
                'description': '3.56-mile road course with asphalt surface',
                'track_type': 'road',
                'surface_type': 'asphalt',
                'length': 3.56,
                'is_active': True
            },
            {
                'name': 'Indianapolis Motor Speedway Road Course',
                'location': 'Indianapolis, Indiana',
                'description': '2.439-mile road course with asphalt surface',
                'track_type': 'road',
                'surface_type': 'asphalt',
                'length': 2.439,
                'is_active': True
            },
            {
                'name': 'Laguna Seca Raceway',
                'location': 'Monterey, California',
                'description': '2.238-mile road course with asphalt surface',
                'track_type': 'road',
                'surface_type': 'asphalt',
                'length': 2.238,
                'is_active': True
            },
            {
                'name': 'Mid-Ohio Sports Car Course',
                'location': 'Lexington, Ohio',
                'description': '2.258-mile road course with asphalt surface',
                'track_type': 'road',
                'surface_type': 'asphalt',
                'length': 2.258,
                'is_active': True
            },
            {
                'name': 'Road America',
                'location': 'Elkhart Lake, Wisconsin',
                'description': '4.048-mile road course with asphalt surface',
                'track_type': 'road',
                'surface_type': 'asphalt',
                'length': 4.048,
                'is_active': True
            },
            {
                'name': 'Road Atlanta',
                'location': 'Braselton, Georgia',
                'description': '2.54-mile road course with asphalt surface',
                'track_type': 'road',
                'surface_type': 'asphalt',
                'length': 2.54,
                'is_active': True
            },
            {
                'name': 'Sebring International Raceway',
                'location': 'Sebring, Florida',
                'description': '3.74-mile road course with asphalt surface',
                'track_type': 'road',
                'surface_type': 'asphalt',
                'length': 3.74,
                'is_active': True
            },
            {
                'name': 'Virginia International Raceway',
                'location': 'Alton, Virginia',
                'description': '3.27-mile road course with asphalt surface',
                'track_type': 'road',
                'surface_type': 'asphalt',
                'length': 3.27,
                'is_active': True
            },
            {
                'name': 'Watkins Glen International',
                'location': 'Watkins Glen, New York',
                'description': '3.4-mile road course with asphalt surface',
                'track_type': 'road',
                'surface_type': 'asphalt',
                'length': 3.4,
                'is_active': True
            },

            # Oval Tracks
            {
                'name': 'Atlanta Motor Speedway',
                'location': 'Hampton, Georgia',
                'description': '1.54-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 1.54,
                'is_active': True
            },
            {
                'name': 'Auto Club Speedway',
                'location': 'Fontana, California',
                'description': '2-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 2.0,
                'is_active': True
            },
            {
                'name': 'Bristol Motor Speedway',
                'location': 'Bristol, Tennessee',
                'description': '0.533-mile oval with concrete surface',
                'track_type': 'oval',
                'surface_type': 'concrete',
                'length': 0.533,
                'is_active': True
            },
            {
                'name': 'Charlotte Motor Speedway',
                'location': 'Concord, North Carolina',
                'description': '1.5-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 1.5,
                'is_active': True
            },
            {
                'name': 'Chicagoland Speedway',
                'location': 'Joliet, Illinois',
                'description': '1.5-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 1.5,
                'is_active': True
            },
            {
                'name': 'Darlington Raceway',
                'location': 'Darlington, South Carolina',
                'description': '1.366-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 1.366,
                'is_active': True
            },
            {
                'name': 'Daytona International Speedway',
                'location': 'Daytona Beach, Florida',
                'description': '2.5-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 2.5,
                'is_active': True
            },
            {
                'name': 'Dover International Speedway',
                'location': 'Dover, Delaware',
                'description': '1-mile oval with concrete surface',
                'track_type': 'oval',
                'surface_type': 'concrete',
                'length': 1.0,
                'is_active': True
            },
            {
                'name': 'Homestead-Miami Speedway',
                'location': 'Homestead, Florida',
                'description': '1.5-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 1.5,
                'is_active': True
            },
            {
                'name': 'Indianapolis Motor Speedway',
                'location': 'Indianapolis, Indiana',
                'description': '2.5-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 2.5,
                'is_active': True
            },
            {
                'name': 'Kansas Speedway',
                'location': 'Kansas City, Kansas',
                'description': '1.5-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 1.5,
                'is_active': True
            },
            {
                'name': 'Kentucky Speedway',
                'location': 'Sparta, Kentucky',
                'description': '1.5-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 1.5,
                'is_active': True
            },
            {
                'name': 'Las Vegas Motor Speedway',
                'location': 'Las Vegas, Nevada',
                'description': '1.5-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 1.5,
                'is_active': True
            },
            {
                'name': 'Martinsville Speedway',
                'location': 'Martinsville, Virginia',
                'description': '0.526-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 0.526,
                'is_active': True
            },
            {
                'name': 'Michigan International Speedway',
                'location': 'Brooklyn, Michigan',
                'description': '2-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 2.0,
                'is_active': True
            },
            {
                'name': 'New Hampshire Motor Speedway',
                'location': 'Loudon, New Hampshire',
                'description': '1.058-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 1.058,
                'is_active': True
            },
            {
                'name': 'Phoenix Raceway',
                'location': 'Avondale, Arizona',
                'description': '1-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 1.0,
                'is_active': True
            },
            {
                'name': 'Pocono Raceway',
                'location': 'Long Pond, Pennsylvania',
                'description': '2.5-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 2.5,
                'is_active': True
            },
            {
                'name': 'Richmond Raceway',
                'location': 'Richmond, Virginia',
                'description': '0.75-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 0.75,
                'is_active': True
            },
            {
                'name': 'Talladega Superspeedway',
                'location': 'Talladega, Alabama',
                'description': '2.66-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 2.66,
                'is_active': True
            },
            {
                'name': 'Texas Motor Speedway',
                'location': 'Fort Worth, Texas',
                'description': '1.5-mile oval with asphalt surface',
                'track_type': 'oval',
                'surface_type': 'asphalt',
                'length': 1.5,
                'is_active': True
            }
        ]

        with transaction.atomic():
            # Clear existing tracks
            Track.objects.all().delete()
            
            # Create new tracks
            created_tracks = []
            for track_data in tracks_data:
                track, created = Track.objects.get_or_create(
                    name=track_data['name'],
                    defaults=track_data
                )
                created_tracks.append(track)
                
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {len(created_tracks)} tracks from the United States racing circuit!'
                )
            )
            
            # Print summary by type
            drag_tracks = Track.objects.filter(track_type='drag').count()
            road_tracks = Track.objects.filter(track_type='road').count()
            oval_tracks = Track.objects.filter(track_type='oval').count()
            
            self.stdout.write(f'Drag Strips: {drag_tracks}')
            self.stdout.write(f'Road Courses: {road_tracks}')
            self.stdout.write(f'Oval Tracks: {oval_tracks}')
            self.stdout.write(f'Total Tracks: {Track.objects.count()}') 