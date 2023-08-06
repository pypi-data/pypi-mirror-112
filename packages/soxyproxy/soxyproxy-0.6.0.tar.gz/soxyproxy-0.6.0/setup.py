# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soxyproxy',
 'soxyproxy.internal',
 'soxyproxy.models',
 'soxyproxy.models.socks4',
 'soxyproxy.models.socks5']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'passlib>=1.7.4,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'soxyproxy',
    'version': '0.6.0',
    'description': 'Pure Python SOCKS proxy server implementation',
    'long_description': '# SoxyProxy\n\n## Getting Started\n\n### Installing\n\nSoxyProxy can be installed using pip:\n\n```bash\npip install soxyproxy\n```\n\n## Usage\n\nTo test that installation was successful, try:\n\n```bash\npython -m soxyproxy --help\n```\n\n## Features\n\n### Protocols\n\n- [x] SOCKS4\n\n- [x] SOCKS5\n\n  * Protocols\n    * [x] TCP\n    * [ ] UDP\n\n  * Auth\n    * [x] None\n    * [x] Login/Password\n    * [ ] GSSAPI\n\n  * CMC\n    * [x] Connect\n    * [ ] Bind\n    * [ ] ASSOCIATE\n\n  * ADDR\n    * [x] IPv4\n    * [x] IPv6\n    * [x] Domain\n\n## Configuration\n\n### Apache-Like Authentication (htpasswd)\n\nhttps://pypi.org/project/pypiserver/#apache-like-authentication-htpasswd\n\n### Rulesets\n',
    'author': 'Aleksandr Shpak',
    'author_email': 'shpaker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shpaker/soxyproxy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
