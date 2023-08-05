# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stickybeak',
 'stickybeak.dj',
 'stickybeak.vendored',
 'stickybeak.vendored.pip',
 'stickybeak.vendored.pip._internal',
 'stickybeak.vendored.pip._internal.cli',
 'stickybeak.vendored.pip._internal.commands',
 'stickybeak.vendored.pip._internal.distributions',
 'stickybeak.vendored.pip._internal.index',
 'stickybeak.vendored.pip._internal.models',
 'stickybeak.vendored.pip._internal.network',
 'stickybeak.vendored.pip._internal.operations',
 'stickybeak.vendored.pip._internal.operations.build',
 'stickybeak.vendored.pip._internal.operations.install',
 'stickybeak.vendored.pip._internal.req',
 'stickybeak.vendored.pip._internal.resolution',
 'stickybeak.vendored.pip._internal.resolution.legacy',
 'stickybeak.vendored.pip._internal.resolution.resolvelib',
 'stickybeak.vendored.pip._internal.utils',
 'stickybeak.vendored.pip._internal.vcs',
 'stickybeak.vendored.pip._vendor',
 'stickybeak.vendored.pip._vendor.cachecontrol',
 'stickybeak.vendored.pip._vendor.cachecontrol.caches',
 'stickybeak.vendored.pip._vendor.certifi',
 'stickybeak.vendored.pip._vendor.chardet',
 'stickybeak.vendored.pip._vendor.chardet.cli',
 'stickybeak.vendored.pip._vendor.colorama',
 'stickybeak.vendored.pip._vendor.distlib',
 'stickybeak.vendored.pip._vendor.distlib._backport',
 'stickybeak.vendored.pip._vendor.html5lib',
 'stickybeak.vendored.pip._vendor.html5lib._trie',
 'stickybeak.vendored.pip._vendor.html5lib.filters',
 'stickybeak.vendored.pip._vendor.html5lib.treeadapters',
 'stickybeak.vendored.pip._vendor.html5lib.treebuilders',
 'stickybeak.vendored.pip._vendor.html5lib.treewalkers',
 'stickybeak.vendored.pip._vendor.idna',
 'stickybeak.vendored.pip._vendor.msgpack',
 'stickybeak.vendored.pip._vendor.packaging',
 'stickybeak.vendored.pip._vendor.pep517',
 'stickybeak.vendored.pip._vendor.pkg_resources',
 'stickybeak.vendored.pip._vendor.progress',
 'stickybeak.vendored.pip._vendor.requests',
 'stickybeak.vendored.pip._vendor.resolvelib',
 'stickybeak.vendored.pip._vendor.resolvelib.compat',
 'stickybeak.vendored.pip._vendor.toml',
 'stickybeak.vendored.pip._vendor.urllib3',
 'stickybeak.vendored.pip._vendor.urllib3.contrib',
 'stickybeak.vendored.pip._vendor.urllib3.contrib._securetransport',
 'stickybeak.vendored.pip._vendor.urllib3.packages',
 'stickybeak.vendored.pip._vendor.urllib3.packages.backports',
 'stickybeak.vendored.pip._vendor.urllib3.packages.ssl_match_hostname',
 'stickybeak.vendored.pip._vendor.urllib3.util',
 'stickybeak.vendored.pip._vendor.webencodings']

package_data = \
{'': ['*']}

install_requires = \
['dill', 'requests', 'typing-extensions', 'virtualenv']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.9']}

setup_kwargs = {
    'name': 'stickybeak',
    'version': '0.7.5',
    'description': 'Package that makes e2e tests easy.',
    'long_description': None,
    'author': 'Damian Krystkiewicz',
    'author_email': 'damian.krystkiewicz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reloadware/stickybeak',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
