readme = """
# {{ module }}

This is an empty readme.
"""

fabfile = """
from fabric.api import local, cd, env
from resco import api

env.module_name = '{{ module }}'
env.remote_working_dir = '{{ module }}-wd'
env.venv = api.RemoteVirtualEnv('{{ module }}-env',
                            dependencies=['requirements/all.txt',
                                          'requirements/remote.txt'])

run_unit_tests = api.run_unit_tests


def run_script(script_name):
    api.run_script(script_name, env.venv, '{{ module }}', env.remote_working_dir)


def update_venv():
    with cd(env.remote_working_dir):
        venv.install()


def install_local():
    local('pip install -r requirements/all.txt -r requirements/local.txt')


def ls(glob_pattern='*'):
    api.ls(remote_working_dir, glob_pattern)


def fetch(glob_pattern='*'):
    api.fetch(remote_working_dir, glob_pattern)
"""
