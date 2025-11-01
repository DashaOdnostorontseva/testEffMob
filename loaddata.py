import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testEffMob.settings")
django.setup()

def load_data():
    print("Starting data load...")

    dir = "effMobApp/db_data/"

    with open(f'{dir}users_data.json', 'r', encoding='utf-8') as f:
        call_command('loaddata', f.name)

    with open(f'{dir}roles_data.json', 'r', encoding='utf-8') as f:
        call_command('loaddata', f.name)

    with open(f'{dir}userroles_data.json', 'r', encoding='utf-8') as f:
        call_command('loaddata', f.name)

    with open(f'{dir}passwords_data.json', 'r', encoding='utf-8') as f:
        call_command('loaddata', f.name)

    with open(f'{dir}entrymonitoring_data.json', 'r', encoding='utf-8') as f:
        call_command('loaddata', f.name)

    print("Data load completed.")

if __name__ == "__main__":
    load_data()
