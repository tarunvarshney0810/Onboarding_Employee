
from django.core.management.base import BaseCommand
from employees.models import OnboardingTask, JobType, Employee, TaskAssignment
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Load sample cards for demonstration'

    def handle(self, *args, **kwargs):
        # Create job types
        developer = JobType.objects.get_or_create(
            name="Software Developer",
            description="Responsible for software development"
        )[0]

        # Create some tasks
        task1 = OnboardingTask.objects.get_or_create(
            title="Complete IT Setup",
            description="Set up your development environment, email, and access credentials",
            task_type="instructions"
        )[0]
        task1.job_types.add(developer)

        task2 = OnboardingTask.objects.get_or_create(
            title="Review Company Policies",
            description="Read and acknowledge company policies and guidelines",
            task_type="link",
            external_link="https://company-policies.example.com"
        )[0]
        task2.job_types.add(developer)

        task3 = OnboardingTask.objects.get_or_create(
            title="Team Introduction",
            description="Schedule a meet and greet with your team members",
            task_type="email"
        )[0]
        task3.job_types.add(developer)

        # Create a demo employee if not exists
        demo_employee = Employee.objects.get_or_create(
            username="demo_dev",
            defaults={
                'password': make_password('demo123'),
                'employee_id': 'EMP001',
                'first_name': 'Demo',
                'last_name': 'Developer',
                'email': 'demo@example.com',
                'job_type': developer,
                'is_active': True
            }
        )[0]

        # Create task assignments
        TaskAssignment.objects.get_or_create(
            employee=demo_employee,
            task=task1,
            defaults={'status': 'in_progress'}
        )

        TaskAssignment.objects.get_or_create(
            employee=demo_employee,
            task=task2,
            defaults={'status': 'not_started'}
        )

        TaskAssignment.objects.get_or_create(
            employee=demo_employee,
            task=task3,
            defaults={'status': 'completed'}
        )

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample cards'))
