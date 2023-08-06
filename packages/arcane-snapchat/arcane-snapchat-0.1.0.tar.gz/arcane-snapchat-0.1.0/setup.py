# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane', 'arcane.snapchat']

package_data = \
{'': ['*']}

install_requires = \
['arcane-core>=1.3.0,<2.0.0',
 'backoff>=1.10.0,<2.0.0',
 'requests>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'arcane-snapchat',
    'version': '0.1.0',
    'description': 'Helpers to request Snapchat API ',
    'long_description': "# Arcane snapchat README\n\n## Credentials\n\nThe access token for production environnement has been generated with: snapchat@arcane.run\nThe access token for staging environnement has been generated with: billel@arcane.run\n\nThe access token can be be expired, we receive a 401 if it is the case. We need to use the refresh token located in the credentials, this token is generated through a one time life 'code'. For more information :\nhttps://marketingapi.snapchat.com/docs/#receive-the-redirected-user \n\n## Release history\nTo see changes, please see CHANGELOG.md\n",
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
