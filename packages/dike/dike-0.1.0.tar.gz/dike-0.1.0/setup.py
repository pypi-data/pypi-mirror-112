# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dike', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['pymdown-extensions[docs]>=8.2,<9.0']

setup_kwargs = {
    'name': 'dike',
    'version': '0.1.0',
    'description': 'Python asyncio tools for web service resilience.',
    'long_description': '# dike - Python asyncio tools for web service resilience\n\n[<img src="https://img.shields.io/pypi/v/dike.svg" alt="Release Status">](https://pypi.python.org/pypi/dike)\n[<img src="https://github.com/chr1st1ank/dike/actions/workflows/test.yml/badge.svg?branch=main" alt="CI Status">](https://github.com/chr1st1ank/dike/actions)\n[![codecov](https://codecov.io/gh/chr1st1ank/dike/branch/main/graph/badge.svg?token=4oBkRHXbfa)](https://codecov.io/gh/chr1st1ank/dike)\n\n\n* Documentation: <https://chr1st1ank.github.io/dike/>\n* License: Apache-2.0\n* Status: Initial development\n\n## Features\n\n### Concurrency limiting for asynchronous functions\nThe `@limit_jobs` decorator allows to limit the number of concurrent excecutions of a coroutine \nfunction. This can be useful for limiting queueing times or for limiting the load put\nonto backend services.\n\nExample with an external web request using the [httpx](https://github.com/encode/httpx) library:\n\n```python\nimport asyncio\nimport httpx\nimport dike\n\n\n@dike.limit_jobs(limit=2)\nasync def web_request():\n    async with httpx.AsyncClient() as client:\n        response = await client.get("https://httpstat.us/200?sleep=100")\n    return response\n\n\nasync def main():\n    responses = await asyncio.gather(\n        web_request(), web_request(), web_request(), return_exceptions=True\n    )\n    for r in responses:\n        if isinstance(r, dike.TooManyCalls):\n            print("too many calls")\n        else:\n            print(r)\n\n\nasyncio.run(main())\n```\n\nThe output shows that the first two requests succeed. The third one hits the concurrency limit:\n```\n<Response [200 OK]>\n<Response [200 OK]>\ntoo many calls\n```\n\n### Mini-batching for asynchronous function calls\nThe `@batch` decorator groups function calls into batches and only calls the wrapped function \nwith the aggregated input.\n\nThis is useful if the function scales well with the size of the input arguments but you\'re\ngetting the input data in smaller bits, e.g. as individual HTTP requests.\n\nExample:\n\n```python\nimport asyncio\nimport dike\n\n\n@dike.batch(target_batch_size=3, max_waiting_time=10)\nasync def f(arg1, arg2):\n    print(f"arg1: {arg1}")\n    print(f"arg2: {arg2}")\n    return [10, 11, 12]\n\n\nasync def main():\n    result = await asyncio.gather(\n        f([0], ["a"]),\n        f([1], ["b"]),\n        f([2], ["c"]),\n    )\n\n    print(f"Result: {result}")\n\n\nasyncio.run(main())\n```\n\nOutput:\n```\narg1: [0, 1, 2]\narg2: [\'a\', \'b\', \'c\']\nResult: [[10], [11], [12]]\n```\n\n## Installation\nSimply install from pypi. The library is pure Python without any dependencies other than the\nstandard library.\n```\npip install dike\n```\n',
    'author': 'Christian Krudewig',
    'author_email': 'chr1st1ank@krudewig-online.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chr1st1ank/dike',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
