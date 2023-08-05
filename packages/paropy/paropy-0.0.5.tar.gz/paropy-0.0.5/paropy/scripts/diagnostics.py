#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 09:29:58 2021

@author: wongj

Loads diagnostic outputs from PARODY-JA4.3:
    - kinetic and magnetic energies
    - Nusselt number (not sure this is computed in PARODY for all HeatingModes)
    - dipole e.g. g10, g11, B_rms
    - power e.g. convective power per unit volume
    - scales e.g. mean l for V, B, T (Christensen & Aubert, 2006)
    - spec_l and spec_m
    - inner core and mantle rotation and torques (if Coupled Earth run)

"""
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os

from paropy.data_utils import load_kinetic,load_magnetic,load_nusselt, \
load_dipole,load_power,load_scales,load_spec_l,load_spec_m, load_mantle, \
load_innercore
from paropy.routines import sim_time, grav_torque

matplotlib.use('Agg') # backend for no display 

#%%--------------------------------------------------------------------------%%
# INPUT PARAMETERS
#----------------------------------------------------------------------------%%
run_ID = 'c-200a' # PARODY simulation tag
directory = '/data/geodynamo/wongj/Work/{}/'.format(run_ID) # path containing simulation output
saveDir = '/home/wongj/Work/figures/diagnostics/' # path to save files

plotOn=1 # Plot and save

#%% Load data
kinetic_data=load_kinetic(run_ID,directory)
magnetic_data=load_magnetic(run_ID,directory)
# nusselt_data=load_nusselt(run_ID,directory)
# dipole_data=load_dipole(run_ID,directory)
# power_data=load_power(run_ID,directory)
# scales_data=load_scales(run_ID,directory)
# spec_l_data=load_spec_l(run_ID,directory)
# spec_m_data=load_spec_m(run_ID,directory)
try:
    mantle_data=load_mantle(run_ID,directory)
except FileNotFoundError:
    mantle_data=pd.DataFrame({'A' : []})
# try:
#     ic_data=load_innercore(run_ID,directory)
# except:
#     ic_data=pd.DataFrame({'A' : []})

#%%----------------------------------------------------------------------------
# Output data
print('run_ID: {}'.format(run_ID))
time = sim_time(kinetic_data)
print('Simulation time: {:.3f}'.format(time))
(gamma,gamma_max)=grav_torque(mantle_data)
print('Mean of gravitational torque on mantle: {:.2f} ({:.4e} of the maximum absolute value)'.format(
                gamma, gamma/gamma_max))

# Plot
if plotOn==1:
    ax1=kinetic_data.plot("time","ke_per_unit_vol")
    kinetic_data.plot("time","poloidal_ke",ax=ax1)
    kinetic_data.plot("time","toroidal_ke",ax=ax1)
    fig1 = ax1.get_figure()

    ax2=magnetic_data.plot("time","me_per_unit_vol")
    magnetic_data.plot("time","poloidal_me",ax=ax2)
    magnetic_data.plot("time","toroidal_me",ax=ax2)
    fig2 = ax2.get_figure()

    ax3=mantle_data.plot("time","mantle_rotation_rate")
    fig3 = ax3.get_figure()

    ax4=mantle_data.plot("time","gravitational_torque_on_mantle")
    fig4 = ax4.get_figure()

    # Save 
    if not os.path.exists(saveDir+'{}'.format(run_ID)):
        os.makedirs(saveDir+'{}'.format(run_ID))
    fig1.savefig(saveDir+'{}/kinetic.png'.format(run_ID))
    fig2.savefig(saveDir+'{}/magnetic.png'.format(run_ID))
    fig3.savefig(saveDir+'{}/mantle_rotation.png'.format(run_ID))
    fig4.savefig(saveDir+'{}/mantle_grav_torque.png'.format(run_ID))
    print('Figures saved in {}{}'.format(saveDir,run_ID))
