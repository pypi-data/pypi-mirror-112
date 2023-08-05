# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiothrift']

package_data = \
{'': ['*']}

install_requires = \
['async-timeout>=3.0.1,<4.0.0', 'thriftpy2>=0.4.9,<0.5.0']

setup_kwargs = {
    'name': 'aiothrift',
    'version': '0.2.4',
    'description': 'Async Thrift server and client',
    'long_description': 'aiothrift\n=========\n\nAsyncio implementation for thrift protocol, which is heavily based on thriftpy2_.\n\n.. image:: https://travis-ci.org/ryanwang520/aiothrift.svg?branch=master\n   :target: https://travis-ci.org/ryanwang520/aiothrift\n\n\nDocumentation: https://aiothrift.readthedocs.org/\n\nInstallation\n------------\n\n::\n\n    $ pip install aiothrift\n\n\nUsage example\n-------------\n\nThrift file\n^^^^^^^^^^^\n\n::\n\n    service PingPong {\n        string ping(),\n        i64 add(1:i32 a, 2:i64 b),\n    }\n\n\nServer\n^^^^^^\n\n.. code:: python\n\n    import asyncio\n    import aiothrift\n\n    pingpong_thrift = aiothrift.load(\'pingpong.thrift\', module_name=\'pingpong_thrift\')\n\n    class Dispatcher:\n        def ping(self):\n            return "pong"\n\n        async def add(self, a, b):\n            await asyncio.sleep(1)\n            return a + b\n\n    async def main():\n      server = await aiothrift.create_server(pingpong_thrift.PingPong, Dispatcher()))\n      async with server:\n          await server.serve_forever()\n\n    asyncio.run(main())\n\nClient\n^^^^^^\n\n.. code:: python\n\n    import asyncio\n    import aiothrift\n\n    pingpong_thrift = aiothrift.load(\'pingpong.thrift\', module_name=\'pingpong_thrift\')\n\n    async def go():\n        conn = await aiothrift.create_connection(pingpong_thrift.PingPong)\n        print(await conn.ping())\n        print(await conn.add(5, 6))\n        conn.close()\n\n    asyncio.run(go())\n\nOr use ConnectionPool\n^^^^^^^^^^^^^^^^^^^^^\n\n.. code:: python\n\n    import asyncio\n    import aiothrift\n\n    pingpong_thrift = aiothrift.load(\'pingpong.thrift\', module_name=\'pingpong_thrift\')\n\n    async def go():\n        client = await aiothrift.create_pool(pingpong_thrift.PingPong)\n        print(await client.ping())\n        print(await client.add(5, 6))\n        client.close()\n        await client.wait_closed()\n\n    asyncio.run(go())\n\n\nIt\'s just that simple to begin with ``aiothrift``, and you are not forced to use ``aiothrift`` on both server and client side.\nSo if you already have a normal thrift server setup, feel free to create an async thrift client to communicate with that server.\n\nRequirements\n------------\n\n- Python >= 3.7.0\n- async-timeout_\n- thriftpy2_\n\n.. _async-timeout: https://pypi.python.org/pypi/async_timeout\n.. _thriftpy2: https://thriftpy2.readthedocs.org/en/latest/\n\n\nLICENSE\n-------\n\n``aiothrift`` is offered under the MIT license.\n',
    'author': 'Ryan Wang',
    'author_email': 'hwwangwang@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/moonshadow/aiothrift/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
