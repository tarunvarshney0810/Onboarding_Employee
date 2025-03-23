from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser with employee_id'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Create superuser with all required fields
        user = User.objects.create_superuser(
            username='tarun',
            email='tarun@example.com',
            password='Leo@1grip',
            employee_id='EMP001',  # You can change this ID as needed
            first_name='Tarun',
            last_name='Varshney'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created superuser: {user.username}')
        ) 