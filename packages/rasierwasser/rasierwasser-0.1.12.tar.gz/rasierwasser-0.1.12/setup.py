# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rasierwasser',
 'rasierwasser.configuration',
 'rasierwasser.helper',
 'rasierwasser.server',
 'rasierwasser.server.fastapi',
 'rasierwasser.service',
 'rasierwasser.storage',
 'rasierwasser.storage.database']

package_data = \
{'': ['*'], 'rasierwasser.server': ['data/*']}

install_requires = \
['Flask>=2.0.1,<3.0.0',
 'Jinja2>=3.0.1,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy>=1.4.17,<2.0.0',
 'fastapi>=0.65.1,<0.66.0',
 'pyOpenSSL>=20.0.1,<21.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'uvicorn>=0.14.0,<0.15.0']

entry_points = \
{'console_scripts': ['rasierwasser = rasierwasser.service.server:main',
                     'rasierwasser_sign = rasierwasser.helper.signing:main']}

setup_kwargs = {
    'name': 'rasierwasser',
    'version': '0.1.12',
    'description': 'Simple pip repository server for internal usage',
    'long_description': None,
    'author': 'voidpointercast',
    'author_email': 'patrick.daniel.gress@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/voidpointercast/rasierwasser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
