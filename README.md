# CalloutRacing - Advanced Racing Community Platform

A comprehensive racing community platform that connects racers, tracks, events, and enthusiasts through callouts, marketplace, and social features.

## 🏁 Features

### Core Racing Features
- **Race Callouts**: Challenge other racers to head-to-head competitions
- **Event Management**: Create and join racing events, car meets, and shows
- **Track Directory**: Discover and review racing tracks and locations
- **Performance Tracking**: Log and share car performance data and build logs

### Social & Community
- **User Profiles**: Detailed racer profiles with stats and car information
- **Friends System**: Connect with other racers and build your network
- **Messaging**: Direct communication between users
- **Posts & Content**: Share updates, builds, and racing content
- **Racing Crews**: Join or create racing crews and car clubs

### Marketplace & Commerce
- **Parts Marketplace**: Buy and sell car parts, wheels, and accessories
- **Car Sales**: List and browse cars for sale
- **Reviews & Ratings**: Build trust through verified purchase reviews
- **Payment Integration**: Secure payment processing and wallet system

### Advanced Features
- **Location Broadcasting**: "I'm Here, Who's There?" real-time location sharing
- **Hot Spots**: Discover popular racing locations and meet points
- **Open Challenges**: Public challenges for any racer to respond to
- **Betting System**: Place bets on races and events
- **Build Logs**: Document and share car build progress
- **Performance Data**: Track and verify quarter-mile times, dyno results

### Authentication & Security
- **Email Verification**: Secure account creation with email verification
- **SSO Integration**: Google and Facebook single sign-on
- **Reputation System**: Rate other racers for sportsmanship and reliability

## 🏗️ Project Structure

### Backend (Django)

```
backend/
├── api/
│   ├── views/                    # Modular API views
│   │   ├── auth.py              # Authentication & user management
│   │   ├── racing.py            # Events, tracks, callouts
│   │   ├── marketplace.py       # Marketplace functionality
│   │   ├── social.py            # Friends, messages, posts
│   │   ├── cars.py              # Car profiles & build logs
│   │   ├── payments.py          # Subscriptions & payments
│   │   ├── locations.py         # Hot spots & crews
│   │   └── utils.py             # Search, SSO, utilities
│   ├── serializers.py           # DRF serializers
│   └── urls.py                  # API routing
├── core/
│   ├── models/                  # Modular database models
│   │   ├── auth.py              # User & UserProfile
│   │   ├── racing.py            # Track, Event, Callout, RaceResult
│   │   ├── marketplace.py       # Marketplace, Orders, Reviews
│   │   ├── social.py            # Friendship, Message, Post
│   │   ├── cars.py              # CarProfile, BuildLog, Modifications
│   │   ├── payments.py          # Subscription, Payment, Wallet
│   │   └── locations.py         # HotSpot, RacingCrew, LocationBroadcast
│   ├── email_service.py         # Email verification & notifications
│   └── admin.py                 # Django admin configuration
├── templates/                   # Email templates
└── manage.py
```

### Frontend (React + TypeScript)

```
frontend/
├── src/
│   ├── components/
│   │   ├── search/              # Modular search components
│   │   │   ├── SearchFilters.tsx
│   │   │   ├── SearchResults.tsx
│   │   │   └── SearchTabs.tsx
│   │   ├── Layout.tsx           # Main app layout
│   │   ├── ProtectedRoute.tsx   # Authentication wrapper
│   │   ├── SSOButtons.tsx       # Social login buttons
│   │   └── GlobalSearchBar.tsx  # Global search component
│   ├── pages/                   # Page components
│   │   ├── auth/                # Authentication pages
│   │   ├── racing/              # Racing feature pages
│   │   ├── marketplace/         # Marketplace pages
│   │   └── social/              # Social feature pages
│   ├── services/
│   │   └── api.ts               # API service layer
│   ├── contexts/
│   │   └── AuthContext.tsx      # Authentication context
│   └── types/
│       └── index.ts             # TypeScript type definitions
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (recommended) or SQLite
- Redis (for caching and sessions)

### Backend Setup

1. **Clone and setup environment**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment variables**:
```bash
cp env.example .env
# Edit .env with your database, email, and SSO settings
```

3. **Database setup**:
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. **Run development server**:
```bash
python manage.py runserver
```

### Frontend Setup

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Configure environment**:
```bash
cp env.example .env
# Set your backend API URL
```

3. **Run development server**:
```bash
npm run dev
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/calloutracing

# Email (Gmail recommended)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# SSO
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret

# Security
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000/api
VITE_GOOGLE_CLIENT_ID=your-google-client-id
VITE_FACEBOOK_APP_ID=your-facebook-app-id
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/verify-email/<token>/` - Email verification
- `POST /api/auth/resend-verification/` - Resend verification email

### SSO Endpoints
- `POST /api/auth/google-sso/` - Google OAuth login
- `POST /api/auth/facebook-sso/` - Facebook OAuth login
- `GET /api/auth/sso-config/` - SSO configuration

### Racing Endpoints
- `GET /api/tracks/` - List racing tracks
- `GET /api/events/` - List racing events
- `POST /api/events/` - Create new event
- `GET /api/callouts/` - List race callouts
- `POST /api/callouts/` - Create new callout

### Marketplace Endpoints
- `GET /api/marketplace/` - List marketplace items
- `POST /api/marketplace/` - Create new listing
- `GET /api/marketplace/orders/` - List orders
- `POST /api/marketplace/orders/` - Create new order

### Social Endpoints
- `GET /api/friends/` - List friends
- `POST /api/friends/send-request/` - Send friend request
- `GET /api/messages/` - List messages
- `POST /api/messages/` - Send message
- `GET /api/posts/` - List posts
- `POST /api/posts/` - Create new post

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Railway Deployment (Recommended)
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push to main branch

### Manual Deployment
1. Build frontend: `npm run build`
2. Collect static files: `python manage.py collectstatic`
3. Set `DEBUG=False` in production
4. Configure production database and email settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes following the coding standards
4. Add tests for new functionality
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📝 Coding Standards

### Backend (Python/Django)
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions under 50 lines when possible
- Use meaningful variable and function names

### Frontend (TypeScript/React)
- Use TypeScript for all new code
- Follow React best practices and hooks
- Use functional components with hooks
- Implement proper error handling
- Write unit tests for components

### Database Models
- Use descriptive field names
- Add proper help_text for all fields
- Implement proper relationships
- Use appropriate field types and constraints

## 🐛 Troubleshooting

### Common Issues

1. **Email not sending**: Check Gmail app password and SMTP settings
2. **SSO not working**: Verify client IDs and secrets are correct
3. **Database migrations**: Run `python manage.py makemigrations` and `python manage.py migrate`
4. **Frontend build errors**: Clear node_modules and reinstall dependencies

### Support
- Check the documentation in `/docs/` directory
- Review environment variable configuration
- Ensure all dependencies are installed correctly

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django REST Framework for the robust API framework
- React and TypeScript for the modern frontend
- Tailwind CSS for the beautiful UI components
- Heroicons for the icon library
- All contributors and racing community members

---

**Happy Racing! 🏁**

**Latest Update**: Fixed Django import linter errors and JSX children structure issues for Railway deployment. #   U p d a t e d   0 6 / 2 7 / 2 0 2 5   2 2 : 4 9 : 2 1 
 
 