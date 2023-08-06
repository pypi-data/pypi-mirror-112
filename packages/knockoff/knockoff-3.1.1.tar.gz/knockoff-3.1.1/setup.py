# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['knockoff',
 'knockoff.factory',
 'knockoff.sdk',
 'knockoff.sdk.factory',
 'knockoff.sdk.factory.next_strategy',
 'knockoff.utilities',
 'knockoff.utilities.date',
 'knockoff.utilities.orm',
 'knockoff.writer']

package_data = \
{'': ['*']}

install_requires = \
['dotty_dict>=1.2.1',
 'enum34>=1.1.9',
 'faker>=3.0.1',
 'ipython>=5.9.0',
 'joblib>=0.14.1',
 'networkx>=2.2',
 'numpy>=1.16.6',
 'pandas>=0.24.2',
 'psycopg2>=2.8.4',
 'pyaml>=19.12.0',
 'pyarrow>=0.15.1',
 'python-interface>=1.5.3',
 's3fs>=0.2.2',
 'six>=1.12.0',
 'sqlalchemy-utils>=0.32.12',
 'testing.postgresql>=1.3.0']

extras_require = \
{'complete': ['Pyrseas>=0.9.0']}

entry_points = \
{'console_scripts': ['knockoff = knockoff.cli:main'],
 'knockoff.factory.component.function': ['numpy.random.poisson = '
                                         'numpy.random:poisson'],
 'knockoff.factory.sink.dump_strategy': ['noop = knockoff.utilities.mixin:noop',
                                         'parquet = '
                                         'knockoff.writer.pandas:to_parquet',
                                         'sql = knockoff.writer.pandas:to_sql'],
 'knockoff.factory.source.component.load_strategy': ['autoincrement = '
                                                     'knockoff.factory.component:load_autoincrement',
                                                     'faker = '
                                                     'knockoff.factory.counterfeit:load_faker_component_generator',
                                                     'function = '
                                                     'knockoff.utilities.mixin:noop',
                                                     'knockoff = '
                                                     'knockoff.utilities.mixin:noop'],
 'knockoff.factory.source.part.load_strategy': ['cartesian-product = '
                                                'knockoff.factory.part:cartesian_product_strategy',
                                                'concat = '
                                                'knockoff.factory.part:concat_strategy',
                                                'faker = '
                                                'knockoff.factory.counterfeit:load_faker',
                                                'inline = '
                                                'knockoff.factory.part:read_part_inline',
                                                'io = '
                                                'knockoff.io:load_strategy_io',
                                                'period = '
                                                'knockoff.factory.part:generate_part_periods'],
 'knockoff.factory.source.prototype.load_strategy': ['components = '
                                                     'knockoff.factory.prototype:load_prototype_from_components',
                                                     'concat = '
                                                     'knockoff.factory.part:concat_strategy',
                                                     'io = '
                                                     'knockoff.io:load_strategy_io'],
 'knockoff.factory.source.table.load_strategy': ['io = '
                                                 'knockoff.io:load_strategy_io',
                                                 'knockoff = '
                                                 'knockoff.factory.table:load_knockoff'],
 'knockoff.io.readers': ['inline = knockoff.io:read_inline',
                         'pandas.read_csv = pandas:read_csv',
                         'pandas.read_json = pandas:read_json',
                         'pandas.read_parquet = pandas:read_parquet',
                         'read_multi_parquet = knockoff.io:read_multi_parquet',
                         'sql = knockoff.io:read_sql']}

