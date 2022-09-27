from models import Entity, GameState
from resources import offsets
from pymem import Pymem
from functools import cached_property
from datetime import timedelta


class CampRespawnEntity(Entity):
    jungle_camps = {
        "gromp_blue": {
            "spawn_pos": {'x': 2288.0185546875, 'y': 51.777305603027344, 'z': 8448.1337890625},
            "initial_time": "01:42",
            "respawn_time": "02:15"
        },
        "blue_blue": {
            "spawn_pos": {'x': 3821.488525390625, 'y': 51.12874221801758, 'z': 8101.05419921875},
            "initial_time": "01:30",
            "respawn_time": "05:00"
        },
        "wolves_blue": {
            "spawn_pos": {'x': 3783.3798828125, 'y': 52.46272277832031, 'z': 6495.56005859375},
            "initial_time": "01:30",
            "respawn_time": "02:15"
        },
        "raptors_blue": {
            "spawn_pos": {'x': 7061.5, 'y': 50.12364196777344, 'z': 5325.509765625},
            "initial_time": "01:30",
            "respawn_time": "02:15"
        },
        "red_blue": {
            "spawn_pos": {'x': 7762.24365234375, 'y': 53.967735290527344, 'z': 4011.186767578125},
            "initial_time": "01:30",
            "respawn_time": "05:00"
        },
        "krugs_blue": {
            "spawn_pos": {'x': 8394.76953125, 'y': 50.7310676574707, 'z': 2641.590087890625},
            "initial_time": "01:42",
            "respawn_time": "02:15"
        },
        "gromp_red": {
            "spawn_pos": {'x': 12703.62890625, 'y': 51.6907844543457, 'z': 6443.98388671875},
            "initial_time": "01:42",
            "respawn_time": "02:15"
        },
        "blue_red": {
            "spawn_pos": {'x': 11131.728515625, 'y': 51.72368621826172, 'z': 6990.84423828125},
            "initial_time": "01:30",
            "respawn_time": "05:00"
        },
        "wolves_red": {
            "spawn_pos": {'x': 11059.76953125, 'y': 60.35258483886719, 'z': 8419.830078125},
            "initial_time": "01:30",
            "respawn_time": "02:15"
        },
        "raptors_red": {
            "spawn_pos": {'x': 7820.22021484375, 'y': 52.19202423095703, 'z': 9644.4501953125},
            "initial_time": "01:30",
            "respawn_time": "02:15"
        },
        "red_red": {
            "spawn_pos": {'x': 7066.869140625, 'y': 56.186641693115234, 'z': 10975.546875},
            "initial_time": "01:30",
            "respawn_time": "05:00"
        },
        "krugs_red": {
            "spawn_pos": {'x': 6499.490234375, 'y': 56.47679901123047, 'z': 12287.3798828125},
            "initial_time": "01:42",
            "respawn_time": "02:15"
        },
        "scuttle_top": {
            "spawn_pos": {'x': 4400.0, 'y': -66.53082275390625, 'z': 9600.0},
            "initial_time": "03:15",
            "respawn_time": "02:30"
        },
        "scuttle_bottom": {
            "spawn_pos": {'x': 10500.0, 'y': -62.81019973754883, 'z': 5170.0},
            "initial_time": "03:15",
            "respawn_time": "02:30"
        },
        "drake": {
            "spawn_pos": {'x': 9866.1484375, 'y': -71.2406005859375, 'z': 4414.01416015625},
            "initial_time": "05:00",
            "respawn_time": "05:00"
        },
        "herald": {
            "spawn_pos": {'x': 5007.12353515625, 'y': -71.2406005859375, 'z': 10471.4462890625},
            "initial_time": "08:00",
            "respawn_time": "06:00"
        },
        "baron": {
            "spawn_pos": {'x': 5007.12353515625, 'y': -71.2406005859375, 'z': 10471.4462890625},
            "initial_time": "20:00",
            "respawn_time": "06:00"
        },
    }

    def __init__(self, pm: Pymem, mem, overlay, viewProjMatrix, entityAddress: int):
        super().__init__(pm, mem, overlay, viewProjMatrix, entityAddress)
        self.camp_name = self._get_camp_name()
        self.death_time = timedelta(seconds=GameState(self.pm).gameTime)
        self.initial_time = self._initial_time()
        self.respawn_time = self._respawn_time()
        self.spawn_time = self._respawn_time()

        self.initial_time = self._initial_time()
        self.respawn_time = self._respawn_time()
        self.spawn_time = self._spawn_time()

    def _get_camp_name(self):
        for camp_name, camp_info in CampRespawnEntity.jungle_camps.items():
            current_time = timedelta(seconds=GameState(self.pm).gameTime)
            if self.gamePos == camp_info["spawn_pos"]:
                if camp_name == "herald" and current_time < timedelta(seconds=self.initial_time.seconds):
                    return camp_name
                elif camp_name == "baron":
                    return camp_name
                return camp_name
        return None

    def _initial_time(self):
        if self.camp_name:
            minutes, seconds = CampRespawnEntity.jungle_camps[self.camp_name]["initial_time"].split(":")
            return timedelta(minutes=int(minutes), seconds=int(seconds))
        return None

    def _respawn_time(self):
        if self.camp_name:
            minutes, seconds = CampRespawnEntity.jungle_camps[self.camp_name]["respawn_time"].split(":")
            return timedelta(minutes=int(minutes), seconds=int(seconds))
        return None

    def _spawn_time(self):
        if self.camp_name:
            return self.death_time + self.respawn_time
        return None

    def spawn_time_left(self):
        def convert(seconds):
            min, sec = divmod(seconds, 60)
            return '%02d:%02d' % (min, sec)

        if self.camp_name:
            current_time = timedelta(seconds=GameState(self.pm).gameTime)
            # Add 1 second
            spawn_time_left = timedelta(seconds=1) + self.spawn_time - current_time
            if spawn_time_left.total_seconds() > 0:
                return convert(spawn_time_left.total_seconds())
            else:
                return "UP!"
        return None
