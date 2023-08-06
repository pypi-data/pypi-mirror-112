# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3_path_wrangler']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 's3-path-wrangler',
    'version': '0.4.0',
    'description': 'Provides S3 path manipulation, similar to PurePath in pathlib',
    'long_description': None,
    'author': 'Saulius Beinorius',
    'author_email': 'saulius.beinorius@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
