# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myst',
 'myst.cli',
 'myst.data',
 'myst.endpoints',
 'myst.openapi_client',
 'myst.openapi_client.api',
 'myst.openapi_client.api.model_connectors',
 'myst.openapi_client.api.models',
 'myst.openapi_client.api.operation_connectors',
 'myst.openapi_client.api.operations',
 'myst.openapi_client.api.organizations',
 'myst.openapi_client.api.projects',
 'myst.openapi_client.api.source_connectors',
 'myst.openapi_client.api.sources',
 'myst.openapi_client.api.time_series',
 'myst.openapi_client.api.users',
 'myst.openapi_client.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<22.0.0',
 'google-auth-oauthlib>=0.4.1,<1.0.0',
 'google-auth>=1.11.0,<2.0.0',
 'httpx>=0.15.4,<0.19.0',
 'python-dateutil>=2.8.0,<3.0.0',
 'pytz>=2019.1',
 'toml>=0.10.2,<0.11.0',
 'urllib3>=1.24.3,<2.0.0']

setup_kwargs = {
    'name': 'myst-alpha',
    'version': '0.0.1',
    'description': 'This is the official Python library for the Myst Platform.',
    'long_description': '# Myst Python Library\n\nThis is the official Python client library for the Myst Platform.\n\n## Requirements\n\n- Python version 3.6.2+\n\n## Installation\n\nTo install the package from PyPI:\n\n    $ pip install --upgrade myst\n\n## Authentication\n\nThe Myst API uses JSON Web Tokens (JWTs) to authenticate requests.\nThe Myst Python library handles the sending of JWTs to the API automatically and currently supports two ways to authenticate to obtain a JWT: through your Google user account or a Myst service account.\n\n### Authenticating using your user account\n\nIf you don\'t yet have a Google account, you can create one on the [Google Account Signup](https://accounts.google.com/signup) page.\n\nOnce you have access to a Google account, send an email to `support@myst.ai` with your email so we can authorize you to use the Myst Platform.\n\nUse the following code snippet to authenticate using your user account:\n\n```python\nfrom myst import Client, GoogleConsoleCredentials\n\nclient = Client(credentials=GoogleConsoleCredentials())\n```\n\nThe first time you run this, you\'ll be presented with a web browser and asked to authorize the Myst Python library to make requests on behalf of your Google user account.\n\n### Authenticating using a service account\n\nYou can also authenticate using a Myst service account. To request a service account, email `support@myst.ai`.\n\nTo authenticate using a service account, set the `MYST_APPLICATION_CREDENTIALS` environment variable to the path to your service account key file and specify `use_service_account=True`:\n\n```sh\n$ export MYST_APPLICATION_CREDENTIALS=</path/to/key/file.json>\n```\n\n```python\nfrom myst import Client, GoogleServiceAccountCredentials\n\nclient = Client(credentials=GoogleServiceAccountCredentials())\n```\n\nYou can also explicitly pass the path to your service account key:\n\n```python\nfrom pathlib import Path\nfrom myst import Client, GoogleServiceAccountCredentials\n\nclient = Client(credentials=GoogleServiceAccountCredentials(Path("/path/to/key/file.json")))\n```\n\n## Working with time series\n\nTBD!\n\n## Support\n\nFor questions or just to say hi, reach out to `support@myst.ai`.\n',
    'author': 'Myst AI, Inc.',
    'author_email': 'support@myst.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
