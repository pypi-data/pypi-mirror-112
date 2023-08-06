# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gtexquery',
 'gtexquery.data_handling',
 'gtexquery.logs',
 'gtexquery.multithreading']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1',
 'aiohttp>=3.7.4',
 'bioservices>=1.7.11,<2.0.0',
 'lxml>=4.6.3,<5.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.3.0,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'gtexquery',
    'version': '0.2.1',
    'description': 'Code for handling multithreaded queries for GTEx',
    'long_description': '# GTExQuery\n\n[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n[![Python 3.9](https://img.shields.io/badge/Python-3.9-brightgreen.svg)](https://docs.python.org/3/whatsnew/3.9.html)\n[![Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)\n[![CI/CD](https://github.com/IMS-Bio2Core-Facility/GTExQuery/actions/workflows/main.yml/badge.svg)](https://github.com/IMS-Bio2Core-Facility/GTExQuery/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/IMS-Bio2Core-Facility/GTExQuery/branch/main/graph/badge.svg?token=L56T1KFL1J)](https://codecov.io/gh/IMS-Bio2Core-Facility/GTExQuery)\n[![Documentation Status](https://readthedocs.org/projects/gtexquery/badge/?version=latest)](https://gtexquery.readthedocs.io/en/latest/)\n[![Codestyle: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI](https://img.shields.io/pypi/v/gtexquery)](https://pypi.org/project/gtexquery/)\n\n```{admonition} For use with GTExSnake\n:class: tip\n\nThis repository houses the code, tests, etc.,\nthat run the nuts and bolts of the Snakemake pipeline\n[GTExSnake][GTExSnake]\n```\n\nGTExSnake is a fully concurrent pipeline for querying\ntranscript-level GTEx data in specific tissues.\nThis package handles all the code needed for\nmultithreading,\ndata handling,\nand file manipulation necessary for so-said pipeline.\n\nIf you find the project useful,\nleaves us a star on [github][stars]!\n\nIf you want to contribute,\nplease see the [guide on contributing](./CONTRIBUTING.md)\n\n## Motivation\n\nThere are a number of circumstances where transcript level expressed data for a\nspecific tissue is highly valuable.\nFor tissue-dependent expression data,\nthere are few resources better than GTEx.\nIn this case, the `medianTranscriptExpression` query provides the necessary data.\nIt returns the median expression of each transcript for a gene in a given tissue.\n\nAs the code and tests necessary to handle the multithreading and data grew,\nmaintaining both the pipeline and the source code in a single repository\nbecame quite the challenge.\nTo help alleviate this,\nit was decided to refactor the source code into its own repository,\nallowing both the pipeline and the code to more easily adhere to best practices.\n\n## Further Information\n\nFor more information about the source code,\nsee our [documentation][docs] on ReadTheDocs.\nYou can learn more about the pipeline this code supports [here][GTExSnake].\n\n[GTExSnake]: HOLDING "GTExSnake Snakemake Pipeline"\n[stars]: https://github.com/IMS-Bio2Core-Facility/GTExQuery/stargazers "Stargazers"\n[docs]: https://gtexquery.readthedocs.io/en/latest/ "Package Documentation"\n',
    'author': 'rbpatt2019',
    'author_email': 'rb.patterson.cross@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
