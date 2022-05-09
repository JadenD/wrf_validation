import functions_and_loaders as fnl
import xarray as xr
import seaborn as sns
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import cmocean as cmo
from scipy import stats


def plot_val_time_series(start_date, end_date, buoy, height, ws_df, dt_df, season):
    # variable reassign
    obs_ws = ws_df[0]
    wrf_v41_ws = ws_df[1]
    nam_ws = ws_df[2]
    gfs_ws = ws_df[3]
    hrrr_ws = ws_df[4]

    obs_time = dt_df[0]
    wrf_v41_time = dt_df[1]
    nam_dt = dt_df[2]
    gfs_dt = dt_df[3]
    hrrr_dt = dt_df[4]

    # Statistics Setup
    mf_41 = fnl.metrics(obs_ws, wrf_v41_ws)
    nam_m = fnl.metrics(obs_ws, nam_ws)
    hrrr_m = fnl.metrics(obs_ws, hrrr_ws)
    gfs_m = fnl.metrics(obs_ws, gfs_ws)

    # Plotting Start
    plt.figure(figsize=(14, 5))
    plt.style.use(u'seaborn-colorblind')
    lw = 1

    line3, = plt.plot(obs_time, obs_ws, color='black', label=buoy[0], linewidth=lw+.5, zorder=3)
    line1, = plt.plot(wrf_v41_time, wrf_v41_ws, color='red', label='RU WRF', linewidth=lw, zorder=5)

    # Power Law Wind Speed Change
    if height[0] == 160:
        alpha = 0.14
        nam_ws = nam_ws*(160/80)**alpha
        gfs_ws = gfs_ws*(160/100)**alpha
        hrrr_ws = hrrr_ws*(160/80)**alpha
        print('Power Law used')
    else:
        print(str(height[0]) + 'm was used, no power law')
        line5, = plt.plot(hrrr_dt, hrrr_ws, color='tab:blue', label='HRRR', linewidth=lw, zorder=4)
        # line4, = plt.plot(nam_dt, nam_ws, color='tab:olive', label='NAM', linewidth=lw-1, zorder=2)
        # line6, = plt.plot(gfs_dt, gfs_ws, color='tab:green', label='GFS', linewidth=lw-1, zorder=1)

    plt.ylabel('wind speed (m/s)')
    plt.xlabel('start date: ' + start_date.strftime("%Y/%m/%d"))
    plt.title('Wind Speeds at ' + buoy[0] + ' at ' + str(height[0]) + 'm' +
              ' during ' + season[0] + ' ' + start_date.strftime("%Y"))
    plt.legend(loc='best', fontsize='medium')
    plt.ylim(bottom=0)
    plt.grid(True)
    ax = plt.gca()
    ax.autoscale(enable=True, axis='x', tight=True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))

    columns = ('Model', 'RMS', 'CRMS', 'MB', 'Count')

    metric_frame = {'Model': ['RU WRF', 'NAM', 'GFS', 'HRRR'],
                    'RMS':   np.round([mf_41[0], nam_m[0], gfs_m[0], hrrr_m[0]], 3),
                    'CRMS':  np.round([mf_41[1], nam_m[1], gfs_m[1], hrrr_m[1]], 3),
                    'MB':    np.round([mf_41[2], nam_m[2], gfs_m[2], hrrr_m[2]], 3),
                    'Count': [mf_41[3], nam_m[3], gfs_m[3], hrrr_m[3]]
                    }

    metric_frame = pd.DataFrame(metric_frame)

    metric_frame_1 = {'Model': ['RU WRF', 'HRRR'],
                      'RMS':   np.round([mf_41[0], hrrr_m[0]], 3),
                      'CRMS':  np.round([mf_41[1], hrrr_m[1]], 3),
                      'MB':    np.round([mf_41[2], hrrr_m[2]], 3),
                      'Count':          [mf_41[3], hrrr_m[3]]
                      }

    metric_frame_1 = pd.DataFrame(metric_frame_1)

    ds_table_1 = plt.table(metric_frame_1.values, colLabels=columns, bbox=([.1, -.5, .3, .3]))

    plt.savefig('/Users/JadenD/PycharmProjects/wrf_validation/figures/seasonal_validation/ws' +
                '_' + buoy[0] +
                '_' + str(height[0]) + 'm'
                '_' + start_date.strftime("%Y%m%d") +
                '_' + end_date.strftime("%Y%m%d") + '.png',
                dpi=300, bbox_inches='tight')

    os.makedirs('/Volumes/www/cool/mrs/weather/RUWRF/validation/seasonally/' +
                buoy[0] + '/time_series/wind_speed/' + start_date.strftime("%Y") + '/' + season[1], exist_ok=True)
    plt.savefig('/Volumes/www/cool/mrs/weather/RUWRF/validation/seasonally/' + buoy[0] + '/time_series/wind_speed' +
                '/' + start_date.strftime("%Y") + '/' + season[1] + '/' +
                'ws' +
                '_' + buoy[0] +
                '_' + str(height[0]) + 'm'
                '_' + start_date.strftime("%Y%m%d") +
                '_' + end_date.strftime("%Y%m%d") + '.png',
                dpi=300, bbox_inches='tight')

    metric_frame.to_csv('/Users/JadenD/PycharmProjects/wrf_validation/figures/seasonal_validation/stats' +
                        '_' + buoy[0] +
                        '_' + str(height[0]) + 'm'
                        '_' + start_date.strftime("%Y%m%d") +
                        '_' + end_date.strftime("%Y%m%d") + '.csv', index=None)

    os.makedirs('/Volumes/www/cool/mrs/weather/RUWRF/validation/seasonally/' +
                buoy[0] + '/statistics/wind_speed/' + start_date.strftime("%Y") + '/' + season[1], exist_ok=True)
    metric_frame.to_csv('/Volumes/www/cool/mrs/weather/RUWRF/validation/seasonally/' + buoy[0] + '/statistics/wind_speed' +
                        '/' + start_date.strftime("%Y") + '/' + season[1] + '/' +
                        'stats' +
                        '_' + buoy[0] +
                        '_' + str(height[0]) + 'm'
                        '_' + start_date.strftime("%Y%m%d") +
                        '_' + end_date.strftime("%Y%m%d") + '.csv', index=None)

    print(metric_frame)

    plt.clf()
    plt.close()

    return


