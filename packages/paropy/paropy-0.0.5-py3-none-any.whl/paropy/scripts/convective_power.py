'''
convective_power.py

Calculate the convective power as a function of radius.

PARODY-JA power.runid computes -Ra_parody/Ekman* 1/(volume of the shell) * int(u_r * r/r_o * (C perturbation) * r^2 dt dtheta sin(theta) dphi)
'''

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import h5py
from numpy.lib.function_base import trapz

from paropy.coreproperties import icb_radius, cmb_radius
from paropy.data_utils import load_dimensionless, load_power
from paropy.plot_utils import streamfunction, C_shift, merid_outline
from paropy.routines import convective_power_timeavg, ref_codensity

# matplotlib.use('Agg')  # backend for no display
plt.close('all')
#%% INPUT PARAMETERS
run_ID = ['chem_200d', 'd_0_55a', 'd_0_6a', 'd_0_65b',
          'c-200a', 'd_0_75a', 'd_0_8a']  # PARODY simulation tag
# path containing simulation output
dirName = '/data/geodynamo/wongj/Work'

fig_aspect = 1  # figure aspect ratio

saveOn = 1  # save figures?
saveDir = '/home/wongj/Work/figures/convective_power'  # path to save files
# saveDir = '/Users/wongj/Documents/isterre/parody/figures/convective_power'

#%%----------------------------------------------------------------------------
# Load data
shell_gap = cmb_radius - icb_radius
ri = icb_radius/shell_gap

w, h = plt.figaspect(fig_aspect)
fig1, ax1 = plt.subplots(1, 1, figsize=(1.5*w, h))
ax1.axhline(0,linestyle='--',color='k')

i=0
for run in run_ID:
    directory = '/data/geodynamo/wongj/Work/{}'.format(run)
    (NR, Ek, Ra, Pr, Pm, fi, rf) = load_dimensionless(run, directory)
    if not os.path.exists('{}/convective_power'.format(directory)):
        (radius, I) = convective_power_timeavg(run, directory)  # timeavg
    else:  # load timeavg data
        print('Loading {}/convective_power'.format(directory))
        f = h5py.File('{}/convective_power'.format(directory), 'r')
        for key in f.keys():
            globals()[key] = np.array(f[key])
    # Check with diagnostics
    df_power = load_power(run,directory)
    check_diag = df_power["available_convective_power_per_unit_vol"].mean()

    ro = radius[-1]
    convective_power = Ra*I/(Ek*radius[-1])

    # Plot
    if rf==ri:
        ax1.plot(radius, convective_power, lw = 2, label=r'$r_f$ = {:.2f}'.format(rf), color='black')
    else:
        ax1.plot(radius, convective_power, lw = 2, label=r'$r_f$ = {:.2f}'.format(rf))
    i+=1

ax1.set_xlabel(r'$r_f$')
ax1.set_ylabel(r'$\mathcal{P}$')
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.legend(loc='lower right')

if saveOn == 1:
    if not os.path.exists('{}'.format(saveDir)):
        os.makedirs('{}'.format(saveDir))
    fig1.savefig('{}/compare_rf.png'.format(saveDir),
                format='png', dpi=200, bbox_inches='tight')
    fig1.savefig('{}/compare_rf.pdf'.format(saveDir),
                format='pdf', dpi=200, bbox_inches='tight')
    print('Figures saved as {}/compare_rf.*'.format(saveDir))
