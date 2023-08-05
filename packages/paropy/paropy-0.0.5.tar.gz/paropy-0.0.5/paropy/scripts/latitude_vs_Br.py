'''
latitude_vs_Br.py

Latitude versus time and phi averaged surface Br
'''

#%% Import
import os
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
from cycler import cycler
import h5py

from paropy.coreproperties import icb_radius, cmb_radius
from paropy.data_utils import load_dimensionless
from paropy.routines import surface_phiavg_timeavg
from paropy.plot_utils import rad_to_deg, tangent_cylinder_latitude, polar_minimum_latitude

#%% Input parameters
# run_ID = ['c-200a']
run_ID = ['chem_200d','d_0_55a','d_0_6a','d_0_65b','c-200a','d_0_75a','d_0_8a']  # PARODY simulation tag
# path containing simulation output
dirName = '/data/geodynamo/wongj/Work'
# directory = '/Volumes/NAS/ipgp/Work/'
# directory = '/Users/wongj/Desktop/data/'

fig_aspect = 1  # figure aspect ratio

saveOn = 1  # save figures?
saveDir = '/home/wongj/Work/figures/latitude_vs_Br' # path to save files
# saveDir = '/Users/wongj/Documents/isterre/parody/figures/surface'

#%% Load
w, h = plt.figaspect(fig_aspect)
fig1, ax1 = plt.subplots(1, 1, figsize=(1.5*w, h))
fig2, ax2 = plt.subplots(1, 1, figsize=(1.2*w, h))
ax3 = ax2.twinx()
tc_lat = tangent_cylinder_latitude(0) # latitude of cylinder tangent to ic
ax1.axhline(0,linewidth=1, color='k')
ax1.axvline(0, linewidth=1, color='k')
ax1.axvline(-tc_lat, linewidth=1, color='darkgrey')
ax1.axvline(tc_lat, linewidth=1, color='darkgrey')

shell_gap = cmb_radius - icb_radius
strat_lat=[]
pm_north = []
pm_south = []
for run in run_ID:
    directory = '{}/{}'.format(dirName,run)
    _, _, _, _, _, fi, rf = load_dimensionless(run, directory)
    if not os.path.exists('{}/surface_phiavg_timeavg'.format(directory)):
        (theta, phi, Vt, Vp, Br, dtBr) = surface_phiavg_timeavg(
            run, directory)  # timeavg
    else: # load timeavg data
        print('Loading {}/surface_phiavg_timeavg'.format(directory))
        f = h5py.File('{}/surface_phiavg_timeavg'.format(directory), 'r')
        for key in f.keys():
            globals()[key] = np.array(f[key])

    # Find stationary points
    pm_lat_north, pm_lat_south = polar_minimum_latitude(theta,Br)
    strat_lat.append(rf)
    pm_north.append(pm_lat_north)
    pm_south.append(pm_lat_south)

    #%% Plot
    lon, lat = rad_to_deg(phi, theta)
    if rf == icb_radius/shell_gap:
        h1 = ax1.plot(lat, Br, linewidth=2, label = r'R2'.format(rf), color = 'darkgrey')
        h2, = ax2.plot(rf, pm_lat_north, 'o', markersize=10,
                   markerfacecolor='None', label='_nolegend_', color = 'darkgrey')
        h3 = ax3.plot(rf, pm_lat_south, 's', markersize=10, markerfacecolor='None',label='_nolegend_', color = 'darkgrey')
    else:
        h1 = ax1.plot(lat, Br, linewidth=2, label = r'$r_f = {:.2f}$'.format(rf))
        h2, = ax2.plot(rf, pm_lat_north, 'o', markersize=10,
                       markerfacecolor='None', label='_nolegend_')
        h3 = ax3.plot(rf, pm_lat_south, 's', color=h2.get_color(), markersize=10, markerfacecolor='None',label='_nolegend_')

# Scaling
y_north = np.polyfit(strat_lat,pm_north,1)
p_north = np.poly1d(y_north)
y_south = np.polyfit(strat_lat,pm_south,1)
p_south = np.poly1d(y_south)

x = np.linspace(strat_lat[1],strat_lat[-1])
h4 = ax2.plot(x, p_north(x), color='k',
              label=r'$\langle \overline{{\theta}}^{{NP}}_{{max}} \rangle_\phi = {:.1f} + {:.1f} r_f$'.format(y_north[0], y_north[1]))
h5 = ax3.plot(x, p_south(x), color='k', linestyle='--',
              label=r'$\langle \overline{{\theta}}^{{SP}}_{{max}} \rangle_\phi = {:.1f} + {:.1f} r_f$'.format(y_south[0], y_south[1]))

ax1.set_xlim([-90,90])
ax1.set_xlabel(r'latitude')
ax1.set_ylabel(r'$\langle \overline{B_r} \rangle_\phi$')
ax1.xaxis.set_ticks(np.arange(-90,91,30))
ax1.legend()

ax2.set_xlabel(r'$r_f$')
ax2.set_ylabel(r'$\langle \overline{\theta}^{NP}_{max} \rangle_\phi$')
ax2.set_ylim([55,65])
ax2.yaxis.set_ticks(np.arange(55,71,1))
ax3.set_ylim([-65,-55])
ax3.yaxis.set_ticks(np.arange(-70,-54,1))
ax3.invert_yaxis()
ax3.set_ylabel(r'$\langle \overline{\theta}^{SP}_{max} \rangle_\phi$')
handles = h4 + h5
labs = [h.get_label() for h in handles]
ax3.legend(handles,labs) 

# Save
if saveOn == 1:
    if not os.path.exists('{}'.format(saveDir)):
        os.makedirs('{}'.format(saveDir))
    fig1.savefig('{}/latitude_vs_Br.png'.format(saveDir),
                format='png', dpi=200, bbox_inches='tight')
    fig1.savefig('{}/latitude_vs_Br.pdf'.format(saveDir),
                format='pdf', dpi=200, bbox_inches='tight')
    print('Figures saved as {}/latitude_vs_Br.*'.format(saveDir))                
    fig2.savefig('{}/rf_vs_polar_minima.png'.format(saveDir),
                format='png', dpi=200, bbox_inches='tight')
    fig2.savefig('{}/rf_vs_polar_minima.pdf'.format(saveDir),
                format='pdf', dpi=200, bbox_inches='tight')
    print('Figures saved as {}/rf_vs_polar_minima.*'.format(saveDir))
