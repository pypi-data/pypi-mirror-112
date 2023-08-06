# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydactory']

package_data = \
{'': ['*']}

install_requires = \
['faker>=4.15.0,<5.0.0', 'pydantic>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'pydactory',
    'version': '0.2.0',
    'description': 'A factory library for pydantic models.',
    'long_description': '# `pydactory`\n\n`pydactory` is a factory library for [`pydantic`](https://github.com/samuelcolvin/pydantic/) models with an API inspired by [`factory_boy`](https://github.com/FactoryBoy/factory_boy).\n\n## Installation\n\nPyPI: https://pypi.org/project/pydactory/\n\n`pip install pydactory`\n\n## Features\n\n`pydactory` is...\n\n**low boilerplate**: provides default values for many common types. You don\'t need to tell `pydactory` how to build your `name: str` fields\n\n**familiar**: define your factories like you define your `pydantic` models: in a simple, declarative syntax\n\n## Getting started\n\n### Declare your `pydantic` models\n\n```python\nfrom datetime import datetime\nfrom typing import Optional\n\nfrom pydantic import BaseModel, Field\n\n\nclass Address(BaseModel):\n    street1: str\n    street2: str\n    city: str\n    state: str\n    zip_code: str = Field(max_length=5)\n\n\nclass Author(BaseModel):\n    name: str\n    address: Address\n    date_of_birth: datetime\n\n\nclass Book(BaseModel):\n    title: str = Field(alias="Title")\n    author: Author = Field(alias="Author")\n    pages: int = Field(alias="PageCount")\n    publish_date: datetime = Field(alias="PublishDate")\n    isbn_13: str = Field(alias="ISBN-13")\n    isbn_10: Optional[str] = Field(alias="ISBN-10")\n```\n\n### Declare your factories\n\n```python\nfrom pydactory import Factory\n\n\nclass AuthorFactory(Factory[Author]):\n    name = "Leo Tolstoy"\n\n\nclass BookFactory(Factory[Book]):\n    title = "War and Peace"\n    author = AuthorFactory\n    publish_date = datetime.today\n```\n\n### Use the factories to build your models\n\n```python\ndef test_book_factory():\n    book: Book = BookFactory.build(title="Anna Karenina")\n    assert Book(\n        title="Anna Karenina",\n        author=Author(\n            name="Leo Tolstoy",\n            address=Address(\n                street1="fake", street2="fake", city="fake", state="fake", zip_code="fake"\n            ),\n            date_of_birth=datetime.datetime(2000, 1, 1, 0, 0),\n        ),\n        pages=1,\n        publish_date=datetime.datetime(2021, 3, 26, 14, 15, 22, 613309),\n        isbn_13="fake",\n        isbn_10=None,\n    ) == book\n```\n\n## Roadmap\n\n`pydactory` is still very much in progress.\n',
    'author': 'Richard Howard',
    'author_email': 'richard@howard.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rthoward/pydactory',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
