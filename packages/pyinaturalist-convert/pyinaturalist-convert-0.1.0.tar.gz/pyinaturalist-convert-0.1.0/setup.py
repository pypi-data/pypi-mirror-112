# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyinaturalist_convert']

package_data = \
{'': ['*']}

install_requires = \
['flatten-dict>=0.4.0,<0.5.0',
 'pyinaturalist>=0.14.0,<0.15.0',
 'tablib>=3.0.0,<4.0.0',
 'tabulate>=0.8.9,<0.9.0']

extras_require = \
{'all': ['gpxpy>=1.4.2,<2.0.0',
         'openpyxl>=2.6',
         'pandas>=1.2',
         'pyarrow>=4.0',
         'python-dwca-reader>=0.15.0,<0.16.0',
         'xmltodict>=0.12'],
 'csv-import': ['pandas>=1.2'],
 'df': ['pandas>=1.2'],
 'dwc': ['python-dwca-reader>=0.15.0,<0.16.0', 'xmltodict>=0.12'],
 'feather': ['pandas>=1.2', 'pyarrow>=4.0'],
 'gpx': ['gpxpy>=1.4.2,<2.0.0'],
 'hdf': ['pandas>=1.2', 'tables>=3.6'],
 'parquet': ['pandas>=1.2', 'pyarrow>=4.0'],
 'xlsx': ['openpyxl>=2.6']}

setup_kwargs = {
    'name': 'pyinaturalist-convert',
    'version': '0.1.0',
    'description': 'Convert iNaturalist observation data to and from multiple formats',
    'long_description': "# pyinaturalist-convert\n\n[![Build status](https://github.com/JWCook/pyinaturalist-convert/workflows/Build/badge.svg)](https://github.com/JWCook/pyinaturalist-convert/actions)\n[![PyPI](https://img.shields.io/pypi/v/pyinaturalist-convert?color=blue)](https://pypi.org/project/pyinaturalist-convert)\n[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/pyinaturalist-convert)](https://pypi.org/project/pyinaturalist-convert)\n[![PyPI - Format](https://img.shields.io/pypi/format/pyinaturalist-convert?color=blue)](https://pypi.org/project/pyinaturalist-convert)\n\n**This is an incomplete work in progress!**\n\nThis package provides tools to convert iNaturalist observation data to and from multiple formats.\nThis is mainly intended for use with data from the iNaturalist API\n(via [pyinaturalist](https://github.com/JWCook/pyinaturalist)), but also works with other\niNaturalist data sources.\n\n# Formats\n\nImport formats currently supported:\n* CSV (Currently from API results only, but see planned features below)\n* JSON (either from a `requests.Response` or `pyinaturalist` results)\n* parquet\n\nExport formats currently supported:\n* CSV\n* Excel (xlsx)\n* GPX (experimental)\n* HDF5\n* Feather\n* Parquet\n* pandas DataFrame\n\n\n# Installation\n\nInstall with pip:\n```bash\npip install pyinaturalist-convert\n```\n\nTo keep things modular, many format-specific dependencies are not installed by default, so you may need to install some\nmore packages depending on which formats you want. See\n[pyproject.toml]([pyproject.toml](https://github.com/JWCook/pyinaturalist-convert/blob/7098c05a513ddfbc254a446aeec1dfcfa83e92ff/pyproject.toml#L44-L50))\nfor the full list (TODO: docs on optional dependencies).\n\nTo install all of the things:\n```bash\npip install pyinaturalist-convert[all]\n```\n\n# Usage\n\nBasic usage example:\n```python\nfrom pyinaturalist import get_observations\nfrom pyinaturalist_convert import to_csv\n\nobservations = get_observations(user_id='my_username')\nto_csv(observations, 'my_observations.csv')\n```\n\n# Planned and Possible Features\n\n* Convert to an HTML report\n* Convert to print-friendly format\n* Convert to Simple Darwin Core\n* Export to any [SQLAlchemy-compatible database engine](https://docs.sqlalchemy.org/en/14/core/engines.html#supported-databases)\n* Import and convert observation data from the [iNaturalist export tool](https://www.inaturalist.org/observations/export) and convert it to be compatible with observation data from the iNaturalist API\n* Import and convert metadata and images from [iNaturalist open data on Amazon]()\n    * See also [pyinaturalist-open-data](https://github.com/JWCook/pyinaturalist-open-data), which may eventually be merged with this package\n* Import and convert observation data from the [iNaturalist GBIF Archive](https://www.inaturalist.org/pages/developers)\n* Import and convert observation data from the[iNaturalist Taxonomy Archive](https://www.inaturalist.org/pages/developers)\n* Note: see [API Recommended Practices](https://www.inaturalist.org/pages/api+recommended+practices)\n  for details on which data sources are best suited to different use cases\n",
    'author': 'Jordan Cook',
    'author_email': 'Jordan.Cook@pioneer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JWCook/pyinaturalist_convert',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
