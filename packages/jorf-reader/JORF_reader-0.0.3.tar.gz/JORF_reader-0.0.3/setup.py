# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jorf_reader']

package_data = \
{'': ['*'], 'jorf_reader': ['JOs/*']}

install_requires = \
['dateparser>=1.0.0,<2.0.0',
 'jellyfish>=0.8.2,<0.9.0',
 'py-pdf-parser>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'jorf-reader',
    'version': '0.0.3',
    'description': 'Small python script to parse a pdf from https://www.legifrance.gouv.fr in order to search for all persons that obtained the French nationality within the pdf file. Keeps track of number of persons, name, origin, and department of a specific series (54 series by year).',
    'long_description': '# Naturalisation\nSmall python script to parse a pdf from https://www.legifrance.gouv.fr in order to search for all persons that obtained the French nationality within the pdf file.\nKeeps track of number of persons, name, origin, and department of a specific series (54 series by year).\n',
    'author': 'Alejandro VILLARREAL LARRAURI',
    'author_email': 'alex.villarreal.larrauri@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AlexVillarra/Naturalisation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
