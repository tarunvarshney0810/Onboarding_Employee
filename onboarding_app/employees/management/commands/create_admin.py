from django.core.management.base import BaseCommand
from employees.models import Employee

class Command(BaseCommand):
    help = 'Creates a superuser with the specified employee_id'

    def add_arguments(self, parser):
        parser.add_argument('--employee_id', type=str, help='Employee ID for the superuser')
        parser.add_argument('--email', type=str, help='Email for the superuser')
        parser.add_argument('--password', type=str, help='Password for the superuser')

    def handle(self, *args, **options):
        try:
            # Get values from arguments or use defaults
            employee_id = options.get('employee_id') or 'ADMIN003'
            email = options.get('email') or 'admin@example.com'
            password = options.get('password') or 'Leo@1grip'

            # Create superuser with employee_id as username
            superuser = Employee.objects.create_superuser(
                employee_id=employee_id,
                username=employee_id,  # Using employee_id as username
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser created successfully with employee_id: {employee_id}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e)}')) 