class MeerkatCommands:
    def bulkUse(self, uses):
        for use in uses:
            # ? Types verifications
            if type(use) != tuple:
                self.badFormedCommandBulkUse()
            if type(use[0]) != str or not callable(use[1]):
                self.badFormedCommandBulkUse()

            # ? Setting up discord command
            name, command = use
            self.use(name, command, False)
        return self

    def use(self, name=None, command=None, end=True):
        if type(name) != str or not callable(command):
            raise Exception(
                'Verify you are sending name and command to MeerkatBot <use> method, these are required arguments.'
            )

        self.meerkat.command(name=name)(command)

        if end:
            return self
