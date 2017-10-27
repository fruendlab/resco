readme = """
# {{ module }}

This is an empty readme.
"""

fabfile = """
from resco api

remote_working_dir = ''
venv = api.RemoteVirtualEnv({{ module }}-env,
                            dependencies=[])

run_unit_tests = api.run_unit_tests

def run_script(script_name):
    api.run_script(script_name, venv, '{{ module }}', remote_working_dir)
"""
