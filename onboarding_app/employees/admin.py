from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, OnboardingTask, TaskAssignment, JobType

class EmployeeAdmin(UserAdmin):
    list_display = ('employee_id', 'username', 'email', 'first_name', 'last_name', 'job_type', 'manager_name', 'is_admin', 'is_enroller')
    search_fields = ('employee_id', 'username', 'email', 'first_name', 'last_name', 'manager_name')
    readonly_fields = ('date_joined', 'last_login')
    
    filter_horizontal = ()
    list_filter = ('is_admin', 'is_enroller', 'job_type')
    fieldsets = (
        (None, {'fields': ('employee_id', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'manager_name', 'job_type')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_enroller')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee_id', 'username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'manager_name', 'job_type', 'is_admin', 'is_enroller'),
        }),
    )
    
    ordering = ('employee_id',)

class OnboardingTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_type', 'get_job_types')
    list_filter = ('task_type', 'job_types')
    search_fields = ('title', 'description')
    filter_horizontal = ('job_types',)
    
    def get_job_types(self, obj):
        return ", ".join([job.name for job in obj.job_types.all()])
    get_job_types.short_description = 'Job Types'

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Basic Information', {
                'fields': ['title', 'description', 'task_type', 'job_types']
            }),
        ]
        
        if obj and obj.task_type == 'email':
            fieldsets.append(('Email Details', {
                'fields': ['email_to', 'email_subject', 'email_body']
            }))
        elif obj and obj.task_type == 'link':
            fieldsets.append(('Link Details', {
                'fields': ['external_link']
            }))
            
        return fieldsets

    class Media:
        js = ('admin/js/task_type_handler.js',)

class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'task', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('employee__employee_id', 'employee__username', 'task__title')

class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(OnboardingTask, OnboardingTaskAdmin)
admin.site.register(TaskAssignment, TaskAssignmentAdmin)
admin.site.register(JobType, JobTypeAdmin)
