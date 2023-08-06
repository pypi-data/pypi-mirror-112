# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chocs_middleware', 'chocs_middleware.parsed_body']

package_data = \
{'': ['*']}

install_requires = \
['chili>=1.0.0-beta.0,<2.0.0',
 'chocs>=1.0.0-beta.0,<2.0.0',
 'typing_extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'chocs-middleware.parsed-body',
    'version': '1.0.0',
    'description': 'This middleware changes behaviour of chocs.HttpRequest.parsed_body.',
    'long_description': '# Chocs - Parsed body middleware <br>[![CI](https://github.com/kodemore/chocs-parsed-body/actions/workflows/main.yaml/badge.svg)](https://github.com/kodemore/chocs-parsed-body/actions/workflows/main.yaml) [![codecov](https://codecov.io/gh/kodemore/chocs-parsed-body/branch/main/graph/badge.svg?token=Q5PL6W5DTB)](https://codecov.io/gh/kodemore/chocs-parsed-body) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nParsed body middleware for chocs package.\n\nParsed body middleware helps converting json/yaml data that comes with request into any dataclass. Please consider the following example:\n\n```python\nfrom middleware import ParsedBodyMiddleware\nfrom chocs_middleware import Application, HttpRequest, HttpResponse\nfrom chocs_middleware import asdict\nfrom dataclasses import dataclass\nimport json\n\n# You can define whether to use strict mode or not for all defined routes.\napp = Application(ParsedBodyMiddleware(strict=False))\n\n\n@dataclass\nclass Pet:\n    id: str\n    name: str\n\n\n@app.post("/pets", parsed_body=Pet, strict=True)  # you can also override default strict mode inside the route\ndef create_pet(request: HttpRequest) -> HttpResponse:\n    pet: Pet = request.parsed_body\n    assert isinstance(pet, Pet)\n    return HttpResponse(json.dumps(asdict(pet)))\n```\n\nIn the above example we can see that `request.parsed_body` is no longer carrying `chocs.JsonHttpMessage` instead it was transformed into dataclass hinted inside the route definition (`Pet`).\n\n## Strict mode\n\nStrict mode is using initialiser defined in dataclass. Which means the request data\nis simply unpacked and passed to your dataclass, so you have to manually transform \nnested data to dataclasses in order to conform your dataclass interface, for example:\n\n```python\nfrom chocs_middleware import ParsedBodyMiddleware\nfrom chocs_middleware import Application, HttpRequest, HttpResponse\nfrom dataclasses import dataclass\nfrom typing import List\n\napp = Application(ParsedBodyMiddleware())\n\n\n@dataclass\nclass Tag:\n    name: str\n    id: str\n\n\n@dataclass\nclass Pet:\n    id: str\n    name: str\n    age: int\n    tags: List[Tag]\n\n    def __post_init__(self):  # post init might be used to reformat your data\n        self.age = int(self.age)\n        tmp_tags = self.tags\n        self.tags = []\n        for tag in tmp_tags:\n            self.tags.append(Tag(**tag))\n\n\n@app.post("/pets", parsed_body=Pet)\ndef create_pet(request: HttpRequest) -> HttpResponse:\n    pet: Pet = request.parsed_body\n    assert isinstance(pet.tags[0], Tag)\n    assert isinstance(pet, Pet)\n    return HttpResponse(pet.name)\n\n```\n\n## Non-strict mode, aka: auto hydration\n\nIn non-strict mode `chocs` takes care of instantiating and hydrating your dataclasses. Complex and deeply\nnested structures are supported as long as used types are supported by `chocs` hydration mechanism.\nList of supported types can be found in [dataclass support library](/kodemore/chocs/wiki/dataclass-support#supported-data-types)\n\n> Note: __post_init__ method is also called as a part of hydration process.\n',
    'author': 'Dawid Kraczkowski',
    'author_email': 'dawid.kraczkowski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kodemore/chocs-parsed-body',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
