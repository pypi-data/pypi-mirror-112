'''
differential_rotation.py

Analyse differential rotation rates of Cf, Cicb, S and D
'''

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from paropy.coreproperties import icb_radius, cmb_radius
from paropy.data_utils import load_dimensionless, load_mantle, load_innercore

# matplotlib.use('Agg')  # backend for no display
plt.close('all')
#%% INPUT PARAMETERS
run_ID = ['chem_200d', 'ref_c', 'd_0_55a', 'd_0_6a', 'd_0_65b',
          'c-200a', 'd_0_75a', 'd_0_8a']  # PARODY simulation tag
dirName = '/data/geodynamo/wongj/Work' # path containing simulation output


fig_aspect = 1  # figure aspect ratio

saveOn = 1  # save figures?
saveDir = '/home/wongj/Work/figures/rotation'  # path to save files
# saveDir = '/Users/wongj/Documents/isterre/parody/figures/rotation'

# %% LOAD
w, h = plt.figaspect(fig_aspect)
fig1, ax1 = plt.subplots(1, 1, figsize=(1.5*w, h))
fig2, ax2 = plt.subplots(1, 1, figsize=(1.5*w, h))
shell_gap = cmb_radius - icb_radius
ri = icb_radius/shell_gap
ax1.axhline(0,linewidth=1,color='k', linestyle='--')

rf = np.zeros(len(run_ID))
Cf = np.zeros(len(run_ID))
Cicb = np.zeros(len(run_ID))
S = np.zeros(len(run_ID))
D = np.zeros(len(run_ID))
i=0
for run in run_ID:
    directory = '{}/{}'.format(dirName, run)
    print('Loading {}'.format(directory))
    (NR, Ek, Ra, Pr, Pm_out, fi, rf_out) = load_dimensionless(run, directory)
    df_mantle = load_mantle(run,directory)
    df_ic = load_innercore(run,directory)

    Cf_out = (df_ic['rotation_fic']-df_mantle['rotation_rate_on_CMB_fluid_side']).mean()
    Cicb_out = (df_ic['rotation_fic'] - df_ic['rotation_sic']).mean()
    S_out = (df_ic['rotation_sic'] - df_mantle['mantle_rotation_rate']).mean()
    D_out = (df_mantle['rotation_rate_on_CMB_fluid_side'] -
             df_mantle['mantle_rotation_rate']).mean()
    rf[i] = rf_out
    Cf[i] = Cf_out
    Cicb[i] = Cicb_out
    S[i] = S_out
    D[i] = D_out

    # Plot rotation
    mantle_time = df_mantle.time.to_numpy()
    mantle_time = (mantle_time - mantle_time[0])/Pm_out # shift to start from zero and use magnetic diffusion time
    mantle_rotation = df_mantle.mantle_rotation_rate.to_numpy()
    fcmb_rotation = df_mantle.rotation_rate_on_CMB_fluid_side.to_numpy()
    ic_rotation = df_ic.rotation_sic.to_numpy()
    fic_rotation = df_ic.rotation_fic.to_numpy()
    if i==0:
        ax2.plot(mantle_time,mantle_rotation,label=r'reference'.format(rf_out),color='k')
        ax2.plot(mantle_time,fcmb_rotation,label=r'reference'.format(rf_out),color='k',linestyle='--')
        ax2.plot(mantle_time,ic_rotation,label=r'reference'.format(rf_out),color='k')
        ax2.plot(mantle_time,fic_rotation,label=r'reference'.format(rf_out),color='k',linestyle=':')
    elif i ==1:
        ax2.plot(mantle_time,mantle_rotation,label=r'reference'.format(rf_out),color='darkgrey')
        ax2.plot(mantle_time,fcmb_rotation,label=r'reference'.format(rf_out),color='darkgrey',linestyle='--')
        ax2.plot(mantle_time,ic_rotation,label=r'reference'.format(rf_out),color='darkgrey')
        ax2.plot(mantle_time, fic_rotation, label=r'reference'.format(
            rf_out), color='darkgrey', linestyle='--')
    else:    
        h1, = ax2.plot(mantle_time,mantle_rotation,label=r'$r_f = ${:.2f}'.format(rf_out))
        ax2.plot(mantle_time,fcmb_rotation,label=r'$r_f = ${:.2f}'.format(rf_out),linestyle='--', color = h1.get_color())
        ax2.plot(mantle_time, ic_rotation, label=r'reference'.format(
            rf_out), color=h1.get_color())
        ax2 .plot(mantle_time,fic_rotation,label=r'$r_f = ${:.2f}'.format(rf_out),linestyle='--', color = h1.get_color())            

    i+=1

