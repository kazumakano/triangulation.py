import os.path as path
from typing import Union
import numpy as np
from particle_filter.script.parameter import set_params as set_pf_params


def _set_log_params(conf: dict) -> None:
    global LERP_WIN_POLICY, FREQ, MAX_BLANK_LEN, MAX_USE_BEACON_NUM

    LERP_WIN_POLICY = np.int8(conf["lerp_win_policy"])           # 1 linear interpolation, 2: sliding window
    FREQ = np.float16(conf["lerp_freq"])                         # frequency at log interpolation [/second]
    MAX_BLANK_LEN = np.float16(conf["max_blank_len"])            # maximum length of blank to interpolate [second]
    MAX_USE_BEACON_NUM = np.uint8(conf["max_use_beacon_num"])    # maximum number of beacons to use at triangulastion (>= 3) 

def _set_map_params(conf: dict) -> None:
    global TRIANGULATE_POLICY

    TRIANGULATE_POLICY = np.int8(conf["triangulate_policy"])     # 1: normal distribution probability, 2: interior division

def set_params(conf_file: Union[str, None] = None) -> dict:
    global ROOT_DIR

    ROOT_DIR = path.join(path.dirname(__file__), "../")          # project root directory

    if conf_file is None:
        conf_file = path.join(ROOT_DIR, "config/default.yaml")    # load default file if not specified

    conf = set_pf_params(conf_file)
    _set_log_params(conf)
    _set_map_params(conf)

    return conf
