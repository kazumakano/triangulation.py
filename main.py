import argparse
from datetime import datetime
import numpy as np
import particle_filter.script.parameter as pf_param
import script.parameter as param
from script.log import Log
from script.map import Map
from script.parameter import set_params


def _set_main_params(conf: dict) -> None:
    global BEGIN, END

    BEGIN = datetime.strptime(conf["begin"], "%Y-%m-%d %H:%M:%S")
    END = datetime.strptime(conf["end"], "%Y-%m-%d %H:%M:%S")

def triangulation() -> None:
    log = Log(BEGIN, END)
    map = Map(log)

    if pf_param.ENABLE_SAVE_VIDEO:
        map.init_recorder()
    if pf_param.ENABLE_DRAW_BEACONS:
        map.draw_beacons(True)

    if param.LERP_WIN_POLICY == 1:    # liner interpolation
        for i in range(len(log.lerped_ts)):
            strong_beacon_indexes, strong_rssis = log.get_strong_beacons(i)
            estim_pos = map.estim_pos_by_triangulation(strong_beacon_indexes, strong_rssis)

            if not np.isnan(estim_pos[0]):    # if not lost
                map.draw_any_pos(estim_pos)
                map.show()
            if pf_param.ENABLE_SAVE_VIDEO:
                map.record()

    print("main.py: reached end of log")
    if pf_param.ENABLE_SAVE_VIDEO:
        map.save_video()
    if pf_param.ENABLE_SAVE_IMG:
        map.save_img()
    map.show(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="specify your config file", metavar="PATH_TO_CONFIG_FILE")

    conf = set_params(parser.parse_args().config)
    _set_main_params(conf)
    triangulation()