# Scale time with Earth's rotation rate
day_in_seconds = 24*60*60
rotation_rate_Earth = 1/day_in_seconds
Cf = Cf*rotation_rate_Earth
Cicb = Cicb*rotation_rate_Earth
S = S*rotation_rate_Earth
D = D* rotation_rate_Earth

# Thermal wind scaling (doesn't hold)
RaF = Ra*Ek**2/Pr
Cf_scaling = 2.01*RaF**0.5 # (Pichon 2011, eq.53)
# ax1.axhline(Cf_scaling,linestyle='--',color='k')

# %% PLOT
# Reference
ax1.plot(rf[0], Cf[0], 'o', ms = 10, color = 'k', markerfacecolor = "None", label = '_nolegend_')
ax1.plot(rf[0], Cicb[0], '^', ms = 10, color = 'k', markerfacecolor = "None", label = '_nolegend_')
ax1.plot(rf[0], S[0], 's', ms = 10, color = 'k', markerfacecolor = "None", label = '_nolegend_')
ax1.plot(rf[0], D[0], '*', ms=10, color='k', markerfacecolor = "None", label='_nolegend_')

ax1.plot(rf[1], Cf[1], 'o', ms = 10, color = 'darkgrey', markerfacecolor = "None", label = '_nolegend_')
ax1.plot(rf[1], Cicb[1], '^', ms = 10, color = 'darkgrey', markerfacecolor = "None", label = '_nolegend_')
ax1.plot(rf[1], S[1], 's', ms = 10, color = 'darkgrey', markerfacecolor = "None", label = '_nolegend_')
ax1.plot(rf[1], D[1], '*', ms=10, color='darkgrey', markerfacecolor = "None", label='_nolegend_')

# Runs
ax1.plot(rf[2:], Cf[2:], 'o-', ms = 10, color = 'tab:blue', label = r'$\mathcal{C}_f$')
ax1.plot(rf[2:], Cicb[2:], '^-', ms = 10, color = 'tab:orange', label = r'$\mathcal{C}_{icb}$')
ax1.plot(rf[2:], S[2:], 's-', ms = 10, color = 'tab:green', label = r'$\mathcal{S}$')
ax1.plot(rf[2:], D[2:], '*-', ms=10, color='tab:red', label = r'$\mathcal{D}$')

ax1.set_xlabel(r'$r_f$')
ax1.set_ylabel(r'rotation rate')
ax1.legend(loc='lower right')

ax2.set_xlabel("magnetic diffusion time")
ax2.set_ylabel("rotation rate")
ax2.legend()
ax2.autoscale(enable=True, axis='x', tight=True)

if saveOn == 1:
    if not os.path.exists('{}'.format(saveDir)):
        os.makedirs('{}'.format(saveDir))
    fig1.savefig('{}/compare_rf.png'.format(saveDir),
                 format='png', dpi=200, bbox_inches='tight')
    fig1.savefig('{}/compare_rf.pdf'.format(saveDir),
                 format='pdf', dpi=200, bbox_inches='tight')
    print('Figures saved as {}/compare_rf.*'.format(saveDir))


