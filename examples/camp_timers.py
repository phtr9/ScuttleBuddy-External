import os, sys
sys.path.insert(0, os.getcwd())

from pymem import Pymem, exception
from resources import LeagueReader, LeagueStorage, offsets
from resources.overlay import Overlay
from models import GameState, Monster

import time
import utils


# WAIT FOR GAME TO LOAD SUMMONER'S RIFT, IF ERRORS START AGAIN
# MANUALLY GENERATING CAMPS IN PRACTICE TOOL FOR THE FIRST TIME BREAKS SCRIPT
# SIMPLY RESTART AGAIN


pm = Pymem('League of Legends.exe')
lStorage = LeagueStorage(pm)
mem = None
overlay = None

camps_stored = {}
camps_memory = {}


def get_timers():
    global pm
    global lStorage
    global mem
    global overlay

    global camps_stored
    global camps_memory

    # n = 0
    while True:
        # n += 1
        # st = time.time()

        view_proj_matrix = utils.find_view_proj_matrix(pm)
        lReader = LeagueReader(pm, mem, overlay, view_proj_matrix, lStorage)
        camp_respawns = lReader.campRespawns

        camps_memory = []
        # ACTIVATE TIMERS WHEN CAMP SPAWNS
        for camp_respawn in camp_respawns:
            if camp_respawn.camp_name:
                camps_memory.append(camp_respawn.camp_name)
                if camp_respawn.camp_name not in camps_stored.keys():
                    camps_stored[camp_respawn.camp_name] = {}
                if not camps_stored[camp_respawn.camp_name]:
                    camps_stored[camp_respawn.camp_name] = camp_respawn

        # # DEACTIVATE TIMERS WHEN CAMP DIES
        # # TODO: check if camp is already in monster manager, timers don't work properly if manually respawned inside practice tool
        for camp_name, camp_respawn in camps_stored.items():
            if camp_name not in camps_memory:
                camps_stored[camp_name] = {}

        camps_timers = {}
        for camp_name, camp_respawn in camps_stored.items():
            if camp_respawn:
                camps_timers[camp_respawn.camp_name] = camp_respawn.spawn_time_left()        

        # # et = time.time()
        # # execution_time = (et - st) * 1000
        # # print(f"Average Execution time: {execution_time} ms")

        return camps_timers


if __name__ == '__main__':
    # get_timers()
    camp_names = [
        'gromp_blue', 'blue_blue', 'wolves_blue', 'raptors_blue', 'red_blue', 'krugs_blue',
        'gromp_red', 'blue_red', 'wolves_red', 'raptors_red', 'red_red', 'krugs_red',
        'scuttle_top', 'scuttle_bottom', 'drake', 'herald', 'baron'
    ]
    gui = Overlay(camp_names, False, get_timers)
    gui.run()
