# halon-api
A Python wrapper for the API for Mail Transport Agent Halon.
Please read [the original documentation](https://docs.halon.io/api) for
complete in depth documentation on function arguments and the data returned by the API.

The wrapper is available as a PyPI package [_halon-api_](https://pypi.org/project/halon-api/).

# Install
Install the PyPI package using _pip_: `pip install halon-api`

# How to use

```
from halon_api import HalonAPI

h = HalonAPI(
    "https://halon.example.com",
    "halon-user",
    "secret-password",
)

print("Halon software version:", h.get_software_version())
```

# Development
How to set up development environment.

* Make virtual python environment: `python -m venv .venv`
* Activate environment: `source .venv/bin/activate`
* Install required packages: `pip install requirements.txt`
* Install required packages for development: `pip install requirements-dev.txt`
* Install _pre-commit_ git hook scripts: `pre-commit install`

# Build the PyPI package
In the project root dir: `python -m build`
