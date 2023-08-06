# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['babelfish', 'babelfish.converters']

package_data = \
{'': ['*'], 'babelfish': ['data/*']}

setup_kwargs = {
    'name': 'babelfish',
    'version': '0.6.0b1',
    'description': 'A module to work with countries and languages',
    'long_description': '# BabelFish\nBabelFish is a Python library to work with countries and languages.\n\n[![tests](https://github.com/Diaoul/babelfish/actions/workflows/test.yml/badge.svg)](https://github.com/Diaoul/babelfish/actions/workflows/test.yml)\n\n## Usage\nBabelFish provides scripts, countries and languages from their respective ISO\nstandards and a handy way to manipulate them with converters.\n\n### Script\nScript representation from 4-letter code (ISO-15924):\n```python\n>>> import babelfish\n>>> script = babelfish.Script(\'Hira\')\n>>> script\n<Script [Hira]>\n```\n\n### Country\nCountry representation from 2-letter code (ISO-3166):\n```python\n>>> country = babelfish.Country(\'GB\')\n>>> country\n<Country [GB]>\n```\n\nBuilt-in country converters (name):\n```python\n>>> country = babelfish.Country(\'GB\')\n>>> country\n<Country [GB]>\n```\n\n### Language\nLanguage representation from 3-letter code (ISO-639-3):\n```python\n>>> language = babelfish.Language("eng")\n>>> language\n<Language [en]>\n```\n\nCountry-specific language:\n```python\n>>> language = babelfish.Language(\'por\', \'BR\')\n>>> language\n<Language [pt-BR]>\n```\n\nLanguage with specific script:\n```python\n>>> language = babelfish.Language.fromalpha2(\'sr\')\n>>> language.script = babelfish.Script(\'Cyrl\')\n>>> language\n<Language [sr-Cyrl]>\n```\n\nBuilt-in language converters (alpha2, alpha3b, alpha3t, name, scope, type and opensubtitles):\n```python\n>>> language = babelfish.Language(\'por\', \'BR\')\n>>> language.alpha2\n\'pt\'\n>>> language.scope\n\'individual\'\n>>> language.type\n\'living\'\n>>> language.opensubtitles\n\'pob\'\n>>> babelfish.Language.fromalpha3b(\'fre\')\n<Language [fr]>\n```\n\n## License\nBabelFish is licensed under the [3-clause BSD license](http://opensource.org/licenses/BSD-3-Clause>)\n\nCopyright (c) 2013, the BabelFish authors and contributors.\n',
    'author': 'Antoine Bertin',
    'author_email': 'ant.bertin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Diaoul/babelfish',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
