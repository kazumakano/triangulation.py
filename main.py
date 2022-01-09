import os.path as path
from datetime import datetime, timedelta
import numpy as np
import particle_filter.script.parameter as pf_param
import script.parameter as param
import script.utility as util
from script.log import Log
from script.map import Map
from script.window import Window


def _set_main_params(conf: dict) -> None:
    global BEGIN, END, LOG_FILE

    BEGIN = datetime.strptime(conf["begin"], "%Y-%m-%d %H:%M:%S")
    END = datetime.strptime(conf["end"], "%Y-%m-%d %H:%M:%S")
    LOG_FILE = str(conf["log_file"])

def triangulate() -> None:
    log = Log(BEGIN, END, path.join(pf_param.ROOT_DIR, "log/observed/", LOG_FILE))
    map = Map(log.mac_list)

    if pf_param.ENABLE_DRAW_BEACONS:
        map.draw_beacons(True)
    if pf_param.ENABLE_SAVE_VIDEO:
        map.init_recorder()

    t: datetime
    if param.LERP_WIN_POLICY == 1:    # liner interpolation
        for i, t in enumerate(log.lerped_ts):
            print(f"main.py: {t.time()}")

            strong_beacon_indexes, strong_rssis = util.get_strong_beacons(log.lerped_rssi[i])
            estim_pos = map.estim_pos_by_triangulation(strong_beacon_indexes, strong_rssis)

            if not np.isnan(estim_pos[0]):    # if not lost
                map.draw_pos(estim_pos)
                map.show()
            if pf_param.ENABLE_SAVE_VIDEO:
                map.record()

    elif param.LERP_WIN_POLICY == 2:    # sliding window
        t = BEGIN
        while t <= END:
            print(f"main.py; {t.time()}")
            win = Window(t, log)

            strong_beacon_indexes, strong_rssis = util.get_strong_beacons(win.rssi_list)
            estim_pos = map.estim_pos_by_triangulation(strong_beacon_indexes, strong_rssis)

            if not np.isnan(estim_pos[0]):
                map.draw_pos(estim_pos)
                map.show()
            if pf_param.ENABLE_SAVE_VIDEO:
                map.record()
            
            t += timedelta(seconds=pf_param.WIN_STRIDE)

    print("main.py: reached end of log")
    if pf_param.ENABLE_SAVE_IMG:
        map.save_img()
    if pf_param.ENABLE_SAVE_VIDEO:
        map.save_video()
    map.show(0)

if __name__ == "__main__":
    import argparse
    from script.parameter import set_params

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf_file", help="specify config file", metavar="PATH_TO_CONF_FILE")

    _set_main_params(set_params(parser.parse_args().conf_file))

    triangulate()
