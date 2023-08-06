# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['playwbot', 'playwbot.src']

package_data = \
{'': ['*']}

install_requires = \
['playwright>=1.12.1,<2.0.0', 'robotframework>=4.0.3,<5.0.0']

setup_kwargs = {
    'name': 'playwbot',
    'version': '0.2.0',
    'description': 'RobotFramework wrapper of Playwright-Python',
    'long_description': '# playwbot\n[Playwright-python](https://github.com/microsoft/playwright-python) wrapper for [RobotFramework](https://robotframework.org/).\n\n## Installation\n\n### From the repository\n\n- clone the repo\n- easiest way is to use [poetry](https://python-poetry.org/) and run `poetry install` and then `poetry shell`\n- to be able to run the tests, install the package for the development by `python setup.py develop`\n- RF tests are run by standard command `robot <path>`\n\n### From the Pypi\n\n- if using poetry, run `poetry add playwbot` and then `poetry install`\n- if using pip, run `pip install playwbot`\n\n## Importing module into the RF suite\n\n- if you have the file directly accesible, just point directly to the location, like this\n\n```\nLibrary    /some/path/to/the/library/Playwbot.py    browser=<chromium|firefox|webkit>\n```\n\n- if you installed it from Pypi, then import it like this\n\n```\nLibrary    playwbot.Playwbot    browser=<chromium|firefox|webkit>\n```\n\n## RobotFramework-style documentation\n\nIs available here https://radekbednarik.github.io/playwbot/\n\n',
    'author': 'radekBednarik',
    'author_email': 'radek.bednarik@tesena.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://radekbednarik.github.io/playwbot/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
