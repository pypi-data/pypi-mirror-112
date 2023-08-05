# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['easystruct']
setup_kwargs = {
    'name': 'easystruct',
    'version': '0.1.0',
    'description': 'A Python library to make the usage of struct from the stdlib a little bit easier.',
    'long_description': '# easy-struct\nA Python library to make the usage of struct from the stdlib a little bit easier.\n\n## Installation\n\n```bash\npip3 install easy-struct\n```\n',
    'author': 'zocker_160',
    'author_email': 'zocker1600@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zocker-160/simple-struct',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
