#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 11:13:57 2021

@author: wongj

Python version of PARODY-JA4.3 Matlab file 'Matlab/surfaceload_v4.m'.

Loads core surface data and plots core surface field snapshot.

ATTENTION: Folder structure should be of the form `<folder>/<run_ID>/St_*.run_ID`
"""

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from paropy.data_utils import surfaceload
from paropy.plot_utils import rad_to_deg, get_Z_lim

matplotlib.use('Agg')  # backend for no display
#%%--------------------------------------------------------------------------%%
# INPUT PARAMETERS
#----------------------------------------------------------------------------%%
run_ID, timestamp = 'c-200a', '16.84707134'
directory = '/data/geodynamo/wongj/Work/{}'.format(run_ID) # path containing simulation output
# directory = '/Volumes/NAS/ipgp/Work/{}/'.format(run_ID)
# directory = '/Users/wongj/Desktop/data/{}'.format(run_ID)

fig_aspect = 1 # figure aspect ratio
n_levels = 60 # no. of contour levels

saveOn = 1 # save figures?
saveDir = '/home/wongj/Work/figures/surface'  # path to save files
# saveDir = '/Users/wongj/Documents/isterre/parody/figures/surface'
#%%----------------------------------------------------------------------------
# Load data
St_file = 'St={}.{}'.format(timestamp,run_ID)
filename = '{}/{}'.format(directory,St_file)

(version, time, DeltaU, Coriolis, Lorentz, Buoyancy, ForcingU, 
            DeltaT, ForcingT, DeltaB, ForcingB, Ek, Ra, Pm, Pr,
            nr, ntheta, nphi, azsym, radius, theta, phi, Vt, Vp,
            Br, dtBr) = surfaceload(filename)

#%%----------------------------------------------------------------------------
# Plot
w, h = plt.figaspect(fig_aspect)
fig, ax = plt.subplots(1, 1, figsize=(1.5*w,h), 
                       subplot_kw={'projection': ccrs.Mollweide()})
X,Y = rad_to_deg(phi, theta)
Z = Br.T
Z_lim = get_Z_lim(Z)
levels = np.linspace(-Z_lim,Z_lim,n_levels)
c = ax.contourf(X, Y, Z, levels, transform=ccrs.PlateCarree(), cmap='PuOr_r',
                extend='both')
cbar_ax = fig.add_axes([0.2,0.06,0.6,0.04])
cbar = fig.colorbar(c, cax=cbar_ax, orientation='horizontal')
cbar.set_ticks([-Z_lim,-Z_lim/2,0,Z_lim/2,Z_lim])
cbar.ax.set_xlabel(r'$B_{r}$',fontsize=12)
cbar.ax.tick_params(labelsize=12)
cbar.ax.tick_params(length=6)
ax.gridlines()
ax.set_global()

# Save
if saveOn == 1:
    if not os.path.exists(saveDir+'/{}'.format(run_ID)):
        os.makedirs(saveDir+'/{}'.format(run_ID))
    fig.savefig(saveDir+'/{}/{}.png'.format(run_ID, timestamp), format='png',
                dpi=200, bbox_inches='tight')
    fig.savefig(saveDir+'/{}/{}.pdf'.format(run_ID, timestamp), format='pdf',
                dpi=200, bbox_inches='tight')
    print('Figures saved as {}/{}/{}.*'.format(saveDir, run_ID, timestamp))