def plot_heatmap(start_date, end_date, buoy, height, ws_df, season):
    # variable reassign
    obs_ws = ws_df[0]
    wrf_v41_ws = ws_df[1]
    nam_ws = ws_df[2]
    gfs_ws = ws_df[3]
    hrrr_ws = ws_df[4]

    # Statistics Setup
    mf_41 = fnl.metrics(obs_ws, wrf_v41_ws)
    nam_m = fnl.metrics(obs_ws, nam_ws)
    hrrr_m = fnl.metrics(obs_ws, hrrr_ws)
    gfs_m = fnl.metrics(obs_ws, gfs_ws)

    # Heat SCATTER Plots--------------------------------------------------------------------------------------------
    wind_speeds = [wrf_v41_ws, nam_ws, gfs_ws, hrrr_ws]
    model_names = ['RU WRF', 'NAM', 'GFS', 'HRRR']
    model_names_dir = ['RUWRF', 'NAM', 'GFS', 'HRRR']
    metrics_n = [mf_41, nam_m, gfs_m, hrrr_m]

    for ii in range(0, 4):
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        plt.style.use(u'seaborn-colorblind')
        # params = {
        #     'axes.labelsize': 10,
        #     'legend.fontsize': 12,
        #     'xtick.labelsize': 12,
        #     'ytick.labelsize': 12,
        #     'text.usetex': False
        # }
        # plt.rcParams.update(params)

        idx = np.isfinite(obs_ws) & np.isfinite(wind_speeds[ii])

        cmap = cmo.cm.algae
        # cmap = mpl.cm.Greens
        cmaplist = [cmap(i) for i in range(cmap.N)]
        cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', cmaplist, cmap.N)

        hexplot = plt.hexbin(obs_ws[idx], wind_speeds[ii][idx],
                             cmap=cmap, linewidths=.1, gridsize=50, mincnt=1, vmin=0, vmax=30) #, bins='log', cmap='jet')
        slope, intercept, r_value, p_value, std_err = stats.linregress(obs_ws[idx],
                                                                       wind_speeds[ii][idx])
        r2_value = r_value ** 2
        plt.plot(obs_ws[idx], intercept + slope * obs_ws[idx],
                 'r', label='fitted line')
        plt.plot([0, 25], [0, 25], 'silver')
        plt.xlabel('Buoy: ' + buoy[0] + ' Wind Speed (m/s)', fontsize='x-large')
        plt.ylabel(model_names[ii] + ' Wind Speed (m/s)', fontsize='x-large')
        plt.text(1, 20,
                 'slope: ' + str("{0:.2f}".format(slope)) + '\n' +
                 'intercept: ' + str("{0:.2f}".format(intercept)) + '\n' +
                 'R-squared: ' + str("{0:.2f}".format(r2_value)) + '\n' +
                 'RMS: ' + str("{0:.2f}".format(metrics_n[ii][0])) + '\n' +
                 'model bias: ' + str("{0:.2f}".format(metrics_n[ii][2])),
                 bbox=dict(facecolor='white', alpha=1), fontsize='medium'
                 )
        plt.title('Wind Speeds at ' + buoy[0] + ' at ' + str(height[0]) + 'm' + ' during ' +
                  season[0] + ' ' + start_date.strftime("%Y"), fontsize='large')

        plt.grid(True)
        plt.xlim(left=0, right=25)
        plt.ylim(bottom=0, top=25)

        cb = fig.colorbar(
            hexplot,
            ax=ax,
            # cmap=cmap,
            extend='max',
            spacing='proportional',
            label='counts',
            # norm=norm,
            # ticks=bounds
        )

        os.makedirs('/Volumes/www/cool/mrs/weather/RUWRF/validation/seasonally/' +
                    buoy[0] + '/heatmap/wind_speed/' + start_date.strftime("%Y") + '/' + season[1], exist_ok=True)
        plt.savefig('/Volumes/www/cool/mrs/weather/RUWRF/validation/seasonally/' + buoy[0] + '/heatmap/wind_speed' +
                    '/' + start_date.strftime("%Y") + '/' + season[1] + '/' +
                    'ws' +
                    '_' + buoy[0] +
                    '_' + model_names_dir[ii] +
                    '_' + str(height[0]) + 'm'
                    '_' + start_date.strftime("%Y%m%d") +
                    '_' + end_date.strftime("%Y%m%d") + '.png',
                    dpi=300, bbox_inches='tight')

        plt.clf()
        plt.close()


