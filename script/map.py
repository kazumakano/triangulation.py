from typing import Union
import numpy as np
import particle_filter.script.parameter as pf_param
from particle_filter.script.map import Map as PfMap
from . import parameter as param
from . import utility as util


class Map(PfMap):
    def __init__(self, mac_list: np.ndarray, result_dir: Union[str, None]) -> None:
        self.rssi_at_beacon = np.float32(util.calc_rssi_by_dist(0))

        super().__init__(mac_list, result_dir)

    def estim_pos_by_trilateration(self, beacon_indexes: np.ndarray, rssis: np.ndarray) -> np.ndarray:
        if len(beacon_indexes) < 3:
            return np.full(2, np.nan, dtype=np.float32)    # can't solve trilateration

        else:
            if param.TRILATERATE_POLICY == 1:
                pass    # not implemented yet
            elif param.TRILATERATE_POLICY == 2:    # interior division
                estim_pos, divided_rssi = util.divide_pos_and_rssi(self.beacon_pos_list[beacon_indexes[0]], self.beacon_pos_list[beacon_indexes[1]], rssis[0], rssis[1], self.rssi_at_beacon)
                for i in range(2, len(beacon_indexes)):
                    estim_pos, divided_rssi = util.divide_pos_and_rssi(estim_pos, self.beacon_pos_list[beacon_indexes[i]], divided_rssi, rssis[i], self.rssi_at_beacon)

                return estim_pos

    def draw_pos(self, pos: np.ndarray) -> None:
        if pf_param.ENABLE_CLEAR:
            self.clear()
        self._draw_pos((0, 0, 255), False, pos)
