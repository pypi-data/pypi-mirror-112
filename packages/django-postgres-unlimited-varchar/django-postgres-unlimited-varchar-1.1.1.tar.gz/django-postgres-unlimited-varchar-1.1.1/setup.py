# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['django_postgres_unlimited_varchar']
install_requires = \
['django>=2,<4']

setup_kwargs = {
    'name': 'django-postgres-unlimited-varchar',
    'version': '1.1.1',
    'description': 'A tiny app adding support unlimited varchar fields in Django/Postgres.',
    'long_description': "A tiny app adding support unlimited ``varchar`` fields (no specified max length) in Django/Postgres.\n\nUsage::\n\n    from django.db import models\n    from django_postgres_unlimited_varchar import UnlimitedCharField\n\n    class Person(models.Model):\n        name = UnlimitedCharField()\n        ...\n\nWhy?\n\nOut of the box, Django has two fields for text:\n\n* ``CharField``, which is for single-line text, and has a required maximum length (the ``max_length`` argument). In the database, this creates a field of type ``varchar(LENGTH)``.\n* ``TextField``, which is for multi-line text, and has no maximum length. In the database, this creates a field of type ``text``.\n\nClearly missing is a third type: single-line, no max length. Postgres supports this as the ``varchar`` type (note the lack of a length).\n\nThis field adds that type. AFAIK there isn't any performance hit in using this, so it's suitable for any situation where there isn't a clear required max length.\n",
    'author': 'Jacob Kaplan-Moss',
    'author_email': 'jacob@jacobian.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