def load_data_make_plots(start_date, end_date, buoy, point_location, season, height):
    # Model Range and NYSERDA BUOY and other models

    # WRF Load
    wrf_v41_ds = fnl.load_wrf(start_date, end_date, 1, 'v4.1', point_location, buoy=buoy, height=height)
    wrf_v41_ws = wrf_v41_ds.wind_speed.sel(time=slice(start_date, end_date), station=buoy[1], height=height).data
    wrf_v41_ws = wrf_v41_ws.reshape(wrf_v41_ws.__len__())
    wrf_v41_time = wrf_v41_ds.time.sel(time=slice(start_date, end_date)).data

    if buoy[0] in ['NYNE05', 'NYSWE05', 'NYSE06']:
        nys_ws_1hr_nonav = fnl.load_nyserda_ws(buoy, height[0], start_date, end_date)
        nys_ws_1hr_nonav[nys_ws_1hr_nonav > 55] = np.nan
        obs_time = nys_ws_1hr_nonav.index
        obs_ws = nys_ws_1hr_nonav.values
    elif buoy[0] == 'SODAR':
        r = pd.date_range(start=start_date, end=end_date, freq='H')
        df_ws, df_wd, df_dt = fnl.sodar_loader(start_date, end_date,  height=height)
        df_ws = df_ws[df_ws['height'] == height[0]]
        df_ws = df_ws.set_index('dt').reindex(r).fillna(np.nan).rename_axis('dt').reset_index()
        obs_time = df_ws['dt'].values
        obs_ws = df_ws['value'].values
    elif buoy[0][0:5] == 'ASOSB':
        try:
            if buoy[0][-1] == '6':
                as_ds = fnl.load_ASOSB(start_date, end_date, ASbuoy=6, height=height)
            elif buoy[0][-1] == '4':
                as_ds = fnl.load_ASOSB(start_date, end_date, ASbuoy=4, height=height)
            else:
                print('Atlantic Shores Buoy Number might not exist')
                as_ds = []
        except:
            print('Atlantic Shores loader failed, date might not exist')
            as_ds = []

        as_dt = pd.to_datetime(as_ds.time.data, format='%m-%d-%Y %H:%M')
        time_h = pd.date_range(start_date, end_date, freq='H')
        time_m = pd.date_range(start_date, end_date, freq='10min')
        as_ds.wind_speed[as_ds.wind_speed > 55] = np.nan
        as_ds.wind_speed[as_ds.wind_speed < 0] = np.nan
        as_ws = pd.Series(as_ds.wind_speed.values, index=as_dt)
        as_ws = as_ws.reindex(time_h)
        as_ws_m = pd.Series(as_ds.wind_speed.values, index=as_dt)
        as_ws_m = as_ws_m.reindex(time_m)
        # as_ds.time.data = pd.to_numeric(as_ds.time.data, errors='coerce')
        as_ws_av = []
        for i in range(0, len(as_ws_m), 6):
            as_ws_av.append(np.mean(as_ws_m[i:i + 6]))
        asosb_ws_1hr_avg = pd.Series(as_ws_av, index=as_ws.index)
        obs_time = asosb_ws_1hr_avg.index
        obs_ws = asosb_ws_1hr_avg.values
    else:
        print('Not a valid validation point.')
        obs_time = []
        obs_ws = []

    nam_ws, nam_dt = fnl.load_nam(start_date, end_date, buoy[0], point_location, height=height)
    gfs_ws, gfs_dt = fnl.load_gfs(start_date, end_date, buoy[0], point_location, height=height)
    hrrr_ws, hrrr_dt = fnl.load_hrrr(start_date, end_date, buoy[0], point_location, height=height)

    ws_df = [obs_ws, wrf_v41_ws, nam_ws, gfs_ws, hrrr_ws]
    dt_df = [obs_time, wrf_v41_time, nam_dt, gfs_dt, hrrr_dt]

    plot_heatmap(start_date, end_date, buoy, height, ws_df, season)
    plot_val_time_series(start_date, end_date, buoy, height, ws_df, dt_df, season)


