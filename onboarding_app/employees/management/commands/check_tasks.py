from django.core.management.base import BaseCommand
from employees.models import OnboardingTask

class Command(BaseCommand):
    help = 'Check if there are any tasks in the database'

    def handle(self, *args, **options):
        tasks = OnboardingTask.objects.all()
        self.stdout.write(f'Total number of tasks: {tasks.count()}')
        
        if tasks.exists():
            self.stdout.write('\nTask List:')
            for task in tasks:
                self.stdout.write(f'- {task.title} (ID: {task.id}, Type: {task.get_task_type_display()})')
        else:
            self.stdout.write(self.style.WARNING('No tasks found in the database.')) 