# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['txt2ebook']

package_data = \
{'': ['*']}

install_requires = \
['EbookLib>=0.17.1,<0.18.0', 'Markdown>=3.3.4,<4.0.0', 'click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['txt2ebook = txt2ebook.txt2ebook:main']}

setup_kwargs = {
    'name': 'txt2ebook',
    'version': '0.1.1',
    'description': 'Console tool to convert txt file to different ebook format',
    'long_description': "# txt2ebook\n\nConsole tool to convert txt file to different ebook format.\n\n## Installation\n\nFrom PyPI:\n\n```\npip install txt2ebook\n```\n\n## Usage\n\nShowing help message:\n\n```\ntxt2ebook --help\nUsage: txt2ebook [OPTIONS] FILENAME\n\nOptions:\n  --help  Show this message and exit.\n```\n\nIf no file was specified:\n\n```\ntxt2ebook\nUsage: txt2ebook [OPTIONS] FILENAME\nTry 'txt2ebook --help' for help.\n\nError: Missing argument 'FILENAME'.\n```\n\nConvert a txt file into epub:\n\n```\ntxt2book ebook.txt\n```\n\n## Copyright and License\n\nCopyright (C) 2021 Kian-Meng, Ang\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <https://www.gnu.org/licenses/>.\n",
    'author': 'Kian-Meng Ang',
    'author_email': 'kianmeng@cpan.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kianmeng/txt2ebook',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
