# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_server_state']

package_data = \
{'': ['*']}

install_requires = \
['streamlit>=0.65.0']

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'streamlit-server-state',
    'version': '0.1.0',
    'description': '',
    'long_description': '# streamlit-server-state',
    'author': 'Yuichiro Tachibana (Tsuchiya)',
    'author_email': 't.yic.yt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whitphx/streamlit-server-state',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
