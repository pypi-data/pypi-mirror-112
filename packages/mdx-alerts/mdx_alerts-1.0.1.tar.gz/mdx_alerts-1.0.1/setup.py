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
    'version': '1.0.1',
    'description': 'Python-Markdown extension to support bootstrap alerts',
    'long_description': '# Boostrap alerts extension for Python-Markdown\n\n![Tests](https://github.com/DahlitzFlorian/python-markdown-bootstrap-alerts/actions/workflows/main.yml/badge.svg?branch=master)\n![Python 3.6](https://img.shields.io/badge/Python-%3E%3D%203.6-blue)\n\nThis extension adds bootstrap alerts support to [Python-Markdown].\n\n[Python-Markdown]: https://github.com/Python-Markdown/markdown\n\n\n## Installation\n\n### Install from PyPI\n\n```\n$ python -m pip install mdx_alerts\n```\n\n### Install locally using poetry\n\nUse `poetry build` to build the extensions.\nThen, you can install it via pip:\n\n```shell\n$ python -m pip install dist/mdx_alerts-1.0.0-py3-none-any.whl\n```\n\n\n## Usage\n\nThere are two different ways to use the extensions.\nEither, by using its identifier `mdx_alerts`:\n\n```python\n>>> import markdown\n>>> md = markdown.Markdown(extensions=["mdx_alerts"])\n```\n\n... or by supplying an instance of `AlertExtension`:\n\n```python\n>>> import markdown\n>>> from mdx_alerts import AlertExtension\n>>> md = markdown.Markdown(extensions=[AlertExtension()])\n```\n\n\n## Markdown pattern and customization\n\nThe pattern starts with two colons follows by the alert level, e.g. info.\nEverything after the newline character is counted towards the alert message/body until on an empty line the two colons appear again.\n\n```markdown\n:: info\nThis is the body.\n\nEven multi-line is possible.\n::\n```\n\nThe above snippet results in:\n\n```html\n<div class="alert alert-info" role="alert">\n    <h4 class="alert-heading"><strong>Info</strong></h4>\n    <p>This is the body.</p>\n    <p>Even multi-line is possible.</p>\n</div>\n```\n\nAdditionally, you can overwrite the default heading by supplying an alternative via the `heading=` attribute after the alert level:\n\n```markdown\n:: info heading="Alternative Heading"\nThis is the body.\n::\n```\n\n... which results in:\n\n```html\n<div class="alert alert-info" role="alert">\n    <h4 class="alert-heading"><strong>Alternative Heading</strong></h4>\n    <p>This is the body.</p>\n</div>\n```\n',
    'author': 'Florian Dahlitz',
    'author_email': 'f2dahlitz@freenet.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DahlitzFlorian/python-markdown-bootstrap-alerts',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
