"""
SEO Views for CalloutRacing Application

This module provides SEO optimization features including:
- Dynamic meta tag generation
- Structured data for events, tracks, and marketplace items
- Sitemap generation
- SEO-friendly URLs
"""

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime
import json
from typing import Dict, Any, List
import logging

from core.models.racing import Track, Event, Callout
from core.models.marketplace import MarketplaceListing
from core.models.locations import HotSpot

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_seo_meta_tags(request, content_type: str, content_id: int = None):
    """
    Get SEO meta tags for different content types.
    
    Args:
        content_type: Type of content (event, track, callout, listing)
        content_id: ID of the specific content item
    
    Returns:
        JSON with meta tags and structured data
    """
    
    base_url = request.build_absolute_uri('/').rstrip('/')
    
    if content_type == 'event' and content_id:
        return get_event_seo(content_id, base_url)
    elif content_type == 'track' and content_id:
        return get_track_seo(content_id, base_url)
    elif content_type == 'callout' and content_id:
        return get_callout_seo(content_id, base_url)
    elif content_type == 'listing' and content_id:
        return get_listing_seo(content_id, base_url)
    elif content_type == 'hotspot' and content_id:
        return get_hotspot_seo(content_id, base_url)
    else:
        return get_general_seo(base_url)


def get_event_seo(event_id: int, base_url: str) -> Response:
    """Get SEO data for a specific event."""
    try:
        event = Event.objects.get(id=event_id)
        
        title = f"{event.title} - Racing Event | CalloutRacing"
        description = f"Join {event.title} at {event.track.name if event.track else 'our racing venue'}. {event.description[:100]}..."
        
        structured_data = {
            "@context": "https://schema.org",
            "@type": "Event",
            "name": event.title,
            "description": event.description,
            "startDate": event.start_time.isoformat() if event.start_time else None,
            "endDate": event.end_time.isoformat() if event.end_time else None,
            "location": {
                "@type": "Place",
                "name": event.track.name if event.track else "Racing Venue",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": event.track.location if event.track else "Racing Location"
                }
            } if event.track else None,
            "organizer": {
                "@type": "Organization",
                "name": "CalloutRacing"
            },
            "url": f"{base_url}/events/{event.id}"
        }
        
        return Response({
            'title': title,
            'description': description,
            'keywords': f"racing event, {event.title}, drag racing, motorsports, racing competition",
            'image': event.image.url if hasattr(event, 'image') and event.image else f"{base_url}/callourRacingLaunch.jpg",
            'url': f"{base_url}/events/{event.id}",
            'type': 'event',
            'structured_data': structured_data
        })
        
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=404)


def get_track_seo(track_id: int, base_url: str) -> Response:
    """Get SEO data for a specific track."""
    try:
        track = Track.objects.get(id=track_id)
        
        title = f"{track.name} - Race Track | CalloutRacing"
        description = f"Discover {track.name} in {track.location}. {track.description[:100]}..."
        
        structured_data = {
            "@context": "https://schema.org",
            "@type": "SportsActivityLocation",
            "name": track.name,
            "description": track.description,
            "address": {
                "@type": "PostalAddress",
                "addressLocality": track.location,
                "addressCountry": "US"
            },
            "url": f"{base_url}/tracks/{track.id}",
            "sport": "Racing",
            "facilityType": track.track_type
        }
        
        return Response({
            'title': title,
            'description': description,
            'keywords': f"race track, {track.name}, {track.location}, drag racing, motorsports",
            'image': track.image.url if hasattr(track, 'image') and track.image else f"{base_url}/callourRacingLaunch.jpg",
            'url': f"{base_url}/tracks/{track.id}",
            'type': 'website',
            'structured_data': structured_data
        })
        
    except Track.DoesNotExist:
        return Response({'error': 'Track not found'}, status=404)


