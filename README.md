# CalloutRacing - Drag Racing Social Network

A modern web application built with Django backend and React frontend for drag racing enthusiasts to challenge each other, join events, and trade parts.

## 🚀 Project Overview

CalloutRacing is a comprehensive drag racing social network that connects racers through challenges, events, and marketplace transactions. The platform combines the power of Django's robust backend framework with React's dynamic frontend capabilities.

## 📁 Project Structure

```
CalloutRacing/
├── backend/                 # Django backend application
│   ├── manage.py
│   ├── requirements.txt
│   ├── calloutracing/       # Django project settings
│   ├── api/                 # Django REST API
│   ├── core/                # Core Django apps & models
│   └── static/              # Static files
├── frontend/                # React frontend application
│   ├── package.json
│   ├── public/
│   ├── src/
│   └── README.md
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
└── README.md               # This file
```

## 🛠️ Technology Stack

### Backend (Django)
- **Django 4.2.10** - Web framework
- **Django REST Framework 3.14.0** - API framework
- **PostgreSQL** - Database (production)
- **SQLite** - Database (development)
- **Django CORS Headers** - Cross-origin resource sharing
- **Django Environment Variables** - Environment management
- **Django Filter** - Advanced filtering
- **DRF Simple JWT** - JWT authentication
- **Celery & Redis** - Background tasks
- **Gunicorn** - Production WSGI server
- **Whitenoise** - Static file serving

### Frontend (React)
- **React 18.2.0** - UI library
- **TypeScript 4.9.3** - Type safety
- **Vite 4.1.0** - Build tool and dev server
- **React Router 6.8.1** - Client-side routing
- **Axios 1.3.4** - HTTP client
- **Tailwind CSS 3.2.7** - Styling framework
- **React Query 4.29.5** - Data fetching
- **React Hook Form 7.43.5** - Form handling
- **Zustand 4.3.6** - State management
- **Heroicons 2.0.16** - Icon library

## ✅ Currently Implemented Features

### Backend (Django)
- **Authentication System**
  - User registration and login
  - JWT token-based authentication
  - Password reset functionality
  - Email verification (configured)

- **User Profiles**
  - Extended user profiles with racing stats
  - Car profiles with detailed specifications
  - Car modifications tracking
  - Profile pictures and cover photos
  - Win/loss statistics

- **Core Models**
  - User profiles with racing statistics
  - Track management (drag strips, road courses, ovals)
  - Event system (races, meets, shows, test & tune)
  - Callout system (race challenges)
  - Race results tracking
  - Marketplace for buying/selling
  - Friendship system
  - Direct messaging
  - User posts and comments
  - Car profiles with modifications

- **API Endpoints**
  - Complete REST API for all models
  - Advanced filtering and search
  - Pagination support
  - Custom actions (accept/decline callouts, join events, etc.)
  - File upload support for images

- **Deployment Ready**
  - Railway deployment configuration
  - Production settings
  - Static file serving
  - CORS configuration
  - Environment variable management

### Frontend (React)
- **Authentication**
  - Login and signup forms
  - Protected routes
  - Token management
  - Automatic logout on token expiry

- **User Interface**
  - Modern, responsive design
  - Red, white, and yellow racing theme
  - Mobile-friendly layout
  - Loading states and error handling

- **Pages Implemented**
  - Landing page (About)
  - Login/Signup forms
  - Contact form
  - Dashboard (Home)
  - User profiles
  - Callouts listing (static data)
  - Events listing (static data)
  - Marketplace listing (static data)
  - Create forms for callouts, events, marketplace

- **Features**
  - Real-time data fetching with React Query
  - Form validation with React Hook Form
  - Responsive navigation
  - Toast notifications
  - Image upload support

## 🚧 Current Status & What Needs Work

### Backend - ✅ Mostly Complete
- **Models**: All core models implemented
- **API**: Complete REST API with all endpoints
- **Authentication**: Fully functional
- **Deployment**: Railway deployment configured

