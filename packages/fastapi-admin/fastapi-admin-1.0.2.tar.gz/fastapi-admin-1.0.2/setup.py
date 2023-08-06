# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_admin',
 'fastapi_admin.providers',
 'fastapi_admin.routes',
 'fastapi_admin.widgets']

package_data = \
{'': ['*'],
 'fastapi_admin': ['locales/en_US/LC_MESSAGES/*',
                   'locales/zh_CN/LC_MESSAGES/*',
                   'templates/*',
                   'templates/components/*',
                   'templates/errors/*',
                   'templates/providers/login/*',
                   'templates/widgets/displays/*',
                   'templates/widgets/filters/*',
                   'templates/widgets/inputs/*']}

install_requires = \
['Babel',
 'aiofiles',
 'aioredis',
 'bcrypt',
 'fastapi',
 'jinja2',
 'pendulum',
 'python-multipart',
 'tortoise-orm',
 'uvicorn[standard]']

setup_kwargs = {
    'name': 'fastapi-admin',
    'version': '1.0.2',
    'description': 'A fast admin dashboard based on FastAPI and TortoiseORM with tabler ui, inspired by Django admin.',
    'long_description': '# FastAPI Admin\n\n[![image](https://img.shields.io/pypi/v/fastapi-admin.svg?style=flat)](https://pypi.python.org/pypi/fastapi-admin)\n[![image](https://img.shields.io/github/license/fastapi-admin/fastapi-admin)](https://github.com/fastapi-admin/fastapi-admin)\n[![image](https://github.com/fastapi-admin/fastapi-admin/workflows/deploy/badge.svg)](https://github.com/fastapi-admin/fastapi-admin/actions?query=workflow:deploy)\n[![image](https://github.com/fastapi-admin/fastapi-admin/workflows/pypi/badge.svg)](https://github.com/fastapi-admin/fastapi-admin/actions?query=workflow:pypi)\n\n## Introduction\n\n`fastapi-admin` is a fast admin dashboard based on [FastAPI](https://github.com/tiangolo/fastapi)\nand [TortoiseORM](https://github.com/tortoise/tortoise-orm/) with [tabler](https://github.com/tabler/tabler) ui,\ninspired by Django admin.\n\n## Installation\n\n```shell\n> pip install fastapi-admin\n```\n\n## Requirements\n\n- [Redis](https://redis.io)\n\n## Online Demo\n\nYou can check a online demo [here](https://fastapi-admin.long2ice.cn/admin/login).\n\n- username: `admin`\n- password: `123456`\n\nOr pro version online demo [here](https://fastapi-admin-pro.long2ice.cn/admin/login).\n\n- username: `admin`\n- password: `123456`\n\n## Screenshots\n\n![](https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/login.png)\n\n![](https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/dashboard.png)\n\n## Run examples in local\n\n1. Clone repo.\n2. Create `.env` file.\n\n   ```dotenv\n   DATABASE_URL=mysql://root:123456@127.0.0.1:3306/fastapi-admin\n   REDIS_HOST=localhost\n   REDIS_PORT=6379\n   REDIS_PASSWORD=\n   REDIS_DB=0\n   ```\n\n3. Run `docker-compose up -d --build`.\n4. Visit <http://localhost:8000/admin/init> to create first admin.\n\n## Documentation\n\nSee documentation at <https://fastapi-admin.github.io>.\n\n## License\n\nThis project is licensed under the\n[Apache-2.0](https://github.com/fastapi-admin/fastapi-admin/blob/master/LICENSE)\nLicense.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fastapi-admin/fastapi-admin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
