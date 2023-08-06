# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apifactory']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.0.0,<6.0.0',
 'bcrypt>=3.0.0,<4.0.0',
 'fastapi<1.0.0',
 'passlib>=1.0.0,<2.0.0',
 'pydantic>=1.0.0,<2.0.0',
 'pymssql>=2.0.0,<3.0.0',
 'python-jose>=3.0.0,<4.0.0',
 'python-multipart<1.0.0',
 'sqlalchemy>=1.0.0,<2.0.0',
 'uvicorn<1.0.0']

setup_kwargs = {
    'name': 'apifactory',
    'version': '0.2.1',
    'description': 'package for automatically creating an api on an existing database',
    'long_description': '[![Downloads](https://pepy.tech/badge/apifactory/month)](https://pepy.tech/project/apifactory)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![](https://img.shields.io/pypi/pyversions/apifactory)\n[![codecov](https://codecov.io/gh/sebastiaanbroekema/apifactory/branch/develop/graph/badge.svg?token=28U38TJ6I8)](https://codecov.io/gh/sebastiaanbroekema/apifactory)\n\n# Apifactory\n\nApifacotry\xa0allows\xa0you\xa0to\xa0create\xa0APIs\xa0on\xa0existing\xa0(currently\xa0only\xa0SQL)\xa0databases\xa0nearly\xa0automatically.\xa0It\xa0handles\xa0all\xa0sorts\xa0of\xa0setup\xa0automatically\xa0for\xa0you,\xa0including\xa0creating\xa0pydantic\xa0data schemas\xa0setting\xa0up\xa0login\xa0and\xa0JWT.\xa0\n\n\nApifactory\xa0uses\xa0SQLAlchemy\xa0to\xa0automatically\xa0detect\xa0tables\xa0in\xa0the\xa0given\xa0database.\xa0If\xa0these\xa0tables\xa0have\xa0single\xa0column\xa0primary keys\xa0they\xa0are\xa0added\xa0to\xa0your\xa0API, multicolumn\xa0primary\xa0keys\xa0will\xa0be\xa0added\xa0in\xa0the\xa0future.\n\nApifactory\xa0uses\xa0fastapi\xa0to\xa0construct\xa0its\xa0APIs. This\xa0means\xa0the\xa0schemas\xa0you\xa0accept\xa0or\xa0return\xa0in\xa0your\xa0API\xa0are\xa0defined\xa0by\xa0pydantic,\xa0which\xa0also\xa0handles\xa0validation\xa0of\xa0input\xa0types\xa0and\xa0return\xa0types.\xa0These\xa0schemas\xa0are\xa0automatically\xa0generated\xa0from\xa0the\xa0SQLAlchemy\xa0table\xa0models\xa0that\xa0are\xa0generated\xa0by\xa0apifactory.\n\nApifactory\xa0automatically\xa0prevents\xa0unauthorized\xa0access.\xa0Users\xa0of\xa0your\xa0API\xa0need\xa0to\xa0log in\xa0and\xa0get\xa0a\xa0JWT\xa0to\xa0authenticate\xa0at\xa0the\xa0API\xa0endpoints Authorization\xa0is\xa0based\xa0on\xa0a\xa0user\xa0defined\xa0existing\xa0Users\xa0table.\n\n## A\xa0short\xa0example\xa0how\xa0to\xa0set up\xa0an\xa0API\n\nApifactory\xa0will\xa0add\xa0all\xa0tables\xa0with\xa0a\xa0single\xa0column\xa0primary\xa0key. All\xa0columns\xa0of\xa0these\xa0table\xa0will\xa0be\xa0added\xa0to\xa0the\xa0schema\xa0of\xa0your\xa0API. However,\xa0this\xa0might\xa0not\xa0be\xa0preferred\xa0for\xa0all\xa0methods. For\xa0example,\xa0you\xa0might\xa0not\xa0want\xa0your\xa0post\xa0requests\xa0to\xa0also\xa0dictate\xa0the\xa0primary\xa0key\xa0the\xa0entry. This\xa0could\xa0for\xa0example\xa0be\xa0handled\xa0by\xa0the\xa0database\xa0itself. Currently,\xa0you\xa0can\xa0add\xa0some\xa0config\xa0to\xa0dictate\xa0which\xa0columns\xa0to\xa0exclude\xa0in\xa0post\xa0and\xa0put\xa0requests.In\xa0addition,\xa0you\xa0need\xa0to\xa0specify\xa0the\xa0database\xa0connection\xa0string.\xa0And\xa0specify\xa0the\xa0name\xa0of\xa0the\xa0table\xa0containing\xa0hashed\xa0passwords\xa0for\xa0user\xa0authentication.\n\n\n```python\nfrom apifactory.app_factory import ApiFactory\n\ndburl = "<database url>"\n\nkey = "<key for jwt encryption>"\nconfigs = {\n    "Persons": {\n        "excluded_columns_put": ["Personid", "createdDate"],\n        "excluded_columns_post": ["Personid", "createdDate"],\n    },\n    "test_table": {"excluded_columns_put": ["primarykey"]},\n}\nusermodel_name = \'Users\'\n\napp = ApiFactory(dburl, usermodel_name, key, configs).app_factory()\n```\n\nYou\xa0can\xa0serve\xa0the\xa0file\xa0\n```bash\xa0\nuvicorn\xa0<name\xa0of\xa0your\xa0file\xa0containg\xa0the\xa0app>:app\xa0\n```\n\nSince\xa0apifactory\xa0uses\xa0fastapi\xa0you\xa0automatically\xa0can\xa0visit\xa0an\xa0openapi\xa0page\xa0containing\xa0the\xa0details\xa0of\xa0your\xa0API.\n\n![](Swagger_UI.png)\n\n\n\n\nApifactory\xa0is\xa0currently\xa0heavily\xa0under\xa0development\xa0and\xa0not\xa0feature\xa0complete/stable.\xa0\nFeatures\xa0to\xa0be\xa0included\xa0in\xa0the\xa0future:\n* More\xa0configuration\xa0options\n* Multicolumn\xa0primary\xa0key\xa0support\n* Support\xa0for\xa0views\xa0\n* Add\xa0scopes\xa0to\xa0JWT\n* Configure\xa0from\xa0files\xa0YAML/JSON\n* Add\xa0support\xa0for\xa0custom\xa0classes\xa0inserted\xa0into\xa0ApiFactory\n* Make\xa0apifactory\xa0completely\xa0asynchronous\n* docs\n* ratelimitting\n',
    'author': 'Sebastiaan Broekema',
    'author_email': 'sebastiaanbroekema@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sebastiaanbroekema/apifactory',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
