# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tortoise',
 'tortoise.backends',
 'tortoise.backends.asyncpg',
 'tortoise.backends.base',
 'tortoise.backends.mysql',
 'tortoise.backends.sqlite',
 'tortoise.contrib',
 'tortoise.contrib.aiohttp',
 'tortoise.contrib.fastapi',
 'tortoise.contrib.mysql',
 'tortoise.contrib.postgres',
 'tortoise.contrib.pydantic',
 'tortoise.contrib.pylint',
 'tortoise.contrib.quart',
 'tortoise.contrib.sanic',
 'tortoise.contrib.starlette',
 'tortoise.contrib.test',
 'tortoise.fields']

package_data = \
{'': ['*']}

install_requires = \
['aiosqlite>=0.16.0,<0.17.0',
 'iso8601>=0.1.13,<0.2.0',
 'pypika-tortoise>=0.1.1,<0.2.0',
 'pytz']

extras_require = \
{'accel': ['python-rapidjson'],
 'accel:sys_platform != "win32" and implementation_name == "cpython"': ['ciso8601>=2.1.2,<3.0.0',
                                                                        'uvloop>=0.14.0,<0.15.0'],
 'aiomysql': ['aiomysql'],
 'asyncmy': ['asyncmy'],
 'asyncpg': ['asyncpg'],
 'docs': ['sphinx', 'cloud_sptheme', 'Pygments', 'docutils']}

