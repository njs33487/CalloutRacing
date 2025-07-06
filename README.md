# 🏁 CalloutRacing - Advanced Racing Community Platform

A comprehensive racing community platform that connects racers, tracks, events, and enthusiasts through callouts, marketplace, and social features.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Installation](#️-installation)
- [⚙️ Configuration](#️-configuration)
- [🚀 Deployment](#-deployment)
- [📚 API Documentation](#-api-documentation)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [🐛 Troubleshooting](#-troubleshooting)

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **PostgreSQL** (recommended) or SQLite
- **Git**

### One-Command Setup (Development)

```bash
# Clone the repository
git clone https://github.com/njs33487/CalloutRacing.git
cd CalloutRacing

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
python manage.py migrate
python manage.py runserver

# Frontend setup (new terminal)
cd ../frontend
npm install
cp env.example .env
npm run dev
```

**Visit:** http://localhost:5173 (Frontend) | http://localhost:8000 (Backend)

## ✨ Features

### 🏎️ Core Racing Features
- **Race Callouts** - Challenge other racers to head-to-head competitions
- **Event Management** - Create and join racing events, car meets, and shows
- **Track Directory** - Discover and review racing tracks and locations
- **Performance Tracking** - Log and share car performance data and build logs

### 👥 Social & Community
- **User Profiles** - Detailed racer profiles with stats and car information
- **Friends System** - Connect with other racers and build your network
- **Messaging** - Direct communication between users
- **Posts & Content** - Share updates, builds, and racing content
- **Racing Crews** - Join or create racing crews and car clubs

### 🛒 Marketplace & Commerce
- **Parts Marketplace** - Buy and sell car parts, wheels, and accessories
- **Car Sales** - List and browse cars for sale
- **Reviews & Ratings** - Build trust through verified purchase reviews
- **Payment Integration** - Secure payment processing and wallet system

### 🔥 Advanced Features
- **Location Broadcasting** - "I'm Here, Who's There?" real-time location sharing
- **Hot Spots** - Discover popular racing locations and meet points
- **Open Challenges** - Public challenges for any racer to respond to

- **Build Logs** - Document and share car build progress
- **Performance Data** - Track and verify quarter-mile times, dyno results

### 🔐 Authentication & Security
- **Email Verification** - Secure account creation with email verification
- **SSO Integration** - Google and Facebook single sign-on
- **Reputation System** - Rate other racers for sportsmanship and reliability

## 🏗️ Architecture

### Backend (Django REST Framework)
```
backend/
├── api/                    # API endpoints and views
│   ├── views/             # Modular API views
│   ├── serializers.py     # DRF serializers
│   └── urls.py           # API routing
├── core/                  # Core application logic
│   ├── models/           # Database models
│   ├── email_service.py  # Email functionality
│   └── admin.py         # Django admin
├── templates/            # Email templates
└── manage.py
```

### Frontend (React + TypeScript)
```
frontend/
├── src/
│   ├── components/       # Reusable components
│   ├── pages/           # Page components
│   ├── services/        # API services
│   ├── contexts/        # React contexts
│   └── types/          # TypeScript definitions
├── public/             # Static assets
└── package.json
```

## 🛠️ Installation

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

4. **Configure environment:**
```bash
cp env.example .env
# Edit .env with your settings
```

5. **Setup database:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Run development server:**
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

3. **Configure environment:**
```bash
cp env.example .env
# Set VITE_API_URL=http://localhost:8000/api
```

4. **Run development server:**
```bash
npm run dev
```

## ⚙️ Configuration

### Environment Variables

#### Backend Configuration (.env)
```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:pass@localhost/calloutracing

# Email Configuration (Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@calloutracing.com

# Frontend URL
FRONTEND_URL=http://localhost:5173

# SSO Configuration
GOOGLE_CLIENT_ID=your-google-client-id
FACEBOOK_APP_ID=your-facebook-app-id
```

#### Frontend Configuration (.env)
```bash
# API Configuration
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=CalloutRacing

# Development Settings
VITE_DEV_MODE=true
```

### Email Setup (Gmail)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password:**
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Select "Mail" and generate password
3. **Use the 16-character password** as `EMAIL_HOST_PASSWORD`

## 🚀 Deployment

### Railway Deployment (Recommended)

1. **Connect to Railway:**
   - Fork this repository
   - Connect your fork to Railway
   - Railway will auto-deploy on push

2. **Configure Environment Variables:**
   - Add all required environment variables in Railway dashboard
   - Set `DEBUG=False` for production

3. **Database Setup:**
   - Railway will automatically provision PostgreSQL
   - Migrations run automatically on deployment

### Manual Deployment

1. **Build frontend:**
```bash
cd frontend
npm run build
```

2. **Collect static files:**
```bash
cd backend
python manage.py collectstatic --noinput
```

3. **Set production settings:**
```bash
DEBUG=False
ALLOWED_HOSTS=your-domain.com
```

## 📚 API Documentation

### Authentication Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/` | User registration |
| `POST` | `/api/auth/login/` | User login |
| `POST` | `/api/auth/logout/` | User logout |
| `GET` | `/api/auth/verify-email/<token>/` | Email verification |
| `POST` | `/api/auth/resend-verification/` | Resend verification |

### Racing Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/tracks/` | List racing tracks |
| `GET` | `/api/events/` | List racing events |
| `POST` | `/api/events/` | Create new event |
| `GET` | `/api/callouts/` | List race callouts |
| `POST` | `/api/callouts/` | Create new callout |

### Marketplace Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/marketplace/` | List marketplace items |
| `POST` | `/api/marketplace/` | Create new listing |
| `GET` | `/api/marketplace/orders/` | List orders |

### Social Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/friends/` | List friends |
| `POST` | `/api/friends/send-request/` | Send friend request |
| `GET` | `/api/messages/` | List messages |
| `GET` | `/api/posts/` | List posts |

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

### API Testing
```bash
# Using curl
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch:**
```bash
git checkout -b feature/amazing-feature
```

3. **Make your changes** following our coding standards
4. **Add tests** for new functionality
5. **Commit your changes:**
```bash
git commit -m 'Add amazing feature'
```

6. **Push to your branch:**
```bash
git push origin feature/amazing-feature
```

7. **Submit a pull request**

### Coding Standards

#### Backend (Python/Django)
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all functions
- Keep functions under 50 lines
- Use meaningful variable names

#### Frontend (TypeScript/React)
- Use TypeScript for all new code
- Follow React best practices
- Use functional components with hooks
- Implement proper error handling
- Write unit tests for components

## 🐛 Troubleshooting

### Common Issues

#### Email Not Sending
```bash
# Check Gmail app password
# Verify SMTP settings in .env
# Check Railway logs for errors
```

#### Database Migration Issues
```bash
# Reset migrations
python manage.py makemigrations --empty core
python manage.py migrate

# Or recreate database
python manage.py flush
```

#### Frontend Build Errors
```bash
# Clear dependencies
rm -rf node_modules package-lock.json
npm install

# Check TypeScript errors
npm run type-check
```

#### SSO Not Working
```bash
# Verify client IDs in environment variables
# Check CORS settings
# Ensure redirect URIs are correct
```

### Getting Help

1. **Check the logs** in Railway dashboard
2. **Review environment variables** configuration
3. **Ensure all dependencies** are installed correctly
4. **Check the documentation** in `/docs/` directory

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django REST Framework** for the robust API framework
- **React and TypeScript** for the modern frontend
- **Tailwind CSS** for the beautiful UI components
- **Heroicons** for the icon library
- **Railway** for seamless deployment
- All contributors and racing community members

---

## 🏁 Ready to Race?

**Live Demo:** [https://calloutracing.up.railway.app](https://calloutracing.up.railway.app)

**Support:** Create an issue on GitHub or contact us through the platform

**Latest Update:** Fixed database migration issues and email configuration for production deployment.

**Happy Racing! 🏁**

**Latest Update**: Fixed Django import linter errors and JSX children structure issues for Railway deployment.
