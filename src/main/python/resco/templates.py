readme = """
# {{ module }}

This is an empty readme.
"""

fabfile = """
from fabric.api import local
from resco import api

remote_working_dir = ''
venv = api.RemoteVirtualEnv('{{ module }}-env',
                            dependencies=['requirements/all.txt',
                                          'requirements/remote.txt'])

run_unit_tests = api.run_unit_tests


def run_script(script_name):
    api.run_script(script_name, venv, '{{ module }}', remote_working_dir)


def update_venv():
    venv.install()


def install_local():
    local('pip install -r requirements/all.txt -r requirements/local.txt')
"""
