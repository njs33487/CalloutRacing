from django.core.management.base import BaseCommand
from core.models.racing import Track
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate the database with comprehensive dragstrip data from the United States'

    def handle(self, *args, **options):
        self.create_dragstrips()
        self.stdout.write(self.style.SUCCESS('Successfully created comprehensive dragstrip data!'))  # type: ignore

    def create_dragstrips(self):
        """Create comprehensive dragstrip data for the US"""
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
                'name': 'Atmore Dragway',
                'location': 'Atmore, Alabama',
                'description': 'Eighth-mile concrete dragstrip opened in 1975.',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.125,
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
                'name': 'Bremerton Raceway',
                'location': 'Bremerton, Washington',
                'description': 'Eighth-mile asphalt dragstrip opened in 1959.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.125,
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
                'name': 'Buffalo Valley Dragway',
                'location': 'Buffalo Valley, Tennessee',
                'description': 'Quarter-mile asphalt dragstrip opened in 1965.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Bunker Hill Dragstrip',
                'location': 'Bunker Hill, Indiana',
                'description': 'Quarter-mile concrete dragstrip opened in 1956.',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Byron Dragway',
                'location': 'Byron, Illinois',
                'description': 'Quarter-mile concrete dragstrip opened in 1964.',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Cecil County Dragway',
                'location': 'Rising Sun, Maryland',
                'description': 'Quarter-mile concrete dragstrip opened in 1963.',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Dominion Raceway',
                'location': 'Thornburg, Virginia',
                'description': 'Eighth-mile asphalt dragstrip opened in 2016. CARS Tour venue.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.125,
                'is_active': True
            },
            {
                'name': 'Firebird Raceway',
                'location': 'Eagle, Idaho',
                'description': 'Quarter-mile asphalt dragstrip opened in 1968.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
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
                'name': 'GALOT Motorsports Park',
                'location': 'Benson, North Carolina',
                'description': 'Eighth-mile asphalt dragstrip opened in 1957.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.125,
                'is_active': True
            },
            {
                'name': 'George Ray\'s Dragstrip',
                'location': 'Paragould, Arkansas',
                'description': 'Eighth-mile concrete dragstrip opened in 1961.',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.125,
                'is_active': True
            },
            {
                'name': 'Great Lakes Dragaway',
                'location': 'Union Grove, Wisconsin',
                'description': 'Quarter-mile asphalt dragstrip opened in 1955.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Heartland Motorsports Park',
                'location': 'Topeka, Kansas',
                'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile asphalt dragstrip opened in 1989.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Hilo Dragstrip',
                'location': 'Hilo, Hawaii',
                'description': 'Quarter-mile asphalt dragstrip opened in 1978.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
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
                'name': 'Keystone Raceway Park',
                'location': 'New Alexandria, Pennsylvania',
                'description': 'Quarter-mile asphalt dragstrip opened in 1968.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Kil-Kare Raceway',
                'location': 'Xenia, Ohio',
                'description': 'Quarter-mile concrete dragstrip opened in 1959.',
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
                'name': 'Lebanon Valley Dragway',
                'location': 'West Lebanon, New York',
                'description': 'Quarter-mile asphalt dragstrip opened in 1963.',
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
                'name': 'Magic City International Dragway',
                'location': 'Minot, North Dakota',
                'description': 'Eighth-mile asphalt dragstrip opened in 1988.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.125,
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
                'name': 'Maryland International Raceway',
                'location': 'Mechanicsville, Maryland',
                'description': 'Quarter-mile asphalt dragstrip opened in 1966.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'National Trail Raceway',
                'location': 'Hebron, Ohio',
                'description': 'Quarter-mile concrete/asphalt dragstrip opened in 1964.',
                'track_type': 'drag',
                'surface_type': 'concrete',
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
                'name': 'Portland International Raceway',
                'location': 'Portland, Oregon',
                'description': 'Quarter-mile concrete dragstrip opened in 1960.',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Rockingham Dragway',
                'location': 'Rockingham, North Carolina',
                'description': 'Quarter-mile asphalt dragstrip opened in 1970.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Route 66 Raceway',
                'location': 'Joliet, Illinois',
                'description': 'Quarter-mile concrete dragstrip opened in 1998.',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Roxboro Motorsports Park',
                'location': 'Timberlake, North Carolina',
                'description': 'Quarter-mile asphalt dragstrip opened in 1959.',
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
                'name': 'State Capitol Raceway',
                'location': 'Port Allen, Louisiana',
                'description': 'Quarter-mile asphalt dragstrip opened in 1969.',
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
                'name': 'Tulsa Raceway Park',
                'location': 'Tulsa, Oklahoma',
                'description': 'Quarter-mile concrete dragstrip opened in 1965.',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'US 13 Dragway',
                'location': 'Delmar, Delaware',
                'description': 'Quarter-mile asphalt dragstrip opened in 1963.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'US 90 Dragway',
                'location': 'Irvington, Alabama',
                'description': 'Eighth-mile concrete dragstrip opened in 1998.',
                'track_type': 'drag',
                'surface_type': 'concrete',
                'length': 0.125,
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
                'name': 'Wisconsin International Raceway',
                'location': 'Kaukauna, Wisconsin',
                'description': 'Quarter-mile asphalt dragstrip opened in 1964.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'Woodburn Dragstrip',
                'location': 'Woodburn, Oregon',
                'description': 'Quarter-mile asphalt dragstrip opened in 1961.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
                'length': 0.25,
                'is_active': True
            },
            {
                'name': 'World Wide Technology Raceway',
                'location': 'Madison, Illinois',
                'description': 'NHRA Camping World Drag Racing Series venue. Quarter-mile asphalt dragstrip opened in 1967.',
                'track_type': 'drag',
                'surface_type': 'asphalt',
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

        created_count = 0
        updated_count = 0

        for track_data in dragstrips_data:
            track, created = Track.objects.get_or_create(
                name=track_data['name'],
                defaults=track_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created: {track_data['name']}")
            else:
                # Update existing track with new data
                for key, value in track_data.items():
                    setattr(track, key, value)
                track.save()
                updated_count += 1
                self.stdout.write(f"Updated: {track_data['name']}")

        self.stdout.write(f"\nCreated {created_count} new dragstrips")
        self.stdout.write(f"Updated {updated_count} existing dragstrips")
        self.stdout.write(f"Total dragstrips processed: {created_count + updated_count}") 