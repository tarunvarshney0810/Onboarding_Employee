from django.db import migrations
from django.contrib.auth import get_user_model

def create_default_superuser(apps, schema_editor):
    User = get_user_model()
    
    # Check if default superuser already exists
    if not User.objects.filter(employee_id='e3017847').exists():
        User.objects.create_superuser(
            username='e3017847',
            email='tarun.varshney@example.com',
            password='Leo@1grip',
            employee_id='e3017847',
            first_name='Tarun',
            last_name='Varshney',
            is_admin=True,
            is_enroller=True
        )

def reverse_func(apps, schema_editor):
    User = get_user_model()
    User.objects.filter(employee_id='e3017847').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('employees', '0004_alter_onboardingtask_options_onboardingtask_order'),
    ]

    operations = [
        migrations.RunPython(create_default_superuser, reverse_func),
    ] 