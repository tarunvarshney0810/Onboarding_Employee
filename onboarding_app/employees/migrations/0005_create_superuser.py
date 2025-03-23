from django.db import migrations
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    User = get_user_model()
    
    # Check if superuser already exists
    if not User.objects.filter(username='e3017847').exists():
        User.objects.create_superuser(
            username='e3017847',
            email='e3017847@example.com',
            password='Leo@1grip',
            employee_id='e3017847',
            first_name='Admin',
            last_name='User',
            is_admin=True,
            is_enroller=True
        )

class Migration(migrations.Migration):
    dependencies = [
        ('employees', '0004_alter_onboardingtask_options_onboardingtask_order'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ] 