#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 10:49:39 2021

@author: wongj

Python version of PARODY-JA4.3 Matlab file 'Matlab/parodyloadload_v4.m'.

Loads graphics file and plots time average of the azimuthal velocity field,
azimuthal magnetic field, temperature/codensity field in meridional slices.

"""

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import h5py

from paropy.data_utils import load_dimensionless
from paropy.plot_utils import streamfunction, C_shift, merid_outline
from paropy.routines import meridional_timeavg

# matplotlib.use('Agg')  # backend for no display
plt.style.use('dark_background')

#%%--------------------------------------------------------------------------%%
# INPUT PARAMETERS
#----------------------------------------------------------------------------%%
# run_ID  = 'chem_200d'
run_ID  = 'ref_c'
# run_ID = 'd_0_55a'
# run_ID = 'd_0_6a'
# run_ID = 'd_0_65a'
# run_ID = 'c-200a'
# run_ID = 'd_0_75a'
# run_ID = 'd_0_8a'
# directory = '/data/geodynamo/wongj/Work/{}'.format(run_ID) # path containing runs
directory = '/Volumes/NAS/ipgp/Work/{}'.format(run_ID)

fig_aspect = 1 # figure aspect ratio
n_levels = 21 # no. of contour levels
Vmax = 250 # max Vp
Bmax = 2.5 # max Bp
Tr_min = 1.23
lineWidth = 0.8

saveOn = 1 # save figures?
# saveDir = '/home/wongj/Work/figures/meridional'  # path to save files
saveDir = '/Users/wongj/Documents/isterre/parody/figures/meridional'

#%%----------------------------------------------------------------------------
# Load data
_, _, _, _, _, fi, rf = load_dimensionless(run_ID, directory)
if not os.path.exists('{}/meridional_timeavg'.format(directory)):
    (radius, theta, phi, Vr, Vt, Vp, Br, Bt,
     Bp, T) = meridional_timeavg(run_ID, directory)  # timeavg
else:  # load timeavg data
    print('Loading {}/meridional_timeavg'.format(directory))
    f = h5py.File('{}/meridional_timeavg'.format(directory), 'r')
    for key in f.keys():
        globals()[key] = np.array(f[key])

#%%----------------------------------------------------------------------------
# Plot
w, h = plt.figaspect(fig_aspect)
fig = plt.figure(constrained_layout=True, figsize = (2*w,h))
spec = gridspec.GridSpec(ncols = 3, nrows = 1, figure=fig)

# Velocity
ax = fig.add_subplot(spec[0,0])
X = np.outer(np.sin(theta),radius)
Y = np.outer(np.cos(theta),radius)
Z = Vp
Z_lim = Vmax
levels = np.linspace(-Z_lim,Z_lim,n_levels)
c = ax.contourf(X,Y,Z,levels,cmap='RdYlBu_r',extend='both')
cbar=plt.colorbar(c,ax=ax, aspect = 50, ticks=levels[::2])
cbar.ax.set_title(r'$\mathbf{u}$')
# streamfunction
idx = np.argwhere(radius > rf)[0][0]
Z = streamfunction(radius[idx:], theta, Vr[:,idx:], Vt[:,idx:])
c = ax.contour(X[:,idx:],Y[:,idx:],Z, 9 , colors='grey', linewidths = lineWidth, alpha = 0.5)
merid_outline(ax,radius)
ax.axis('off')

# Field
ax = fig.add_subplot(spec[0,1])
Z = Bp
Z_lim = Bmax
levels = np.linspace(-Z_lim,Z_lim,n_levels)
c = ax.contourf(X,Y,Z,levels,cmap='PuOr_r',extend='both')
cbar=plt.colorbar(c,ax=ax, aspect = 50, ticks=levels[::2])
cbar.ax.set_title(r'$\mathbf{B}$')
# poloidal
Z = streamfunction(radius, theta, Br, Bt)
c = ax.contour(X,Y,Z, 9 , colors='grey', linewidths = lineWidth, alpha = 0.5)
merid_outline(ax,radius)
ax.axis('off')

# Codensity
ax = fig.add_subplot(spec[0,2])
Z0 = T
# Z = T
Z, levels = C_shift(radius, rf, Z0, n_levels)
c = ax.contourf(X,Y,Z,levels,extend = 'both', cmap='YlOrRd_r') 
cbar=plt.colorbar(c,ax=ax,aspect = 50, ticks=levels[::2])
cbar.ax.set_title(r'$C$')
merid_outline(ax,radius)
# flayerline(ax,rf)
ax.axis('off')

# Save
if saveOn==1:
    if not os.path.exists(saveDir+'/{}'.format(run_ID)):
        os.makedirs(saveDir+'/{}'.format(run_ID))
    fig.savefig(saveDir+'/{}/meridional_timeavg_dark.png'.format(run_ID),format='png',
                dpi=200,bbox_inches='tight')
    fig.savefig(saveDir+'/{}/meridional_timeavg_dark.pdf'.format(run_ID), format='pdf',
                dpi=200,bbox_inches='tight')
    print('Figures saved as {}/{}/meridional_timeavg_dark.*'.format(saveDir, run_ID))
