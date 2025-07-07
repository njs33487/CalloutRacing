# Callouts and Events Organization Plan

## Overview

This document outlines the comprehensive plan for organizing race callouts and events throughout the CalloutRacing platform to provide a seamless user experience.

## 1. Post Type Classification

### Race Callouts (`race_callout`)
- **Purpose**: Direct challenges between users for races
- **Special Fields**:
  - `callout_challenged_user`: Username of the person being called out
  - `callout_location`: Where the race will take place
  - `callout_location_type`: 'street' or 'dragstrip'
  - `callout_race_type`: Type of race (quarter mile, roll race, etc.)
  - `callout_wager_amount`: Money on the line
  - `callout_scheduled_date`: When the race is scheduled

### Announcements (`announcement`)
- **Purpose**: Platform-wide or community announcements
- **Special Fields**:
  - `is_pinned`: Whether to pin at the top of feeds
  - `announcement_type`: 'general', 'feature', 'maintenance', 'promotion', 'event'
  - `announcement_priority`: 'low', 'medium', 'high', 'critical'

### Events (`event`)
- **Purpose**: Organized racing events and meetups
- **Integration**: Connected to the Events system

## 2. Homepage Organization

### Featured Banner Section
```
┌─────────────────────────────────────────────────────────┐
│ 🏁 FEATURED RACE CALLOUTS                              │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│ │ Callout 1   │ │ Callout 2   │ │ Callout 3   │       │
│ │ vs User A   │ │ vs User B   │ │ vs User C   │       │
│ │ $500 Race   │ │ $1000 Race  │ │ $750 Race   │       │
│ └─────────────┘ └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────────────────────┘
```

### Upcoming Events Section
```
┌─────────────────────────────────────────────────────────┐
│ 📅 UPCOMING EVENTS                                     │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│ │ Event 1     │ │ Event 2     │ │ Event 3     │       │
│ │ Date/Time   │ │ Date/Time   │ │ Date/Time   │       │
│ │ Location    │ │ Location    │ │ Location    │       │
│ └─────────────┘ └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────────────────────┘
```

### Pinned Announcements
```
┌─────────────────────────────────────────────────────────┐
│ 📢 IMPORTANT ANNOUNCEMENTS                             │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 🚨 CRITICAL: Platform maintenance tonight          │ │
│ │ ⚡ NEW FEATURE: Live streaming now available       │ │
│ │ 🎉 PROMOTION: 50% off premium membership          │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 3. Social Feed Integration

### Feed Tabs
1. **My Feed**: Posts from followed users + announcements
2. **Trending**: High-engagement posts from the community
3. **Live Streams**: Currently live streams
4. **Callouts**: Active race callouts
5. **Events**: Event-related posts

### Post Type Icons
- 🏁 Race Callout
- 📢 Announcement
- 🎥 Live Stream
- 🏆 Race Result
- 🚗 Car Update
- 📷 Photo
- 📹 Video
- 📝 Text

### Callout Post Display
```
┌─────────────────────────────────────────────────────────┐
│ 🏁 RACE CALLOUT                                        │
│ UserA has called out UserB for a race!                │
│                                                       │
│ 📍 Location: Downtown Dragstrip                       │
│ 💰 Wager: $500                                        │
│ 🏁 Race Type: Quarter Mile                            │
│ 📅 Date: Saturday, 8:00 PM                           │
│                                                       │
│ [Accept Challenge] [Decline] [Message]               │
└─────────────────────────────────────────────────────────┘
```

## 4. Notification System

### Callout Notifications
- **Challenged User**: Immediate notification when called out
- **Followers**: Notification about the callout
- **Community**: Optional notification for high-profile callouts

### Announcement Notifications
- **High Priority**: Sent to all users immediately
- **Medium Priority**: Sent to followers and interested users
- **Low Priority**: Only shown in feed, no push notification

## 5. Search and Discovery

### Callout Discovery
- **Active Callouts**: Users can browse open challenges
- **Location-based**: Filter by city/region
- **Wager-based**: Filter by amount range
- **Race Type**: Filter by race type preference

### Event Discovery
- **Upcoming Events**: Chronological listing
- **Location-based**: Events near user
- **Type-based**: Drag races, car shows, meets
- **Featured Events**: Promoted events

## 6. User Experience Flow

### Creating a Callout
1. User clicks "Create Callout" button
2. Selects target user from dropdown
3. Chooses location and race type
4. Sets wager amount (optional)
5. Schedules date/time
6. Posts callout to feed

### Responding to Callouts
1. User receives notification
2. Views callout details
3. Can accept, decline, or message
4. If accepted, event is created
5. Both users notified of acceptance

### Creating Announcements
1. Admin/Moderator selects "Announcement" post type
2. Chooses announcement type and priority
3. Sets pin status if needed
4. Posts announcement
5. System handles notifications based on priority

## 7. Technical Implementation

### Backend Models
```python
# Enhanced UserPost model
class UserPost(models.Model):
    # ... existing fields ...
    
    # Callout fields
    callout_challenged_user = models.CharField(max_length=150, blank=True)
    callout_location = models.CharField(max_length=200, blank=True)
    callout_location_type = models.CharField(max_length=20, choices=[('street', 'Street'), ('dragstrip', 'Dragstrip')], blank=True)
    callout_race_type = models.CharField(max_length=100, blank=True)
    callout_wager_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    callout_scheduled_date = models.DateTimeField(null=True, blank=True)
    
    # Announcement fields
    is_pinned = models.BooleanField(default=False)
    announcement_type = models.CharField(max_length=20, choices=[...], blank=True)
    announcement_priority = models.CharField(max_length=20, choices=[...], default='medium')
```

### Frontend Components
- `CalloutCard`: Displays callout posts with action buttons
- `AnnouncementBanner`: Shows pinned announcements
- `EventCard`: Displays event information
- `CreateCalloutForm`: Form for creating new callouts
- `CalloutFeed`: Dedicated feed for callouts

## 8. Analytics and Insights

### Callout Metrics
- **Acceptance Rate**: Percentage of callouts accepted
- **Average Wager**: Mean wager amount
- **Popular Locations**: Most common race locations
- **Response Time**: Time between callout and response

### Event Metrics
- **Attendance**: Number of users attending events
- **Engagement**: Posts and interactions during events
- **Popularity**: Most viewed/engaged events

## 9. Future Enhancements

### Advanced Features
- **Live Betting**: Real-time wager system
- **Video Challenges**: Video callouts with car footage
- **Tournament System**: Organized racing tournaments
- **Achievement System**: Badges for race wins/losses
- **Reputation System**: User ratings and credibility

### Integration Features
- **Calendar Integration**: Add events to user calendars
- **Location Services**: GPS-based event discovery
- **Weather Integration**: Weather alerts for outdoor events
- **Social Sharing**: Share callouts on external platforms

## 10. Success Metrics

### User Engagement
- **Callout Creation Rate**: Number of callouts created per day
- **Response Rate**: Percentage of callouts that get responses
- **Event Attendance**: Number of users attending events
- **Feed Activity**: Posts and interactions in social feed

### Platform Growth
- **User Retention**: Users returning after callouts/events
- **Community Growth**: New users joining through events
- **Content Generation**: User-generated posts and media
- **Monetization**: Revenue from premium features and events

This comprehensive plan ensures that callouts and events are seamlessly integrated throughout the platform, providing users with multiple ways to discover, create, and participate in racing activities while maintaining a cohesive and engaging user experience. 