### Frontend - 🚧 Partially Complete
- **Static Data**: Many pages still use hardcoded data instead of API calls
- **API Integration**: Need to connect frontend components to backend API
- **Real-time Features**: No real-time updates implemented
- **Image Upload**: Frontend forms need file upload integration

### Missing Features
1. **Real-time Updates**
   - WebSocket integration for live callout updates
   - Real-time messaging
   - Live event notifications

2. **Advanced Search & Filtering**
   - Frontend search functionality
   - Advanced filters for marketplace
   - Location-based search

3. **Payment Integration**
   - Stripe/PayPal integration for wagers
   - Event entry fee payments
   - Marketplace transactions

4. **Social Features**
   - User following system
   - Activity feed
   - Notifications system
   - Social sharing

5. **Mobile App**
   - React Native mobile app
   - Push notifications
   - GPS tracking for street races

6. **Advanced Racing Features**
   - Race timing integration
   - Performance tracking
   - Leaderboards
   - Season championships

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- PostgreSQL (optional, SQLite for development)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Django development server:**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your API configuration
   ```

4. **Start React development server:**
   ```bash
   npm run dev
   ```

## 🌐 Development Servers

- **Django Backend:** http://localhost:8000
- **Django Admin:** http://localhost:8000/admin
- **React Frontend:** http://localhost:5173
- **API Documentation:** http://localhost:8000/api/docs/

## 📚 API Documentation

The API documentation is available at `/api/docs/` when the Django server is running. This provides interactive documentation for all available endpoints.

## 🔧 Development Workflow

### Backend Development
1. Make changes to Django models, views, or serializers
2. Create and run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Test your changes with the Django development server
4. Write tests for new functionality

### Frontend Development
1. Make changes to React components or pages
2. The development server will hot-reload automatically
3. Test your changes in the browser
4. Write tests for new components

### Database Management
- **Create migrations:** `python manage.py makemigrations`
- **Apply migrations:** `python manage.py migrate`
- **Reset database:** `python manage.py flush`
- **Create fixtures:** `python manage.py dumpdata > fixtures/data.json`

## 🧪 Testing

### Backend Testing
```bash
cd backend
python manage.py test
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Backend Deployment
1. Set `DEBUG=False` in production settings
2. Configure your production database
3. Set up static file serving
4. Use a production WSGI server (Gunicorn recommended)

### Frontend Deployment
1. Build the production bundle: `npm run build`
2. Serve the `dist` folder with a web server
3. Configure environment variables for production

## 📝 Environment Variables

### Backend (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=CalloutRacing
```

## 🎯 Next Steps & Priority Tasks

### High Priority
1. **Connect Frontend to API**
   - Replace static data with API calls in Callouts, Events, Marketplace pages
   - Implement proper error handling and loading states
   - Add form submission to create pages

2. **Image Upload Integration**
   - Connect file upload forms to backend
   - Add image preview functionality
   - Implement drag-and-drop upload

3. **Real-time Features**
   - Add WebSocket support for live updates
   - Implement real-time messaging
   - Add push notifications

### Medium Priority
4. **Advanced Search**
   - Implement search functionality
   - Add filters for marketplace items
   - Location-based search for events

5. **Payment Integration**
   - Add Stripe integration for wagers
   - Implement event payment system
   - Add marketplace escrow system

6. **Social Features**
   - User following system
   - Activity feed
   - Social sharing buttons

### Low Priority
7. **Mobile App**
   - React Native development
   - Push notifications
   - GPS integration

8. **Advanced Racing Features**
   - Race timing system
   - Performance analytics
   - Championship system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Write tests for new functionality
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the documentation in the `docs/` folder
2. Search existing issues
3. Create a new issue with detailed information

## 🔄 Updates and Maintenance

- Keep dependencies updated regularly
- Monitor for security vulnerabilities
- Update documentation as features change
- Maintain test coverage above 80%

---

**Happy Racing! 🏁**

**Latest Update**: Fixed Django import linter errors and JSX children structure issues for Railway deployment. 