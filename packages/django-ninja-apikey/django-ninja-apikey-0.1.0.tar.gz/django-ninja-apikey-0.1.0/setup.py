# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ninja_apikey', 'ninja_apikey.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.0.13', 'django-ninja>=0.13']

setup_kwargs = {
    'name': 'django-ninja-apikey',
    'version': '0.1.0',
    'description': 'Easy to use API key authentication for Django Ninja REST Framework',
    'long_description': '# Django Ninja APIKey - Easy to use API key authentication for Django Ninja REST Framework\nThis is an unofficial [Django](https://github.com/django/django) app which makes it **easy** to manage API keys for the [Django Ninja REST Framework](https://github.com/vitalik/django-ninja).\n\n**Key Features:**\n- **Easy** integration in your projects\n- Well integrated in the **admin interface**\n- **Secure** API keys due to hashing \n- Works with the **standard** user model\n\n## Installation\n\n```\npip install django-ninja-apikey\n```\n\n## Usage\nAdd `ninja_apikey` to your installed apps in your django project:\n```Python\n# settings.py\n\nINSTALLED_APPS = [\n    # ...\n    "ninja_apikey",\n]\n```\nRun the included migrations:\n```\npython manage.py migrate\n```\nSecure an api endpoint with the API keys:\n```Python\n# api.py\n\nfrom ninja import NinjaAPI\nfrom ninja_apikey.security import APIKeyAuth\n\n#  ...\n\nauth = APIKeyAuth()\napi = NinjaAPI()\n\n# ...\n\n@api.get("/secure_endpoint", auth=auth)\ndef secure_endpoint(request):\n    return f"Hello, {request.user}!" \n```\nOr secure your whole api (or a specific [router](https://django-ninja.rest-framework.com/tutorial/routers/)) with the API keys:\n```Python\n# api.py\n\nfrom ninja import NinjaAPI\nfrom ninja_apikey.security import APIKeyAuth\n\n#  ...\n\napi = NinjaAPI(auth=APIKeyAuth())\n\n# ...\n\n@api.get("/secure_endpoint")\ndef secure_endpoint(request):\n    return f"Hello, {request.user}!" \n```\nYou can create now API keys from django\'s admin interface.\n\n## What next?\n- To support this project, please give a star on GitHub.\n- For any kind of issue feel free to open an Issue.\n- Contributors are welcome! Please refer to `CONTRIBUTING.md`.',
    'author': 'Maximilian Wassink',
    'author_email': 'wassink.maximilian@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mawassk/django-ninja-apikey',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
