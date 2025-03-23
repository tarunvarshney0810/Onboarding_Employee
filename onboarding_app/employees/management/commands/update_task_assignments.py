from django.core.management.base import BaseCommand
from employees.models import Employee, OnboardingTask, TaskAssignment

class Command(BaseCommand):
    help = 'Updates task assignments based on current job types'

    def handle(self, *args, **options):
        # Get all employees
        employees = Employee.objects.all()
        tasks_updated = 0

        for employee in employees:
            if employee.job_type:
                # Delete old task assignments
                TaskAssignment.objects.filter(employee=employee).delete()
                
                # Get tasks for current job type
                tasks = OnboardingTask.objects.filter(job_types=employee.job_type)
                
                # Create new task assignments
                for task in tasks:
                    TaskAssignment.objects.create(
                        employee=employee,
                        task=task,
                        status='not_started'
                    )
                    tasks_updated += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {tasks_updated} task assignments')) 