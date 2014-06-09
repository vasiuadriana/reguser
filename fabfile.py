from fabric.api import local, lcd, prefix, env
import os

TEST_PROJECT_DIR = os.path.join(os.path.dirname(env.real_fabfile), 'test_project')

def test():
    with lcd(TEST_PROJECT_DIR):
        local("coverage run --source='../reguser/' manage.py test -v 2 ")
        local("coverage report -m --omit=../reguser/management/*")

def run_server():
    with lcd(TEST_PROJECT_DIR):
        local("python manage.py runserver")
