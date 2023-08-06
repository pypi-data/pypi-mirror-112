# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mugen']

package_data = \
{'': ['*']}

install_requires = \
['httptools>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'mugen',
    'version': '0.5.0',
    'description': 'Mugen - HTTP for Asynchronous Requests',
    'long_description': "## Mugen - HTTP for Asynchronous Requests\n\nMugen is library for http asynchronous requests.\n\nOnly running on python ^3.7\n\nok, code demo:\n\n```python\nimport asyncio\nimport mugen\n\nasync def task():\n    url = 'https://www.google.com'\n    resp = await mugen.get(url)\n    print(resp.text)\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(task())\n```\n\nSee, [Documention](https://peterding.github.io/mugen-docs/).\n\n> Mugen is a name from _Samurai Champloo_ (サムライチャンプル, 混沌武士)\n\n### Feature Support\n\n- Keep-Alive & Connection Pooling\n- DNS cache\n- Sessions with Cookie Persistence\n- Automatic Decompression\n- Automatic Content Decoding\n- HTTP(S)/SOCKS5 Proxy Support\n- Connection Timeouts\n",
    'author': 'PeterDing',
    'author_email': 'dfhayst@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PeterDing/mugen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
