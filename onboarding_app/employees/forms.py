from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Employee, OnboardingTask, TaskAssignment, JobType

class EmployeeLoginForm(AuthenticationForm):
    """Custom login form for employees"""
    username = forms.CharField(
        label='Employee ID',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Employee ID'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

class EmployeeRegistrationForm(UserCreationForm):
    """Form for enrolling new employees"""
    employee_id = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee ID'})
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    manager_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manager Name'})
    )
    job_type = forms.ModelChoiceField(
        queryset=JobType.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Employee
        fields = ('employee_id', 'first_name', 'last_name', 'email', 'manager_name', 'job_type', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['employee_id']  # Set username to employee_id
        if commit:
            user.save()
        return user

class OnboardingTaskForm(forms.ModelForm):
    """Form for creating or updating onboarding tasks"""
    job_types = forms.ModelMultipleChoiceField(
        queryset=JobType.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = OnboardingTask
        fields = ('title', 'description', 'task_type', 'external_link', 'email_to', 'email_subject', 'email_body', 'job_types')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'task_type': forms.Select(attrs={'class': 'form-control'}),
            'external_link': forms.URLInput(attrs={'class': 'form-control'}),
            'email_to': forms.EmailInput(attrs={'class': 'form-control'}),
            'email_subject': forms.TextInput(attrs={'class': 'form-control'}),
            'email_body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['external_link'].widget.attrs['style'] = 'display: none;'
        self.fields['email_to'].widget.attrs['style'] = 'display: none;'
        self.fields['email_subject'].widget.attrs['style'] = 'display: none;'
        self.fields['email_body'].widget.attrs['style'] = 'display: none;'
        
        if self.instance.pk and self.instance.task_type == 'email':
            self.fields['email_to'].widget.attrs['style'] = 'display: block;'
            self.fields['email_subject'].widget.attrs['style'] = 'display: block;'
            self.fields['email_body'].widget.attrs['style'] = 'display: block;'
        elif self.instance.pk and self.instance.task_type == 'link':
            self.fields['external_link'].widget.attrs['style'] = 'display: block;'
    
    def clean(self):
        cleaned_data = super().clean()
        task_type = cleaned_data.get('task_type')
        
        if task_type == 'email':
            if not cleaned_data.get('email_to'):
                self.add_error('email_to', 'Email address is required for email tasks.')
            if not cleaned_data.get('email_subject'):
                self.add_error('email_subject', 'Subject is required for email tasks.')
            if not cleaned_data.get('email_body'):
                self.add_error('email_body', 'Body is required for email tasks.')
        elif task_type == 'link':
            if not cleaned_data.get('external_link'):
                self.add_error('external_link', 'External link is required for link tasks.')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.task_type == 'email':
            # Add automatic signature to email body
            signature = "\n\nBest regards,\n{employee_name}\n{employee_id}"
            instance.email_body = instance.email_body + signature
        return super().save(commit)

class TaskAssignmentUpdateForm(forms.ModelForm):
    """Form for updating task status"""
    class Meta:
        model = TaskAssignment
        fields = ('status',)
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }

class JobTypeForm(forms.ModelForm):
    """Form for creating or updating job types"""
    class Meta:
        model = JobType
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class UserManagementForm(forms.ModelForm):
    """Form for managing employee details"""
    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'email', 'job_type', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
