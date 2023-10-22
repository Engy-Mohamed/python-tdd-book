import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL ="https://github.com/Engy-Mohamed/python-tdd-book.git"

def _get_latest_source(site_folder):
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    # get the id of the current commit
    current_commit = local("git log -n 1 --format=%H",capture=True)
    # as git pull but it is used to override any local changes
    run(f'sudo git reset --hard {current_commit}')

def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run('python3 -m venv virtualenv')
    run('./virtualenv/bin/python ./virtualenv/bin/pip install -r requirements.txt')

def _create_or_update_dotenv():
    # append add it if not exists
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    # we can not rely on append condition bec the new secret key 
    # will not like the new one.
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ) )
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')
    email_password = os.environ['EMAIL_PASSWORD']  
    append('.env', f'EMAIL_PASSWORD={email_password}')

def _update_static_files():
    # --noinput remove any yes/no confirmation that fabric would 
    # find hard to deal with
    run('./virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database():
    #just for test Engy
    run('rm db.sqlite3')
    run('./virtualenv/bin/python manage.py migrate --noinput')

def deploy():
    site_folder =f"/home/{env.user}/sites/{env.host}"
    run(f"mkdir -p {site_folder}")
    with cd(site_folder):
        _get_latest_source(site_folder)
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


