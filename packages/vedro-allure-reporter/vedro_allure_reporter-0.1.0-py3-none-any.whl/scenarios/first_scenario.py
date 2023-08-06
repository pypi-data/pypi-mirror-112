import vedro
from vedro import params


class Scenario(vedro.Scenario):
    subject = "first scenario {username!r}"

    @params("Bob")
    @params("Alice")
    def __init__(self, username):
        self.username = username

    def given(self):
        self.result = []

    async def when(self):
        pass

    def then(self):
        assert self.username == "Bob"
