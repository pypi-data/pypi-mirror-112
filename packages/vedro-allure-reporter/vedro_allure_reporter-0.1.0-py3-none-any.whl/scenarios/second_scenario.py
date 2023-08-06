import vedro


@vedro.skip
class Scenario(vedro.Scenario):
    subject = "second scenario"

    def given(self):
        pass

    def when(self):
        pass

    def then(self):
        # print(self.response)
        pass
