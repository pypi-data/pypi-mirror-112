# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory',
 'understory.indieweb',
 'understory.indieweb.indieauth',
 'understory.indieweb.indieauth.client',
 'understory.indieweb.indieauth.client.templates',
 'understory.indieweb.indieauth.server',
 'understory.indieweb.indieauth.server.templates',
 'understory.indieweb.indieauth.templates',
 'understory.indieweb.micropub',
 'understory.indieweb.micropub.templates',
 'understory.indieweb.microsub',
 'understory.indieweb.microsub.templates',
 'understory.indieweb.templates',
 'understory.indieweb.webmention',
 'understory.indieweb.websub']

package_data = \
{'': ['*'],
 'understory.indieweb.templates': ['cache/*', 'content/*', 'people/*'],
 'understory.indieweb.webmention': ['templates/*'],
 'understory.indieweb.websub': ['templates/*']}

install_requires = \
['understory-web>=0.0.21,<0.0.22']

entry_points = \
{'console_scripts': ['loveliness = understory.loveliness:main'],
 'web.apps': ['content = understory.indieweb:content',
              'indieauth-client = understory.indieweb.indieauth:client',
              'indieauth-server = understory.indieweb.indieauth:server',
              'micropub = understory.indieweb.micropub:server',
              'microsub = understory.indieweb.microsub:server',
              'webmention = understory.indieweb.webmention:receiver',
              'websub = understory.indieweb.websub:hub']}

setup_kwargs = {
    'name': 'understory',
    'version': '0.0.39',
    'description': 'The tools that power the canopy',
    'long_description': '    ██╗   ██╗███╗   ██╗██████╗ ███████╗██████╗ ███████╗████████╗ ██████╗ ██████╗ ██╗   ██╗\n    ██║   ██║████╗  ██║██╔══██╗██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝\n    ██║   ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝███████╗   ██║   ██║   ██║██████╔╝ ╚████╔╝ \n    ██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗╚════██║   ██║   ██║   ██║██╔══██╗  ╚██╔╝  \n    ╚██████╔╝██║ ╚████║██████╔╝███████╗██║  ██║███████║   ██║   ╚██████╔╝██║  ██║   ██║   \n     ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   \n\nThe tools that power the canopy..\n\n## An IndieWeb-compatible personal website packaged and deployed\n\nInstall [Poetry](https://python-poetry.org).\n\nClone your empty website repository and descend into it. *If you\nuse a **private** GitHub repository your changes will be deployed through\nGitHub. If you use a **public** repository your changes will be deployed\nthrough PyPI.*\n\nInitialize your project and add understory as a dependency.\n\n    poetry init\n    poetry add understory\n\nCreate a file `site.py`:\n\n    from understory import indieweb\n    \n    app = indieweb.site()\n\nAdd your site\'s app as an entry point in your `pyproject.toml`:\n\n    poetry run web install site:app AliceAnderson\n\nServe your website locally in development mode:\n\n    poetry run web serve AliceAnderson\n\nOpen <a href=http://localhost:9000>localhost:9000</a> in your browser.\n\n*Develop.* For example, add a custom route:\n\n    import random\n    \n    @app.route(r"hello")\n    class SayHello:\n        return random.choice(["How you doin\'?", "What\'s happening?", "What\'s up?"])\n\nTo publish:\n\n    poetry run pkg publish patch\n\nTo deploy:\n\n    poetry run web deploy\n',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@lahacker.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
