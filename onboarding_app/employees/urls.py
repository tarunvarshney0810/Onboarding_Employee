from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin Panel URLs
    path('portal-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('portal-admin/users/', views.user_management, name='user_management'),
    path('portal-admin/users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('portal-admin/users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('portal-admin/tasks/', views.task_management, name='task_management'),
    path('portal-admin/task-assignments/', views.task_assignment_management, name='task_assignment_management'),
    path('portal-admin/task-assignments/<int:assignment_id>/edit/', views.task_assignment_edit, name='task_assignment_edit'),
    path('portal-admin/task-assignments/<int:assignment_id>/delete/', views.task_assignment_delete, name='task_assignment_delete'),
    
    # Existing URLs
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('enroll/', views.enroll_employee, name='enroll'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/edit/<int:task_id>/', views.task_edit, name='task_edit'),
    path('task/delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('task-assignment/update/<int:assignment_id>/', views.update_task_status, name='update_task_status'),
    path('job-type/create/', views.job_type_create, name='job_type_create'),
    path('job-type/edit/<int:job_type_id>/', views.job_type_edit, name='job_type_edit'),
    path('job-type/delete/<int:job_type_id>/', views.job_type_delete, name='job_type_delete'),
]
