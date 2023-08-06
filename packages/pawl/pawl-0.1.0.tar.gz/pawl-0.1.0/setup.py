# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pawl', 'pawl.core', 'pawl.service', 'pawl.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pawl',
    'version': '0.1.0',
    'description': "PAWL (an acronym for `Python API Wrapper - LinkedIn`) allows for simple access to LinkedIn's API.",
    'long_description': '# PAWL: Python API Wrapper for LinkedIn\n\n---\n\n![PyPI - Version](https://img.shields.io/pypi/v/pawl?color=blue)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pawl)\n![PyPI - Monthly Downloads](https://img.shields.io/pypi/dm/pawl)\n\nPAWL (an acronym for `Python API Wrapper - LinkedIn`) allows for simple access to LinkedIn\'s API with only a single dependency.\n\n## Installation\n\nPAWL is supported on Python 3.9+. The recommended way to install PAWL is with pip.\n\n`pip install pawl`\n\n## Examples\n\nExamples are provided in [docs/examples](docs/examples).\n\n## Quickstart\n\n```python\n# Demo in python/ipython shell\n# Don\'t forget to install pawl first\n\n>>> import pawl\n\n>>> linkedin = pawl.Linkedin(\n    client_id="CLIENT_ID_VALUE",\n    client_secret="CLIENT_SECRET_VALUE",\n    redirect_uri="http://localhost:8000",\n)\n\n>>> linkedin\n<pawl.linkedin.Linkedin at 0x10ea46af0>\n```\n\n#### GET PROFILE:\n\n```python\n# Demo in python/ipython shell\n\n>>> linkedin\n<pawl.linkedin.Linkedin at 0x10ea46af0>\n\n>>> response = linkedin.current_user.basic_profile()\n\n>>> response\n{\n    \'localizedLastName\': \'LAST_NAME\',\n    \'profilePicture\': {\n        \'displayImage\': \'PHOTO_ID\'\n    },\n    \'firstName\': {\n        \'localized\': {\n            \'LANG_CODE_COUNTRY_CODE\': \'FIRST_NAME\'\n        },\n        \'preferredLocale\': {\n            \'country\': \'COUNTRY_CODE_VALUE\',\n            \'language\': \'LANGUAGE_CODE\'\n        }\n    },\n    \'lastName\': {\n        \'localized\': {\n            \'LANG_CODE_COUNTRY_CODE\':\n            \'LAST_NAME\'\n        },\n        \'preferredLocale\': {\n            \'country\': \'COUNTRY_CODE\',\n            \'language\': \'LANGUAGE_CODE\'\n        }\n    },\n    \'id\': \'USER_ID\',\n    \'localizedFirstName\': \'LOCALIZED_FIRST_NAME\'\n}\n```\n\n## Sources\n\nThe work that went into PAWL is not entirely my own. I learned a lot from open-sourced code written by [many incredible developers](docs/CREDITS.md).\n\n## License\n\nPAWL\'s source is provided under the MIT License.\n\n- Copyright © 2021 Kyle J. Burda\n',
    'author': 'Kyle J. Burda',
    'author_email': 'kylejbdev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
