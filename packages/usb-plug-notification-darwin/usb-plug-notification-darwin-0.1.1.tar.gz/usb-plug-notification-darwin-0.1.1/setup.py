# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['usb_plug_notification_darwin']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'pyobjc-framework-Cocoa>=7.3,<8.0']

entry_points = \
{'console_scripts': ['usb-plug-notification = '
                     'usb_plug_notification_darwin.main:main']}

setup_kwargs = {
    'name': 'usb-plug-notification-darwin',
    'version': '0.1.1',
    'description': 'Python script to get plug/unplug events on Darwin (MacOS)',
    'long_description': None,
    'author': 'Dick Marinus',
    'author_email': 'dick@mrns.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
