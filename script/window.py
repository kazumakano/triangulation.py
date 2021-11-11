from datetime import datetime
import numpy as np
import particle_filter.script.parameter as pf_param
from .log import Log
from .map import Map


class Window:
    def __init__(self, log: Log, map: Map, current: datetime) -> None:
        ts, mac, rssi = log.slice_win(current)
        
        self.rssi_list = np.full(len(log.mac_list), -np.inf, dtype=np.float16)
        if pf_param.WIN_POLICY == 1:      # use maximum RSSI
            for i in range(len(ts)):
                for j, m in enumerate(log.mac_list):
                    if m == mac[i] and self.rssi_list[j] < rssi[i]:
                        self.rssi_list[j] = rssi[i]
                        break    
        elif pf_param.WIN_POLICY == 2:    # use latest RSSI
            for i in reversed(range(len(ts))):
                for j, m in enumerate(log.mac_list):
                    if m == mac[i] and np.isneginf(self.rssi_list[j]):
                        self.rssi_list[j] = rssi[i]
                        break
