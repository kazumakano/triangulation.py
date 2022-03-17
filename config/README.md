# config
This is directory for config files.
Put your config files here.
You can customize following parameters:
| Key                 | Description                                       | Notes                                                                | Type          |
| ---                 | ---                                               | ---                                                                  | ---           |
| begin               | begin datetime of RSSI log                        | must be like 'yyyy-mm-dd hh:mm:ss'                                   | `str`         |
| end                 | end datetime of RSSI log                          | must be like 'yyyy-mm-dd hh:mm:ss'                                   | `str`         |
| log_file            | RSSI log file                                     |                                                                      | `str`         |
| result_dir_name     | name of directory for result files                | auto generated if unspecified                                        | `str \| None` |
|                     |                                                   |                                                                      |               |
| win_size            | size of sliding window [s]                        |                                                                      | `float`       |
|                     |                                                   |                                                                      |               |
| beacon_dir          | directory for beacon config files                 |                                                                      | `str`         |
| enable_clear_map    | clear map image at each step or not               |                                                                      | `bool`        |
| enable_draw_beacons | draw beacon positions or not                      |                                                                      | `bool`        |
| enable_save_img     | capture image at last or not                      |                                                                      | `bool`        |
| enable_save_video   | record video or not                               |                                                                      | `bool`        |
| frame_rate          | frame rate of video [fps]                         | synchronized with real speed if 0                                    | `float`       |
| map_conf_file       | map config file                                   |                                                                      | `str`         |
| map_img_file        | map image file                                    |                                                                      | `str`         |
| map_show_policy     | policy to show particles and trajectory           | 1: all, 2: all & likeliest, 3: all & center, 4: likeliest, 5: center | `int`         |
| map_show_range      | range to show map                                 | whole map if unspecified                                             | `list[int]`   |
| win_stride          | stride width of sliding window [s]                |                                                                      | `float`       |
|                     |                                                   |                                                                      |               |
| truth_log_file      | ground truth position log file                    | disabled if unspecified                                              | `str \| None` |
|                     |                                                   |                                                                      |               |
| el_correction       | correction term for difference in elevation [m]   |                                                                      | `float`       |
| enable_write_conf   | write config file or not                          |                                                                      | `bool`        |
| propag_coef         | propagation coefficient                           | takes 2 in ideal environment                                         | `float`       |
|                     |                                                   |                                                                      |               |
| win_policy          | policy to get representative RSSI value in window | 1: maximum, 2: latest                                                | `int`         |
|                     |                                                   |                                                                      |               |
| log_lerp_freq       | frequency of log interpolation [Hz]               |                                                                      | `float`       |
| max_blank_len       | maximum length of blank to interpolate [s]        |                                                                      | `float`       |
|                     |                                                   |                                                                      |               |
| trilaterate_policy  | policy to trilaterate                             | 1: normal distribution probability, 2: interior division             | `int`         |
|                     |                                                   |                                                                      |               |
| max_use_beacon_num  | maximum number of beacons to use at trilateration | must be >= 3                                                         | `int`         |
