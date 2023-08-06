# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoklik']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['autoklik = autoklik.__init__:main']}

setup_kwargs = {
    'name': 'autoklik',
    'version': '0.1.1',
    'description': 'Auto clicker built around xdotool.',
    'long_description': '# Autoklik\n\nAn auto clicker built around xdotool.\n\n## License\n\nThis program is licensed under the GPLv3 or later.\n',
    'author': 'Magnus Walbeck',
    'author_email': 'mw@mwalbeck.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.walbeck.it/mwalbeck/autoklik',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
