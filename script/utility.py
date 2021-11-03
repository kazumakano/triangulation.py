
import math
from typing import Any, Tuple, Union
import numpy as np
import particle_filter.script.parameter as pf_param


# calculate RSSI backward by distance-RSSI relation
def calc_rssi_by_dist(dist: float) -> float:
    return -10 * pf_param.PROPAG_COEF * math.log10(dist + pf_param.EL_CORRECTION) - 68

def _divide_interiorly(val_1: Any, val_2: Any, ratio_1: np.float64, ratio_2: np.float64) -> Any:
    return (ratio_2 * val_1 + ratio_1 * val_2) / (ratio_1 + ratio_2)

def divide_pos_and_rssi(pos_1: np.ndarray, pos_2: np.ndarray, rssi_1: Union[np.float16, np.float64], rssi_2: Union[np.float16, np.float64], rssi_at_beacon: float) -> Tuple[np.ndarray, np.float64]:
    rssi_diff_1 = rssi_at_beacon - rssi_1
    rssi_diff_2 = rssi_at_beacon - rssi_2

    return _divide_interiorly(pos_1, pos_2, rssi_diff_1, rssi_diff_2), _divide_interiorly(rssi_1, rssi_2, rssi_diff_1, rssi_diff_2)
