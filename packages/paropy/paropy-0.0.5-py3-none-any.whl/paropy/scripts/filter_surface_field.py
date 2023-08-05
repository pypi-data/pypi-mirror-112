'''
filter_surface_field.py

Use SHTns library to filter core surface magnetic field
'''

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from paropy.data_utils import surfaceload
from paropy.plot_utils import rad_to_deg, get_Z_lim
from paropy.routines import filter_field

# matplotlib.use('Agg')  # backend for no display
#%%--------------------------------------------------------------------------%%
# INPUT PARAMETERS
#----------------------------------------------------------------------------%%
run_ID = ['chem_200d','c-200a']  # PARODY simulation tag
timestamp = ['6.648476379', '16.84707134']
l_max = 133 # max. spherical harmonic degree from simulation
l_trunc = 14 # SH degree truncation

fig_aspect = 1  # figure aspect ratio
n_levels = 30  # no. of contour levels

saveOn = 1  # save figures?
saveDir = '/home/wongj/Work/figures/filter_surface_field'  # path to save files
# saveDir = '/Users/wongj/Documents/isterre/parody/figures/filter_surface_field'
#%% Load data
w, h = plt.figaspect(fig_aspect)
fig, axs = plt.subplots(2, 2, figsize=(1.5*w, h),
                    subplot_kw={'projection': ccrs.Mollweide()})
axs = axs.reshape(-1)
i=0                    
for run in run_ID:
    # path containing simulation output
    directory = '/data/geodynamo/wongj/Work/{}'.format(run)
    St_file = 'St={}.{}'.format(timestamp[i], run)
    filename = '{}/{}'.format(directory, St_file)

    (version, time, DeltaU, Coriolis, Lorentz, Buoyancy, ForcingU,
    DeltaT, ForcingT, DeltaB, ForcingB, Ek, Ra, Pm, Pr,
    nr, ntheta, nphi, azsym, radius, theta, phi, Vt, Vp,
    Br, dtBr) = surfaceload(filename)

    Br_f = filter_field(Br, nphi, ntheta, l_trunc)

    #%% Plot
    X, Y = rad_to_deg(phi, theta)
    Z_lim = get_Z_lim(Br_f)
    levels = np.linspace(-Z_lim, Z_lim, n_levels) # NOTE: bug with cartopy contours, try different n_levels
    c = axs[2*i].contourf(X, Y, Br.T, levels, transform=ccrs.PlateCarree(), cmap='PuOr_r',
                    extend='both')
    c_f = axs[2*i+1].contourf(X, Y, Br_f, levels, transform=ccrs.PlateCarree(), cmap='PuOr_r',
                    extend='both')                    
    axs[2*i].gridlines()
    axs[2*i].set_global()
    axs[2*i+1].gridlines()
    axs[2*i+1].set_global()    

    #get size and extent of axes:
    axpos = axs[2*i+1].get_position()
    pos_x = axpos.x0+axpos.width + 0.06# + 0.25*axpos.width
    pos_y = axpos.y0
    cax_width = 0.02
    cax_height = axpos.height
    #create new axes where the colorbar should go.
    #it should be next to the original axes and have the same height!
    cbar_ax = fig.add_axes([pos_x,pos_y,cax_width,cax_height])
    cbar = fig.colorbar(c, cax=cbar_ax, orientation='vertical')
    cbar.set_ticks([-Z_lim, -Z_lim/2, 0, Z_lim/2, Z_lim])
    cbar.ax.set_xlabel(r'$B_{r}$', fontsize=12, labelpad=5, y=0.5)

    cbar.ax.tick_params(labelsize=10)
    cbar.ax.tick_params(length=5)
    i+=1


if saveOn == 1:
    if not os.path.exists('{}/{}'.format(saveDir, run_ID)):
        os.makedirs('{}/{}'.format(saveDir, run_ID))
    fig.savefig('{}/{}/{}.png'.format(saveDir, run_ID, timestamp),
                format='png', dpi=200, bbox_inches='tight')
    fig.savefig('{}/{}/{}.pdf'.format(saveDir, run_ID, timestamp),
                format='pdf', dpi=200, bbox_inches='tight')
    print('Figures saved as {}/{}/{}.*'.format(saveDir, run_ID, timestamp))
