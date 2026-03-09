#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Penelope How, pho@geus.dk
"""

import datetime as dt
import xarray as xr
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.geodesic import Geodesic
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

# Prime plot layout
print('Priming plot...')
fig = plt.figure(figsize=(10,20))
ax_map = plt.subplot(projection=ccrs.Stereographic(central_latitude=70, central_longitude=-42))
fsize1=20
fsize2=16
fsize3=14
fsize4=12

# Define map layers
coastline = cfeature.NaturalEarthFeature(
    category='physical',
    name='land',
    scale='10m',
    edgecolor='darkgray',
    facecolor='lightgray'
)
ice_margin = cfeature.NaturalEarthFeature(
    category='physical',
    name='glaciated_areas',
    scale='10m',        #10m, 50m or 110m
    edgecolor='darkgray',
    facecolor='white'
)
ice_margin_50m = cfeature.NaturalEarthFeature(
    category='physical',
    name='glaciated_areas',
    scale='50m',        #10m, 50m or 110m
    edgecolor='darkgray',
    facecolor='white'
)

# Main map customization
ax_map.set_extent([-58, -25, 58.1, 85], crs=ccrs.PlateCarree())
ax_map.add_feature(coastline, zorder=0)
ax_map.add_feature(ice_margin_50m, zorder=1)
gls = ax_map.gridlines(draw_labels=True)
gls.bottom_labels=False
gls.left_labels=False
gls.xlabel_style = {'size': fsize4, 'color': '#787878'}
gls.ylabel_style = {'size': fsize4, 'color': '#787878'}

# Add scalebars to maps
def add_scalebar(ax, length=None, location=(0.5, 0.05), linewidth=1.5):
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]
    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]
    if not length:
        length = (x1 - x0) / 5000 #in km
        ndim = int(np.floor(np.log10(length))) #number of digits in number
        length = round(length, -ndim) #round to 1sf
        def scale_number(x):
            if str(x)[0] in ['1', '2', '5']: return int(x)
            else: return scale_number(x - 10 ** ndim)
        length = scale_number(length)
    bar_xs = [sbx - length * 500, sbx + length * 500]
    ax.plot(bar_xs, [sby, sby], transform=tmc, color='#787878', linewidth=linewidth)
    ax.text(sbx, sby+0.1, str(length)+' km', color='#787878', fontsize=fsize3, transform=tmc,
            horizontalalignment='center', verticalalignment='bottom')

add_scalebar(ax_map, 400, (0.5, 0.02))

# Create manual symbols for legend
gcnet_color = "#004949"
promice_color = "#b66dff"
glaciobasis_color = "#db6d00"
pt_size=8

#pt1 = Line2D([0], [0], label='GC-Net station', marker='s', markersize=pt_size,
#         markeredgecolor='k', markerfacecolor=gcnet_color, linestyle='')
#pt2 = Line2D([0], [0], label='PROMICE station', marker='o', markersize=pt_size,
#         markeredgecolor='k', markerfacecolor=promice_color, linestyle='')
#pt3 = Line2D([0], [0], label='GlacioBasis station', marker='^', markersize=pt_size,
#         markeredgecolor='k', markerfacecolor=glaciobasis_color, linestyle='')
#ax_map.legend(loc=2, handles=[pt1, pt2, pt3], fontsize=fsize3)

# Show/save
plt.subplots_adjust(wspace=0.2, hspace=0.1, left=0.1, right=0.9)
#plt.tight_layout()
#plt.show()
plt.savefig('greenland_basemap.pdf', dpi=600, bbox_inches="tight")
plt.savefig('greenland_basemap.png', dpi=600)