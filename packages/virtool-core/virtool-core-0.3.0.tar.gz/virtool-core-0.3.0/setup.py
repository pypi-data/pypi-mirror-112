# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virtool_core', 'virtool_core.data_model']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles==0.7.0',
 'arrow==0.15.5',
 'dictdiffer==0.8.1',
 'psutil>=5.8.0,<6.0.0']

setup_kwargs = {
    'name': 'virtool-core',
    'version': '0.3.0',
    'description': 'Core utilities for Virtool.',
    'long_description': '# virtool-core\n\nCore utilities for Virtool and associated packages.\n\n![Tests](https://github.com/virtool/virtool-core/workflows/Tests/badge.svg?branch=master&event=push)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f04b88f74f2640588ba7dec5022c9b51)](https://www.codacy.com/gh/virtool/virtool-core/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=virtool/virtool-core&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/f04b88f74f2640588ba7dec5022c9b51)](https://www.codacy.com/gh/virtool/virtool-core/dashboard?utm_source=github.com&utm_medium=referral&utm_content=virtool/virtool-core&utm_campaign=Badge_Coverage)\n\n## Install\n\n### Last Stable Release\n\n```shell script\npip install virtool-core\n```\n\n### Latest Changes\n\n```shell script\npip install git+https://github.com/virtool/virtool-core.git\n```\n\n## Contribute \n\n### Unit Tests\n\n#### Install Tox\n\n`tox` is used to run the tests in a fresh virtual environment with all of the test dependencies. To install it use;\n\n```shell script\npip install tox tox-poetry\n```\n\n#### Run Tests\n\n```shell script\ntox\n```\n\nAny arguments given to tox after a `--` token will be supplied to pytest.\n\n```shell script\ntox -- --log-cli-level=DEBUG\n```\n\n### Documentation\n\nFor docstrings, use the [**Sphinx** docstring format](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html).\n\nThe packages `sphinx_rtd_theme` and `sphinx_autoapi` are used in rendering the documentation. \n\n```  shell script\npip install sphinx_rtd_theme sphinx_autoapi\n```\n\n#### Markdown for Sphinx\n\n[recommonmark](https://github.com/readthedocs/recommonmark) is used so that Sphinx can \nrender documentation from *markdown* files as well as *rst* files. It will need to \nbe installed before running `sphinx-build`:\n\n```shell script\npip install recommonmark\n```\n\nTo use sphinx rst [directives](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html) in a *markdown* file use the \n`eval_rst` [code block](https://recommonmark.readthedocs.io/en/latest/auto_structify.html#embed-restructuredtext)\n\n\n#### Building the documentation\n\n```shell script\ncd sphinx && make html\n```\n\nThe rendered HTML files are found under `sphinx/build/html`\n',
    'author': 'Ian Boyes',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/virtool/virtool-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
