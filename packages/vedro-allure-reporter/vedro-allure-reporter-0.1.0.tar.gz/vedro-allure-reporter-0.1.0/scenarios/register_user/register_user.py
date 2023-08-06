import asyncio

import vedro
from time import monotonic_ns


class Scenario(vedro.Scenario):
    subject = "register user"

    def given(self):
        pass

    async def when(self):
        await asyncio.sleep(0.2)
        self.res = 1

    def then(self):
       pass
