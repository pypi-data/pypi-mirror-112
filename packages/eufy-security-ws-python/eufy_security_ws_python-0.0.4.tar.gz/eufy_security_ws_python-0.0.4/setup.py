# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eufy_security_ws_python', 'eufy_security_ws_python.model']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4.post0,<4.0.0']

setup_kwargs = {
    'name': 'eufy-security-ws-python',
    'version': '0.0.4',
    'description': 'A Python wrapper around eufy-security-ws',
    'long_description': '# 🚨 eufy-security-ws-python: A Python wrapper around eufy-security-ws\n\n[![CI](https://github.com/bachya/eufy-security-ws-python/workflows/CI/badge.svg)](https://github.com/bachya/eufy-security-ws-python/actions)\n[![PyPi](https://img.shields.io/pypi/v/eufy-security-ws-python.svg)](https://pypi.python.org/pypi/eufy-security-ws-python)\n[![Version](https://img.shields.io/pypi/pyversions/eufy-security-ws-python.svg)](https://pypi.python.org/pypi/eufy-security-ws-python)\n[![License](https://img.shields.io/pypi/l/eufy-security-ws-python.svg)](https://github.com/bachya/eufy-security-ws-python/blob/master/LICENSE)\n[![Code Coverage](https://codecov.io/gh/bachya/eufy-security-ws-python/branch/dev/graph/badge.svg)](https://codecov.io/gh/bachya/eufy-security-ws-python)\n[![Maintainability](https://api.codeclimate.com/v1/badges/81a9f8274abf325b2fa4/maintainability)](https://codeclimate.com/github/bachya/eufy-security-ws-python/maintainability)\n[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)\n\n`eufy-security-ws-python` is a simple Python wrapper around [`https://github.com/bropat/eufy-security-ws`](https://github.com/bropat/eufy-security-ws).\n\n# Installation\n\n```python\npip install eufy-security-ws-python\n```\n\n# Python Versions\n\n`eufy-security-ws-python` is currently supported on:\n\n* Python 3.8\n* Python 3.9\n\n# Contributing\n\n1. [Check for open features/bugs](https://github.com/bachya/eufy-security-ws-python/issues)\n  or [initiate a discussion on one](https://github.com/bachya/eufy-security-ws-python/issues/new).\n2. [Fork the repository](https://github.com/bachya/eufy-security-ws-python/fork).\n3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`\n4. (_optional, but highly recommended_) Enter the virtual environment: `source ./venv/bin/activate`\n5. Install the dev environment: `script/setup`\n6. Code your new feature or bug fix.\n7. Write tests that cover your new functionality.\n8. Run tests and ensure 100% code coverage: `script/test`\n9. Update `README.md` with any new documentation.\n10. Add yourself to `AUTHORS.md`.\n11. Submit a pull request!\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bachya/eufy-security-ws-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
