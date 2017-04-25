from subprocess import call
from pathlib import Path
import os, django, sys


def check_db_files():
    path = Path()
    for fl in path.iterdir():
        if str(fl) == 'db.sqlite3':
            return True
    return False


def check_migrations_files():
    path = Path() / 'account' / 'migrations'
    problems_files = []
    for fl in path.iterdir():
        if fl.is_dir() or str(fl) == 'account\migrations\__init__.py':
            continue
        if str(fl).find('py') != -1:
            problems_files.append(str(fl))
    return problems_files


def create_superuser():
    username = input('Enter username for superuser:\n')
    password = input('Enter password for superuser:\n')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "snuppy_manager.settings")
    django.setup()
    from django.contrib.auth.models import User

    u = User(username=username)
    u.set_password(password)
    u.is_superuser = True
    u.is_staff = True
    u.save()

    print('superuser create succefully')

def call_shell():
    _py_call('manage.py makemigrations')
    _py_call('manage.py migrate')

    abs_path = Path().absolute()
    auth_path = abs_path / 'account' / 'fixtures' / 'auth_data.json'
    data_path = abs_path / 'account' / 'fixtures' / 'initial_data.json'

    _py_call('manage.py loaddata {}'.format(auth_path))
    _py_call('manage.py loaddata {}'.format(data_path))

def _py_call(com):
    call(sys.executable + ' ' + com, shell=True)

if __name__ == '__main__':

    if check_db_files():
        print('First, you must remove old database\nScript terminate')
        sys.exit()

    mg_files = check_migrations_files()
    if mg_files:
        for i in mg_files: print(i)
        print('Please, remove migrations files, listed above')
        sys.exit()

    call_shell()

    create_superuser()

