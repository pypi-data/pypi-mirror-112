# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyalko', 'pyalko.objects']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'pyalko',
    'version': '0.1.0',
    'description': 'Asynchronous python client for AL-KO Robolinho Mowers.',
    'long_description': '# PyAlko\n\nAsynchronous python client for AL-KO Robolinho Mowers.\nThis package allows you to interact with AL-KO API to control your robolinho mower.\n\nTested with:\n- AL-KO Robolinho 800W\n\n## Installation\n\n```bash\npip install pyalko\n```\n\n## Attributions\n- [@timmo001](https://github.com/timmo001) for source of inspiration with his [aiolyric package](https://github.com/timmo001/aiolyric).\n- [@ludeeus](https://github.com/ludeeus) for his generator class.\n\n#\n\n⭐️ this repository if you found it useful ❤️\n\n<a href="https://www.buymeacoffee.com/jonkristian" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/white_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>',
    'author': 'Jon Kristian Nilsen',
    'author_email': 'hello@jonkristian.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jonkristian/pyalko',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
