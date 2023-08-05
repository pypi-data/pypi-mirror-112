# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gingerit']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'gingerit',
    'version': '0.8.2',
    'description': 'Correcting spelling and grammar mistakes based on the context of complete entences. Wrapper around the gingersoftware.com API',
    'long_description': "===============================\nGingerit\n===============================\n\n.. image:: https://github.com/Azd325/gingerit/workflows/Python%20package/badge.svg\n\n.. image:: https://img.shields.io/pypi/v/gingerit.svg\n        :target: https://pypi.python.org/pypi/gingerit\n\n\nCorrecting spelling and grammar mistakes based on the context of complete sentences. Wrapper around the gingersoftware.com API\n\n* Free software: MIT license\n* Documentation: https://gingerit.readthedocs.org.\n\nInstallation:\n-------------\n\n::\n\n    pip install gingerit\n\nUsage:\n------\n\n::\n\n    from gingerit.gingerit import GingerIt\n\n    text = 'The smelt of fliwers bring back memories.'\n\n    parser = GingerIt()\n    parser.parse(text)\n\nTODO:\n-----\n\n    - Commandline Tool\n\n\nThanks\n------\n\nThank you for  `Ginger Proofreader <http://www.gingersoftware.com/>`_ for such awesome service. Hope they will keep it free :)\n\nThanks to @subosito for this inspriration `Gingerice <https://github.com/subosito/gingerice>`_\n",
    'author': 'Tim Kleinschmdit',
    'author_email': 'tim.kleinschmidt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Azd325/gingerit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
