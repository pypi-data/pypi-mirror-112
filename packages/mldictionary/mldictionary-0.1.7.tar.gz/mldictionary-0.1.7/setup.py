# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mldictionary']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'mldictionary',
    'version': '0.1.7',
    'description': "word's dictionary for several languages",
    'long_description': '# MLDictionary\n\n## **MLDictionary** is word\'s dictionary for several language\n\n```python\n>>> from mldictionary import English\n>>> english_dictionary = English()\n>>> snake_means = english_dictionary.get_meanings(\'snake\')\n>>> len(snake_means)\n4\n>>> snake_means\n[\'a reptile with a long body and no legs: \' ...]\n...\n```\n\n<p align="center">\n    <a href="https://pypi.org/project/mldictionary/" target="_blank" align="center">\n        <img alt="PyPI" src="https://img.shields.io/pypi/v/mldictionary?color=%233f7&logo=pypi&style=plastic">    \n    </a>&nbsp&nbsp\n    <a href="https://pypi.org/project/mldictionary/" target="_blank" align="center">\n        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/mldictionary?color=%237f7&logo=pypi&style=plastic">    \n    </a>&nbsp&nbsp\n    <a href="https://pypi.org/project/mldictionary/" target="_blank" align="center">\n        <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/mldictionary?color=%237f7&logo=pypi&style=plastic">    \n    </a>\n</p>\n\n---\n\n## **Installing MLDictionary** \n\n```console\n$ pip install mldictionary\n```\nMLDictionary officially supports 3.9+.\n\n---\n\n## Some examples\n\n```python\n>>> from mldictionary import Portuguese\n>>> portuguese_dictionary = Portuguese()\n>>> vida_means = portuguese_dictionary.get_meanings(\'vida\')\n>>> vida_means\n[\'Conjunto dos hábitos e costumes de alguém; maneira de viver: tinha uma vida de milionário.\' ...]\n>>> from mldictionary import Spanish\n>>> spanish_dictionary = Spanish()\n>>> coche_means = spanish_dictionary.get_meanings(\'coche\')\n>>> coche_means\n[\'1. m. Automóvil destinado al transporte de personas y con capacidad no superior a siete plazas.\' ...]\n```\n\n---\n\n### Make your own dictionary\n```python\nfrom typing import List\n\nfrom mldictionary import Dictionary\n\nclass MyOwnDictionary(Dictionary):\n    URL = \'somedictionary.com\' #required\n    LANGUAGE = \'language name\' #requerid\n    TARGET_TAG = \'tag_where_means_is\' #depend if you\'re gonna overwrite _soup_meanings method\n    TARGET_ATTR = {\'attr\': \'attr_value\'} #depend if you\'re gonna overwrite _soup_meanings method\n\n    @classmethod\n    def _soup_meanings(cls, html_tree: str)->List[str]: #optional\n       \'\'\'\n        Method to overwrite the meanings select by Dictionary class;\n        Used when you wanna change something which comes with the meanings\n       \'\'\'\n>>> myowndictionary = MyOwnDictionary()\n>>> myowndictionary.get_meanings(\'other language word\')\n```\nTo more details, see the [wiki](https://github.com/PabloEmidio/mldictionary/wiki)\n\nAlso, it has a insightful [article on linkedin](https://www.linkedin.com/pulse/mldictionary-pablo-em%25C3%25ADdio)\n',
    'author': 'Pablo Emidio',
    'author_email': 'p.emidiodev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/mldictionary/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
