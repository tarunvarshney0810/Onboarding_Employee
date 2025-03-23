from django.core.management.base import BaseCommand
from employees.models import OnboardingTask

class Command(BaseCommand):
    help = 'Sets initial order for all tasks based on their creation date'

    def handle(self, *args, **kwargs):
        # Get all tasks ordered by creation date
        tasks = OnboardingTask.objects.all().order_by('created_at')
        
        # Update order for each task
        for index, task in enumerate(tasks, start=1):
            task.order = index
            task.save()
            self.stdout.write(
                self.style.SUCCESS(f'Set order {index} for task: {task.title}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated order for {len(tasks)} tasks')
        ) 