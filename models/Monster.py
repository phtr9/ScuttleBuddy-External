from models import Entity
from pymem import Pymem
import math


class MonsterEntity(Entity):

    jungle_monsters = {
        "gromp_blue": {"type": "SRU_Gromp", "spawn_pos": {'x': 2110.6279296875, 'y': 51.77731704711914, 'z': 8450.984375}},
        "blue_blue": {"type": "SRU_Blue", "spawn_pos": {'x': 3821.488525390625, 'y': 52.03593063354492, 'z': 7901.05419921875}},
        "wolf_blue": {"type": "SRU_Murkwolf", "spawn_pos": {'x': 3780.6279296875, 'y': 52.46319580078125, 'z': 6443.98388671875}},
        "wolf_mini_blue": {"type": "SRU_MurkwolfMini", "spawn_pos": {'x': 3980.6279296875, 'y': 52.465576171875, 'z': 6443.98388671875}},
        "wolf_mini_blue": {"type": "SRU_MurkwolfMini", "spawn_pos": {'x': 3730.6279296875, 'y': 52.461395263671875, 'z': 6593.98388671875}},
        "raptor_blue": {"type": "SRU_Razorbeak", "spawn_pos": {'x': 6823.89501953125, 'y': 54.782833099365234, 'z': 5507.755859375}},
        "raptor_mini_blue": {"type": "SRU_RazorbeakMini", "spawn_pos": {'x': 6923.89501953125, 'y': 58.17090606689453, 'z': 5607.755859375}},
        "raptor_mini_blue": {"type": "SRU_RazorbeakMini", "spawn_pos": {'x': 7060.4580078125, 'y': 54.98870849609375, 'z': 5499.27392578125}},
        "raptor_mini_blue": {"type": "SRU_RazorbeakMini", "spawn_pos": {'x': 6962.7177734375, 'y': 50.31254196166992, 'z': 5354.35400390625}},
        "raptor_mini_blue": {"type": "SRU_RazorbeakMini", "spawn_pos": {'x': 6852.22900390625, 'y': 48.527000427246094, 'z': 5227.083984375}},
        "raptor_mini_blue": {"type": "SRU_RazorbeakMini", "spawn_pos": {'x': 7106.22900390625, 'y': 48.71413040161133, 'z': 5266.083984375}},
        "red_blue": {"type": "SRU_Red", "spawn_pos": {'x': 7765.244140625, 'y': 53.956443786621094, 'z': 4020.18701171875}},
        "krug_blue": {"type": "SRU_Krug", "spawn_pos": {'x': 8482.470703125, 'y': 50.648094177246094, 'z': 2705.947998046875}},
        "krug_mini_blue": {"type": "SRU_KrugMini", "spawn_pos": {'x': 8275.470703125, 'y': 51.130001068115234, 'z': 2688.947998046875}},
        "gromp_red": {"type": "SRU_Gromp", "spawn_pos": {'x': 12703.62890625, 'y': 51.6907844543457, 'z': 6443.98388671875}},
        "blue_red": {"type": "SRU_Blue", "spawn_pos": {'x': 11031.728515625, 'y': 51.72364044189453, 'z': 6990.84423828125}},
        "wolf_red": {"type": "SRU_Murkwolf", "spawn_pos": {'x': 11008.15234375, 'y': 62.09050369262695, 'z': 8387.408203125}},
        "wolf_mini_red": {"type": "SRU_MurkwolfMini", "spawn_pos": {'x': 11058.15234375, 'y': 62.23262405395508, 'z': 8217.408203125}},
        "wolf_mini_red": {"type": "SRU_MurkwolfMini", "spawn_pos": {'x': 10808.15234375, 'y': 63.012882232666016, 'z': 8387.408203125}},
        "raptor_red": {"type": "SRU_Razorbeak", "spawn_pos": {'x': 7986.9970703125, 'y': 52.347938537597656, 'z': 9471.388671875}},
        "raptor_mini_red": {"type": "SRU_RazorbeakMini", "spawn_pos": {'x': 7886.99658203125, 'y': 52.44501495361328, 'z': 9312.3896484375}},
        "raptor_mini_red": {"type": "SRU_RazorbeakMini", "spawn_pos": {'x': 7756.9970703125, 'y': 52.363792419433594, 'z': 9451.388671875}},
        "raptor_mini_red": {"type": "SRU_RazorbeakMini", "spawn_pos": {'x': 7854.38916015625, 'y': 52.265750885009766, 'z': 9610.4736328125}},
        "raptor_mini_red": {"type": "SRU_RazorbeakMini", "spawn_pos": {'x': 7997.22900390625, 'y': 51.425865173339844, 'z': 9772.083984375}},
        "raptor_mini_red": {"type": "SRU_RazorbeakMini", "spawn_pos": {'x': 7724.22900390625, 'y': 51.87107467651367, 'z': 9724.083984375}},
        "red_red": {"type": "SRU_Red", "spawn_pos": {'x': 7101.869140625, 'y': 56.282676696777344, 'z': 10900.546875}},
        "krug_red": {"type": "SRU_Krug", "spawn_pos": {'x': 6317.09228515625, 'y': 56.47679901123047, 'z': 12146.4580078125}},
        "krug_mini_red": {"type": "SRU_KrugMini", "spawn_pos": {'x': 6547.09228515625, 'y': 56.47679901123047, 'z': 12156.4580078125}}
    }

    def __init__(self, pm: Pymem, mem, overlay, viewProjMatrix, entityAddress: int):
        super().__init__(pm, mem, overlay, viewProjMatrix, entityAddress)
        self.monster_name = self._get_monster_name()
        
    def _get_monster_name(self):
        for monster_name, monster_info in MonsterEntity.jungle_monsters.items():
            if self.name == monster_info["type"]:
                spawn_pos = (monster_info["spawn_pos"]["x"], monster_info["spawn_pos"]["y"], monster_info["spawn_pos"]["z"])
                current_pos = (self.gamePos["x"], self.gamePos["y"], self.gamePos["z"])
                distance = math.dist(spawn_pos, current_pos)
                if distance <= 2000:
                    return monster_name
        return None
