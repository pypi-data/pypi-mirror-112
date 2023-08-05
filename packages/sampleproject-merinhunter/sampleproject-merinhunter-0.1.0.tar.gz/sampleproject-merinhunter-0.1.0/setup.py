# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sample']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sampleproject-merinhunter',
    'version': '0.1.0',
    'description': 'A sample Python project',
    'long_description': '# A sample Python project\n\n![Python Logo](https://www.python.org/static/community_logos/python-logo.png "Sample inline image")\n\nA sample project that exists as an aid to the [Python Packaging User\nGuide][packaging guide]\'s [Tutorial on Packaging and Distributing\nProjects][distribution tutorial].\n\nThis project does not aim to cover best practices for Python project\ndevelopment as a whole. For example, it does not provide guidance or tool\nrecommendations for version control, documentation, or testing.\n\n[The source for this project is available here][src].\n\nMost of the configuration for a Python project is done in the `setup.py` file,\nan example of which is included in this project. You should edit this file\naccordingly to adapt this sample project to your needs.\n\n----\n\nThis is the README file for the project.\n\nThe file should use UTF-8 encoding and can be written using\n[reStructuredText][rst] or [markdown][md use] with the appropriate [key set][md\nuse]. It will be used to generate the project webpage on PyPI and will be\ndisplayed as the project homepage on common code-hosting services, and should be\nwritten for that purpose.\n\nTypical contents for this file would include an overview of the project, basic\nusage examples, etc. Generally, including the project changelog in here is not a\ngood idea, although a simple “What\'s New” section for the most recent version\nmay be appropriate.\n\n[packaging guide]: https://packaging.python.org\n[distribution tutorial]: https://packaging.python.org/tutorials/packaging-projects/\n[src]: https://github.com/pypa/sampleproject\n[rst]: http://docutils.sourceforge.net/rst.html\n[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"\n[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional\n',
    'author': 'A. Random Developer',
    'author_email': 'author@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pypa/sampleproject',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
