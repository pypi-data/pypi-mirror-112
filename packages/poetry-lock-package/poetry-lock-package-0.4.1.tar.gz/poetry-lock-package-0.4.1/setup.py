# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_lock_package']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.1,<0.11.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=0.22']}

entry_points = \
{'console_scripts': ['poetry-lock-package = poetry_lock_package.app:main']}

setup_kwargs = {
    'name': 'poetry-lock-package',
    'version': '0.4.1',
    'description': 'Poetry lock package generator',
    'long_description': "Poetry lock package generator\n=========================\n\n\nSimple script that will take a `pyproject.toml` and a `poetry.lock` and generate a new poetry project where all the lock versions are pinned dependencies.\n\nIn theory this will allow you to transport your lock file to any system that is able to install python packages and dependencies.\n\nAfter installation, the command `poetry-lock-package` should be run next to your `pyproject.toml` and `poetry.lock` files and will generate a subdirectory with a `pyproject.toml` requiring all the dependencies of the lock file.\n\nSimply enter the subdirectory, build and publish the package and you have a '-lock' package that depends on all the exact versions from your lock file.\n\n\nExample workflow\n---------------\nThe example workflow below will add `poetry-lock-package` as a dev dependency, allowing `poetry run` to find the command.\n\nFirst create a new poetry project\n\n    poetry new example-package\n    cd example-package\n\nAdd some dependencies, and see what we have build so far\n\n    poetry add loguru click\n    poetry install\n    poetry build\n    ls dist\n\nAdd `poetry-lock-package` to allow for `poetry run` to find the entry point script:\n\n    poetry add --dev poetry-lock-package\n\nFinally build the lock package and see what we have gotten\n\n    poetry run poetry-lock-package --build\n    ls -al dist\n\nYou will now have two wheel files in your dist folder: one with the project code, one name `example-package-lock` which depends on the exact version of all the packages specified in your `poetry.lock` file.\n\nUsing `--no-root`\n-----------------\nDefault behavior is to have the lock package depend on the original package the lock was created for. If you have a private repository, this will allow you to publish both packages to the private repository and only require you to point at one package to install everything.\n\nIf you want to be able to install the dependencies, but not the package itself, you can use the `--no-root` command line argument to stop `poetry-lock-package` from adding your root project to the lock package dependencies.\n\nUsing `--ignore`\n----------------\nIf you want to allow pip to have freedom in selecting a package, or you expect to deploy in an environment that already has the right version installed, you can opt to use `--ignore` to remove that dependency from the lock package pinned dependencies.\n\nBecause `poetry-lock-package` is aware of the dependency graph, it will not only skip locking the dependency but also transitive dependencies.\n\nContributing code\n-----------------\n\n- Open an issue\n- Create an associated PR\n- Make sure to black format the proposed change\n\n    poetry run pre-commit install\n\n- Add tests where possible\n\nLicense\n-------\nGPLv3, use at your own risk.\n\n",
    'author': 'Bram Neijt',
    'author_email': 'bram@neijt.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bneijt/poetry-lock-package',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
