# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loomxpy',
 'loomxpy._io',
 'loomxpy._specifications',
 'loomxpy._specifications.v1',
 'tests']

package_data = \
{'': ['*']}

install_requires = \
['click',
 'dataclasses-json>=0.5.3,<0.6.0',
 'loompy>=3.0.6,<4.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pyscenic>=0.11.1,<0.12.0',
 'scikit-learn>=0.24.2,<0.25.0']

entry_points = \
{'console_scripts': ['loomxpy = loomxpy.cli:main']}

setup_kwargs = {
    'name': 'loomxpy',
    'version': '0.3.1',
    'description': 'Top-level package for LoomXpy.',
    'long_description': '=======\nLoomXpy\n=======\n\nPython package (compatible with SCope) to create .loom files and extend them with other data e.g.: SCENIC regulons\n\n.. image:: https://img.shields.io/pypi/v/loomxpy.svg\n        :target: https://pypi.python.org/pypi/loomxpy\n\n.. image:: https://readthedocs.org/projects/loomxpy/badge/?version=latest\n        :target: https://loomxpy.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n.. image:: https://pyup.io/repos/github/aertslab/loomxpy/shield.svg\n     :target: https://pyup.io/repos/github/aertslab/loomxpy/\n     :alt: Updates\n\n\n\nPython package containing code for Loom files generation.\n\n\n* Free software: MIT\n* Documentation: https://loomxpy.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Maxime De Waegeneer',
    'author_email': 'mdewaegeneer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aertslab/loomxpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1',
}


setup(**setup_kwargs)
