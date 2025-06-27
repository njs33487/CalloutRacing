@echo off
echo 🚀 Setting up CalloutRacing - Django/React Project
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Backend setup
echo.
echo 🔧 Setting up Django Backend...
cd backend

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create .env file
echo Creating environment file...
copy env.example .env

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo Creating superuser...
python manage.py createsuperuser --noinput --username admin --email admin@example.com

echo ✅ Backend setup complete!

REM Frontend setup
echo.
echo 🔧 Setting up React Frontend...
cd ..\frontend

REM Install dependencies
echo Installing Node.js dependencies...
npm install

REM Create .env file
echo Creating environment file...
copy env.example .env

echo ✅ Frontend setup complete!

echo.
echo 🎉 Setup complete! To start the application:
echo.
echo Backend (Django):
echo   cd backend
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Frontend (React):
echo   cd frontend
echo   npm run dev
echo.
echo 🌐 Access the application:
echo   Frontend: http://localhost:5173
echo   Backend API: http://localhost:8000/api
echo   Django Admin: http://localhost:8000/admin
echo.
echo 👤 Default admin credentials:
echo   Username: admin
echo   Email: admin@example.com
echo   Password: (you'll be prompted to set this)

pause 