# def plot_val_fig_NYSERDA(start_date, end_date, buoy, point_location, height, folder):
#     # Model Range and NYSERDA BUOY and other models
#     plt.figure(figsize=(18, 4))
#     plt.style.use(u'seaborn-colorblind')
#
#     lw = 2
#     wrf_v41_ds = fnl.load_wrf(start_date, end_date, 1, 'v4.1', point_location, buoy=buoy, height=height)
#     wrf_v41_ws = wrf_v41_ds.wind_speed.sel(time=slice(start_date, end_date), station=buoy[1], height=height).data
#     wrf_v41_ws = wrf_v41_ws.reshape(wrf_v41_ws.__len__())
#     wrf_v41_time = wrf_v41_ds.time.sel(time=slice(start_date, end_date)).data
#
#     nys_ws_1hr_nonav = fnl.load_nyserda_ws(buoy, height, start_date, end_date)
#     nys_ws_1hr_nonav[nys_ws_1hr_nonav > 55] = np.nan
#
#     nam_ws, nam_dt = fnl.load_nam(start_date, end_date, buoy[0], point_location, height=height)
#     gfs_ws, gfs_dt = fnl.load_gfs(start_date, end_date, buoy[0], point_location, height=height)
#     hrrr_ws, hrrr_dt = fnl.load_hrrr(start_date, end_date, buoy[0], point_location, height=height)
#
#     # Power Law Wind Speed Change
#     if height[0] == 160:
#         alpha = 0.14
#         nam_ws = nam_ws*(160/80)**alpha
#         gfs_ws = gfs_ws*(160/100)**alpha
#         hrrr_ws = hrrr_ws*(160/80)**alpha
#         print('Power Law used')
#     else:
#         print(str(height[0]) + 'm was used, no power law')
#
#     line1, = plt.plot(wrf_v41_time, wrf_v41_ws, label='WRF 4.1', linewidth=lw)
#     line3, = plt.plot(nys_ws_1hr_nonav.index, nys_ws_1hr_nonav.values,
#                       color='black', label=buoy[0], linewidth=lw)
#     line4, = plt.plot(nam_dt, nam_ws, '-.', label='NAM', linewidth=lw)
#     line5, = plt.plot(hrrr_dt, hrrr_ws, '-.', label='HRRR', linewidth=lw)
#     line6, = plt.plot(gfs_dt, gfs_ws, '-.', label='GFS', linewidth=lw)
#
#     plt.ylabel('wind speed (m/s)')
#     plt.xlabel('start date: ' + start_date.strftime("%Y/%m/%d"))
#     plt.title('Wind Speeds at ' + buoy[0] + ' at ' + str(height[0]) + 'm')
#     plt.legend(handles=[line1, line3, line4, line5, line6], loc='best', fontsize='medium')
#     plt.ylim(bottom=0)
#     plt.grid(True)
#     ax = plt.gca()
#     ax.autoscale(enable=True, axis='x', tight=True)
#     ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
#
#     params = {
#         'axes.labelsize': 8,
#         'legend.fontsize': 10,
#         'xtick.labelsize': 10,
#         'ytick.labelsize': 10,
#         'text.usetex': False
#     }
#     plt.rcParams.update(params)
#
#     plt.savefig('/Users/JadenD/PycharmProjects/wrf_validation/figures/seasonally_validation/ws' +
#                 '_' + buoy[0] +
#                 '_' + str(height[0]) + 'm'
#                 '_' + start_date.strftime("%Y%m%d") +
#                 '_' + end_date.strftime("%Y%m%d") + '.png',
#                 dpi=300)
#
#     os.makedirs('/Volumes/www/cool/mrs/weather/RUWRF/validation/' + folder + '/' +
#              buoy[0] + '/time_series/wind_speed/' + start_date.strftime("%Y%m%d"), exist_ok=True)
#     plt.savefig('/Volumes/www/cool/mrs/weather/RUWRF/validation/' + folder + '/' + buoy[0] + '/time_series/wind_speed' +
#                 '/' + start_date.strftime("%Y%m%d") + '/'
#                 'ws' +
#                 '_' + buoy[0] +
#                 '_' + str(height[0]) + 'm'
#                 '_' + start_date.strftime("%Y%m%d") +
#                 '_' + end_date.strftime("%Y%m%d") + '.png',
#                 dpi=300)
#
#     mf_41 = fnl.metrics(nys_ws_1hr_nonav.values, wrf_v41_ws)
#     nam_m = fnl.metrics(nys_ws_1hr_nonav.values, nam_ws)
#     hrrr_m = fnl.metrics(nys_ws_1hr_nonav.values, hrrr_ws)
#     gfs_m = fnl.metrics(nys_ws_1hr_nonav.values, gfs_ws)
#
#     metric_frame = {'Model': ['WRF 4.1', 'NAM', 'GFS', 'HRRR'],
#                     'RMS': np.round([mf_41[0], nam_m[0], gfs_m[0], hrrr_m[0]], 3),
#                     'CRMS': np.round([mf_41[1], nam_m[1], gfs_m[1], hrrr_m[1]], 3),
#                     'MB': np.round([mf_41[2], nam_m[2], gfs_m[2], hrrr_m[2]], 3),
#                     'Count': [mf_41[3], nam_m[3], gfs_m[3], hrrr_m[3]]
#                     }
#
#     metric_frame = pd.DataFrame(metric_frame)
#
#     metric_frame.to_csv('/Users/JadenD/PycharmProjects/wrf_validation/figures/seasonally_validation/stats' +
#                         '_' + buoy[0] +
#                         '_' + str(height[0]) + 'm'
#                         '_' + start_date.strftime("%Y%m%d") +
#                         '_' + end_date.strftime("%Y%m%d") + '.csv', index=None)
#
#     os.makedirs('/Volumes/www/cool/mrs/weather/RUWRF/validation/' + folder + '/' +
#              buoy[0] + '/statistics/wind_speed/' + start_date.strftime("%Y%m"), exist_ok=True)
#     metric_frame.to_csv('/Volumes/www/cool/mrs/weather/RUWRF/validation/' + folder + '/' + buoy[0] + '/statistics' +
#                         '/' + start_date.strftime("%Y%m%d") + '/'
#                         'stats' +
#                         '_' + buoy[0] +
#                         '_' + str(height[0]) + 'm'
#                         '_' + start_date.strftime("%Y%m%d") +
#                         '_' + end_date.strftime("%Y%m%d") + '.csv', index=None)
#
#     print(metric_frame)
#
#     return


