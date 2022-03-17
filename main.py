import os.path as path
from datetime import datetime, timedelta
from typing import Any
import numpy as np
import particle_filter.script.parameter as pf_param
import particle_filter.script.utility as pf_util
import script.utility as util
from script.log import Log
from script.map import Map
from script.window import Window


def _set_main_params(conf: dict[str, Any]) -> None:
    global BEGIN, END, LOG_FILE, RESULT_DIR_NAME

    BEGIN = datetime.strptime(conf["begin"], "%Y-%m-%d %H:%M:%S")
    END = datetime.strptime(conf["end"], "%Y-%m-%d %H:%M:%S")
    LOG_FILE = str(conf["log_file"])
    RESULT_DIR_NAME = None if conf["result_dir_name"] is None else str(conf["result_dir_name"])

def triangulate(conf: dict[str, Any], enable_show: bool = True) -> None:
    log = Log(BEGIN, END, path.join(pf_param.ROOT_DIR, "log/observed/", LOG_FILE))
    result_dir = pf_util.make_result_dir(RESULT_DIR_NAME)
    map = Map(log.mac_list, result_dir)

    if pf_param.ENABLE_DRAW_BEACONS:
        map.draw_beacons(True)
    if pf_param.ENABLE_SAVE_VIDEO:
        map.init_recorder()

    if pf_param.WIN_SIZE == 0:    # liner interpolation
        t: datetime
        for i, t in enumerate(log.lerped_ts):
            print(f"main.py: {t.time()}")

            strong_beacon_indexes, strong_rssis = util.get_strong_beacons(log.lerped_rssi[i])
            estim_pos = map.estim_pos_by_trilateration(strong_beacon_indexes, strong_rssis)

            if not np.isnan(estim_pos[0]):    # if not lost
                map.draw_pos(estim_pos)
            if pf_param.ENABLE_SAVE_VIDEO:
                map.record()
            if enable_show:
                map.show()

    else:                         # sliding window
        t = BEGIN
        while t <= END:
            print(f"main.py; {t.time()}")
            win = Window(t, log)

            strong_beacon_indexes, strong_rssis = util.get_strong_beacons(win.rssi_list)
            estim_pos = map.estim_pos_by_trilateration(strong_beacon_indexes, strong_rssis)

            if not np.isnan(estim_pos[0]):
                map.draw_pos(estim_pos)
            if pf_param.ENABLE_SAVE_VIDEO:
                map.record()
            if enable_show:
                map.show()
            
            t += timedelta(seconds=pf_param.WIN_STRIDE)

    print("main.py: reached end of log")
    if pf_param.ENABLE_SAVE_IMG:
        map.save_img()
    if pf_param.ENABLE_SAVE_VIDEO:
        map.save_video()
    if pf_param.ENABLE_WRITE_CONF:
        pf_util.write_conf(conf, result_dir)
    if enable_show:
        map.show(0)

if __name__ == "__main__":
    import argparse
    from script.parameter import set_params

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf_file", help="specify config file", metavar="PATH_TO_CONF_FILE")
    parser.add_argument("--no_display", action="store_true", help="run without display")
    args = parser.parse_args()

    conf = set_params(args.conf_file)
    _set_main_params(conf)

    triangulate(conf, not args.no_display)
