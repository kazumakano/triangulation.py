from datetime import datetime, timedelta
from typing import Tuple
import numpy as np
from particle_filter.script.log import Log as PfLog
from . import parameter as param


class Log(PfLog):
    def __init__(self, begin: datetime, end: datetime) -> None:
        super().__init__(begin, end)

        if param.LERP_WIN_POLICY == 1:    # if linear interpolation is enabled
            sample_num = np.uint32(param.FREQ * (end - begin).seconds)    # the number of samples at interpolation
            self.lerped_ts = np.empty(sample_num, dtype=datetime)
            self.lerped_rssi = np.full((sample_num, len(self.mac_list)), -np.inf, dtype=np.float16)

            stride: timedelta = (end - begin) / sample_num
            separated_ts, separated_rssi = self._separate_by_mac()
            for i in range(sample_num):
                self.lerped_ts[i] = begin + i * stride
                for j in range(len(self.mac_list)):
                    for k in range(len(separated_ts[j]) - 1):
                        if separated_ts[j][k] <= self.lerped_ts[i] <= separated_ts[j][k+1]:
                            if (separated_ts[j][k+1] - separated_ts[j][k]).seconds < param.MAX_BLANK_LEN:    # if blank length is short enough to interpolate
                                self.lerped_rssi[i][j] = (separated_rssi[j][k] * (separated_ts[j][k+1] - self.lerped_ts[i]) + separated_rssi[j][k+1] * (self.lerped_ts[i] - separated_ts[j][k])) / (separated_ts[j][k+1] - separated_ts[j][k])
                            break

            print("log.py: log has been interpolated")

    # separate log by MAC address
    def _separate_by_mac(self) -> Tuple[np.ndarray, np.ndarray]:
        sorted_ts = np.empty(len(self.mac_list), dtype=np.ndarray)
        sorted_rssi = np.empty(len(self.mac_list), dtype=np.ndarray)
        for i in range(len(self.mac_list)):
            sorted_ts[i] = np.empty(0, dtype=datetime)
            sorted_rssi[i] = np.empty(0, dtype=np.int8)

        for i, t in enumerate(self.ts):
            for j, m in enumerate(self.mac_list):
                if m == self.mac[i]:
                    sorted_ts[j] = np.hstack((sorted_ts[j], t))
                    sorted_rssi[j] = np.hstack((sorted_rssi[j], self.rssi[i]))
                    break

        return sorted_ts, sorted_rssi
