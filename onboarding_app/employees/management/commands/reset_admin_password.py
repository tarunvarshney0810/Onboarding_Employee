from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates or resets password for user ADMIN001'

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            # First try to find by username
            user = User.objects.get(username='ADMIN001')
            user.set_password('Leo@1grip')
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully reset password for user ADMIN001'))
        except User.DoesNotExist:
            try:
                # Check if employee_id exists
                user = User.objects.get(employee_id='ADMIN001')
                user.username = 'ADMIN001'
                user.set_password('Leo@1grip')
                user.email = 'admin001@example.com'
                user.first_name = 'Admin'
                user.last_name = 'User'
                user.is_admin = True
                user.is_enroller = True
                user.save()
                self.stdout.write(self.style.SUCCESS('Successfully updated existing user with employee_id ADMIN001'))
            except User.DoesNotExist:
                # Create new user if neither exists
                user = User.objects.create_user(
                    username='ADMIN001',
                    email='admin001@example.com',
                    password='Leo@1grip',
                    employee_id='ADMIN001',
                    first_name='Admin',
                    last_name='User',
                    is_admin=True,
                    is_enroller=True
                )
                self.stdout.write(self.style.SUCCESS('Successfully created user ADMIN001 with password Leo@1grip')) 