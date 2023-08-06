# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libretranslate_euber']

package_data = \
{'': ['*'],
 'libretranslate_euber': ['static/*',
                          'static/css/*',
                          'static/fonts/*',
                          'static/js/*',
                          'templates/*']}

install_requires = \
['APScheduler>=3.7.0,<4.0.0',
 'Flask-Limiter>=1.4,<2.0',
 'Flask>=2.0.1,<3.0.0',
 'Morfessor>=2.0.6,<3.0.0',
 'PyICU>=2.7.4,<3.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'argostranslate>=1.4.0,<2.0.0',
 'expiringdict>=1.2.1,<2.0.0',
 'flask-swagger-ui>=3.36.0,<4.0.0',
 'flask-swagger>=0.2.14,<0.3.0',
 'polyglot>=16.7.4,<17.0.0',
 'pycld2>=0.41,<0.42',
 'pysqlite3>=0.4.6,<0.5.0',
 'waitress>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['libretranslate-euber = libretranslate_euber.main:main']}

setup_kwargs = {
    'name': 'libretranslate-euber',
    'version': '0.1.0',
    'description': 'My personal porting of libretranslate',
    'long_description': None,
    'author': 'euberdeveloper',
    'author_email': 'euberdeveloper@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
