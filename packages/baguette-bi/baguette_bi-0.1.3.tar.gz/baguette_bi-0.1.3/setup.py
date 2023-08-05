# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baguette_bi',
 'baguette_bi.alembic.migrations',
 'baguette_bi.alembic.migrations.versions',
 'baguette_bi.cli',
 'baguette_bi.core',
 'baguette_bi.core.connections',
 'baguette_bi.examples',
 'baguette_bi.examples.altair_examples',
 'baguette_bi.examples.altair_examples.case_studies',
 'baguette_bi.examples.altair_examples.other',
 'baguette_bi.examples.docs',
 'baguette_bi.examples.docs.charts',
 'baguette_bi.examples.docs.charts.tutorial',
 'baguette_bi.examples.new',
 'baguette_bi.examples.new.charts',
 'baguette_bi.schema',
 'baguette_bi.server',
 'baguette_bi.server.api',
 'baguette_bi.server.models',
 'baguette_bi.server.schema',
 'baguette_bi.server.static',
 'baguette_bi.server.templates',
 'baguette_bi.server.views']

package_data = \
{'': ['*'],
 'baguette_bi': ['alembic/*'],
 'baguette_bi.examples.docs': ['pages/*',
                               'pages/docs/*',
                               'pages/docs/tutorial/*',
                               'pages/docs/tutorial/examples/*',
                               'pages/docs/tutorial/examples/final/*'],
 'baguette_bi.examples.new': ['pages/*'],
 'baguette_bi.server.static': ['css/*',
                               'css/codehilite/*',
                               'fonts/*',
                               'js/*',
                               'locales/format/*',
                               'locales/time-format/*'],
 'baguette_bi.server.templates': ['elements/*']}

install_requires = \
['Babel>=2.9.1,<3.0.0',
 'Jinja2>=3.0.1,<4.0.0',
 'Markdown>=3.3.4,<4.0.0',
 'Pygments>=2.9.0,<3.0.0',
 'SQLAlchemy>=1.4.15,<2.0.0',
 'WTForms>=2.3.3,<3.0.0',
 'aiofiles>=0.7.0,<0.8.0',
 'alembic>=1.6.5,<2.0.0',
 'altair>=4.1.0,<5.0.0',
 'fastapi[dotenv]>=0.65.1,<0.66.0',
 'gunicorn>=20.1.0,<21.0.0',
 'httptools>=0.2.0,<0.3.0',
 'itsdangerous>=2.0.1,<3.0.0',
 'passlib[bcrypt]>=1.7.4,<2.0.0',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'python-dotenv>=0.17.1,<0.18.0',
 'python-multipart>=0.0.5,<0.0.6',
 'typer>=0.3.2,<0.4.0',
 'uvicorn>=0.13.4,<0.14.0',
 'uvloop>=0.15.2,<0.16.0',
 'vega-datasets>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['baguette = baguette_bi.cli:app']}

setup_kwargs = {
    'name': 'baguette-bi',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Mikhail Akimov',
    'author_email': 'rovinj.akimov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
