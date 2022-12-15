#CODE: BENJAMIN HUANG (PRIMARY), VIKRAM GILL

import sc2
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.data import Race
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.buff_id import BuffId

#Lists to help determine which production building type to use
gatewayunits = [UnitTypeId.ZEALOT, UnitTypeId.STALKER, UnitTypeId.SENTRY, UnitTypeId.ADEPT, UnitTypeId.HIGHTEMPLAR, UnitTypeId.DARKTEMPLAR]
robounits = [UnitTypeId.OBSERVER, UnitTypeId.WARPPRISM]
stargateunits = []
build_order = [
                [14, UnitTypeId.PYLON],
                [15, UnitTypeId.GATEWAY],
                [16, AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, UnitTypeId.NEXUS],
                [16, UnitTypeId.ASSIMILATOR],
                [20, UnitTypeId.CYBERNETICSCORE],
                [20, UnitTypeId.NEXUS],
                [20, UnitTypeId.PYLON],
                [21, UnitTypeId.ASSIMILATOR],
                [21, UnitTypeId.ADEPT],
                [21, UpgradeId.WARPGATERESEARCH, UnitTypeId.CYBERNETICSCORE],
                [24, AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, UnitTypeId.GATEWAY],
                [25, UnitTypeId.STALKER],
                [28, AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, UnitTypeId.GATEWAY],
                [28, UnitTypeId.TWILIGHTCOUNCIL],
                [29, UnitTypeId.STALKER],
                [34, UnitTypeId.ROBOTICSFACILITY],
                [37, AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, UnitTypeId.NEXUS],
                [37, UpgradeId.BLINKTECH, UnitTypeId.TWILIGHTCOUNCIL],
                [37, AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, UnitTypeId.TWILIGHTCOUNCIL],
                [38, UnitTypeId.GATEWAY],
                [39, UnitTypeId.GATEWAY],
                [40, UnitTypeId.GATEWAY],
                [40, UnitTypeId.PYLON],
                [40, UnitTypeId.OBSERVER],
                [43, UnitTypeId.STALKER],
                #[45, AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, UnitTypeId.TWILIGHTCOUNCIL],
                [46, UnitTypeId.PYLON],
                [46, UnitTypeId.WARPPRISM],
                [50, AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, UnitTypeId.TWILIGHTCOUNCIL],
                #[43, UnitTypeId.STALKER],
                [53, UnitTypeId.PYLON],
                [53, UnitTypeId.ASSIMILATOR]
                #benchmark 5:11, 11 stalkers
                ]

#i mean, you can get started with troop movement in a different bot I think? maybe use a different build order that only involves zealots or easily moved-across-the-map-and-win units?

class Zealot(BotAI): 
    def __init__(self):
        super().__init__()
        self.order_number = 0
        self.structuresDict = {
            UnitTypeId.GATEWAY: UnitTypeId.PYLON,
            UnitTypeId.CYBERNETICSCORE: UnitTypeId.GATEWAY,
            UnitTypeId.TWILIGHTCOUNCIL: UnitTypeId.CYBERNETICSCORE, 
            UnitTypeId.ROBOTICSFACILITY: UnitTypeId.CYBERNETICSCORE
        }
    def has_tech_unlocked(self,unit):
        return len(self.structures(self.structuresDict[unit]).ready) > 0
    async def on_step(self,iteration: int):
        current_order = build_order[self.order_number]
        


        