setup_kwargs = {
    'name': 'knockoff',
    'version': '3.1.1',
    'description': 'Library for generating and bootstrapping mock data',
    'long_description': 'Knockoff Factory\n---\n[![codecov](https://codecov.io/gh/Nike-Inc/knockoff-factory/branch/master/graph/badge.svg?token=93wOmtZxIk)](https://codecov.io/gh/Nike-Inc/knockoff-factory)\n[![Test](https://github.com/Nike-Inc/knockoff-factory/actions/workflows/python-test.yaml/badge.svg)](https://github.com/Nike-Inc/knockoff-factory/actions/workflows/python-test.yaml) \n[![PyPi Release](https://github.com/Nike-Inc/knockoff-factory/actions/workflows/python-build.yaml/badge.svg)](https://github.com/Nike-Inc/knockoff-factory/actions/workflows/python-build.yaml) \n[![Docker Build](https://github.com/Nike-Inc/knockoff-factory/actions/workflows/docker-build.yaml/badge.svg)](https://github.com/Nike-Inc/knockoff-factory/actions/workflows/docker-build.yaml)\n\nA library for generating fake data and populating database tables.\n\n# Run poetry install/update with psycopg2\n\nRequirements:\n* postgresql (`brew install postrgresql`)\n\nRun the following command:\n```shell script\npg_config | grep "LDFLAGS ="\n```\nOutput:\n> LDFLAGS = -L/usr/local/opt/openssl@1.1/lib -L/usr/local/opt/readline/lib -Wl,-dead_strip_dylibs\n\nTake the value of `LDFLAGS` and set that environment variable. E.g.:\n```shell script\nexport LDFLAGS="-L/usr/local/opt/openssl@1.1/lib -L/usr/local/opt/readline/lib -Wl,-dead_strip_dylibs"\n``` \nYou should now be able to run poetry install and/or update commands without failing on psycopg2.\n\n\n### Local Postgres Setup\nThe following steps can be used to setup a local postgres instance for testing.\n\n#### Requirements\n* docker\n* poetry (`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`)\n* postgresql (`brew install postgresql`) or pgcli (`brew install pgcli`) \n  \n#### Run Postgres\n1. Pull docker image `docker pull postgres:11.7`\n2. Run docker container: `docker run --rm  --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432  postgres:11.7` \n    * Note: you can see the running container with `docker ps` and can terminate it with `docker kill pg-docker`\n\nYou can now access the shell with `PGPASSWORD=docker pgcli -h localhost -U postgres` or\n`PGPASSWORD=docker psql -h localhost -U postgres`.\n    \n\n## Tests\nRun unit tests\n```bash\npoetry run pytest\n```\n\nThe unit tests depend on fixtures using ephemeral postgres databases\nand/or instances. By default it will attempt to connect to an existing\ninstance at `postgresql://postgres@localhost:5432/postgres` and will\ncreate and destroy databases per fixture. This postgres location can\nbe overridden with the `KNOCKOFF_TEST_DB_URI` environment variable.\n\nIf no external postgres instance is available for testing, but postgresql is\ninstalled, the `TEST_USE_EXTERNAL_DB` environment variable can be set to `0`.\nThe fixtures will then rely on the `testing.postgresql` library to create\nephemeral postgres instances per fixture.\n\nIf postgres is not available, dependent tests can be disabled with the\nfollowing environment variable\n```bash\nexport TEST_POSTGRES_ENABLED=0\n```\n\n\n### Knockoff Configuration\n\n\n#### Creating Databases\nKnockoff will start by creating any specified databases. This section\nis optional if you do not need a database created. You can also configure\nan engine builder to use by providing the `config` parameter for each\nconfigured database (factory function used is knockoff.utilities.orm.sql.EngineBuilder.from_config)\notherwise the default engine based on knockoff environment variables will be used.\nThe following yaml will result in the following sql queries:\n* `create database mydb;`\n* `create user myuser with encrypted password \'MYUSER_PASSWORD\';`\n    * `MYUSER_PASSWORD` is replaced with the value of the corresponding environment variable\n* `grant all privileges on database mydb to myuser;`\n```yaml\ncreate-databases:\n  - name: mydb\n    type: postgres\n    users:\n      - user: myuser\n        password_env: MYUSER_PASSWORD\n```\n\n#### Load existing table definitions\nKnockoff uses [Pyrseas](https://github.com/perseas/Pyrseas)\'s yamltodb tool to load existing table\ndefinitions into a database.\n\n##### Example:\nIn this example there is a table `films` with the following definition:\n```commandline\n+----------+-------------------+-------------+\n| Column   | Type              | Modifiers   |\n|----------+-------------------+-------------|\n| title    | character varying |  not null   |\n| director | character varying |             |\n| year     | character varying |             |\n+----------+-------------------+-------------+\nIndexes:\n    "films_pkey" PRIMARY KEY, btree (title)\n```\nExecuting `dbtoyaml mydb` results in the following yaml that knockoff\ncan be configured to use to load with `yamltodb`. \n```yaml\nschema public:\n  description: standard public schema\n  owner: postgres\n  privileges:\n  - PUBLIC:\n    - all\n  - postgres:\n    - all\n  table films:\n    columns:\n    - title:\n        not_null: true\n        type: character varying\n    - director:\n        type: character varying\n    - year:\n        type: character varying\n    owner: myuser\n    primary_key:\n      films_pkey:\n        columns:\n        - title\n```\nNote: If you are running the local postgres setup described above and running from within a docker container on your mac, you can use the following: `PGPASSWORD=docker dbtoyaml -H docker.for.mac.host.internal -U postgres mydb`\n\n#### Loading data into tables\nData can be loaded into new or existing tables.\n\n##### Examples\nThe following example loads data into an existing table from a provided csv.\n```yaml\nknockoff:\n  dag:\n    - name: films # arbitrary name of node in dag\n      type: table # table | prototype | component | part\n      table: films # defaults to the name of the node if not provided \n      source:\n        strategy: io\n        reader: pandas.read_csv\n        kwargs:\n          filepath_or_buffer: example/films.csv # local or s3:// path\n          sep: "|"\n      sink:\n        database: mydb\n        kwargs:\n          if_exists: append # defaults to fail\n          index: false # Data is loaded into a pandas DataFrame this option ignores the index\n```\n\nThe following example loads data into a new table from data defined in the yaml.\n```yaml\nknockoff:\n  dag:\n    - name: films2 # Note: "table" key not specified, so defaults to "film2"\n      type: table\n      source:\n        strategy: io\n        reader: inline\n        kwargs:\n          sep: ","\n          data: |\n            title,director,year\n            t5,d1,2020\n            t6,d2,2020\n            t7,d1,2020\n      sink:\n        database: mydb\n        user: myuser\n        password_env: MYUSER_PASSWORD\n        kwargs:\n          index: false\n```\n\n#### Generating fake retail data\nKnockoff uses [faker](https://github.com/joke2k/faker) to help generate fake retail data that can be used for testing.\nHierarchical relationships with various dependencies can be also be modelled with knockoff. This [example](examples/knockoff.yaml)\ngenerates the following tables (in addition to the above examples).\n```shell script\npostgres@localhost:mydb> select * from location;\n+-------------------------------+---------------+-----------+\n| address                       | location_id   | channel   |\n|-------------------------------+---------------+-----------|\n| 07528 Fischer Track Suite 779 | 1             | nfs       |\n| Melissaview, MD 90363         |               |           |\n| 1535 Kelly Canyon             | 2             | nso       |\n| Rhodesborough, CA 43893       |               |           |\n| 216 Kayla Lake Apt. 126       | 3             | nso       |\n| South Matthewmouth, OH 36332  |               |           |\n| 561 Jones Burg Suite 382      | 4             | nso       |\n| Hugheschester, DE 21908       |               |           |\n| 042 Robinson Fort Suite 945   | 5             | nfs       |\n| Pattersonshire, NC 96317      |               |           |\n| 2332 Watkins Road             | 0             | digital   |\n| Davidfort, MS 71411           |               |           |\n+-------------------------------+---------------+-----------+\n\npostgres@localhost:mydb> select * from product;\n+------------+----------+-----------------------+---------------+------------+\n| division   | gender   | category              | color         | sku        |\n|------------+----------+-----------------------+---------------+------------|\n| apparel    | men      | shorts                | PaleGoldenRod | 6357812379 |\n| apparel    | women    | pants & tights        | NavajoWhite   | 8332320303 |\n| apparel    | men      | tops & t-shirts       | Lavender      | 9243289077 |\n| shoes      | men      | lifestyle             | PaleGoldenRod | 7270972977 |\n| apparel    | women    | pants & tights        | PaleGoldenRod | 4443641793 |\n| apparel    | women    | hoodies & sweatshirts | NavajoWhite   | 6130018459 |\n| shoes      | women    | jordan                | Lavender      | 3791231041 |\n| apparel    | men      | pants & tights        | PaleGoldenRod | 3899370297 |\n| apparel    | men      | shorts                | Lavender      | 7557742055 |\n| apparel    | men      | pants & tights        | SkyBlue       | 9785957221 |\n| apparel    | women    | shorts                | SkyBlue       | 9979359561 |\n| apparel    | women    | tops & t-shirts       | Lavender      | 7006056836 |\n| shoes      | women    | jordan                | Lavender      | 4853474331 |\n| shoes      | women    | jordan                | NavajoWhite   | 6589395336 |\n| apparel    | men      | pants & tights        | Beige         | 7168664719 |\n| apparel    | men      | hoodies & sweatshirts | Beige         | 7525844204 |\n| apparel    | men      | shorts                | SkyBlue       | 9735336861 |\n| shoes      | men      | skateboarding         | SkyBlue       | 6385212885 |\n| apparel    | men      | tops & t-shirts       | Beige         | 9735107927 |\n| apparel    | women    | pants & tights        | SkyBlue       | 2633853831 |\n| apparel    | women    | jackets & vests       | NavajoWhite   | 2758275877 |\n| apparel    | men      | shorts                | Lavender      | 1330756304 |\n| apparel    | women    | tops & t-shirts       | NavajoWhite   | 9334676293 |\n| shoes      | men      | skateboarding         | Lavender      | 6735393792 |\n| apparel    | men      | jackets & vests       | Lavender      | 2907811814 |\n+------------+----------+-----------------------+---------------+------------+\n\npostgres@localhost:mydb> select * from transactions limit 10;\n+---------------+------------+-----------+------------+------------+------------+\n| location_id   | sku        | line_id   | order_id   | quantity   | date       |\n|---------------+------------+-----------+------------+------------+------------|\n| 5             | 7557742055 | 2         | 2957859949 | 0          | 2018-05-06 |\n| 1             | 1330756304 | 1         | 3920316859 | 0          | 2018-07-19 |\n| 4             | 9243289077 | 3         | 1875617688 | 0          | 2019-10-14 |\n| 3             | 9334676293 | 2         | 7317451987 | 0          | 2018-06-09 |\n| 0             | 9979359561 | 3         | 1236640244 | 2          | 2019-07-17 |\n| 0             | 9735107927 | 1         | 9030486883 | 3          | 2018-04-27 |\n| 1             | 9735336861 | 2         | 6196902209 | 2          | 2020-01-21 |\n| 3             | 7006056836 | 4         | 1432537227 | 0          | 2019-04-22 |\n| 2             | 2907811814 | 1         | 4039132536 | 0          | 2019-09-23 |\n| 0             | 4443641793 | 5         | 8648324533 | 2          | 2018-09-06 |\n+---------------+------------+-----------+------------+------------+------------+\n```\n\n#### Run the example:\n\n1. Run postgres: `docker run --rm  --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432  postgres:11.4`\n    * Terminate existing container with `docker kill pg-docker`\n    * Note: The example assumes you\'re running with *POSTGRES_PASSWORD=docker* and on port *5432*\n2. Checkout the repo or download the examples folder\n3. Pull knockoff docker image: `docker pull knockoff-factory`\n```commandline\ndocker run --rm -v $PWD/examples:/examples \\\n-e KNOCKOFF_DB_HOST=\'docker.for.mac.host.internal\' \\\n-e KNOCKOFF_DB_USER=\'postgres\' \\\n-e KNOCKOFF_DB_PASSWORD=\'docker\' \\\n-e KNOCKOFF_DB_NAME=\'knockoff\' \\\n-e KNOCKOFF_CONFIG=/examples/knockoff.yaml nikelab222/knockoff-factory:latest knockoff\n```\nNote: if you are loading data from an s3 bucket you have access to, you can enable your docker\ncontainer access to those credentials by adding `-v ~/.aws:/root/.aws` to the `docker run` command.\n\n\n### Future work\n* Add documentation for SDK\n* Autodiscover and populate all tables by using reflection and building dependency graph with foreign key relationships\n* Update CLI and yaml configuration to use SDK\n* Documentation / use-cases\n* Parallelize execution of dag. (e.g. https://ipython.org/ipython-doc/stable/parallel/dag_dependencies.html)\n',
    'author': 'Gregory Yu',
    'author_email': 'gregory.yu@nike.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Nike-Inc/knockoff-factory',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
