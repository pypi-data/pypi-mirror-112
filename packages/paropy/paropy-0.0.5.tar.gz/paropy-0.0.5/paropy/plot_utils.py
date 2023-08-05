#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 16:10:19 2021

@author: wongj
"""

import numpy as np
import scipy.special as sp
import math
from scipy.integrate import cumtrapz

from paropy.coreproperties import icb_radius, cmb_radius

def rad_to_deg(phi,theta):
    '''Converts radians into longitudinal and latitudinal degrees where -180 < phi_deg < 180 and -90 < theta_deg < 90 degrees'''
    lon=np.zeros(len(phi))
    lat=np.zeros(len(theta))    
    i=0
    for val in phi:
        lon[i]=math.degrees(val)-180
        i=i+1
    i=0
    for val in theta:
        lat[i]=math.degrees(val)-90
        i=i+1    
    
    return (lon, lat)

def deg_to_rad(lon, lat):
    '''Converts longitudinal and latitudinal degrees where -180 < phi_deg < 180 and -90 < theta_deg < 90 degrees into radians'''
    phi = np.zeros(len(lon))
    theta = np.zeros(len(lat))
    i = 0
    for val in lon:
        phi[i] = math.radians(val)+np.pi
        i = i+1
    i = 0
    for val in lat:
        theta[i] = math.radians(val)+np.pi/2
        i = i+1

    return (phi, theta)

def get_Z_lim(Z,dp=1):
    '''Choose Z limit for plot to dp decimal places'''
    Z_lim = np.max(np.abs(Z))
    Z_lim = np.round(Z_lim, dp)

    return Z_lim        
    
def streamfunction(radius,theta,ur,ut):
    '''Streamfunction for merdional cuts:
        - radius and theta are 1d arrays
        - ur and ut are 2d arrays of size len(radius)*len(theta)
    '''
    r,t = np.meshgrid(radius, theta)
    # integrate for streamfunction (polars)
    intr = cumtrapz(ut,r,axis=1,initial=0)
    intt = cumtrapz(r*ur,t,axis=0,initial=0)[:,0][:,None]
    psi = -intr + intt # + C, could add constant of integration here
     
    return (psi)

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

def C_shift(radius, rf, Z0, n_levels, lev_min=0, lev_max=1):
    '''Normalise and shift the codensity field scale so that a < C < b -> 0 < (C - b)/h + 1 < 1'''
    idx = np.argwhere(radius > rf)[0][0]
    if rf !=0: 
        # b: max T near top of F-layer
        Ts_max = np.mean(Z0[:, idx+1]) 
        # a: min T outside F-layer
        Ts_min = np.min(Z0[:, idx:])
    else:
        Ts_max = np.max(Z0)
        Ts_min = np.min(Z0)
    h = Ts_max-Ts_min
    Z1 = (Z0 - Ts_max)/h  # normalise
    Z = Z1 + lev_max
    levels = np.linspace(lev_min, lev_max, n_levels)
    return Z, levels

def semicircle(center_x, center_y, radius, stepsize=0.1):
    """
    generates coordinates for a semicircle, centered at center_x, center_y
    """        

    x = np.arange(center_x, center_x+radius+stepsize, stepsize)
    y = np.sqrt(abs(radius**2 - x**2))

    # since each x value has two corresponding y-values, duplicate x-axis.
    # [::-1] is required to have the correct order of elements for plt.plot. 
    x = np.concatenate([x,x[::-1]])

    # concatenate y and flipped y. 
    y = np.concatenate([y,-y[::-1]])

    return x, y + center_y

def merid_outline(ax,radius,linewidth=0.5):
    x,y = semicircle(0,0,radius[0], 1e-4)
    ax.plot(x, y, 'k', lw=linewidth)
    x,y = semicircle(0,0,radius[-1], 1e-4)
    ax.plot(x, y, 'k', lw=linewidth)
    ax.vlines(0,radius[0],radius[-1],'k', lw=linewidth)
    ax.vlines(0,-radius[0],-radius[-1],'k', lw=linewidth)

def flayer_outline(ax, rf,linewidth=0.5):
    x, y = semicircle(0, 0, rf, 1e-4)
    ax.plot(x, y, '--', lw = linewidth, color='darkgray')


def tangent_cylinder_latitude(rf):
    shell_gap = cmb_radius - icb_radius
    if rf == 0:
        ri = icb_radius/cmb_radius
        tc_lat = 90 - (np.pi/2-math.acos(ri))*180/np.pi
    else:
        tc_lat = 90 - (np.pi/2-math.acos(rf*shell_gap/cmb_radius))*180/np.pi
    return tc_lat

def polar_minimum_latitude(theta,Br):
    '''
    Maximum (minimum) Br in each hemisphere
    '''
    idx_north = np.where(Br == np.max(Br[theta < np.pi/2]))[0][0]
    idx_south = np.where(Br == np.min(Br[theta > np.pi/2]))[0][0]
    # Convert to latitude
    pm_lat_north = 90 - theta[idx_north]*180/np.pi
    pm_lat_south = 90 - theta[idx_south]*180/np.pi

    return pm_lat_north, pm_lat_south

