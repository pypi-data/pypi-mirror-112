'''
diagnostic_parameters.py

Calculate diagnostic parameters such as magnetic Reynolds and Elsasser numbers

  Re = np.sqrt(2*kinetic_data.ke_per_unit_vol.mean(axis=0))
  El = 2*magnetic_data.me_per_unit_vol.mean(axis=0)*Ek*Pm
  Rm = Pm*Re
  Ro = Re*Ek

'''
#%% Import
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from matplotlib import ticker
from paropy.data_utils import load_kinetic, load_magnetic, load_dimensionless, load_mantle, load_power

#%% Input parameters
run_ID = ['chem_200d','d_0_55a','d_0_6a','d_0_65b','c-200a','d_0_75a','d_0_8a']  # PARODY simulation tag
# run_ID = ['c-200a']
# path containing simulation output
dirName = '/data/geodynamo/wongj/Work'
# directory = '/Volumes/NAS/ipgp/Work//'
# directory = '/Users/wongj/Desktop/data/'

fig_aspect = 1  # figure aspect ratio

saveOn = 1  # save figures?
saveDir = '/home/wongj/Work/figures/diagnostic_parameters'  # path to save files
# saveDir = '/Users/wongj/Documents/isterre/parody/figures/surface'

#%% Pre-allocate
rf = np.zeros(len(run_ID))
time_mag = np.zeros(len(run_ID))
Re = np.zeros(len(run_ID))
El = np.zeros(len(run_ID))
Rm = np.zeros(len(run_ID))
Ro = np.zeros(len(run_ID))
power_density = np.zeros(len(run_ID))
avg_torques = np.zeros(len(run_ID))

#%% Load
w, h = plt.figaspect(fig_aspect)
fig3, ax3 = plt.subplots(1, 1, figsize=(1.5*w, h))
i=0
for run in run_ID:
    directory = '{}/{}'.format(dirName,run)
    (_, Ek_out, Ra_out, Pr_out, Pm_out, fi_out, rf_out) = load_dimensionless(run,directory)
    kinetic_data = load_kinetic(run,directory)
    magnetic_data = load_magnetic(run, directory)
    power_data = load_power(run,directory)
    mantle_data = load_mantle(run,directory)

    #%% Diagnostic parameters
    time_out = (kinetic_data.time.iloc[-1]-kinetic_data.time.iloc[0])/Pm_out
    Re_out = np.sqrt(2*kinetic_data.ke_per_unit_vol.mean(axis=0))
    El_out = 2*magnetic_data.me_per_unit_vol.mean(axis=0)*Ek_out*Pm_out
    Rm_out = Pm_out*Re_out
    Ro_out = Re_out*Ek_out
    power_density_out = power_data.available_convective_power_per_unit_vol.mean(axis=0)
    torque_out = mantle_data.gravitational_torque_on_mantle.mean()/ mantle_data.gravitational_torque_on_mantle.max()

    rf[i]=rf_out
    time_mag[i] = time_out
    Re[i]=Re_out
    El[i]=El_out
    Rm[i]=Rm_out
    Ro[i]=Ro_out
    power_density[i]=power_density_out
    avg_torques[i]=torque_out

    # Plot mantle rotation
    mantle_time = mantle_data.time.to_numpy()
    mantle_time = (mantle_time - mantle_time[0])/Pm_out # shift to start from zero and use magnetic diffusion time
    mantle_rotation = mantle_data.mantle_rotation_rate.to_numpy()
    if i==0:
        ax3.plot(mantle_time,mantle_rotation,label=r'reference'.format(rf_out),color='darkgrey')
    else:    
        ax3.plot(mantle_time,mantle_rotation,label=r'$r_f = ${:.2f}'.format(rf_out))

    i+=1

#%% Plot
# Magnetic Reynolds and Elsasser number
fig1, ax1a = plt.subplots(1, 1, figsize=(1.5*w,h))
ax1b = ax1a.twinx()
h1a = ax1a.plot(rf[0], Rm[0], 'o', ms=10, color='darkgrey', markerfacecolor = 'None', label=r'$Rm$')
h1b = ax1b.plot(rf[0], El[0], 's', ms=10, color='darkgrey',
                markerfacecolor='None', label=r'$\Lambda$')
h1a = ax1a.plot(rf[1:], Rm[1:], 'o', ms=10, color='tab:blue', label=r'$Rm$')
h1b = ax1b.plot(rf[1:],El[1:],'s',ms=10,color='tab:orange',label=r'$\Lambda$')
ax1a.set_xlabel(r'$r_f$')
ax1a.set_ylabel(r'$Rm$')
ax1b.set_ylabel(r'$\Lambda$')
ax1a.set_ylim([700, 1100])
ax1b.set_ylim([16, 30])
handles = h1a + h1b
labs = [h.get_label() for h in handles]
ax1b.legend(handles,labs)

# Power density
fig2, ax2 = plt.subplots(1, 1, figsize=(1.5*w, h))
ax2.plot(rf[0],power_density[0],'o',ms=10,color='darkgrey',markerfacecolor = 'None')
ax2.plot(rf[1:],power_density[1:],'o',ms=10,color='tab:green')
ax2.set_xlabel(r'$r_f$')
ax2.set_ylabel(r'$\mathcal{P}$')
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((-1, 1))
ax2.yaxis.set_major_formatter(formatter)

# Mantle rotation
ax3.set_xlabel("magnetic diffusion time")
ax3.set_ylabel("mantle rotation rate")
ax3.legend()
ax3.autoscale(enable=True, axis='x', tight=True)

# Gravitatoinal torques
fig4, ax4 = plt.subplots(1, 1, figsize=(1.5*w, h))
ax4.plot(rf[0],avg_torques[0],'o',ms=10,color='darkgrey',markerfacecolor = 'None')
ax4.plot(rf[1:],avg_torques[1:],'o',ms=10,color='tab:red')
ax4.set_xlabel(r'$r_f$')
ax4.set_ylabel(r'$|\overline{\Gamma}/\Gamma_{max}|$')

#%% Save
if saveOn == 1:
    if not os.path.exists(saveDir+'/diagnostic_parameters'):
        os.makedirs(saveDir+'/diagnostic_parameters')
    fig1.savefig(saveDir+'/Rm_El.png', format='png',
                dpi=200, bbox_inches='tight')
    fig1.savefig(saveDir+'/Rm_El.pdf', format='pdf',
                dpi=200, bbox_inches='tight')
    print('Figures saved as {}/Rm_El.*'.format(saveDir))
    fig2.savefig(saveDir+'/power_density.png', format='png',
                dpi=200, bbox_inches='tight')
    fig2.savefig(saveDir+'/power_density.pdf', format='pdf',
                dpi=200, bbox_inches='tight')
    print('Figures saved as {}/power_density.*'.format(saveDir))
    fig3.savefig(saveDir+'/mantle_rotation.png', format='png',
                dpi=200, bbox_inches='tight')
    fig3.savefig(saveDir+'/mantle_rotation.pdf', format='pdf',
                dpi=200, bbox_inches='tight')
    print('Figures saved as {}/mantle_rotation.*'.format(saveDir))
    fig4.savefig(saveDir+'/avg_grav_torques.png', format='png',
                dpi=200, bbox_inches='tight')
    fig4.savefig(saveDir+'/avg_grav_torques.pdf', format='pdf',
                dpi=200, bbox_inches='tight')
    print('Figures saved as {}/avg_grav_torques.*'.format(saveDir))
