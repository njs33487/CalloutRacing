# CalloutRacing - Django/React Project

A modern web application built with Django backend and React frontend for racing callouts and management.

## 🚀 Project Overview

This project combines the power of Django's robust backend framework with React's dynamic frontend capabilities to create a comprehensive racing callout system.

## 📁 Project Structure

```
CalloutRacing/
├── backend/                 # Django backend application
│   ├── manage.py
│   ├── requirements.txt
│   ├── calloutracing/       # Django project settings
│   ├── api/                 # Django REST API
│   ├── core/                # Core Django apps
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
- **Django 4.2+** - Web framework
- **Django REST Framework** - API framework
- **PostgreSQL** - Database (recommended)
- **Django CORS Headers** - Cross-origin resource sharing
- **Django Environment Variables** - Environment management

### Frontend (React)
- **React 18+** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Styling framework

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
   cp .env.example .env
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
   cp .env.example .env
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
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=CalloutRacing
```

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

**Happy Coding! 🏁** 