from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    """Custom user manager for Employee model"""
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('employee_id', 'ADMIN001')  # Default admin ID
        extra_fields.setdefault('job_type', None)  # Superuser doesn't need job type

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class JobType(models.Model):
    """Job type model for different roles in the company"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Employee(AbstractUser):
    """Custom user model for employee onboarding"""
    employee_id = models.CharField(max_length=50, unique=True)
    manager_name = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.ForeignKey(JobType, on_delete=models.SET_NULL, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_enroller = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.employee_id} - {self.get_full_name()}"

class OnboardingTask(models.Model):
    """Model for onboarding tasks"""
    TASK_TYPES = [
        ('email', 'Email'),
        ('link', 'External Link'),
        ('instructions', 'Instructions'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    job_types = models.ManyToManyField(JobType, blank=True)
    notes = models.TextField(blank=True, null=True, help_text="Additional notes or instructions for this task")
    order = models.PositiveIntegerField(default=0, help_text="Order in which this task should appear")
    
    # Email-specific fields
    email_to = models.EmailField(blank=True, null=True)
    email_subject = models.CharField(max_length=200, blank=True, null=True)
    email_body = models.TextField(blank=True, null=True)
    
    external_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_email_link(self):
        """Generate mailto link with subject and body"""
        if self.task_type == 'email' and self.email_to:
            subject = self.email_subject or ''
            body = self.email_body or ''
            return f"mailto:{self.email_to}?subject={subject}&body={body}"
        return None

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Onboarding Task'
        verbose_name_plural = 'Onboarding Tasks'

class TaskAssignment(models.Model):
    """Model for task assignments to employees"""
    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='task_assignments')
    task = models.ForeignKey(OnboardingTask, on_delete=models.CASCADE, related_name='assignments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('employee', 'task')
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.task.title}: {self.get_status_display()}"
    
    def get_status_color(self):
        """Returns the bootstrap color class based on status"""
        if self.status == 'not_started':
            return 'danger'
        elif self.status == 'in_progress':
            return 'warning'
        elif self.status == 'completed':
            return 'success'
        return 'secondary'

@receiver(post_save, sender=Employee)
def update_task_assignments(sender, instance, **kwargs):
    """Update task assignments when employee's job type changes"""
    if instance.job_type:
        # Delete old task assignments
        TaskAssignment.objects.filter(employee=instance).delete()
        
        # Get tasks for current job type
        tasks = OnboardingTask.objects.filter(job_types=instance.job_type)
        
        # Create new task assignments
        for task in tasks:
            TaskAssignment.objects.create(
                employee=instance,
                task=task,
                status='not_started'
            )
