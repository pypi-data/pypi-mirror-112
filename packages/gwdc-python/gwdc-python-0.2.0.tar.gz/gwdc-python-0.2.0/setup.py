# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gwdc_python', 'gwdc_python.tests']

package_data = \
{'': ['*']}

install_requires = \
['jwt>=1.2.0,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'gwdc-python',
    'version': '0.2.0',
    'description': 'API for GWDC modules',
    'long_description': 'GWDC Python API\n===============\n\nThis package handles requests for the GWDC modules. Presently, it primarily handles the requests for `gwcloud-python <https://pypi.org/project/gwcloud-python/>`_.',
    'author': 'Thomas Reichardt',
    'author_email': 'treichardt@swin.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gravitationalwavedc/gwdc_python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
