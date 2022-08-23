"""Script for running the HSSRS simulation in Wyoming
around Top of the World wind power plant at 50-m resolution"""

from dataclasses import replace
from ssrs import Simulator, Config
import os

config_base = Config(
    run_name='wy_small_heuristic_local',
    sim_movement='heuristics',
    movement_model='heuristics',
    movement_ruleset='local_moves', # dir_random_walk,step_ahead_drw,step_ahead_look_ahead
    
    out_dir='./output',
    max_cores=16,
    
    random_walk_freq=300, # if > 0, how often random walks will randomly occur -- approx every 1/random_walk_freq steps
    random_walk_step_range=(30,60), # when a random walk does occur, the number of random steps will occur in this range
    
    look_ahead_dist = 2000.0, #distance outward (m) that bird will scan for strong updrafts
    updraft_threshold=0.85,  
    
    thermals_realization_count=5,
    thermal_intensity_scale=2.5, #1 gives weak random field, 3 gives v strong random field    
    
    #southwest_lonlat=(-106.21, 42.78),  # (lon, lat) for southwest pt, no integers!
    #region_width_km=(50., 50.),  # terrain width (xwidth, ywidth) in km
    southwest_lonlat=(-106.05, 42.87),  # (lon, lat) for southwest pt, no integers!
    region_width_km=(30., 30.),  # terrain width (xwidth, ywidth) in km
    resolution=50., # meters
    
    track_direction=202.5, #202.5,
    #track_start_region=(24, 26, 24, 26),  #xmin, xmax, ymin, ymax
    track_start_region=(10, 20, 10, 20),  #xmin, xmax, ymin, ymax
    track_start_type='structured',  # structured, random
    track_count=3,  #per thermals realization
    
    # plotting related
    fig_height=6.,
    fig_dpi=300
)

config_uniform = replace(
    config_base,
    sim_mode='uniform',
    uniform_winddirn=270.,
    uniform_windspeed=10.,
)


config_snapshot = replace(
    config_base,
    sim_mode='snapshot',
    snapshot_datetime=(2010, 6, 17, 13),
)


config_seasonal = replace(
    config_base,
    sim_mode='seasonal',
    seasonal_start=(3, 1),  # start of season (month, day)
    seasonal_end=(6, 1),  # end of season (month, day)
    seasonal_timeofday='daytime',  # morning, afternoon, evening, daytime
    seasonal_count=8,
)

if __name__ == '__main__':
 
    configs_to_run = (
        config_uniform,
        #config_snapshot,
        # config_seasonal
    )
    for i, cfg in enumerate(configs_to_run):

#        for j in range(2):  #allows us to run for multiple realizations of the thermal field
#            sim = Simulator(cfg)
#            sim.simulate_tracks()
#            #sim.plot_terrain_features()
#            #sim.plot_wtk_layers()
#            sim.plot_simulation_output()
#            os.rename(sim.mode_fig_dir, f'{sim.mode_fig_dir}_{j}')
#            os.rename(sim.mode_data_dir, f'{sim.mode_data_dir}_{j}')
        
        sim = Simulator(cfg)

        sim.plot_terrain_features()
        sim.plot_orographic_updrafts()
        sim.plot_thermal_updrafts()
        #sim.plot_wtk_layers()
        #sim.plot_directional_potentials()
        sim.simulate_tracks_HSSRS()
        sim.plot_simulated_tracks_HSSRS()
        sim.plot_presence_map_HSSRS()