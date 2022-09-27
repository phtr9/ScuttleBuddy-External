import os, sys
sys.path.insert(0, os.getcwd())

from audioop import add
from pymem import Pymem
from resources import LeagueReader, LeagueStorage
from resources.overlay import Overlay
from models import GameState

import time
import utils
from datetime import datetime, timedelta
from itertools import groupby
from collections import Counter


# SCRIPT WORKS WITH SOME TIME IN DELAY, BUT CAN SHOW YOU IF ENEMY HAS KILLED A MONSTER IN FOW
# WAIT FOR GAME TO LOAD SUMMONER'S RIFT, IF ERRORS START AGAIN
# MANUALLY GENERATING CAMPS IN PRACTICE TOOL FOR THE FIRST TIME BREAKS SCRIPT
# SIMPLY RESTART AGAIN


pm = Pymem('League of Legends.exe')
lStorage = LeagueStorage(pm)
mem = None
overlay = None

monsters_stored = {}

jungle_camps = {
    "gromp_blue": {
        "jungle_monsters": ["gromp_blue"],
        "initial_time": "01:42",
        "respawn_time": "02:15"
        },
    "blue_blue": {
        "jungle_monsters": ["blue_blue"],
        "initial_time": "01:30",
        "respawn_time": "05:00"
        },
    "wolves_blue": {
        "jungle_monsters": ["wolf_blue", "wolf_mini_blue_0", "wolf_mini_blue_1"],
        "initial_time": "01:30",
        "respawn_time": "02:15"
        },
    "raptors_blue": {
        "jungle_monsters": ["raptor_blue", "raptor_mini_blue_0", "raptor_mini_blue_1", "raptor_mini_blue_2", "raptor_mini_blue_3", "raptor_mini_blue_4"],
        "initial_time": "01:30",
        "respawn_time": "02:15"
        },
    "red_blue": {
        "jungle_monsters": ["red_blue"],
        "initial_time": "01:30",
        "respawn_time": "05:00"
        },
    "krugs_blue": {
        "jungle_monsters": ["krug_blue", "krug_mini_blue"],
        "initial_time": "01:42",
        "respawn_time": "02:15"
        },
    "gromp_red": {
        "jungle_monsters": ["gromp_red"],
        "initial_time": "01:42",
        "respawn_time": "02:15"
        },
    "blue_red": {
        "jungle_monsters": ["blue_red"],
        "initial_time": "01:30",
        "respawn_time": "05:00"
        },
    "wolves_red": {
        "jungle_monsters": ["wolf_red", "wolf_mini_red_0", "wolf_mini_red_1"],
        "initial_time": "01:30",
        "respawn_time": "02:15"
        },
    "raptors_red": {
        "jungle_monsters": ["raptor_red", "raptor_mini_red_0", "raptor_mini_red_1", "raptor_mini_red_2", "raptor_mini_red_3", "raptor_mini_red_4"],
        "initial_time": "01:30",
        "respawn_time": "02:15"
        },
    "red_red": {
        "jungle_monsters": ["red_red"],
        "initial_time": "01:30",
        "respawn_time": "05:00"
        },
    "krugs_red": {
        "jungle_monsters": ["krug_red", "krug_mini_red"],
        "initial_time": "01:42",
        "respawn_time": "02:15"
        },
}

for jungle_camp in jungle_camps:
    jungle_camps[jungle_camp]['is_up'] = False
    jungle_camps[jungle_camp]['death_time'] = None
    jungle_camps[jungle_camp]['timer'] = None


