# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fakewsserver']

package_data = \
{'': ['*']}

install_requires = \
['websockets>=9.1,<10.0']

setup_kwargs = {
    'name': 'fakewsserver',
    'version': '0.2.0',
    'description': 'Websocket server for testing',
    'long_description': '# Fake Websocket Server\n\nFake in the sense that it\'s actually a working server (created using\n`websockets` library) but one that that exists briefly to allow\nintegration testing.\n\n\n# Installation\n\npip install fakewsserver\n \n\n# Usage\n\n## One message sent, one received, everything is as expected\n\n```python\nfrom fakewsserver import assert_communication\n\nasync with assert_communication(\n        port=12345,\n        communication=[(\'hello\', \'there\')],\n        ):\n    async with websockets.connect(\'ws://localhost:12345\') as client:\n        await client.send(\'hello\')\n        response = await client.recv()\n\nassert response == \'there\'\n```\n\n## Expected communication pattern does not match\n\n```python\ncommunication = [\n    (\'hello\', \'there\'),\n    (\'general\', \'Kenobi\'),\n]\n\nasync with assert_communication(\n        port=12345,\n        communication=communication,\n        ):\n    async with websockets.connect(\'ws://localhost:12345\') as client:\n        await client.send(\'hello\')\n        response = await client.recv()\n        assert response == \'there\'\n        await client.send(\'admiral\')\n        await client.recv()\n```\n\nAnd there\'s a feedback what went wrong:\n```\n    AssertionError: Failed 2nd step:\n    Expected: "general"\n    Got: "admiral"\n```\n\n## Utilities\n\nWhen working with APIs it might be convenient to capture real messages\nto write tests against them. Here\'s a simple example (using the fake server;\nin real life we would connect to a real websocket server).\n\n```python\nfrom fakewsserver import respond_with, write_communication\n\nsend = \'Hello there\'\nreceive = [\'General\', \'Kenobi\']\n\nfile = StringIO()\nasync with respond_with(port=12345, responses=receive):\n    async with websockets.connect(\'ws://localhost:12345\') as client:\n        await write_communication(\n            to_send=send,\n            client=client,\n            file=file,\n            timeout=None,\n            num_responses=len(receive),\n        )\n\nfile.seek(0)\ndata_raw = file.read()\ndata = json.loads(data_raw)\n\nassert data == [\n    dict(\n        type=\'send\',\n        data=\'Hello there\',\n    ),\n    dict(\n        type=\'receive\',\n        data=\'General\',\n    ),\n    dict(\n        type=\'receive\',\n        data=\'Kenobi\',\n    ),\n]\n```\n',
    'author': 'uigctaw',
    'author_email': 'uigctaw@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
