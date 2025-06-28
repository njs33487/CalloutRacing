@echo off
echo === Running Django migrations on Railway ===

REM Change to backend directory
cd backend

REM Show current migration status
echo === Current migration status ===
python manage.py showmigrations

REM Run migrations
echo === Running migrations ===
python manage.py migrate --noinput --verbosity=2

REM Show final migration status
echo === Final migration status ===
python manage.py showmigrations

echo === Migrations completed ===
pause 