# config

This is directory for config files.
Put your config files here.
You can customize following parameters:
| Key                      | Description                                             | Notes                                                                | Type          |
| ---                      | ---                                                     | ---                                                                  | ---           |
| begin                    | begin datetime of RSSI log                              | must be like 'yyyy-mm-dd hh:mm:ss'                                   | `str`         |
| end                      | end datetime of RSSI log                                | must be like 'yyyy-mm-dd hh:mm:ss'                                   | `str`         |
| log_file                 | RSSI log file                                           |                                                                      | `str`         |
|                          |                                                         |                                                                      |               |
| win_size                 | size of sliding window [second]                         |                                                                      | `float`       |
|                          |                                                         |                                                                      |               |
| enable_clear_map         | clear map image at each step or not                     |                                                                      | `bool`        |
| enable_draw_beacons      | draw beacon positions or not                            |                                                                      | `bool`        |
| enable_save_img          | capture image or not                                    |                                                                      | `bool`        |
| enable_save_video        | record video or not                                     |                                                                      | `bool`        |
| frame_rate               | frame rate of video [FPS]                               | synchronized with real speed if 0                                    | `float`       |
| map_conf_file            | map config file                                         |                                                                      | `str`         |
| map_img_file             | map image file                                          |                                                                      | `str`         |
| map_show_policy          | policy to show particles and trajectory                 | 1: all, 2: all & likeliest, 3: all & center, 4: likeliest, 5: center | `int`         |
| result_file_name         | file name of image and video                            | auto generated if unspecified                                        | `str \| None` |
| win_stride               | stride width of sliding window [second]                 |                                                                      | `float`       |
|                          |                                                         |                                                                      |               |
| ~~direct_sd~~            | ~~standard deviation of direction at walk~~             |                                                                      | ~~`float`~~   |
| ~~max_particle_stride~~  | ~~maximum stride width of particles in a step [pixel]~~ |                                                                      | ~~`float`~~   |
|                          |                                                         |                                                                      |               |
| ~~lost_resample_policy~~ | ~~policy to resample particles when lost~~              | ~~1: reset, 2: use last particles~~                                  | ~~`int`~~     |
|                          |                                                         |                                                                      |               |
| enable_truth             | enable ground truth or not                              |                                                                      | `bool`        |
|                          |                                                         |                                                                      |               |
| ~~dist_sd~~              | ~~standard deviation of distance gap~~                  |                                                                      | ~~`float`~~   |
| el_correction            | correction term for difference in elevation             |                                                                      | `float`       |
| ~~neg_weight_coef~~      | ~~coefficient for negative weight~~                     | ~~not consider undetected beacons if 0~~                             | ~~`float`~~   |
| propag_coef              | propagation coefficient                                 | takes 2 in ideal environment                                         | `float`       |
|                          |                                                         |                                                                      |               |
| win_policy               | policy to get representative RSSI value in window       | 1: maximum, 2: latest                                                | `int`         |
|                          |                                                         |                                                                      |               |
| log_freq                 | frequency at log interpolation [Hz]                     |                                                                      | `float`       |
| lerp_win_policy          | policy of positioning with RSSI log                     | 1: linear interpolation, 2: sliding window                           | `int`         |
| max_blank_len            | maximum length of blank to interpolate [second]         |                                                                      | `float`       |
| max_use_beacon_num       | maximum number of beacons to use at triangulation       | must be >= 3                                                         | `int`         |
|                          |                                                         |                                                                      |               |
| triangulate_policy       | policy to triangulate                                   | 1: normal distribution probability, 2: interior division             | `int`         |
