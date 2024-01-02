import os
import subprocess
import sys

# shitcode, i know

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')

def pip_install():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

def execute(args: tuple):
    subprocess.check_call([sys.executable, 'manage.py'] + list(args))

def log(string: str):
    print(f'[Configure] {string}')

log('Installing packages..')
pip_install()

log('Creating user..')

username = input('Enter new admin username: ')

os.environ['DJANGO_SUPERUSER_USERNAME'] = username
os.environ['DJANGO_SUPERUSER_PASSWORD'] = input('Enter new admin password: ')

email = input('Enter new admin email (you can leave it empty): ')

execute(('createsuperuser', '--noinput', '--email', email if email != '' else 'blank@email.com'))

os.environ['DJANGO_SUPERUSER_PASSWORD'] = ''

log('Created user: ' + username)

log('All done, you can run destmusic with command: \npython manage.py runserver 7825 --insecure')