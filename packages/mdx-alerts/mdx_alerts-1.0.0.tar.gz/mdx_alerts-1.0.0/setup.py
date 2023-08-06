# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mdx_alerts']
install_requires = \
['Markdown>=3.3.4,<4.0.0']

entry_points = \
{'console_scripts': ['mdx_alerts = mdx_alerts:AlertExtension']}

setup_kwargs = {
    'name': 'mdx-alerts',
    'version': '1.0.0',
    'description': 'Python-Markdown extension to support bootstrap alerts',
    'long_description': '# Boostrap alerts extension for Python-Markdown\n\nThis extension adds bootstrap alerts support to [Python-Markdown].\n\n[Python-Markdown]: https://github.com/Python-Markdown/markdown\n\n\n## Installation\n\n### Install from PyPI\n\n```\n$ python -m pip install python-markdown-bootstrap-alerts\n```\n\n### Install locally\n\nUse `setup.py build` and `setup.py install` to build and install this\nextension, respectively.\n\nThe extension name is `mdx_alerts`, so you need to add that name to your\nlist of Python-Markdown extensions.\nCheck [Python-Markdown documentation] for details on how to load\nextensions.\n\n[Python-Markdown documentation]: https://python-markdown.github.io/reference/#extensions\n\n\n## Usage\n\n',
    'author': 'Florian Dahlitz',
    'author_email': 'f2dahlitz@freenet.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DahlitzFlorian/python-markdown-bootstrap-alerts',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