# def plot_val_fig_ASOSB(start_date, end_date, buoy, point_location, height):
#     # Model Range and ASOSB BUOY and other models
#     lw = 2
#     wrf_v41_ds = fnl.load_wrf(start_date, end_date, 1, 'v4.1', point_location, buoy=buoy, height=height)
#     wrf_v41_ws = wrf_v41_ds.wind_speed.sel(time=slice(start_date, end_date), station=buoy[1], height=height).data
#     wrf_v41_ws = wrf_v41_ws.reshape(wrf_v41_ws.__len__())
#     wrf_v41_time = wrf_v41_ds.time.sel(time=slice(start_date, end_date)).data
#
#     try:
#         as_ds = fnl.load_ASOSB(start_date, end_date, buoy[2], height)
#     except:
#         print('Atlantic Shores loader failed, date might not exist')
#
#     as_dt = pd.to_datetime(as_ds.time.data, format='%m-%d-%Y %H:%M')
#     time_h = pd.date_range(start_date, end_date - timedelta(hours=1), freq='H')
#     time_m = pd.date_range(start_date, end_date - timedelta(hours=1), freq='10min')
#
#     as_ds.wind_speed[as_ds.wind_speed > 55] = np.nan
#     as_ds.wind_speed[as_ds.wind_speed < 0] = np.nan
#
#     as_ws = pd.Series(as_ds.wind_speed.values, index=as_dt)
#     as_ws = as_ws.reindex(time_h)
#
#     as_ws_m = pd.Series(as_ds.wind_speed.values, index=as_dt)
#     as_ws_m = as_ws_m.reindex(time_m)
#
#     # as_ds.time.data = pd.to_numeric(as_ds.time.data, errors='coerce')
#     as_ws_av = []
#     for i in range(0, len(as_ws_m), 6):
#         as_ws_av.append(np.mean(as_ws_m[i:i + 6]))
#
#     asosb_ws_1hr_avg = pd.Series(as_ws_av, index=as_ws.index)
#
#     nam_ws, nam_dt = fnl.load_nam(start_date, end_date, buoy[0], point_location, height=height)
#     gfs_ws, gfs_dt = fnl.load_gfs(start_date, end_date, buoy[0], point_location, height=height)
#     hrrr_ws, hrrr_dt = fnl.load_hrrr(start_date, end_date, buoy[0], point_location, height=height)
#
#     # Power Law Wind Speed Change
#     if height[0] == 160:
#         print('Power Law Used to bring models to 160m')
#         alpha = 0.14
#         nam_ws = nam_ws*(160/80)**alpha
#         gfs_ws = gfs_ws*(160/100)**alpha
#         hrrr_ws = hrrr_ws*(160/80)**alpha
#     else:
#         print(str(height[0]) + 'm was used, no power law')
#
#     # Figure Generation
#     plt.figure(figsize=(18, 4))
#     plt.style.use(u'seaborn-colorblind')
#
#     line1, = plt.plot(wrf_v41_time, wrf_v41_ws, label='WRF 4.1', linewidth=lw)
#     line3, = plt.plot(asosb_ws_1hr_avg.index, asosb_ws_1hr_avg.values,
#                       color='black', label=buoy[0], linewidth=lw
#                       )
#     line4, = plt.plot(nam_dt, nam_ws, '-.', label='NAM', linewidth=lw)
#     line5, = plt.plot(hrrr_dt, hrrr_ws, '-.', label='HRRR', linewidth=lw)
#     line6, = plt.plot(gfs_dt, gfs_ws, '-.', label='GFS', linewidth=lw)
#
#     plt.ylabel('wind speed (m/s)')
#     plt.xlabel('start date: ' + start_date.strftime("%Y/%m/%d"))
#     plt.title('Wind Speeds at ' + buoy[0] + ' at ' + str(height[0]) + 'm')
#
#     plt.legend(handles=[line1, line3, line4, line5, line6], loc='best', fontsize='medium')
#     ###
#     plt.ylim(bottom=0)
#     plt.grid(True)
#     ax = plt.gca()
#     ax.autoscale(enable=True, axis='x', tight=True)
#     ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
#
#     params = {
#         'axes.labelsize': 8,
#         'legend.fontsize': 10,
#         'xtick.labelsize': 10,
#         'ytick.labelsize': 10,
#         'text.usetex': False
#     }
#     plt.rcParams.update(params)
#
#     plt.savefig('ws_' + buoy[0] + '_' +
#                 start_date.strftime("%Y%m%d") + '_' + end_date.strftime("%Y%m%d") + '_' +
#                 str(height[0]) + 'm.png',
#                 dpi=300)
#
#
#
#     mf_41 = fnl.metrics(asosb_ws_1hr_avg.values, wrf_v41_ws)
#     nam_m = fnl.metrics(asosb_ws_1hr_avg.values, nam_ws)
#     hrrr_m = fnl.metrics(asosb_ws_1hr_avg.values, hrrr_ws)
#     gfs_m = fnl.metrics(asosb_ws_1hr_avg.values, gfs_ws)
#
#     metric_frame = {'Model': ['WRF 4.1', 'NAM', 'GFS', 'HRRR'],
#                     'RMS': np.round([mf_41[0], nam_m[0], gfs_m[0], hrrr_m[0]], 3),
#                     'CRMS': np.round([mf_41[1], nam_m[1], gfs_m[1], hrrr_m[1]], 3),
#                     'MB': np.round([mf_41[2], nam_m[2], gfs_m[2], hrrr_m[2]], 3),
#                     'Count': [mf_41[3], nam_m[3], gfs_m[3], hrrr_m[3]]
#                     }
#
#     metric_frame = pd.DataFrame(metric_frame)
#
#     metric_frame.to_csv('~/PycharmProjects/covid19/ASOSB_seasonally_' + str(height[0]) + 'm_' + buoy[0] + '_' +
#                         start_date.strftime("%Y%m%d") + '_' + end_date.strftime("%Y%m%d") + '.csv', index=None)
#
#     print(metric_frame)
#
#     return

