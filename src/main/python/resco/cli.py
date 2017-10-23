import os
import jinja2

from . import templates
from . import utils


def start_project(name):
    utils.create_tree({
        '.': ['README.md', 'fabfile.py'],
        name: '__init__.py',
        'unittests': {},
        'scripts': {
            'behaviour': {},
            'analysis': {},
            'theory': {},
            'figures': {},
            'tools': {},
        },
        'target': {
            'results': {
                'behavour': {},
                'analysis': {},
                'theory': {},
                'figures': {},
            },
        }
    })
    with open('README.md', 'w') as f:
        f.write(jinja2.template(templates.readme).render(module=name))

    with open('fabfile.py', 'w') as f:
        f.write(jinja2.template(templates.fabfile).render())