def get_callout_seo(callout_id: int, base_url: str) -> Response:
    """Get SEO data for a specific callout."""
    try:
        callout = Callout.objects.get(id=callout_id)
        
        title = f"Racing Callout - {callout.message[:50]}... | CalloutRacing"
        description = f"Racing callout: {callout.message[:150]}..."
        
        structured_data = {
            "@context": "https://schema.org",
            "@type": "SportsEvent",
            "name": f"Racing Callout",
            "description": callout.message,
            "sport": "Racing",
            "url": f"{base_url}/callouts/{callout.id}"
        }
        
        return Response({
            'title': title,
            'description': description,
            'keywords': f"racing callout, drag racing challenge, racing competition, motorsports",
            'image': f"{base_url}/callourRacingLaunch.jpg",
            'url': f"{base_url}/callouts/{callout.id}",
            'type': 'website',
            'structured_data': structured_data
        })
        
    except Callout.DoesNotExist:
        return Response({'error': 'Callout not found'}, status=404)


def get_listing_seo(listing_id: int, base_url: str) -> Response:
    """Get SEO data for a specific marketplace listing."""
    try:
        listing = MarketplaceListing.objects.get(id=listing_id)
        
        title = f"{listing.title} - Racing Marketplace | CalloutRacing"
        description = f"Buy {listing.title} in the racing marketplace. {listing.description[:100]}..."
        
        structured_data = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": listing.title,
            "description": listing.description,
            "category": listing.category.name if listing.category else "Racing Equipment",
            "url": f"{base_url}/marketplace/{listing.id}",
            "offers": {
                "@type": "Offer",
                "price": str(listing.price),
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock" if listing.is_active else "https://schema.org/OutOfStock"
            }
        }
        
        return Response({
            'title': title,
            'description': description,
            'keywords': f"racing marketplace, {listing.title}, racing equipment, automotive parts",
            'image': listing.image.url if hasattr(listing, 'image') and listing.image else f"{base_url}/callourRacingLaunch.jpg",
            'url': f"{base_url}/marketplace/{listing.id}",
            'type': 'website',
            'structured_data': structured_data
        })
        
    except MarketplaceListing.DoesNotExist:
        return Response({'error': 'Listing not found'}, status=404)


def get_hotspot_seo(hotspot_id: int, base_url: str) -> Response:
    """Get SEO data for a specific hotspot."""
    try:
        hotspot = HotSpot.objects.get(id=hotspot_id)
        
        title = f"{hotspot.name} - Racing Hotspot | CalloutRacing"
        description = f"Discover {hotspot.name} in {hotspot.city}, {hotspot.state}. {hotspot.description[:100]}..."
        
        structured_data = {
            "@context": "https://schema.org",
            "@type": "Place",
            "name": hotspot.name,
            "description": hotspot.description,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": hotspot.address,
                "addressLocality": hotspot.city,
                "addressRegion": hotspot.state,
                "postalCode": hotspot.zip_code
            },
            "url": f"{base_url}/hotspots/{hotspot.id}"
        }
        
        return Response({
            'title': title,
            'description': description,
            'keywords': f"racing hotspot, {hotspot.name}, {hotspot.city}, car meets, racing location",
            'image': f"{base_url}/callourRacingLaunch.jpg",
            'url': f"{base_url}/hotspots/{hotspot.id}",
            'type': 'website',
            'structured_data': structured_data
        })
        
    except HotSpot.DoesNotExist:
        return Response({'error': 'Hotspot not found'}, status=404)


