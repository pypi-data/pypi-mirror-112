# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mojap_airflow_tools']

package_data = \
{'': ['*']}

install_requires = \
['poetry_version>=0.1.5']

extras_require = \
{':extra == "airflow"': ['apache-airflow[kubernetes]>=1.10.10,<2.0.0']}

setup_kwargs = {
    'name': 'mojap-airflow-tools',
    'version': '0.0.1',
    'description': 'A few wrappers and tools to use airflow on AP',
    'long_description': None,
    'author': 'mojap-data-engineers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
