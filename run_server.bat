@echo off
REM Setup and Run Django E-Commerce Backend

echo.
echo ========================================
echo E-Commerce Django Setup Script
echo ========================================
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo Installing dependencies...
pip install -r requirepip install -r requirements.txtments.txt

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Create superuser
echo.
echo Would you like to create a superuser for the admin panel? (Y/N)
set /p create_user="Enter your choice: "
if /i "%create_user%"=="Y" (
    python manage.py createsuperuser
)

REM Run server
echo.
echo ========================================
echo Starting Django server...
echo ========================================
echo Server will be available at: http://localhost:8000
echo Admin panel at: http://localhost:8000/admin/
echo.
python manage.py runserver

pause
