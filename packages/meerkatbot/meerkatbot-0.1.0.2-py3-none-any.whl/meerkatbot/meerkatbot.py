from discord.ext import commands


class MeerkatBot:
    def __init__(self, **configs):
        hasToken = 'token' in configs
        hasPrefix = 'prefix' in configs
        hasLogging = 'logging' in configs
        if not hasToken or not hasPrefix:
            raise Exception(
                'Verify you are sending token and prefix keyword variables to MeerkatBot <constructor>, these are required arguments.'
            )
        self.token = configs['token']
        self.prefix = configs['prefix']
        self.logging = True if not hasLogging else configs['logging']
        self.meerkat = commands.Bot(command_prefix=self.prefix)

    def badFormedCommandBulkUse(self):
        raise Exception(
            'Verify you are sending (name=str, command=async function) to MeerkatBot <use> method [(name, command), (name,command)], these are required arguments.'
        )

    def bulkUse(self, uses):
        for use in uses:
            # ? Types verifications
            if type(use) != tuple:
                self.badFormedCommandBulkUse()
            if type(use[0]) != str or not callable(use[1]):
                self.badFormedCommandBulkUse()

            # ? Setting up discord command
            name, command = use
            self.meerkat.command(name=name)(command)

        return self

    def use(self, name=None, command=None):
        if type(name) != str or not callable(command):
            raise Exception(
                'Verify you are sending name and command keyword variables to MeerkatBot <use> method, these are required arguments.'
            )

        self.meerkat.command(name=name)(command)
        return self

    def run(self):
        if self.logging:
            print("* STARTING MEERKAT BOT *")
        self.meerkat.run(self.token)