def get_timers():
    start = datetime.now()

    global pm
    global lStorage
    global mem
    global overlay

    global monsters_stored
    global jungle_camps

    def all_equal(iterable):
        g = groupby(iterable)
        return next(g, True) and not next(g, False)

    def most_common(lst):
        data = Counter(lst)
        return max(lst, key=data.get)

    # n = 0
    while True:
        # n += 1
        # st = time.time()
    
        view_proj_matrix = utils.find_view_proj_matrix(pm)
        lReader = LeagueReader(pm, mem, overlay, view_proj_matrix, lStorage)
        game_time = timedelta(seconds=GameState(pm).gameTime) 

        monsters_memory = []  # Monsters (names) in memory
        monsters_mini = ["raptor_mini_red", "raptor_mini_blue", "wolf_mini_red", "wolf_mini_blue"]
        samples = 10

        # To prevent errors reading memory, various samples need to be collected
        for n in range(samples):
            monster_buffer = []
            monsters = lReader.monsters()
            for monster in monsters:
                monster_name = monster.monster_name
                if monster_name:
                    if monster_name in monsters_mini:
                        count = sum([1 for name in monster_buffer if name.startswith(monster_name)])
                        monster_name = f"{monster_name}_{count}"
                    monster_buffer.append(monster_name)
            monsters_memory.append(','.join(monster_buffer))

        # if not all_equal(monsters_memory):
        #     print()
        #     print()
        #     for monsters in monsters_memory:
        #         print('ERRORS', monsters)

        monsters_memory = most_common(monsters_memory).split(',')

        for monster_name in monsters_memory:
            # Add monster to storage
            if monster_name and monster_name not in monsters_stored:
                monsters_stored[monster_name] = {"spawn_time": game_time, "death_time": None}
                # print(monster_name, monsters_stored[monster_name], "Monster spawned!")

            # If a monster is up, a camp is also up
            for jungle_camp, camp_info in jungle_camps.items():
                if monster_name in camp_info["jungle_monsters"] and not camp_info["is_up"]:
                    jungle_camps[jungle_camp]["is_up"] = True
                    # print(jungle_camp, "Camp spawned!")

        # OLD: without sampling
        # monsters_memory = []  # Monsters (names) in memory
        # monsters_mini = ["raptor_mini_red", "raptor_mini_blue", "wolf_mini_red", "wolf_mini_blue"]
        # for monster in monsters:
        #     monster_name = monster.monster_name
        #     if monster_name:
        #         if monster_name in monsters_mini:
        #             count = sum([1 for name in monsters_memory if name.startswith(monster_name)])
        #             monster_name = f"{monster_name}_{count}"
        #         monsters_memory.append(monster_name)
        #         # print(monster.name, monster_name, monster.gamePos)

        #     # Add monster to storage
        #     if monster_name and monster_name not in monsters_stored:
        #         monsters_stored[monster_name] = {"spawn_time": game_time, "death_time": None}
        #         print(monster_name, monsters_stored[monster_name], "Monster spawned!")

        # Add death stamp to stored monster
        for monster_name, monster_info in monsters_stored.items(): 
            if monster_name not in monsters_memory and not monster_info["death_time"]:
                elpased = datetime.now() - start
                monster_info["death_time"] = game_time - timedelta(seconds=4) - timedelta(seconds=elpased.seconds)
                print(monster_name, str(monster_info["death_time"]), "Monster dead!")

        # Set stored monsters after monsters in memory
        # monsters_stored = {monster_name: monster_info for monster_name, monster_info in monsters_stored.items() if monster_name in monsters_memory}

        monsters_dead_names = [monster_name for monster_name, monster_info in monsters_stored.items() if monster_info["death_time"]]
        for jungle_camp, camp_info in jungle_camps.items():
            if all(name in monsters_dead_names for name in camp_info["jungle_monsters"]):
                elpased = datetime.now() - start
                camp_info["death_time"] = game_time - timedelta(seconds=4) - timedelta(seconds=elpased.seconds)
                camp_info["is_up"] = False
                print(jungle_camp, str(camp_info["death_time"]), "Camp cleared!")

                # Delete dead monsters when camp is cleared
                monsters_stored = {monster_name: monster_info for monster_name, monster_info in monsters_stored.items() if monster_name not in camp_info["jungle_monsters"]}

        for jungle_camp, camp_info in jungle_camps.items():
            if not jungle_camps[jungle_camp]["is_up"]:
                if camp_info["death_time"]:
                    death_time = camp_info["death_time"]
                    respawn_time = datetime.strptime(camp_info["respawn_time"], "%M:%S")
                    spawn_time = death_time + respawn_time
                    timer = timedelta(seconds=1) + spawn_time - game_time
                    timer = timer.strftime("%M:%S")
                else:
                    timer = "ERROR"
                jungle_camps[jungle_camp]["timer"] = timer
                # jungle_camps[jungle_camp]["timer"] = "DEAD!"
            else:
                jungle_camps[jungle_camp]["timer"] = "UP!"

        # for jungle_camp, camp_info in jungle_camps.items():
        #     if not jungle_camps[jungle_camp]["is_up"]:
        #         initial_time = datetime.strptime(camp_info["initial_time"], "%M:%S")
        #         initial_delta = timedelta(minutes=initial_time.minute, seconds=initial_time.second)
        #         if game_time < initial_delta:
        #             spawn_time = initial_time - game_time
        #             timer = timedelta(seconds=1) + spawn_time - game_time
        #             timer = timer.strftime("%M:%S")
        #         else:
        #             if camp_info["death_time"]:
        #                 death_time = camp_info["death_time"]
        #                 respawn_time = datetime.strptime(camp_info["respawn_time"], "%M:%S")
        #                 spawn_time = death_time + respawn_time
        #                 timer = timedelta(seconds=1) + spawn_time - game_time
        #                 timer = timer.strftime("%M:%S")
        #             else:
        #                 timer = "ERROR"
                
        #         jungle_camps[jungle_camp]["timer"] = timer
        #         # jungle_camps[jungle_camp]["timer"] = "DEAD!"
        #     else:
        #         jungle_camps[jungle_camp]["timer"] = "UP!"

        # et = time.time()
        # execution_time = (et - st) * 1000
        # print(f"Average Execution time: {execution_time} ms")

        return jungle_camps

        # break

        # time.sleep(0.05)


if __name__ == '__main__':
    # get_timers()
    camp_names = [
        'gromp_blue', 'blue_blue', 'wolves_blue', 'raptors_blue', 'red_blue', 'krugs_blue',
        'gromp_red', 'blue_red', 'wolves_red', 'raptors_red', 'red_red', 'krugs_red'
    ]
    gui = Overlay(jungle_camps, True, get_timers)
    gui.run()
    # get_timers()
