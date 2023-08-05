# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['latticeconstructor']

package_data = \
{'': ['*']}

install_requires = \
['LatticeJSON>=0.1.5,<0.2.0',
 'ipykernel>=5.5.4,<6.0.0',
 'ipython>=7.23.1,<8.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'nbsphinx>=0.8.4,<0.9.0',
 'pandas>=1.2.4,<2.0.0',
 'pandoc>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'latticeconstructor',
    'version': '0.2.2',
    'description': '<Enter a one-sentence description of this project here.>',
    'long_description': '==================\nlatticeconstructor\n==================\n\n\n\nPackage to build accelerator lattice tables based on elements and their\ndefinitions. Supposed to be combined with the `latticeadaptor <https://github.com/tomerten/latticeadaptor>`_\nPackage.\n\n* Free software: MIT license\n* Documentation: https://latticeconstructor.readthedocs.io.\n\n\nFeatures\n--------\n\n* Construct accelerator element table manually\n* Edit accelerator element tables\n* Load definitions and lattice from: Elegant, Madx sequence file, Madx Line definition file. \n\nNon-standard Dependency\n-----------------------\n\n* `latticejson <https://github.com/nobeam/latticejson>`_',
    'author': 'Tom Mertens',
    'author_email': 'your.email@whatev.er',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tomerten/latticeconstructor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
