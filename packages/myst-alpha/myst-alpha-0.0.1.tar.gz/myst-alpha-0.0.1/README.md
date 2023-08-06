# Myst Python Library

This is the official Python client library for the Myst Platform.

## Requirements

- Python version 3.6.2+

## Installation

To install the package from PyPI:

    $ pip install --upgrade myst

## Authentication

The Myst API uses JSON Web Tokens (JWTs) to authenticate requests.
The Myst Python library handles the sending of JWTs to the API automatically and currently supports two ways to authenticate to obtain a JWT: through your Google user account or a Myst service account.

### Authenticating using your user account

If you don't yet have a Google account, you can create one on the [Google Account Signup](https://accounts.google.com/signup) page.

Once you have access to a Google account, send an email to `support@myst.ai` with your email so we can authorize you to use the Myst Platform.

Use the following code snippet to authenticate using your user account:

```python
from myst import Client, GoogleConsoleCredentials

client = Client(credentials=GoogleConsoleCredentials())
```

The first time you run this, you'll be presented with a web browser and asked to authorize the Myst Python library to make requests on behalf of your Google user account.

### Authenticating using a service account

You can also authenticate using a Myst service account. To request a service account, email `support@myst.ai`.

To authenticate using a service account, set the `MYST_APPLICATION_CREDENTIALS` environment variable to the path to your service account key file and specify `use_service_account=True`:

```sh
$ export MYST_APPLICATION_CREDENTIALS=</path/to/key/file.json>
```

```python
from myst import Client, GoogleServiceAccountCredentials

client = Client(credentials=GoogleServiceAccountCredentials())
```

You can also explicitly pass the path to your service account key:

```python
from pathlib import Path
from myst import Client, GoogleServiceAccountCredentials

client = Client(credentials=GoogleServiceAccountCredentials(Path("/path/to/key/file.json")))
```

## Working with time series

TBD!

## Support

For questions or just to say hi, reach out to `support@myst.ai`.
