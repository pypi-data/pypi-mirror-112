# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['usb_plug_notification']
setup_kwargs = {
    'name': 'usb-plug-notification',
    'version': '0.1.0',
    'description': 'USB plug notification package',
    'long_description': None,
    'author': 'Dick Marinus',
    'author_email': 'dick@mrns.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
