from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser for Tarun Varshney'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Delete existing user if exists
        User.objects.filter(employee_id='e3017847').delete()
        
        # Create new superuser
        user = User.objects.create_superuser(
            username='e3017847',
            email='tarun.varshney@example.com',
            password='Leo@1grip',
            employee_id='e3017847',
            first_name='Tarun',
            last_name='Varshney',
            is_admin=True,
            is_enroller=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created superuser: {user.get_full_name()} ({user.employee_id})')
        ) 