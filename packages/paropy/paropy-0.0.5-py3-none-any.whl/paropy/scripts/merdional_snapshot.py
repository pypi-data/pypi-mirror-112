#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 10:49:39 2021

@author: wongj

Python version of PARODY-JA4.3 Matlab file 'Matlab/parodyloadload_v4.m'.

Loads graphics file and plots snapshots of the azimuthal velocity field,
azimuthal magnetic field, temperature/codensity field in meridional slices.

"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from paropy.data_utils import parodyload

#%%--------------------------------------------------------------------------%%
# INPUT PARAMETERS
#----------------------------------------------------------------------------%%
run_ID = 'c-200a' # PARODY simulation tag
directory = '/Volumes/NAS/ipgp/Work/{}/'.format(run_ID) # path containing simulation output
timestamp = '16.84707134' 

fig_aspect = 1 # figure aspect ratio
n_levels = 21 # no. of contour levels
Vmax = 300 # max Vp
Bmax = 2.5 # max Bp
saveOn = 0 # save figures?

#%%----------------------------------------------------------------------------
# Load data
Gt_file = 'Gt={}.{}'.format(timestamp,run_ID)
filename = directory + Gt_file

(version, time, DeltaU, Coriolis, Lorentz, Buoyancy, ForcingU, 
            DeltaT, ForcingT, DeltaB, ForcingB, Ek, Ra, Pm, Pr,
            nr, ntheta, nphi, azsym, radius, theta, phi, Vr, Vt, Vp,
            Br, Bt, Bp, T) = parodyload(filename)

#%%----------------------------------------------------------------------------
# Plot
w, h = plt.figaspect(fig_aspect)
fig = plt.figure(constrained_layout=True, figsize = (1.5*w,h))
spec = gridspec.GridSpec(ncols = 2, nrows = 1, figure=fig)

ax = fig.add_subplot(spec[0,0])
X = np.outer(radius,np.sin(theta),)
Y = np.outer(radius,np.cos(theta))
Z = np.mean(Vp,0).T
# Z_lim = get_Z_lim(Z)
Z_lim = Vmax
levels = np.linspace(-Z_lim,Z_lim,n_levels)
c = ax.contourf(X,Y,Z,levels,cmap='RdYlBu_r',extend='both')
cbar=plt.colorbar(c,ax=ax, aspect = 50, ticks=levels[::2])
cbar.ax.set_title(r'$\mathbf{u}$')
ax.axis('off')

ax = fig.add_subplot(spec[0,1])
Z = np.mean(Bp,0).T
Z_lim = Bmax
levels = np.linspace(-Z_lim,Z_lim,n_levels)
c = ax.contourf(X,Y,Z,levels,cmap='PuOr_r',extend='both')
cbar=plt.colorbar(c,ax=ax, aspect = 50, ticks=levels[::2])
cbar.ax.set_title(r'$\mathbf{B}$')
ax.axis('off')

# ax = fig.add_subplot(spec[0,2])
# Z = np.mean(T,0).T
# c = ax.contourf(X,Y,Z,cmap='BrBG_r',extend='both')
# cbar=plt.colorbar(c,ax=ax,aspect = 50)
# cbar.ax.set_title(r'$T$')
# ax.axis('off')

# Save
if saveOn==1:
    if not os.path.exists(directory+'/figures'):
        os.makedirs(directory+'/figures')
    fig.savefig(directory+'/figures/merid_{}.png'.format(timestamp),format='png',
                dpi=200,bbox_inches='tight')
    fig.savefig(directory+'/figures/merid_{}.pdf'.format(timestamp),format='pdf',
                dpi=200,bbox_inches='tight')
    print('Figures saved as {}/figures/merid_{}'.format(directory,timestamp))
