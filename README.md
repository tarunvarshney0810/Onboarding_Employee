# Employee Onboarding Application

A lightweight Employee Onboarding Web Application built with Django, Python, and SQLite. This application helps streamline the employee onboarding process by managing tasks and tracking progress.

## Technology Stack

- **Backend**: Django 5.1.7 (Python Web Framework)
- **Database**: SQLite3
- **Frontend**: Bootstrap 5, Custom CSS, JavaScript
- **Authentication**: Django's built-in authentication system
- **Web Server**: Gunicorn (Production)
- **Reverse Proxy**: Nginx (Production)

## Project Structure

```
onboarding_app/
├── employees/                 # Main application directory
│   ├── management/           # Custom management commands
│   │   └── commands/        # Custom Django management commands
│   │       ├── create_sample_data.py    # Creates initial sample data
│   │       └── update_task_assignments.py # Updates task assignments
│   ├── migrations/          # Database migrations
│   ├── static/             # Static files (CSS, JS)
│   │   ├── css/           # Stylesheets
│   │   └── js/            # JavaScript files
│   ├── templates/          # HTML templates
│   │   ├── employees/     # Employee-related templates
│   │   │   ├── admin/    # Admin panel templates
│   │   │   └── dashboard/ # Dashboard templates
│   │   └── registration/  # Authentication templates
│   ├── models.py           # Database models
│   ├── views.py            # View controllers
│   ├── forms.py            # Form definitions
│   ├── urls.py             # URL routing
│   └── admin.py            # Admin interface configuration
├── onboarding_project/     # Project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
└── run.sh                 # Linux deployment script
```

## Key Features

1. Employee Dashboard with task tracking
2. Admin Panel for task management
3. Progress tracking with status updates
4. Job type-based task assignment
5. Custom task types (Email, Link, Instructions)
6. ServiceNow integration
7. Email task automation
8. Role-based access control

## Installation Steps

### Windows Setup

1. Install Python 3.11 or higher from python.org
2. Open Command Prompt and navigate to your project directory:
```bash
cd path/to/project
```

3. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

4. Install required packages:
```bash
pip install -r requirements.txt
```

5. Navigate to the application directory:
```bash
cd onboarding_app
```

6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

8. Load sample data (optional):
```bash
python manage.py create_sample_data
```

9. Start the development server:
```bash
python manage.py runserver
```

### Linux Setup

1. Install Python 3.11 and pip:
```bash
sudo apt update
sudo apt install python3.11 python3-pip python3.11-venv
```

2. Navigate to project directory:
```bash
cd path/to/project
```

3. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install required packages:
```bash
pip install -r requirements.txt
```

5. Navigate to application directory:
```bash
cd onboarding_app
```

6. Make the run script executable:
```bash
chmod +x run.sh
```

7. Run migrations:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

8. Create a superuser:
```bash
python3 manage.py createsuperuser
```
Follow the prompts to create your admin account.

9. Load sample data (optional):
```bash
python3 manage.py create_sample_data
```

10. Start the development server:
```bash
./run.sh
```

## Production Deployment

### Windows with IIS

1. Install IIS and URL Rewrite Module
2. Install Python 3.11 and create virtual environment
3. Install wfastcgi:
```bash
pip install wfastcgi
wfastcgi-enable
```

4. Configure IIS:
   - Create a new website
   - Set physical path to your project
   - Add web.config file
   - Configure application pool

5. Create web.config:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <handlers>
            <add name="Python FastCGI" path="*" verb="*" modules="FastCgiModule" scriptProcessor="C:\path\to\venv\Scripts\python.exe|C:\path\to\venv\Lib\site-packages\wfastcgi.py" resourceType="Unspecified" requireAccess="Script" />
        </handlers>
        <rewrite>
            <rules>
                <rule name="Static Files" stopProcessing="true">
                    <match url="^static/.*" ignoreCase="true" />
                    <action type="Rewrite" url="static/{R:0}" />
                </rule>
                <rule name="Configure Python" stopProcessing="true">
                    <match url="(.*)" ignoreCase="false" />
                    <conditions>
                        <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
                        <add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" />
                    </conditions>
                    <action type="Rewrite" url="wsgi.py/{R:1}" />
                </rule>
            </rules>
        </rewrite>
    </system.webServer>