setup_kwargs = {
    'name': 'tortoise-orm',
    'version': '0.17.5',
    'description': 'Easy async ORM for python, built with relations in mind',
    'long_description': '============\nTortoise ORM\n============\n\n.. image:: https://badges.gitter.im/tortoise/community.png\n   :target: https://gitter.im/tortoise/community\n.. image:: https://img.shields.io/pypi/v/tortoise-orm.svg?style=flat\n   :target: https://pypi.python.org/pypi/tortoise-orm\n.. image:: https://readthedocs.org/projects/tortoise-orm/badge/?version=latest\n   :target: http://tortoise-orm.readthedocs.io/en/latest/\n.. image:: https://pepy.tech/badge/tortoise-orm/month\n   :target: https://pepy.tech/project/tortoise-orm\n.. image:: https://github.com/tortoise/tortoise-orm/workflows/ci/badge.svg\n   :target: https://github.com/tortoise/tortoise-orm/actions?query=workflow:ci\n.. image:: https://coveralls.io/repos/github/tortoise/tortoise-orm/badge.svg\n   :target: https://coveralls.io/github/tortoise/tortoise-orm\n.. image:: https://api.codacy.com/project/badge/Grade/b5b77021ba284e4a9e0c033a4611b046\n   :target: https://app.codacy.com/app/Tortoise/tortoise-orm\n\nIntroduction\n============\n\nTortoise ORM is an easy-to-use ``asyncio`` ORM *(Object Relational Mapper)* inspired by Django.\n\nTortoise ORM was built with relations in mind and admiration for the excellent and popular Django ORM.\nIt\'s engraved in its design that you are working not with just tables, you work with relational data.\n\nYou can find the docs at `ReadTheDocs <http://tortoise-orm.readthedocs.io/en/latest/>`_\n\n.. note::\n   Tortoise ORM is a young project and breaking changes are to be expected.\n   We keep a `Changelog <http://tortoise-orm.readthedocs.io/en/latest/CHANGELOG.html>`_ and it will have possible breakage clearly documented.\n\nTortoise ORM is supported on CPython >= 3.7 for SQLite, MySQL and PostgreSQL.\n\nWhy was Tortoise ORM built?\n---------------------------\n\nPython has many existing and mature ORMs, unfortunately they are designed with an opposing paradigm of how I/O gets processed.\n``asyncio`` is relatively new technology that has a very different concurrency model, and the largest change is regarding how I/O is handled.\n\nHowever, Tortoise ORM is not the first attempt of building an ``asyncio`` ORM. While there are many cases of developers attempting to map synchronous Python ORMs to the async world, initial attempts did not have a clean API.\n\nHence we started Tortoise ORM.\n\nTortoise ORM is designed to be functional, yet familiar, to ease the migration of developers wishing to switch to ``asyncio``.\n\nIt also performs well when compared to other Python ORMs. In `our benchmarks <https://github.com/tortoise/orm-benchmarks>`_, where we measure different read and write operations (rows/sec, more is better), it\'s trading places with Pony ORM:\n\n.. image:: https://raw.githubusercontent.com/tortoise/tortoise-orm/develop/docs/ORM_Perf.png\n    :target: https://github.com/tortoise/orm-benchmarks\n\nHow is an ORM useful?\n---------------------\n\nWhen you build an application or service that uses a relational database, there is a point where you can\'t get away with just using parameterized queries or even query builder. You just keep repeating yourself, writing slightly different code for each entity.\nCode has no idea about relations between data, so you end up concatenating your data almost manually.\nIt is also easy to make mistakes in how you access your database, which can be exploited by SQL-injection attacks.\nYour data rules are also distributed, increasing the complexity of managing your data, and even worse, could lead to those rules being applied inconsistently.\n\nAn ORM (Object Relational Mapper) is designed to address these issues, by centralising your data model and data rules, ensuring that your data is managed safely (providing immunity to SQL-injection) and keeping track of relationships so you don\'t have to.\n\nGetting Started\n===============\n\nInstallation\n------------\nFirst you have to install Tortoise ORM like this:\n\n.. code-block:: bash\n\n    pip install tortoise-orm\n\nYou can also install with your db driver (`aiosqlite` is builtin):\n\n.. code-block:: bash\n\n    pip install tortoise-orm[asyncpg]\n\n\nOr for MySQL:\n\n.. code-block:: bash\n\n    pip install tortoise-orm[aiomysql]\n\nOr another asyncio MySQL driver `asyncmy <https://github.com/long2ice/asyncmy>`_:\n\n.. code-block:: bash\n\n    pip install tortoise-orm[asyncmy]\n\nQuick Tutorial\n--------------\n\nThe primary entity of tortoise is ``tortoise.models.Model``.\nYou can start writing models like this:\n\n\n.. code-block:: python3\n\n    from tortoise.models import Model\n    from tortoise import fields\n\n    class Tournament(Model):\n        id = fields.IntField(pk=True)\n        name = fields.TextField()\n\n        def __str__(self):\n            return self.name\n\n\n    class Event(Model):\n        id = fields.IntField(pk=True)\n        name = fields.TextField()\n        tournament = fields.ForeignKeyField(\'models.Tournament\', related_name=\'events\')\n        participants = fields.ManyToManyField(\'models.Team\', related_name=\'events\', through=\'event_team\')\n\n        def __str__(self):\n            return self.name\n\n\n    class Team(Model):\n        id = fields.IntField(pk=True)\n        name = fields.TextField()\n\n        def __str__(self):\n            return self.name\n\n\nAfter you defined all your models, tortoise needs you to init them, in order to create backward relations between models and match your db client with the appropriate models.\n\nYou can do it like this:\n\n.. code-block:: python3\n\n    from tortoise import Tortoise\n\n    async def init():\n        # Here we connect to a SQLite DB file.\n        # also specify the app name of "models"\n        # which contain models from "app.models"\n        await Tortoise.init(\n            db_url=\'sqlite://db.sqlite3\',\n            modules={\'models\': [\'app.models\']}\n        )\n        # Generate the schema\n        await Tortoise.generate_schemas()\n\n\nHere we create a connection to an SQLite database in the local directory called ``db.sqlite3``. Then we discover and initialise the models.\n\nTortoise ORM currently supports the following databases:\n\n* SQLite (requires ``aiosqlite``)\n* PostgreSQL (requires ``asyncpg``)\n* MySQL (requires ``aiomysql``)\n\n``generate_schema`` generates the schema on an empty database. Tortoise generates schemas in safe mode by default which\nincludes the ``IF NOT EXISTS`` clause, so you may include it in your main code.\n\n\nAfter that you can start using your models:\n\n.. code-block:: python3\n\n    # Create instance by save\n    tournament = Tournament(name=\'New Tournament\')\n    await tournament.save()\n\n    # Or by .create()\n    await Event.create(name=\'Without participants\', tournament=tournament)\n    event = await Event.create(name=\'Test\', tournament=tournament)\n    participants = []\n    for i in range(2):\n        team = await Team.create(name=\'Team {}\'.format(i + 1))\n        participants.append(team)\n\n    # M2M Relationship management is quite straightforward\n    # (also look for methods .remove(...) and .clear())\n    await event.participants.add(*participants)\n\n    # You can query a related entity with async for\n    async for team in event.participants:\n        pass\n\n    # After making a related query you can iterate with regular for,\n    # which can be extremely convenient when using it with other packages,\n    # for example some kind of serializers with nested support\n    for team in event.participants:\n        pass\n\n\n    # Or you can make a preemptive call to fetch related objects\n    selected_events = await Event.filter(\n        participants=participants[0].id\n    ).prefetch_related(\'participants\', \'tournament\')\n\n    # Tortoise supports variable depth of prefetching related entities\n    # This will fetch all events for Team and in those events tournaments will be prefetched\n    await Team.all().prefetch_related(\'events__tournament\')\n\n    # You can filter and order by related models too\n    await Tournament.filter(\n        events__name__in=[\'Test\', \'Prod\']\n    ).order_by(\'-events__participants__name\').distinct()\n\nMigration\n=========\n\nTortoise ORM uses `Aerich <https://github.com/tortoise/aerich>`_ as its database migration tool, see more detail at its `docs <https://github.com/tortoise/aerich>`_.\n\nContributing\n============\n\nPlease have a look at the `Contribution Guide <docs/CONTRIBUTING.rst>`_.\n\n\nLicense\n=======\n\nThis project is licensed under the Apache License - see the `LICENSE.txt <LICENSE.txt>`_ file for details.\n',
    'author': 'Andrey Bondar',
    'author_email': 'andrey@bondar.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tortoise/tortoise-orm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
