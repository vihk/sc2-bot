#CODE: BENJAMIN HUANG
import sc2
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.data import Race
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.buff_id import BuffId

#Build Order Infrastructure
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

#Lists to help determine which production building type to use
gatewayunits = [UnitTypeId.ZEALOT, UnitTypeId.STALKER, UnitTypeId.SENTRY, UnitTypeId.ADEPT, UnitTypeId.HIGHTEMPLAR, UnitTypeId.DARKTEMPLAR]
robounits = [UnitTypeId.OBSERVER, UnitTypeId.WARPPRISM]
stargateunits = []


class Parting(BotAI):
    async def on_step(self, iteration: int):
        #Determine if tech tree has been progressed enough to build new tech
        #(without this, the bot will attempt to build a building even if it's impossible. There's no pre-written function to determine tech tree unlocks, only affordability)
        def has_tech_unlocked(unit):
            if unit == UnitTypeId.GATEWAY:
                return len(self.structures(UnitTypeId.PYLON).ready) > 0
            elif unit == UnitTypeId.CYBERNETICSCORE:
                return len(self.structures(UnitTypeId.GATEWAY).ready) > 0
            elif unit == UnitTypeId.TWILIGHTCOUNCIL:
                return len(self.structures(UnitTypeId.CYBERNETICSCORE).ready) > 0
            elif unit == UnitTypeId.ROBOTICSFACILITY:
                return len(self.structures(UnitTypeId.CYBERNETICSCORE).ready) > 0
            else:
                True

        #Testing Tools:
        try:
            print(build_order[0])
            print(has_tech_unlocked(build_order[0][1]))
        except:
            None

        #Automatically distribute any idle workers to mineral lines
        await self.distribute_workers()

        #random nexus selection (the loops go so fast you can just assume it's selecting all nexi)
        nexus = self.townhalls.ready.random

        #Probe Production until user defined cap
        if self.can_afford(UnitTypeId.PROBE) and nexus.is_idle and self.supply_workers < 41:
            nexus.train(UnitTypeId.PROBE)

        #Infrastructure/Tech/Units to be built in Build Order list
        if (
            len(build_order) > 0
            and self.supply_used >= build_order[0][0]
        ):
            #Build buildings and units
            if len(build_order[0]) == 2 and self.can_afford(build_order[0][1]):
                pylon = self.structures(UnitTypeId.PYLON).ready.random_or(None)
                if build_order[0][1] == UnitTypeId.PYLON:
                    #print(f"Attempting to build pylon")
                    act = await self.build(UnitTypeId.PYLON, near=nexus.position.towards(self.game_info.map_center, 9))
                    if act:
                        build_order.remove(build_order[0])
                elif build_order[0][1] == UnitTypeId.NEXUS:
                    #print(f"Attempting to build nexus")
                    await self.expand_now()
                    build_order.remove(build_order[0])
                elif build_order[0][1] == UnitTypeId.ASSIMILATOR:
                    #print(f"Attempting to build assimilator")
                    vgs = self.vespene_geyser.closer_than(15, nexus)
                    for vg in vgs:
                        worker = self.select_build_worker(vg.position)
                        if worker is None:
                            break
                        elif not self.gas_buildings or not self.gas_buildings.closer_than(1, vg):
                            act = worker.build_gas(vg)
                            worker.stop(queue=True)
                            print(act)
                            if act:
                                build_order.remove(build_order[0])
                                break
                elif has_tech_unlocked(build_order[0][1]):
                    #print(f"Attempting to build {build_order[0][1]}")
                    act = await self.build(build_order[0][1], near=pylon)
                    print(act)
                    if act:
                        build_order.remove(build_order[0])
                #If not a building next in list, must be unit, therefore build unit
                else:
                    #print(f"Attempting to build unit")
                    if build_order[0][1] in gatewayunits:
                        if len(self.structures(UnitTypeId.WARPGATE).ready) > 0:
                            warpinpylon = self.structures(UnitTypeId.PYLON).closest_to(self.enemy_start_locations[0]).position.to2.random_on_distance(4)
                            placement = await self.find_placement(AbilityId.WARPGATETRAIN_STALKER, warpinpylon, placement_step=1)
                            warpgate = self.structures(UnitTypeId.WARPGATE).ready.random
                            abilities = await self.get_available_abilities(warpgate)
                            act = warpgate.warp_in(UnitTypeId.STALKER, placement)
                            if act:
                                build_order.remove(build_order[0])
                        elif len(self.structures(UnitTypeId.GATEWAY).ready) > 0:
                            act = self.structures(UnitTypeId.GATEWAY).ready.random.train(build_order[0][1])
                            if act:
                                build_order.remove(build_order[0])
                        else:
                            None
                    elif build_order[0][1] in robounits and len(self.structures(UnitTypeId.ROBOTICSFACILITY).ready) > 0:
                        act = self.structures(UnitTypeId.ROBOTICSFACILITY).ready.random.train(build_order[0][1])
                        if act:
                            build_order.remove(build_order[0])
                    elif build_order[0][1] in robounits and len(self.structures(UnitTypeId.STARGATE).ready) > 0:
                        act = self.structures(UnitTypeId.STARGATE).ready.random.train(build_order[0][1])
                        if act:
                            build_order.remove(build_order[0] )
            #Use unit/building abilities and start upgrades
            elif len(build_order[0]) == 3 and len(self.structures(build_order[0][2]).ready) > 0:
                #Use Chronoboost
                target = self.structures(build_order[0][2]).ready.random_or(None)
                if (
                    build_order[0][1] == AbilityId.EFFECT_CHRONOBOOSTENERGYCOST
                    and not target.has_buff(BuffId.CHRONOBOOSTENERGYCOST)
                    and not target.is_idle
                ):
                    if nexus.energy >= 50:
                        act = nexus(build_order[0][1], target)
                        if act:
                            build_order.remove(build_order[0])
                #Upgrades
                elif build_order[0][1] in UpgradeId and self.can_afford(build_order[0][1]):
                    act = target.research(build_order[0][1])
                    if act:
                        build_order.remove(build_order[0])