</configuration>
```

### Linux with Nginx and Gunicorn

1. Install Nginx and Gunicorn:
```bash
sudo apt install nginx
pip install gunicorn
```

2. Create systemd service file:
```bash
sudo nano /etc/systemd/system/onboarding.service
```

3. Add the following content:
```ini
[Unit]
Description=Gunicorn daemon for Employee Onboarding
After=network.target

[Service]
User=your_username
Group=your_username
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind unix:onboarding.sock onboarding_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

4. Configure Nginx:
```bash
sudo nano /etc/nginx/sites-available/onboarding
```

5. Add the following configuration:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/project;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/project/onboarding.sock;
    }
}
```

6. Enable the site and start services:
```bash
sudo ln -s /etc/nginx/sites-available/onboarding /etc/nginx/sites-enabled
sudo systemctl start onboarding
sudo systemctl enable onboarding
sudo systemctl restart nginx
```

## File Descriptions

### Core Application Files

- `models.py`: Defines database models for Employee, JobType, OnboardingTask, and TaskAssignment
- `views.py`: Contains view logic for dashboard, admin panel, and task management
- `forms.py`: Defines forms for user input and data validation
- `urls.py`: URL routing configuration
- `admin.py`: Admin interface customization

### Templates

- `base.html`: Base template with common layout and navigation
- `dashboard.html`: Employee dashboard showing assigned tasks
- `admin/`: Admin panel templates for managing users and tasks
- `registration/`: Authentication templates for login and password management

### Static Files

- `css/`: Stylesheets for application styling
- `js/`: JavaScript files for dynamic functionality
- `task_type_handler.js`: Handles dynamic form fields based on task type

### Management Commands

- `create_sample_data.py`: Creates initial sample data for testing
- `update_task_assignments.py`: Updates task assignments based on job type changes

### Configuration Files

- `settings.py`: Project settings and configuration
- `requirements.txt`: Python package dependencies
- `run.sh`: Linux deployment script

## Access the Application

- Main dashboard: http://localhost:8000/dashboard/
- Admin panel: http://localhost:8000/admin-panel/
- Admin interface: http://localhost:8000/admin/

## Security Considerations

1. Always use HTTPS in production
2. Keep Django and all dependencies updated
3. Use strong passwords for superuser accounts
4. Regularly backup the database
5. Monitor server logs for security issues

## Troubleshooting

1. Database Issues:
   - Run `python manage.py migrate` to apply pending migrations
   - Check database permissions
   - Verify database connection settings

2. Static Files:
   - Run `python manage.py collectstatic`
   - Check static files configuration in settings.py
   - Verify Nginx/Apache static files configuration

3. Permission Issues:
   - Check file permissions on Linux
   - Verify IIS application pool identity on Windows
   - Ensure proper user permissions for database access

## Support

For issues or questions:
1. Check the documentation
2. Review the logs in `/var/log/`
3. Contact system administrator
4. Submit an issue on the project repository

# Employee Onboarding Portal

A comprehensive web application for managing employee onboarding processes, built with Django and Bootstrap.

## Features

- User Authentication and Authorization
  - Role-based access control (Admin, Enroller, Employee)
  - Secure login/logout functionality
  - Password reset capability
  - Default superuser account for initial setup

- Task Management
  - Create and manage onboarding tasks
  - Set task order and dependencies
  - Track task completion status
  - Support for different task types (Email, Link, Instructions)
  - Task notes and comments

- Employee Management
  - Employee profile creation and management
  - Document upload and management
  - Progress tracking
  - Task assignment and completion tracking

- Document Management
  - Secure document upload and storage
  - Document type categorization
  - Document status tracking
  - Document verification workflow

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd EmployeeOnboardingPortal
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   - Create a `.env` file in the project root
   - Add the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

5. Apply database migrations:
```bash
python manage.py migrate
```

## Default Superuser Account

The application comes with a default superuser account that will be created automatically during the first migration:

- Username: e3017847
- Password: Leo@1grip
- Employee ID: e3017847
- Name: Tarun Varshney
- Email: tarun.varshney@example.com

**Important Security Note**: It is strongly recommended to change the default superuser password after the first login.

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Access the application at http://127.0.0.1:8000/

## Deployment

For production deployment:

1. Set up a production-grade database (e.g., PostgreSQL)
2. Configure proper security settings in settings.py
3. Set up a production-grade web server (e.g., Nginx)
4. Configure static files serving
5. Set up proper logging
6. Use environment variables for sensitive data
7. Enable HTTPS
8. Change the default superuser password

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

