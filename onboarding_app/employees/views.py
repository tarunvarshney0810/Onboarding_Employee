from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from .forms import (
    EmployeeLoginForm, EmployeeRegistrationForm, OnboardingTaskForm,
    TaskAssignmentUpdateForm, JobTypeForm, UserManagementForm
)
from .models import Employee, OnboardingTask, TaskAssignment, JobType

def is_admin(user):
    """Check if user has admin privileges"""
    return user.is_admin

def is_enroller(user):
    """Check if user has enroller privileges"""
    return user.is_enroller or user.is_admin

def login_view(request):
    """Custom login view for employee authentication"""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = EmployeeLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.get_full_name() or user.username}!")
                
                # Handle next parameter
                next_url = request.GET.get('next')
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid Employee ID or password.")
    else:
        form = EmployeeLoginForm()
    
    return render(request, 'employees/login.html', {'form': form})

@login_required
def dashboard(request):
    """Employee dashboard showing task cards"""
    tasks = TaskAssignment.objects.filter(employee=request.user).select_related('task')
    
    # Group tasks by status for better organization
    not_started_tasks = tasks.filter(status='not_started')
    in_progress_tasks = tasks.filter(status='in_progress')
    completed_tasks = tasks.filter(status='completed')
    
    context = {
        'not_started_tasks': not_started_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'is_admin': request.user.is_admin,
        'is_enroller': request.user.is_enroller,
    }
    
    return render(request, 'employees/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    """Admin panel for managing onboarding tasks and job types"""
    tasks = OnboardingTask.objects.all().prefetch_related('job_types')
    job_types = JobType.objects.all()
    
    context = {
        'tasks': tasks,
        'job_types': job_types,
    }
    
    return render(request, 'employees/admin_panel.html', context)

@login_required
@user_passes_test(is_enroller)
def enroll_employee(request):
    """View for enrolling new employees"""
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create new employee
                employee = form.save()
                employee_id = form.cleaned_data.get('employee_id')
                
                # Get job type and assign relevant tasks
                job_type = form.cleaned_data.get('job_type')
                if job_type:
                    # Find all tasks for this job type
                    tasks = OnboardingTask.objects.filter(job_types=job_type)
                    
                    # Create task assignments for the new employee
                    for task in tasks:
                        TaskAssignment.objects.create(
                            employee=employee,
                            task=task,
                            status='not_started'
                        )
                
                messages.success(request, f'Employee {employee_id} has been successfully enrolled and assigned tasks!')
                return redirect('enroll')
    else:
        form = EmployeeRegistrationForm()
    
    return render(request, 'employees/enroll.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def task_create(request):
    """View for creating a new onboarding task"""
    if request.method == 'POST':
        form = OnboardingTaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            
            # Get selected job types or assign to all employees if none selected
            job_types = form.cleaned_data.get('job_types')
            if job_types:
                # Assign to employees with matching job types
                employees = Employee.objects.filter(job_type__in=job_types)
            else:
                # Assign to all employees if no job types selected
                employees = Employee.objects.all()
            
            # Create task assignments for the employees
            for employee in employees:
                TaskAssignment.objects.create(
                    employee=employee,
                    task=task,
                    status='not_started'
                )
            
            messages.success(request, f'Task "{task.title}" has been created and assigned to relevant employees!')
            return redirect('admin_panel')
    else:
        form = OnboardingTaskForm()
    
    return render(request, 'employees/task_form.html', {'form': form, 'action': 'Create'})

@login_required
@user_passes_test(is_admin)
def task_edit(request, task_id):
    """View for editing an existing onboarding task"""
    task = get_object_or_404(OnboardingTask, id=task_id)
    
    if request.method == 'POST':
        form = OnboardingTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" has been updated!')
            return redirect('admin_panel')
    else:
        form = OnboardingTaskForm(instance=task)
    
    return render(request, 'employees/task_form.html', {'form': form, 'action': 'Edit', 'task': task})

@login_required
@user_passes_test(is_admin)
def task_delete(request, task_id):
    """View for deleting an onboarding task"""
    task = get_object_or_404(OnboardingTask, id=task_id)
    task_title = task.title
    
    # Delete all assignments related to this task
    TaskAssignment.objects.filter(task=task).delete()
    
    # Delete the task
    task.delete()
    
    messages.success(request, f'Task "{task_title}" has been deleted!')
    return redirect('admin_panel')

@login_required
def update_task_status(request, assignment_id):
    """View for updating the status of a task assignment"""
    assignment = get_object_or_404(TaskAssignment, id=assignment_id, employee=request.user)
    
    if request.method == 'POST':
        form = TaskAssignmentUpdateForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task status updated to {assignment.get_status_display()}!')
    
    return redirect('dashboard')

@login_required
@user_passes_test(is_admin)
def job_type_create(request):
    """View for creating a new job type"""
    if request.method == 'POST':
        form = JobTypeForm(request.POST)
        if form.is_valid():
            job_type = form.save()
            messages.success(request, f'Job type "{job_type.name}" has been created!')
            return redirect('admin_panel')
    else:
        form = JobTypeForm()
    
    return render(request, 'employees/task_form.html', {'form': form, 'action': 'Create Job Type'})

@login_required
@user_passes_test(is_admin)
def job_type_edit(request, job_type_id):
    """View for editing an existing job type"""
    job_type = get_object_or_404(JobType, id=job_type_id)
    
    if request.method == 'POST':
        form = JobTypeForm(request.POST, instance=job_type)
        if form.is_valid():
            form.save()
            messages.success(request, f'Job type "{job_type.name}" has been updated!')
            return redirect('admin_panel')
    else:
        form = JobTypeForm(instance=job_type)
    
    return render(request, 'employees/task_form.html', {'form': form, 'action': 'Edit Job Type', 'job_type': job_type})

@login_required
@user_passes_test(is_admin)
def job_type_delete(request, job_type_id):
    """View for deleting a job type"""
    job_type = get_object_or_404(JobType, id=job_type_id)
    job_type_name = job_type.name
    
    # Remove this job type from employees and set to null
    Employee.objects.filter(job_type=job_type).update(job_type=None)
    
    # Delete the job type
    job_type.delete()
    
    messages.success(request, f'Job type "{job_type_name}" has been deleted!')
    return redirect('admin_panel')

def logout_view(request):
    """Custom logout view with proper cleanup and redirection"""
    if request.user.is_authenticated:
        messages.info(request, "You have been successfully logged out.")
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard showing overview of all data"""
    context = {
        'total_users': Employee.objects.count(),
        'total_employees': Employee.objects.count(),
        'total_tasks': OnboardingTask.objects.count(),
        'total_job_types': JobType.objects.count(),
        'recent_employees': Employee.objects.order_by('-date_joined')[:5],
        'recent_tasks': OnboardingTask.objects.all()[:5],  # Removed created_at ordering
    }
    return render(request, 'employees/admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def user_management(request):
    """View for managing employees"""
    employees = Employee.objects.all().select_related('job_type').order_by('-date_joined')
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'employees/admin/user_management.html', context)

@login_required
@user_passes_test(is_admin)
def user_edit(request, user_id):
    """View for editing employee details"""
    employee = get_object_or_404(Employee, id=user_id)
    
    if request.method == 'POST':
        form = UserManagementForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f'Employee {employee.employee_id} has been updated!')
            return redirect('user_management')
    else:
        form = UserManagementForm(instance=employee)
    
    return render(request, 'employees/admin/user_form.html', {'form': form, 'employee': employee})

@login_required
@user_passes_test(is_admin)
def user_delete(request, user_id):
    """View for deleting an employee"""
    employee = get_object_or_404(Employee, id=user_id)
    username = employee.user.username
    
    if request.method == 'POST':
        employee.user.delete()  # This will also delete the employee due to CASCADE
        messages.success(request, f'Employee {username} has been deleted!')
        return redirect('user_management')
    
    return render(request, 'employees/admin/user_confirm_delete.html', {'employee': employee})

@login_required
@user_passes_test(is_admin)
def task_management(request):
    """View for managing all tasks"""
    tasks = OnboardingTask.objects.all().prefetch_related('job_types')
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'employees/admin/task_management.html', context)

@login_required
@user_passes_test(is_admin)
def task_assignment_management(request):
    """View for managing task assignments"""
    assignments = TaskAssignment.objects.all().select_related('employee', 'task')
    paginator = Paginator(assignments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'employees/admin/task_assignment_management.html', context)

@login_required
@user_passes_test(is_admin)
def task_assignment_edit(request, assignment_id):
    """View for editing task assignment details"""
    assignment = get_object_or_404(TaskAssignment, id=assignment_id)
    
    if request.method == 'POST':
        form = TaskAssignmentUpdateForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task assignment has been updated!')
            return redirect('task_assignment_management')
    else:
        form = TaskAssignmentUpdateForm(instance=assignment)
    
    return render(request, 'employees/admin/task_assignment_form.html', {'form': form, 'assignment': assignment})

@login_required
@user_passes_test(is_admin)
def task_assignment_delete(request, assignment_id):
    """View for deleting a task assignment"""
    assignment = get_object_or_404(TaskAssignment, id=assignment_id)
    
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, f'Task assignment has been deleted!')
        return redirect('task_assignment_management')
    
    return render(request, 'employees/admin/task_assignment_confirm_delete.html', {'assignment': assignment})