# 'summer', 'fall', 'winter', 'spring'
ssn_code = 'spring'
year = 2020

if ssn_code == 'winter':
    season = 'Winter (DJF)', 'winter_DJF'
    start_date = datetime(year-1, 12, 1)
    end_date = datetime(year, 3, 1) - timedelta(hours=1)
elif ssn_code == 'spring':
    season = 'Spring (MAM)', 'spring_MAM'
    start_date = datetime(year, 3, 1)
    end_date = datetime(year, 6, 1) - timedelta(hours=1)
elif ssn_code == 'summer':
    season = 'Summer (JJA)', 'summer_JJA'
    start_date = datetime(year, 6, 1)
    end_date = datetime(year, 9, 1) - timedelta(hours=1)
elif ssn_code == 'fall':
    season = 'Fall (SON)', 'fall_SON'
    start_date = datetime(year, 9, 1)
    end_date = datetime(year, 12, 1) - timedelta(hours=1)
else:
    print('invalid season')
    season = None
    start_date = None
    end_date = None

point_location = 'wrf_validation_lite_points_v2.csv'
#
# buoy = ['NYSE06', b'NYSE06']
# load_data_make_plots(start_date, end_date, buoy, point_location, season, height=[80])
# load_data_make_plots(start_date, end_date, buoy, point_location, season, height=[160])
# buoy = ['NYSWE05', b'NYSWE05']
# load_data_make_plots(start_date, end_date, buoy, point_location, height=[80])
# load_data_make_plots(start_date, end_date, buoy, point_location, height=[160])
# buoy = ['NYNE05', b'NYNE05']
# load_data_make_plots(start_date, end_date, buoy, point_location, season, height=[80])
# load_data_make_plots(start_date, end_date, buoy, point_location, season, height=[160])
# buoy = ['SODAR', b'SODAR']
# load_data_make_plots(start_date, end_date, buoy, point_location, height=[80])
# load_data_make_plots(start_date, end_date, buoy, point_location, height=[160])
buoy = ['ASOSB6', b'ASOSB6']
load_data_make_plots(start_date, end_date, buoy, point_location, height=[80])
load_data_make_plots(start_date, end_date, buoy, point_location, height=[160])
