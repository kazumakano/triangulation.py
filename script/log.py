from datetime import datetime, timedelta
import numpy as np
import particle_filter.script.parameter as pf_param
from particle_filter.script.log import Log as PfLog
from . import parameter as param


class Log(PfLog):
    def __init__(self, begin: datetime, end: datetime, file: str) -> None:
        super().__init__(begin, end, file)

        if pf_param.WIN_SIZE == 0:    # linear interpolation instead of sliding window
            log_size = end - begin
            log_len = np.int64(param.FREQ * (log_size.seconds + log_size.microseconds / 1000000))    # number of samples for interpolation
            self.lerped_ts = np.empty(log_len, dtype=datetime)
            self.lerped_rssi = np.full((log_len, len(self.mac_list)), -np.inf, dtype=np.float32)

            stride: timedelta = log_size / log_len
            ts_list, rssi_list = self._split_by_mac(self.mac_list)
            for i in range(log_len):
                self.lerped_ts[i] = begin + i * stride
                for j in range(len(self.mac_list)):
                    for k in range(len(ts_list[j]) - 1):
                        if ts_list[j][k] <= self.lerped_ts[i] <= ts_list[j][k+1]:
                            if (ts_list[j][k+1] - ts_list[j][k]).seconds < param.MAX_BLANK_LEN:    # blank length is short enough to interpolate
                                self.lerped_rssi[i][j] = (rssi_list[j][k] * (ts_list[j][k+1] - self.lerped_ts[i]) + rssi_list[j][k+1] * (self.lerped_ts[i] - ts_list[j][k])) / (ts_list[j][k+1] - ts_list[j][k])
                            break

            print("log.py: log has been interpolated")
