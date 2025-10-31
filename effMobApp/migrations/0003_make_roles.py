from django.db import migrations

def create_roles(apps, schema_editor):
    Role = apps.get_model('effMobApp', 'Roles')
    roles = ['user', 'operator', 'admin']  
    for role in roles:
        Role.objects.get_or_create(role_type=role)


class Migration(migrations.Migration):

    dependencies = [
        ('effMobApp', '0002_users_last_login_users_password'),
    ]

    operations = [
        migrations.RunPython(create_roles),
    ]
