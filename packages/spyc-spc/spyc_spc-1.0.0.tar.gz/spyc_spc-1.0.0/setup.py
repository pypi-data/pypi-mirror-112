# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spyc_spc', 'spyc_spc.helpers']

package_data = \
{'': ['*']}

install_requires = \
['cheroot>=8.5.2,<9.0.0',
 'dash>=1.20.0,<2.0.0',
 'docopt>=0.6.2,<0.7.0',
 'ipywidgets>=7.6.3,<8.0.0',
 'mainentry>=2.0,<3.0',
 'numpy>=1.21.0,<2.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.3.0,<2.0.0',
 'plotly>=5.1.0,<6.0.0']

entry_points = \
{'console_scripts': ['spyc = spyc_spc.main:main']}

setup_kwargs = {
    'name': 'spyc-spc',
    'version': '1.0.0',
    'description': 'Simple tool to help plot SPC data from multiple locations for comparison',
    'long_description': "# SPYC\n*pronounced 'spicy'*\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![build](https://github.com/fanoway/spyc/actions/workflows/build.yaml/badge.svg?branch=main)](https://github.com/fanoway/spyc/actions/workflows/build.yaml)\n[![codecov](https://codecov.io/gh/fanoway/spyc/branch/main/graph/badge.svg?token=RMHSZXZSLK)](https://codecov.io/gh/fanoway/spyc)\n\nSimple tool to help plot SPC data for production purposes\n\nSupports comparison of measurment data between locations (could also be hijacked to compare production equipment within a single location)\n\nInteractive plots are outputted in ther browser using plotly and dash\n\n## Installation\npipx is the recommened tool for installation as it will install in a virtual enviroment\n\n```\npython3 -m pip install --user pipx\npython3 -m pipx ensurepath\n```\n\nspyc can then be installed from  pypi\n\n```\npipx install spyc-spc\n```\n\n## Usage\n\nspyc can be ran as follows to display the help\n\n```\nspyc\n```\n\n",
    'author': 'fanoway',
    'author_email': '86997883+fanoway@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fanoway/spyc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
