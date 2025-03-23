from django.core.management.base import BaseCommand
from employees.models import Employee, OnboardingTask, TaskAssignment

class Command(BaseCommand):
    help = 'Assigns tasks to existing employees based on their job types'

    def handle(self, *args, **options):
        # Get all employees
        employees = Employee.objects.all()
        tasks_assigned = 0

        for employee in employees:
            if employee.job_type:
                # Get tasks for this job type
                tasks = OnboardingTask.objects.filter(job_types=employee.job_type)
                
                # Create task assignments for tasks that don't exist yet
                for task in tasks:
                    task_assignment, created = TaskAssignment.objects.get_or_create(
                        employee=employee,
                        task=task,
                        defaults={'status': 'not_started'}
                    )
                    if created:
                        tasks_assigned += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully assigned {tasks_assigned} new tasks to employees')) 