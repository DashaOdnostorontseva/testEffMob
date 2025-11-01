import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testEffMob.settings")
django.setup()

def export_data():
    print("Starting export...")

    dir = "effMobApp/db_data/"

    with open(f'{dir}users_data.json', 'w', encoding='utf-8') as f:
        call_command('dumpdata', 'effMobApp.Users', stdout=f)

    with open(f'{dir}roles_data.json', 'w', encoding='utf-8') as f:
        call_command('dumpdata', 'effMobApp.Roles', stdout=f)

    with open(f'{dir}userroles_data.json', 'w', encoding='utf-8') as f:
        call_command('dumpdata', 'effMobApp.UserRoles', stdout=f)

    with open(f'{dir}passwords_data.json', 'w', encoding='utf-8') as f:
        call_command('dumpdata', 'effMobApp.Passwords', stdout=f)

    with open(f'{dir}entrymonitoring_data.json', 'w', encoding='utf-8') as f:
        call_command('dumpdata', 'effMobApp.EntryMonitoring', stdout=f)

    print("Data export completed.")

if __name__ == "__main__":
    export_data()
