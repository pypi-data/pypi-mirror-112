# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['talus_utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib-venn>=0.11.6,<0.12.0',
 'pandas>=1.3.0,<2.0.0',
 'plotly>=5.1.0,<6.0.0',
 'talus-aws-utils==0.0.1']

setup_kwargs = {
    'name': 'talus-utils',
    'version': '0.0.3',
    'description': 'Talus Utils',
    'long_description': "Talus Utils\n===========\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/talus-utils.svg\n   :target: https://pypi.org/project/talus-utils/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/talus-utils\n   :target: https://pypi.org/project/talus-utils\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/talus-utils\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/talus-utils/latest.svg?label=Read%20the%20Docs\n   :target: https://talus-utils.readthedocs.io/\n   :alt: Read the documentation at https://talus-utils.readthedocs.io/\n.. |Tests| image:: https://github.com/rmeinl/talus-utils/workflows/Tests/badge.svg\n   :target: https://github.com/rmeinl/talus-utils/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/rmeinl/talus-utils/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/rmeinl/talus-utils\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *Talus Utils* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install talus-utils\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Talus Utils* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/rmeinl/talus-utils/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://talus-utils.readthedocs.io/en/latest/usage.html\n",
    'author': 'Rico Meinl',
    'author_email': 'rmeinl@talus.bio',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rmeinl/talus-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
