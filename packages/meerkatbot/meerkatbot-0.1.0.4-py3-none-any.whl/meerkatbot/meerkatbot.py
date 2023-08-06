from meerkatbot.logger import Logger
from discord.ext import commands

from meerkatbot.exceptions import MeerkatExceptions
from meerkatbot.events import MeerkatEvents
from meerkatbot.commands import MeerkatCommands


class MeerkatBot(MeerkatExceptions, MeerkatEvents, MeerkatCommands):
    def __init__(self, **configs):
        hasToken = 'token' in configs
        hasPrefix = 'prefix' in configs
        hasLogger = 'logger' in configs
        # ? the token & prefix are required arguments
        if not hasToken or not hasPrefix:
            return self.badFormedMeerkatInstance()

        self.token = configs['token']
        self.prefix = configs['prefix']
        self.logger = Logger().log if not hasLogger else configs['logger']
        self.meerkat = commands.Bot(command_prefix=self.prefix)

        # ? Initializing inherited modules
        super().__init__()

    def run(self):
        self.logger('okGreen', '* STARTING MEERKAT BOT *')
        self.meerkat.run(self.token)
