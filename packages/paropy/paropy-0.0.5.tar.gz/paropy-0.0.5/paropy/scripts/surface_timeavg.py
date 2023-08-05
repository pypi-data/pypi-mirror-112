#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 11:13:57 2021

@author: wongj

Python version of PARODY-JA4.3 Matlab file 'Matlab/surfaceload_v4.m'.

Loads core surface data and plots core surface field snapshot.

ATTENTION: Folder structure from simulation output should be of the form `<folder>/<run_ID>/Gt_*.run_ID`
"""

import os
import numpy as np
import h5py
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from paropy.data_utils import load_dimensionless
from paropy.plot_utils import rad_to_deg, get_Z_lim
from paropy.routines import surface_timeavg

# matplotlib.use('Agg')  # backend for no display
#%%--------------------------------------------------------------------------%%
# INPUT PARAMETERS
#----------------------------------------------------------------------------%%
# run_ID  = 'ref_c' # PARODY simulation tag
# run_ID = 'd_0_55a'
# run_ID = 'd_0_6a'
# run_ID = 'd_0_65a'
run_ID = 'c-200a'
# run_ID = 'd_0_75a'
# run_ID = 'd_0_8a'
directory = '/data/geodynamo/wongj/Work/{}'.format(run_ID) # path containing simulation output
# directory = '/Users/wongj/Documents/parodydata/{}'.format(run_ID)
# directory = '/Volumes/NAS/ipgp/Work/{}'.format(run_ID)

fig_aspect = 1 # figure aspect ratio
n_levels = 61 # no. of contour levels

saveOn = 1 # save figures?
saveDir = '/home/wongj/Work/figures/surface'  # path to save files
# saveDir = '/Users/wongj/Documents/isterre/parody/figures/surface'
#%%----------------------------------------------------------------------------
# Time average or load data if timeavg data exists
_, _, _, _, _, fi, rf = load_dimensionless(run_ID, directory)
if not os.path.exists('{}/surface_timeavg'.format(directory)):
    (theta, phi, Vt, Vp, Br, dtBr) = surface_timeavg(run_ID,directory) # timeavg
else: # load timeavg data
    print('Loading {}/surface_timeavg'.format(directory))
    f = h5py.File('{}/surface_timeavg'.format(directory), 'r')
    for key in f.keys():
        globals()[key] = np.array(f[key])

#%%----------------------------------------------------------------------------
# Plot
w, h = plt.figaspect(fig_aspect)
fig, ax = plt.subplots(1, 1, figsize=(1.5*w,h), 
                       subplot_kw={'projection': ccrs.Mollweide()})
X,Y = rad_to_deg(phi, theta)
Z = Br.T
Z_lim = get_Z_lim(Z)
levels = np.linspace(-Z_lim,Z_lim,n_levels)

c = ax.contourf(X, Y, Z, levels, transform=ccrs.PlateCarree(),
                extend='both', cmap='PuOr_r')
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
    if not os.path.exists('{}/{}'.format(saveDir,run_ID)):
        os.makedirs('{}/{}'.format(saveDir,run_ID))
    fig.savefig('{}/{}/surface_timeavg.png'.format(saveDir, run_ID), format='png', dpi=200, bbox_inches='tight')
    fig.savefig('{}/{}/surface_timeavg.pdf'.format(saveDir, run_ID), format='pdf', dpi=200, bbox_inches='tight')
    print('Figures saved as {}/{}/surface_timeavg.*'.format(saveDir, run_ID))
