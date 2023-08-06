# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['api_project_generator',
 'api_project_generator.domain',
 'api_project_generator.domain.models',
 'api_project_generator.services']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.18,<4.0.0', 'poetry>=1.1.7,<2.0.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['api-project = api_project_generator.main:app']}

setup_kwargs = {
    'name': 'api-project-generator',
    'version': '0.1.1',
    'description': '',
    'long_description': '# API Project Generator\n\nSimple API Structure Generator using tecnologies:\n\n- FastAPI\n- SQLAlchemy\n- aiohttp\n- aiomysql\n',
    'author': 'Gustavo Correa',
    'author_email': 'self.gustavocorrea@gmail.com',
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
