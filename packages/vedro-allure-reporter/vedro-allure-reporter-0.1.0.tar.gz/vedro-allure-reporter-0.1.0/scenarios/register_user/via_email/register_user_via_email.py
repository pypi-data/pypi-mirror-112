import vedro
import asyncio
import random


class Scenario(vedro.Scenario):
    subject = "register user via email 0"
    tags = ["API"]

    def given(self):
        self.email = "user@"
        self.user_id = random.randint(1, 2**31-1)

    async def when(self):
        print(self.user_id)
        await asyncio.sleep(0.0)

    async def then(self):
        await asyncio.sleep(0.1)
