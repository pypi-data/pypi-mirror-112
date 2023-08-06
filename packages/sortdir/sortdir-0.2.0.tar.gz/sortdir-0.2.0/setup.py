# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sortdir']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0', 'toml>=0.10.2,<0.11.0', 'watchdog>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['sortdir = sortdir:__main__']}

setup_kwargs = {
    'name': 'sortdir',
    'version': '0.2.0',
    'description': 'Sorting directory files made easy.',
    'long_description': '#+TITLE: sortdir\n\n#+BEGIN_QUOTE\nTool to keep your directories clean\n#+END_QUOTE\n\n* Table of contents :TOC_2:\n- [[#installation][Installation]]\n- [[#usage][Usage]]\n- [[#configuration][Configuration]]\n  - [[#example][Example]]\n\n* Installation\n#+BEGIN_SRC shell\npip install sortdir\n#+END_SRC\n\n* Usage\nWhen you run the following command the tool will at first perform initial sorting and then start a server which will be watching for new files and moving them to their destination subdirectories defined in your config\n\n#+BEGIN_SRC shell\nsortdir\n#+END_SRC\n\n* Configuration\nCreate a config file in one of the following locations:\n- ~$HOME/.sortdir.toml~\n- ~$HOME/.config/sortdir/config.toml~\n\n** Example\n#+BEGIN_SRC toml\n[directories]\n\n    [directories."~/Downloads"]\n    documents = [\n        ".doc",\n        ".docx",\n        ".ods",\n        ".odt",\n        ".pdf",\n        ".ppt",\n        ".pptx",\n        ".txt",\n        ".xls",\n        ".xlsx",\n    ]\n    images = [".gif", ".heic", ".png", ".jpeg", ".jpg"]\n\n    [directories."~/dev"]\n    python = [".py"]\n    javascript = [".js"]\n#+END_SRC\n',
    'author': 'Yevhen Shymotiuk',
    'author_email': 'yevhenshymotiuk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yevhenshymotiuk/sortdir',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
