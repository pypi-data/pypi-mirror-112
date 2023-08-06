# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['copernic360_cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=8,<9',
 'imageio>=2.9.0,<3.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['copernic360 = copernic360_cli.__main__:cli']}

setup_kwargs = {
    'name': 'copernic360-cli',
    'version': '1.2.3',
    'description': "Command-line script for Kagenova's Copernic360 API",
    'long_description': "#\xa0Copernic360 command-line tool\n\nThe copernic360 command-line wraps Kagenova's Copernic360 CLI. In short, it\nallows users to post 360 images and videos and get Copernic360 configuration\nfiles back.\n\nUsers first need an account with Kagenova's\n[Copernic360](https://kagenova.com/products/copernic360/) product. After\ninstalling the tool via [pip](https://pypi.org/project/copernic360_cli), users\ncan interact with the Copernic360 API as follows:\n\n```bash\n# get help\ncopernic360 --help\n# check user login\ncopernic350 check-login\n# check user's credits\ncopernic350 check-credit\n# uploaad image.jpg and get its configution back (config.6dof)\ncopernic360 process-content image.jpg config.6dof\n```\n\nSee the command-line help for futher functionality and parameters.",
    'author': 'Kagenova',
    'author_email': None,
    'maintainer': "Mayeul d'Avezac",
    'maintainer_email': 'mayeul.davezac@kagenova.com',
    'url': 'https://kagenova.com/products/copernic360/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
