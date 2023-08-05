# aiomsa
[![build](https://github.com/facebookexternal/aiomsa/actions/workflows/build.yml/badge.svg)](https://github.com/facebookexternal/aiomsa/actions/workflows/build.yml)
[![style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI - Downloads](https://img.shields.io/pypi/dw/aiomsa)

*aiomsa* is a Python 3.7+ framework built using `asyncio`. At its core, *aiomsa*
provides a simple and standardized way to write xApps that can be deployed as
microservices in Python.

## Installation
*aiomsa* can be installed from PyPI.
```bash
pip install aiomsa
```

You can also get the latest code from GitHub.
```bash
poetry add git+https://github.com/facebookexternal/aiomsa
```

## Getting Started
The follwing example shows how to use *aiomsa* to create a simple xApp for subscribing
to the E2T service for a particular custom service model.

```python
import asyncio

import aiomsa
import aiomsa.abc
from onos_ric_sdk_py import E2Client, SDLClient

from .models import MyModel


async def run(e2: aiomsa.abc.E2Client, e2_node_id: str) -> None:
   subscription = await e2.subscribe(
      e2_node_id,
      service_model_name="my_model",
      service_model_version="v1",
      subscription_id="my_app-my_model-sub",
      trigger=bytes(MyModel(param="foo")),
      actions=[
         aiomsa.abc.RICAction(
            id=1,
            type=aiomsa.abc.RICActionType.REPORT,
            subsequent_action_type=aiomsa.abc.RICSubsequentActionType.CONTINUE,
            time_to_wait=aiomsa.abc.RICTimeToWait.ZERO,
         )
      ],
   )

   async for (_header, message) in subscription:
      print(message)


async def main() -> None:
   async with E2Client(app_id="my_app", e2t_endpoint="e2t:5150") as e2, SDLClient(
      topo_endpoint="topo:5150"
   ) as sdl:
      async for e2_node in sdl.watch_e2_connections():
         asyncio.create_task(run(e2, e2_node.id))


if __name__ == "__main__":
   aiomsa.run(main())
```
