# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asgi_typing']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'jetblack-asgi-typing',
    'version': '0.3.0',
    'description': 'Just the types for ASGI',
    'long_description': '# jetblack-asgi-typing\n\nJust the types for ASGI.\n\nTaken from [asgiref](https://github.com/django/asgiref)\nand [hypercorn](https://gitlab.com/pgjones/hypercorn).\n\n## Installation\n\nFrom `pypi.org`:\n\n```bash\npip install jetblack-asgi-typing\n```\n\n## Usage\n\n```python\n\nfrom asgi_typing import (\n    Scope,\n    ASGIReceiveCallable,\n    ASGISendCallable\n)\n\nasync def app(\n        scope: Scope,\n        receive: ASGIReceiveCallable,\n        send: ASGISendCallable\n) -> None:\n    # Implement your ASGI application here.\n    pass\n```\n',
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/jetblack-asgi-typing',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
