#CODE: BEJAMIN HUANG
import sc2
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.data import Race

'''
from botai1 import MrBenBot
from dummybot import DummyBot
run_game(
    sc2.maps.get("68935c92125a3828034dd3f93212ef0adf8ec33b491b7bdd0ee158c3daccc8df"),
    [Bot(Race.Protoss, DummyBot()), Bot(Race.Protoss, MrBenBot())],
    realtime=True,
)
'''

from stalkerbot import Parting
from dummybot import DummyBot
run_game(
    sc2.maps.get("68935c92125a3828034dd3f93212ef0adf8ec33b491b7bdd0ee158c3daccc8df"),
    [Bot(Race.Protoss, DummyBot()), Bot(Race.Protoss, Parting())],
    realtime=False,
)
'''
from stalkerbotbackup import Parting
from dummybot import DummyBot
run_game(
    sc2.maps.get("68935c92125a3828034dd3f93212ef0adf8ec33b491b7bdd0ee158c3daccc8df"),
    [Bot(Race.Protoss, DummyBot()), Bot(Race.Protoss, Parting())],
    realtime=False,
)'''
