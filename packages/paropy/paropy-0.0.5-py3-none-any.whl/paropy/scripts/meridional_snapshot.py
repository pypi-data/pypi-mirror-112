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
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cmocean.cm as cmo

from paropy.data_utils import parodyload, load_dimensionless
from paropy.plot_utils import flayer_outline, streamfunction, C_shift, merid_outline

matplotlib.use('Agg')  # backend for no display

#%%--------------------------------------------------------------------------%%
# INPUT PARAMETERS
#----------------------------------------------------------------------------%%
# run_ID, timestamp = 'ref_c', '6.846397324'
# run_ID, timestamp = 'd_0_55a', '20.28436204'
# run_ID, timestamp = 'd_0_6a', '21.49797360'
# run_ID, timestamp = 'd_0_65a', '18.16950357'
run_ID, timestamp = 'c-200a', '16.84707134'
# run_ID, timestamp = 'd_0_75a', '21.43895335'
# run_ID, timestamp = 'd_0_8a', '21.17830229'
directory = '/data/geodynamo/wongj/Work/{}/'.format(run_ID)  # path containing runs

fig_aspect = 1 # figure aspect ratio
n_levels = 21 # no. of contour levels
Vmax = 250 # max Vp
Bmax = 2.5 # max Bp
Tr_min = 1.23
lineWidth = 0.8

saveOn = 1 # save figures?
saveDir = '/home/wongj/Work/figures/meridional/'  # path to save files

#%%----------------------------------------------------------------------------
# Load data
Gt_file = 'Gt={}.{}'.format(timestamp,run_ID)
filename = directory + Gt_file

(version, time, DeltaU, Coriolis, Lorentz, Buoyancy, ForcingU,
            DeltaT, ForcingT, DeltaB, ForcingB, Ek, Ra, Pm, Pr,
            nr, ntheta, nphi, azsym, radius, theta, phi, Vr, Vt, Vp,
            Br, Bt, Bp, T) = parodyload(filename)

NR, Ek, Ra, Pr, Pm, fi, rf = load_dimensionless(run_ID, directory)

#%%----------------------------------------------------------------------------
# Plot
w, h = plt.figaspect(fig_aspect)
fig = plt.figure(constrained_layout=True, figsize = (2*w,h))
spec = gridspec.GridSpec(ncols = 3, nrows = 1, figure=fig)

# Velocity
ax = fig.add_subplot(spec[0,0])
X = np.outer(np.sin(theta),radius)
Y = np.outer(np.cos(theta),radius)
Z = np.mean(Vp,0) # azimuthal avg
# Z_lim = get_Z_lim(Z)
Z_lim = Vmax
levels = np.linspace(-Z_lim,Z_lim,n_levels)
c = ax.contourf(X,Y,Z,levels,cmap='RdYlBu_r',extend='both')
cbar=plt.colorbar(c,ax=ax, aspect = 50, ticks=levels[::2])
cbar.ax.set_title(r'$\mathbf{u}$')
# streamfunction
Vr_m = np.mean(Vr,0)
Vt_m = np.mean(Vt,0)
Z = streamfunction(radius, theta, Vr_m, Vt_m)
c = ax.contour(X,Y,Z, 9 , colors='grey', linewidths = lineWidth, alpha = 0.5)
merid_outline(ax,radius)
ax.axis('off')

# Field
ax = fig.add_subplot(spec[0,1])
Z = np.mean(Bp, 0)  # azimuthal avg
Z_lim = Bmax
levels = np.linspace(-Z_lim,Z_lim,n_levels)
c = ax.contourf(X,Y,Z,levels,cmap='PuOr_r',extend='both')
cbar=plt.colorbar(c,ax=ax, aspect = 50, ticks=levels[::2])
cbar.ax.set_title(r'$\mathbf{B}$')
# poloidal
Br_m = np.mean(Br,0)
Bt_m = np.mean(Bt,0)
Z = streamfunction(radius, theta, Br_m, Bt_m)
c = ax.contour(X,Y,Z, 9 , colors='grey', linewidths = lineWidth, alpha = 0.5)
merid_outline(ax,radius)
ax.axis('off')

# Codensity
ax = fig.add_subplot(spec[0,2])
Z0 = np.mean(T, 0)  # azimuthal avg
Z, levels = C_shift(radius, rf, Z0, n_levels)
c = ax.contourf(X,Y,Z,levels,cmap='inferno') 
cbar=plt.colorbar(c,ax=ax,aspect = 50, ticks=levels[::2])
cbar.ax.set_title(r'$C$')
merid_outline(ax,radius)
# flayer_outline(ax,rf)
ax.axis('off')

# Save
if saveOn==1:
    if not os.path.exists(saveDir+'{}'.format(run_ID)):
        os.makedirs(saveDir+'{}'.format(run_ID))
    fig.savefig(saveDir+'{}/{}.png'.format(run_ID, timestamp),format='png',
                dpi=200,bbox_inches='tight')
    fig.savefig(saveDir+'{}/{}.pdf'.format(run_ID, timestamp),format='pdf',
                dpi=200,bbox_inches='tight')
    print('Figures saved as {}{}/{}.*'.format(saveDir,run_ID,timestamp))
