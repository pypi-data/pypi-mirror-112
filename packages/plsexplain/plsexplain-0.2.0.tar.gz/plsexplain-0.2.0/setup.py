# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plsexplain']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0,<0.8.0',
 'click>=8.0.1,<9.0.0',
 'dalex>=1.2.0,<2.0.0',
 'fastapi>=0.65.2,<0.66.0',
 'joblib>=1.0.1,<2.0.0',
 'pandas>=1.2.5,<2.0.0',
 'progressbar2>=3.53.1,<4.0.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'tqdm>=4.61.1,<5.0.0',
 'uvicorn[standard]>=0.14.0,<0.15.0']

entry_points = \
{'console_scripts': ['plsexplain = plsexplain.cli:main']}

setup_kwargs = {
    'name': 'plsexplain',
    'version': '0.2.0',
    'description': 'Create an explainable AI dashboard for your machine learning model.',
    'long_description': "![plsexplain logo](assets/logo_transparent_background.png)\n\n---\n\nCreate an explainable AI dashboard for your machine learning model. plsexplain,\nor please, explain is a question that you may want to ask your computer after\nyou've trained a machine learning model.\n\n---\n\n[![package](https://badge.fury.io/py/plsexplain.svg)](https://pypi.org/project/plsexplain/)\n[![downloads](https://img.shields.io/pypi/dm/plsexplain.svg)](https://pypi.org/project/plsexplain/)\n[![continuous-integration](https://github.com/wmeints/plsexplain/actions/workflows/ci.yml/badge.svg)](https://github.com/wmeints/plsexplain/actions/workflows/ci.yml)\n\n## Getting started\n\nYou can install this tool as a python package on your machine by using the\nfollowing command in your favorite shell:\n\n```shell\npip install plsexplain\n```\n\nAfter you've installed the package, use the following command to get an\nexplainable AI dashboard for your trained model:\n\n```shell\nplsexplain <path-to-model> <path-to-sample-set>\n```\n\nCurrently, we support models trained with scikit-learn, but we're planning on\nsupporting tensorflow and pytorch as well.\n\nThe sample set, is a small dataset containing samples you want to use in the\ndashboard for explanations based on sample data. We only support using\nCSV files at the moment.\n\n## Documentation\n\nPlease refer to the documentation for more information on how to use the tool\nfor various types of models and sample datasets.\n\n[📖 Read the documentation][DOCUMENTATION]\n\n## Contributing\n\nWe welcome contributions to this project. Please refer to the\ndeveloper guide for more information on how to submit\nissues and pull requests for this project.\n\n[🛠 Read the developer guide][CONTRIBUTOR_GUIDE]\n\n## Code of conduct\n\nPlease make sure to follow our [code of conduct][CODE_OF_CONDUCT] when\ninteracting with other contributors on this project.\n\n[CODE_OF_CONDUCT]: CODE_OF_CONDUCT.md\n[CONTRIBUTOR_GUIDE]: https://wmeints.github.io/plsexplain/contributing/index.html\n[DOCUMENTATION]: https://wmeints.github.io/plsexplain",
    'author': 'Willem Meints',
    'author_email': 'willem.meints@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://wmeints.github.io/plsexplain',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
