'''
rotation_rate.py

Analyse rotation rates of IC, FICB, FCMB and M
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
dirName = '/data/geodynamo/wongj/Work'  # path containing simulation output


fig_aspect = 1  # figure aspect ratio

saveOn = 1  # save figures?
saveDir = '/home/wongj/Work/figures/rotation_rate'  # path to save files
# saveDir = '/Users/wongj/Documents/isterre/parody/figures/rotation_rate'

# %% LOAD
w, h = plt.figaspect(fig_aspect)

rf = np.zeros(len(run_ID))
Cf = np.zeros(len(run_ID))
Cicb = np.zeros(len(run_ID))
S = np.zeros(len(run_ID))
D = np.zeros(len(run_ID))

shell_gap = cmb_radius - icb_radius
ri = icb_radius/shell_gap

i = 0
for run in run_ID:
    fig1, ax1 = plt.subplots(1, 1, figsize=(1.5*w, h))
    ax1.axhline(0, linewidth=1, color='k', linestyle='--')
    directory = '{}/{}'.format(dirName, run)
    print('Loading {}'.format(directory))
    (NR, Ek, Ra, Pr, Pm_out, fi, rf_out) = load_dimensionless(run, directory)
    df_mantle = load_mantle(run, directory)
    df_ic = load_innercore(run, directory)

    # Plot rotation
    mantle_time = df_mantle.time.to_numpy()
    # shift to start from zero and use magnetic diffusion time
    mantle_time = (mantle_time - mantle_time[0])/Pm_out
    mantle_rotation = df_mantle.mantle_rotation_rate.to_numpy()
    fcmb_rotation = df_mantle.rotation_rate_on_CMB_fluid_side.to_numpy()
    ic_rotation = df_ic.rotation_sic.to_numpy()
    fic_rotation = df_ic.rotation_fic.to_numpy()

    ax1.plot(mantle_time, mantle_rotation,
                    label=r'$\Omega_{m}$')
    ax1.plot(mantle_time, fcmb_rotation, label=r'$\Omega_{fcmb}$')
    # ax1.plot(mantle_time, ic_rotation, label=r'$\Omega_{ic}$')
    ax1.plot(mantle_time, fic_rotation, label=r'$\Omega_{ficb}$')

    ax1.set_xlabel("magnetic diffusion time")
    ax1.set_ylabel("rotation rate")
    ax1.legend()
    ax1.autoscale(enable=True, axis='x', tight=True)

    if saveOn == 1:
        if not os.path.exists('{}'.format(saveDir)):
            os.makedirs('{}'.format(saveDir))
        fig1.savefig('{}/{}.png'.format(saveDir,run),
                    format='png', dpi=200, bbox_inches='tight')
        fig1.savefig('{}/{}.pdf'.format(saveDir,run),
                    format='pdf', dpi=200, bbox_inches='tight')
        print('Figures saved as {}/{}.*'.format(saveDir,run))

    plt.close(fig1)

    i += 1


