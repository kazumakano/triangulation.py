
import math
from typing import Any
import numpy as np
import particle_filter.script.parameter as pf_param
from . import parameter as param


# calculate RSSI backward by distance-RSSI relation
def calc_rssi_by_dist(dist: float) -> float:
    return -5 * pf_param.PROPAG_COEF * math.log10(dist ** 2 + pf_param.EL_CORRECTION ** 2) - 80

def _divide_interiorly(ratio_1: np.float32, ratio_2: np.float32, val_1: Any, val_2: Any) -> Any:
    return (ratio_2 * val_1 + ratio_1 * val_2) / (ratio_1 + ratio_2)

def divide_pos_and_rssi(pos_1: np.ndarray, pos_2: np.ndarray, rssi_1: np.float32, rssi_2: np.float32, rssi_at_beacon: np.float32) -> tuple[np.ndarray, np.float32]:
    rssi_1_diff = rssi_at_beacon - rssi_1
    rssi_2_diff = rssi_at_beacon - rssi_2

    return _divide_interiorly(rssi_1_diff, rssi_2_diff, pos_1, pos_2), _divide_interiorly(rssi_1_diff, rssi_2_diff, rssi_1, rssi_2)

def get_strong_beacons(rssi_list: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    sorted_beacon_index_list: np.ndarray = rssi_list.argsort()[::-1]    # sort by strength

    strong_rssis = np.empty(0, dtype=np.float32)
    for i in range(param.MAX_USE_BEACON_NUM):
        if np.isneginf(rssi_list[sorted_beacon_index_list[i]]):
            break
        strong_rssis = np.hstack((strong_rssis, rssi_list[sorted_beacon_index_list[i]]))

    return sorted_beacon_index_list[:len(strong_rssis)], strong_rssis    # arrays of strong beacon index and RSSI