def get_general_seo(base_url: str) -> Response:
    """Get general SEO data for the website."""
    return Response({
        'title': 'CalloutRacing - Ultimate Racing Community Platform | Find Events, Challenge Racers',
        'description': 'Join the ultimate racing community! Find drag racing events, challenge other racers, discover tracks and hotspots, buy/sell cars, and connect with car enthusiasts nationwide.',
        'keywords': 'racing, drag racing, car community, racing events, car meets, race tracks, car enthusiasts, automotive, motorsports, racing platform, car marketplace, racing hotspots',
        'image': f"{base_url}/callourRacingLaunch.jpg",
        'url': base_url,
        'type': 'website',
        'structured_data': {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "CalloutRacing",
            "url": base_url,
            "description": "Ultimate racing community platform for finding events, challenging racers, and connecting with car enthusiasts"
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
@cache_page(60 * 60 * 24)  # Cache for 24 hours
def generate_sitemap(request):
    """
    Generate a dynamic sitemap for the website.
    """
    base_url = request.build_absolute_uri('/').rstrip('/')
    
    # Get recent content
    recent_events = Event.objects.filter(start_time__gte=timezone.now()).order_by('start_time')[:50]
    active_tracks = Track.objects.filter(is_active=True)[:50]
    recent_callouts = Callout.objects.filter(status='pending').order_by('-created_at')[:50]
    active_listings = MarketplaceListing.objects.filter(is_active=True).order_by('-created_at')[:50]
    hotspots = HotSpot.objects.all()[:50]
    
    sitemap_urls = []
    
    # Add static pages
    static_pages = [
        {'url': '/', 'priority': '1.0', 'changefreq': 'daily'},
        {'url': '/about', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/contact', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/callouts', 'priority': '0.9', 'changefreq': 'hourly'},
        {'url': '/events', 'priority': '0.9', 'changefreq': 'daily'},
        {'url': '/tracks', 'priority': '0.8', 'changefreq': 'weekly'},
        {'url': '/hotspots', 'priority': '0.8', 'changefreq': 'daily'},
        {'url': '/marketplace', 'priority': '0.8', 'changefreq': 'daily'},
        {'url': '/social', 'priority': '0.8', 'changefreq': 'hourly'},
        {'url': '/login', 'priority': '0.6', 'changefreq': 'monthly'},
        {'url': '/signup', 'priority': '0.6', 'changefreq': 'monthly'},
    ]
    
    for page in static_pages:
        sitemap_urls.append({
            'loc': f"{base_url}{page['url']}",
            'lastmod': timezone.now().strftime('%Y-%m-%d'),
            'changefreq': page['changefreq'],
            'priority': page['priority']
        })
    
    # Add dynamic content
    for event in recent_events:
        sitemap_urls.append({
            'loc': f"{base_url}/events/{event.id}",
            'lastmod': event.updated_at.strftime('%Y-%m-%d') if hasattr(event, 'updated_at') else event.created_at.strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.7'
        })
    
    for track in active_tracks:
        sitemap_urls.append({
            'loc': f"{base_url}/tracks/{track.id}",
            'lastmod': track.updated_at.strftime('%Y-%m-%d') if hasattr(track, 'updated_at') else track.created_at.strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.6'
        })
    
    for callout in recent_callouts:
        sitemap_urls.append({
            'loc': f"{base_url}/callouts/{callout.id}",
            'lastmod': callout.updated_at.strftime('%Y-%m-%d') if hasattr(callout, 'updated_at') else callout.created_at.strftime('%Y-%m-%d'),
            'changefreq': 'daily',
            'priority': '0.6'
        })
    
    for listing in active_listings:
        sitemap_urls.append({
            'loc': f"{base_url}/marketplace/{listing.id}",
            'lastmod': listing.updated_at.strftime('%Y-%m-%d') if hasattr(listing, 'updated_at') else listing.created_at.strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.6'
        })
    
    for hotspot in hotspots:
        sitemap_urls.append({
            'loc': f"{base_url}/hotspots/{hotspot.id}",
            'lastmod': hotspot.updated_at.strftime('%Y-%m-%d') if hasattr(hotspot, 'updated_at') else hotspot.created_at.strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.5'
        })
    
    return Response({
        'urls': sitemap_urls,
        'total_urls': len(sitemap_urls),
        'generated_at': timezone.now().isoformat()
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_seo_analytics(request):
    """
    Get SEO analytics and statistics.
    """
    try:
        # Count content for SEO insights
        total_events = Event.objects.count()
        total_tracks = Track.objects.filter(is_active=True).count()
        total_callouts = Callout.objects.filter(status='pending').count()
        total_listings = MarketplaceListing.objects.filter(is_active=True).count()
        total_hotspots = HotSpot.objects.count()
        
        # Get recent activity
        recent_events = Event.objects.filter(start_time__gte=timezone.now()).count()
        recent_callouts = Callout.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(days=7)).count()
        
        return Response({
            'content_counts': {
                'events': total_events,
                'tracks': total_tracks,
                'callouts': total_callouts,
                'listings': total_listings,
                'hotspots': total_hotspots
            },
            'recent_activity': {
                'upcoming_events': recent_events,
                'recent_callouts': recent_callouts
            },
            'seo_health': {
                'has_meta_tags': True,
                'has_structured_data': True,
                'has_sitemap': True,
                'mobile_friendly': True,
                'https_enabled': request.is_secure()
            }
        })
        
    except Exception as e:
        logger.error("Error in get_seo_analytics")
        return Response({'error': 'Internal server error'}, status=500) 