import os.path as path
from typing import Any, Optional
import numpy as np
from particle_filter.script.parameter import set_params as set_pf_params


def _set_log_params(conf: dict[str, Any]) -> None:
    global FREQ, MAX_BLANK_LEN, MAX_USE_BEACON_NUM

    FREQ = np.float32(conf["log_lerp_freq"])
    MAX_BLANK_LEN = np.float32(conf["max_blank_len"])
    MAX_USE_BEACON_NUM = np.int8(conf["max_use_beacon_num"])

def _set_map_params(conf: dict[str, Any]) -> None:
    global TRILATERATE_POLICY

    TRILATERATE_POLICY = np.int8(conf["trilaterate_policy"])

def set_params(conf_file: Optional[str] = None) -> dict[str, Any]:
    global ROOT_DIR

    ROOT_DIR = path.join(path.dirname(__file__), "../")

    if conf_file is None:
        conf_file = path.join(ROOT_DIR, "config/default.yaml")

    conf = set_pf_params(conf_file)
    _set_log_params(conf)
    _set_map_params(conf)

    return conf
