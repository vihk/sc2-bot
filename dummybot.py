#CODE: BENJAMIN HUANG (PRIMARY), VIKRAM GILL

import sc2
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.data import Race

class DummyBot(BotAI):
    async def on_step(self, iteration: int):
        await self.distribute_workers()
