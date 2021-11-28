import numpy as np
import particle_filter.script.parameter as pf_param
from .log import Log
from particle_filter.script.map import Map as PfMap
from . import parameter as param
from . import utility as util


class Map(PfMap):
    def __init__(self, log: Log) -> None:
        global RSSI_AT_BEACON

        RSSI_AT_BEACON = util.calc_rssi_by_dist(0)

        super().__init__(log)

    def estim_pos_by_triangulation(self, beacon_indexes: np.ndarray, rssis: np.ndarray) -> np.ndarray:
        if len(beacon_indexes) < 3:
            return np.full(2, np.nan, dtype=np.float16)    # can't solve triangulation

        else:
            if param.TRIANGULATE_POLICY == 2:    # interior division
                estim_pos, divided_rssi = util.divide_pos_and_rssi(self.beacon_pos_list[beacon_indexes[0]], self.beacon_pos_list[beacon_indexes[1]], rssis[0], rssis[1], RSSI_AT_BEACON)
                i = 2
                while i < len(beacon_indexes):
                    estim_pos, divided_rssi = util.divide_pos_and_rssi(estim_pos, self.beacon_pos_list[beacon_indexes[i]], divided_rssi, rssis[i], RSSI_AT_BEACON)
                    i += 1
            
            return estim_pos
    
    def draw_pos(self, pos: np.ndarray) -> None:
        if pf_param.ENABLE_CLEAR:
            self.clear()
        self._draw_any_pos(pos, (0, 0, 255))
