# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['ntfsfind']
install_requires = \
['mft>=0.5.3,<0.6.0', 'ntfsdump>=2.0.0,<3.0.0', 'pytsk3>=20210419,<20210420']

entry_points = \
{'console_scripts': ['ntfsfind = ntfsfind:ntfsfind']}

setup_kwargs = {
    'name': 'ntfsfind',
    'version': '2.0.0',
    'description': '',
    'long_description': "# ntfsfind\n\n[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)\n[![PyPI version](https://badge.fury.io/py/ntfsfind.svg)](https://badge.fury.io/py/ntfsfind)\n[![Python Versions](https://img.shields.io/pypi/pyversions/ntfsfind.svg)](https://pypi.org/project/ntfsfind/)\n[![DockerHub Status](https://shields.io/docker/cloud/build/sumeshi/ntfsfind)](https://hub.docker.com/r/sumeshi/ntfsfind)\n\n![ntfsfind](https://gist.githubusercontent.com/sumeshi/c2f430d352ae763273faadf9616a29e5/raw/baa85b045e0043914218cf9c0e1d1722e1e7524b/ntfsfind.svg)\n\nA tool for search file paths from an NTFS volume on a Raw Image file.\n\n## Usage\n\n```bash\n$ ntfsfind <query_regex> ./path/to/your/imagefile.raw\n```\n\n### Example\n\n```.bash\n$ ntfsfind '.*\\.evtx' ./path/to/your/imagefile.raw\n```\n\n### Options\n```\n--volume-num, -n:\n    NTFS volume number(default 2, because volume1 is recovery partition).\n```\n\n## Installation\n\n### via PyPI\n\n```\n$ pip install ntfsfind\n```\n\n## Run with Docker\nhttps://hub.docker.com/r/sumeshi/ntfsfind\n\n\n```bash\n$ docker run -t --rm -v $(pwd):/app/work sumeshi/ntfsfind:latest '/\\$MFT' /app/work/sample.raw\n```\n\n## Contributing\n\nThe source code for ntfsfind is hosted at GitHub, and you may download, fork, and review it from this repository(https://github.com/sumeshi/ntfsfind).  \nPlease report issues and feature requests. :sushi: :sushi: :sushi:\n\n## License\n\nntfsfind is released under the [MIT](https://github.com/sumeshi/ntfsfind/blob/master/LICENSE) License.\n\nPowered by [pytsk3](https://github.com/py4n6/pytsk).  ",
    'author': 'sumeshi',
    'author_email': 'j15322sn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sumeshi/ntfsfind',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
