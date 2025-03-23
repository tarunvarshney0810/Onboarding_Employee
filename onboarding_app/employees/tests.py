from django.test import TestCase
from django.urls import reverse
from .models import Employee, JobType, OnboardingTask, TaskAssignment

class EmployeeModelTest(TestCase):
    def setUp(self):
        self.job_type = JobType.objects.create(name='Developer', description='Software Developer')
        self.employee = Employee.objects.create_user(
            employee_id='EMP001',
            username='EMP001',
            password='EMP001',
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            manager_name='Jane Manager',
            job_type=self.job_type
        )

    def test_employee_creation(self):
        self.assertEqual(self.employee.employee_id, 'EMP001')
        self.assertEqual(self.employee.username, 'EMP001')
        self.assertEqual(self.employee.first_name, 'John')
        self.assertEqual(self.employee.last_name, 'Doe')
        self.assertEqual(self.employee.email, 'john@example.com')
        self.assertEqual(self.employee.manager_name, 'Jane Manager')
        self.assertEqual(self.employee.job_type, self.job_type)
        self.assertFalse(self.employee.is_admin)
        self.assertFalse(self.employee.is_enroller)

class OnboardingTaskTest(TestCase):
    def setUp(self):
        self.job_type = JobType.objects.create(name='Developer', description='Software Developer')
        self.task = OnboardingTask.objects.create(
            title='Complete IT Form',
            description='Fill out the IT access form',
            task_type='link',
            external_link='https://example.com/form'
        )
        self.task.job_types.add(self.job_type)

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Complete IT Form')
        self.assertEqual(self.task.description, 'Fill out the IT access form')
        self.assertEqual(self.task.task_type, 'link')
        self.assertEqual(self.task.external_link, 'https://example.com/form')
        self.assertEqual(self.task.job_types.count(), 1)
        self.assertEqual(self.task.job_types.first(), self.job_type)

class TaskAssignmentTest(TestCase):
    def setUp(self):
        self.job_type = JobType.objects.create(name='Developer', description='Software Developer')
        self.employee = Employee.objects.create_user(
            employee_id='EMP001',
            username='EMP001',
            password='EMP001',
            job_type=self.job_type
        )
        self.task = OnboardingTask.objects.create(
            title='Complete IT Form',
            description='Fill out the IT access form',
            task_type='link'
        )
        self.assignment = TaskAssignment.objects.create(
            employee=self.employee,
            task=self.task,
            status='not_started'
        )

    def test_assignment_creation(self):
        self.assertEqual(self.assignment.employee, self.employee)
        self.assertEqual(self.assignment.task, self.task)
        self.assertEqual(self.assignment.status, 'not_started')
        self.assertEqual(self.assignment.get_status_color(), 'danger')
        
        # Test status color changes
        self.assignment.status = 'in_progress'
        self.assignment.save()
        self.assertEqual(self.assignment.get_status_color(), 'warning')
        
        self.assignment.status = 'completed'
        self.assignment.save()
        self.assertEqual(self.assignment.get_status_color(), 'success')
