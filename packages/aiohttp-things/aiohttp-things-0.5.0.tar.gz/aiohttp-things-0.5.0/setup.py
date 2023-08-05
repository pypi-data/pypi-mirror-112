# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_things']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4.post0,<4.0.0']

setup_kwargs = {
    'name': 'aiohttp-things',
    'version': '0.5.0',
    'description': 'Modest utility collection for development with AIOHTTP framework.',
    'long_description': '==============\naiohttp-things\n==============\n|ReadTheDocs| |PyPI release| |PyPI downloads| |License| |Python versions| |GitHub CI| |Codecov|\n\n.. |ReadTheDocs| image:: https://readthedocs.org/projects/aiohttp-things/badge/?version=latest\n  :target: https://aiohttp-things.readthedocs.io/en/latest/?badge=latest\n  :alt: Read The Docs build\n\n.. |PyPI release| image:: https://badge.fury.io/py/aiohttp-things.svg\n  :target: https://pypi.org/project/aiohttp-things/\n  :alt: Release\n\n.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/aiohttp-things\n  :target: https://pypistats.org/packages/aiohttp-things\n  :alt: PyPI downloads count\n\n.. |License| image:: https://img.shields.io/badge/License-MIT-green\n  :target: https://github.com/ri-gilfanov/aiohttp-things/blob/master/LICENSE\n  :alt: MIT License\n\n.. |Python versions| image:: https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9-blue\n  :target: https://pypi.org/project/aiohttp-things/\n  :alt: Python version support\n\n.. |GitHub CI| image:: https://github.com/ri-gilfanov/aiohttp-things/actions/workflows/ci.yml/badge.svg?branch=master\n  :target: https://github.com/ri-gilfanov/aiohttp-things/actions/workflows/ci.yml\n  :alt: GitHub continuous integration\n\n.. |Codecov| image:: https://codecov.io/gh/ri-gilfanov/aiohttp-things/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/ri-gilfanov/aiohttp-things\n  :alt: codecov.io status for master branch\n\nModest utility collection for development with `AIOHTTP\n<https://docs.aiohttp.org/>`_ framework.\n\nDocumentation\n-------------\nhttps://aiohttp-things.readthedocs.io\n\n\nInstallation\n------------\nInstalling ``aiohttp-things`` with pip: ::\n\n  pip install aiohttp-things\n\n\nSimple example\n--------------\nExample of AIOHTTP application\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n.. code-block:: python\n\n  import json\n  import uuid\n  from aiohttp import web\n  from aiohttp_things.views import ItemMixin, JSONMixin\n\n\n  def safe_json_value(value):\n      try:\n          json.dumps(value)\n          return value\n      except (TypeError, OverflowError):\n          return str(value)\n\n\n  class Base(web.View, ItemMixin, JSONMixin):\n      async def get(self):\n          self.context[\'Type of primary key\'] = safe_json_value(type(self.pk))\n          self.context[\'Value of primary key\'] = safe_json_value(self.pk)\n          return await self.finalize_response()\n\n\n  class IntegerExample(Base):\n      pk_factory = int\n\n\n  class UUIDExample(Base):\n      pk_factory = uuid.UUID\n\n\n  UUID = \'[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\'\n  ROUTES = [\n      web.view(\'/integer/{pk:[0-9]+}\', IntegerExample),\n      web.view(f\'/uuid/{{pk:{UUID}}}\', UUIDExample),\n  ]\n\n\n  async def app_factory():\n      app = web.Application()\n      app.add_routes(ROUTES)\n      return app\n\n\n  if __name__ == \'__main__\':\n      web.run_app(app_factory())\n\n\nExamples HTTP requests and response\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n* \\http://0.0.0.0:8080/integer/1\n\n  .. code-block:: json\n\n    {\n      "Type of primary key": "<class \'int\'>",\n      "Value of primary key": 1\n    }\n\n* \\http://0.0.0.0:8080/integer/9999999999999\n\n  .. code-block:: json\n\n    {\n      "Type of primary key": "<class \'int\'>",\n      "Value of primary key": 9999999999999\n    }\n\n* \\http://0.0.0.0:8080/integer/a352da04-c1af-4a44-8a94-c37f8f37b2bc\n  ::\n\n    404: Not Found\n\n* \\http://0.0.0.0:8080/integer/abc\n  ::\n\n    404: Not Found\n\n* \\http://0.0.0.0:8080/uuid/a352da04-c1af-4a44-8a94-c37f8f37b2bc\n\n  .. code-block:: json\n\n    {\n      "Type of primary key": "<class \'uuid.UUID\'>",\n      "Value of primary key": "a352da04-c1af-4a44-8a94-c37f8f37b2bc"\n    }\n\n* \\http://0.0.0.0:8080/uuid/13d1d0e0-4787-4feb-8684-b3da32609743\n\n  .. code-block:: json\n\n    {\n      "Type of primary key": "<class \'uuid.UUID\'>",\n      "Value of primary key": "13d1d0e0-4787-4feb-8684-b3da32609743"\n    }\n\n* \\http://0.0.0.0:8080/uuid/1\n  ::\n\n    404: Not Found\n\n* \\http://0.0.0.0:8080/uuid/abc\n  ::\n\n    404: Not Found\n',
    'author': 'Ruslan Ilyasovich Gilfanov',
    'author_email': 'ri.gilfanov@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ri-gilfanov/aiohttp-things',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
