from subprocess import call, run
from pathlib import Path
import os, django, sys

DB_FILES = ['db.sqlite3']


def check_db_files():
    path = Path()
    for fl in path.iterdir():
        if str(fl) in DB_FILES:
            return DB_FILES
    return None


def del_db_files():
    del_files(DB_FILES)


def del_files(files):
    for p in files:
        os.remove(p)


def check_migrations_files():
    path = Path() #/ 'account' / 'migrations'
    problems_files = []
    for fl in path.iterdir():
        if fl.is_dir():
            mi = fl / 'migrations'
            if mi.exists():
                for p in mi.iterdir():
                    if p.is_dir() or str(p).endswith('__init__.py'):
                        continue
                    if str(p).endswith('.py'):
                        problems_files.append(str(p))
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
    _py_call('manage.py migrate --run-syncdb')

    abs_path = Path().absolute()
    auth_path = abs_path / 'account' / 'fixtures' / 'auth_data3.json'
    data_path = abs_path / 'account' / 'fixtures' / 'initial_data4.json'

    _py_call('manage.py loaddata {}'.format(auth_path))
    _py_call('manage.py loaddata {}'.format(data_path))

def _py_call(com):
    call('"' + sys.executable + '"' + ' ' + com, shell=True)
    # call(sys.executable + ' ' + com, shell=True) old call

def input_with_answer(text):
    ret = input(text)
    return ret.strip().lower() in ('y', 'yes')

if __name__ == '__main__':

    db_files = check_db_files()
    if db_files:
        if input_with_answer(f'I need delete db files: {db_files}. \n\tMay I delete it? (y/n): '):
            del_db_files()
        else:
            sys.exit()

    mg_files = check_migrations_files()
    if mg_files:
        print('You have migration files:')
        for p in mg_files:
            print('\t' + p)
        if input_with_answer('May I delete them? (y/n): '):
            del_files(mg_files)
        else:
            sys.exit()

    call_shell()

    create_superuser()

