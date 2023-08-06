# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['usb_plug_notification_linux']
install_requires = \
['PyGObject>=3.40.1,<4.0.0',
 'click>=8.0.1,<9.0.0',
 'dbus-python>=1.2.16,<2.0.0',
 'pyudev>=0.22.0,<0.23.0']

entry_points = \
{'console_scripts': ['usb-plug-notification = '
                     'usb_plug_notification_linux:main']}

setup_kwargs = {
    'name': 'usb-plug-notification-linux',
    'version': '0.1.0',
    'description': 'Python script to get plug/unplug events on Linux',
    'long_description': None,
    'author': 'Dick Marinus',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
