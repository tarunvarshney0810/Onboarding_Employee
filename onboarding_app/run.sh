#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

# Create migrations for the application
echo "Creating migrations..."
python manage.py makemigrations

# Apply migrations to the database
echo "Applying migrations..."
python manage.py migrate

# Create a superuser for initial admin access if needed
if [ ! -f ".superuser_created" ]; then
    echo "Creating initial superuser..."
    
    # Use environment variables or default values
    ADMIN_USERNAME=${ADMIN_USERNAME:-admin}
    ADMIN_PASSWORD=${ADMIN_PASSWORD:-admin123}
    ADMIN_EMAIL=${ADMIN_EMAIL:-admin@example.com}
    
    # Create superuser using a Python script
    python -c "
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onboarding_project.settings')
django.setup()

from employees.models import Employee, JobType
from django.db import transaction

try:
    with transaction.atomic():
        # Create Developer job type if it doesn't exist
        dev_job, created = JobType.objects.get_or_create(
            name='Developer',
            defaults={'description': 'Software developer role'}
        )
        
        # Create Analyst job type if it doesn't exist
        analyst_job, created = JobType.objects.get_or_create(
            name='Analyst',
            defaults={'description': 'Business analyst role'}
        )
        
        # Create a superuser
        if not Employee.objects.filter(username='${ADMIN_USERNAME}').exists():
            superuser = Employee.objects.create_superuser(
                employee_id='ADMIN',
                username='${ADMIN_USERNAME}',
                password='${ADMIN_PASSWORD}',
                email='${ADMIN_EMAIL}',
                first_name='Admin',
                last_name='User',
                job_type=None,
                is_admin=True,
                is_enroller=True
            )
            print(f'Superuser {superuser.username} created successfully!')
except Exception as e:
    print(f'Error: {e}')
"
    
    # Mark that we've created a superuser
    touch .superuser_created
    echo "Superuser created successfully!"
fi

# Start the development server on 0.0.0.0:5000
echo "Starting server..."
python manage.py runserver 0.0.0.0:5000
