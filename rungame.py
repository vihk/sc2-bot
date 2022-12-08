#CODE: BENJAMIN HUANG (PRIMARY), VIKRAM GILL

import sc2
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.data import Race, Difficulty

from stalkerbot import Parting
from dummybot import DummyBot
run_game(
    sc2.maps.get("AbiogenesisLE"),
    [Bot(Race.Protoss, DummyBot()), Computer(Race.Protoss, Difficulty.Medium)],
    realtime=False,
) 
