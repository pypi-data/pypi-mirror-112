# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decoy', 'decoy.mypy']

package_data = \
{'': ['*']}

entry_points = \
{'pytest11': ['decoy = decoy.pytest_plugin']}

setup_kwargs = {
    'name': 'decoy',
    'version': '1.6.1',
    'description': 'Opinionated mocking library for Python',
    'long_description': '<div align="center">\n    <h1>Decoy</h1>\n    <img src="https://mike.cousins.io/decoy/img/decoy.png" width="256px">\n    <p>Opinionated mocking library for Python</p>\n    <p>\n        <a title="CI Status" href="https://github.com/mcous/decoy/actions">\n            <img src="https://flat.badgen.net/github/checks/mcous/decoy/main">\n        </a>\n        <a title="License" href="https://github.com/mcous/decoy/blob/main/LICENSE">\n            <img src="https://flat.badgen.net/github/license/mcous/decoy">\n        </a>\n        <a title="PyPI Version"href="https://pypi.org/project/decoy/">\n            <img src="https://flat.badgen.net/pypi/v/decoy">\n        </a>\n        <a title="Supported Python Versions" href="https://pypi.org/project/decoy/">\n            <img src="https://flat.badgen.net/pypi/python/decoy">\n        </a>\n    </p>\n    <p>\n        <a href="https://mike.cousins.io/decoy/">Usage guide and documentation</a>\n    </p>\n</div>\n\nThe Decoy library allows you to create, stub, and verify fully-typed, async/await-friendly mocks in your Python unit tests, so your tests are:\n\n-   Less prone to insufficient tests due to unconditional stubbing\n-   Easier to fit into the Arrange-Act-Assert pattern\n-   Covered by typechecking\n\nThe Decoy API is heavily inspired by / stolen from the excellent [testdouble.js][] and [Mockito][] projects.\n\n## Install\n\n```bash\n# pip\npip install decoy\n\n# poetry\npoetry add --dev decoy\n```\n\n## Setup\n\n### Pytest setup\n\nDecoy ships with its own [pytest][] plugin, so once Decoy is installed, you\'re ready to start using it via its pytest fixture, called `decoy`.\n\n```python\n# test_my_thing.py\nfrom decoy import Decoy\n\ndef test_my_thing_works(decoy: Decoy) -> None:\n    # ...\n```\n\nThe `decoy` fixture is function-scoped and will ensure that all stub and spy state is reset between every test.\n\n### Mypy Setup\n\nDecoy\'s API can be a bit confusing to [mypy][]. To suppress mypy errors that may be emitted during valid usage of the Decoy API, we have a mypy plugin that you should add to your configuration file:\n\n```ini\n# mypy.ini\n\n# ...\nplugins = decoy.mypy\n# ...\n```\n\n## Basic Usage\n\nThis example assumes you are using [pytest][]. See Decoy\'s [documentation][] for a more detailed usage guide and API reference.\n\n### Define your test\n\nDecoy will add a `decoy` fixture that provides its mock creation API.\n\n```python\nfrom decoy import Decoy\nfrom todo import TodoAPI, TodoItem\nfrom todo.store TodoStore\n\ndef test_add_todo(decoy: Decoy) -> None:\n    ...\n```\n\n### Create a mock\n\nUse `decoy.mock` to create a mock based on some specification. From there, inject the mock into your test subject.\n\n```python\ndef test_add_todo(decoy: Decoy) -> None:\n    todo_store = decoy.mock(cls=TodoStore)\n    subject = TodoAPI(store=todo_store)\n    ...\n```\n\nSee [creating mocks][] for more details.\n\n### Stub a behavior\n\nUse `decoy.when` to configure your mock\'s behaviors. For example, you can set the mock to return a certain value when called in a certain way using `then_return`:\n\n```python\ndef test_add_todo(decoy: Decoy) -> None:\n    """Adding a todo should create a TodoItem in the TodoStore."""\n    todo_store = decoy.mock(cls=TodoStore)\n    subject = TodoAPI(store=todo_store)\n\n    decoy.when(\n        todo_store.add(name="Write a test for adding a todo")\n    ).then_return(\n        TodoItem(id="abc123", name="Write a test for adding a todo")\n    )\n\n    result = subject.add("Write a test for adding a todo")\n    assert result == TodoItem(id="abc123", name="Write a test for adding a todo")\n```\n\nSee [stubbing with when][] for more details.\n\n### Verify a call\n\nUse `decoy.verify` to assert that a mock was called in a certain way. This is best used with dependencies that are being used for their side-effects and don\'t return a useful value.\n\n```python\ndef test_remove_todo(decoy: Decoy) -> None:\n    """Removing a todo should remove the item from the TodoStore."""\n    todo_store = decoy.mock(cls=TodoStore)\n    subject = TodoAPI(store=todo_store)\n\n    subject.remove("abc123")\n\n    decoy.verify(todo_store.remove(id="abc123"))\n```\n\nSee [spying with verify][] for more details.\n\n[testdouble.js]: https://github.com/testdouble/testdouble.js\n[mockito]: https://site.mockito.org/\n[pytest]: https://docs.pytest.org/\n[mypy]: https://mypy.readthedocs.io/\n[documentation]: https://mike.cousins.io/decoy/\n[creating mocks]: https://mike.cousins.io/decoy/usage/create/\n[stubbing with when]: https://mike.cousins.io/decoy/usage/when/\n[spying with verify]: https://mike.cousins.io/decoy/usage/verify/\n',
    'author': 'Mike Cousins',
    'author_email': 'mike@cousins.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mike.cousins.io/decoy/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
