from fabric.api import local, lcd, prefix, env
import os

TEST_PROJECT_DIR = os.path.join(os.path.dirname(env.real_fabfile), 'test_project')

def test(app=""):
    with lcd(TEST_PROJECT_DIR):
        coverage_cmd = "coverage run "
        if app:
            coverage_cmd += "--source='../{}/' ".format(app)
        else:
            coverage_cmd += "--source='.' "
        local(coverage_cmd + "manage.py test -v 2 " + app)
        local("coverage report")

def run_server():
    with lcd(TEST_PROJECT_DIR):
        local("python manage.py runserver")
