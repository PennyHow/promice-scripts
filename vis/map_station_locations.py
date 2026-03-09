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

# Define PROMICE stations
stations = [ #GC-Net
            'CEN','CP1','DY2','EGP','HUM','JAR','NAE','NAU','NEM','NSE',
            'SDL','SDM','SWC','TUN',
            #GlacioBasis
            'FRE','LYN_L','LYN_T','NUK_K','ZAC_A','ZAC_L','ZAC_U',
            #PROMICE
            'KAN_B','KAN_L','KAN_M','KAN_T','KAN_U','KPC_L','KPC_U','MIT',
            'NUK_B','NUK_L','NUK_U','QAS_A','QAS_L','QAS_M', #'NUK_N',
            'QAS_U','SCO_L', 'SCO_U','TAS_A', 'TAS_L', 'TAS_U','THU_L',
            'THU_L2', 'THU_U','UPE_L','UPE_U',
            #External
#            'RED_L','SER_B','ORO','WEG_B','WEG_L'
            ]

# Define vis parameters
gcnet_color = "#004949"
promice_color = "#b66dff"
glaciobasis_color = "#db6d00"
pt_size=6

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

# Define QAS transect inset map
extent1 = [-46.95, -46.45, 60.93, 61.33]
ax_inset1 = fig.add_axes([0.03, 0.08, 0.25, 0.25], projection=ccrs.Mercator())
ax_inset1.set_extent(extent1, crs=ccrs.PlateCarree())
ax_inset1.add_feature(coastline, zorder=0)
ax_inset1.add_feature(ice_margin, zorder=1)
zoom_box1 = mpatches.Rectangle(xy=[extent1[0]-0.75, extent1[2]-0.75], width=2, height=2.1,
                              edgecolor='red', facecolor='none',
                              linewidth=1.5, transform=ccrs.PlateCarree(), zorder=3)
ax_map.add_patch(zoom_box1)
ax_map.text(extent1[0]-1.8, extent1[3], "c", fontsize=fsize1, color='red', transform=ccrs.PlateCarree())
ax_inset1.text(extent1[0]+0.01, extent1[3]-0.02, "c", fontsize=fsize1, transform=ccrs.PlateCarree())


# Define NUK inset map
extent2 = [-51.5, -49.2, 63.8, 65.51]
ax_inset2 = fig.add_axes([0.03, 0.297, 0.25, 0.25], projection=ccrs.Mercator())
ax_inset2.set_extent(extent2, crs=ccrs.PlateCarree())
ax_inset2.add_feature(coastline, zorder=0)
ax_inset2.add_feature(ice_margin, zorder=1)
zoom_box2 = mpatches.Rectangle(xy=[extent2[0]-0.75, extent2[2]-0.4], width=3, height=2.1,
                              edgecolor='red', facecolor='none',
                              linewidth=1.5, transform=ccrs.PlateCarree(), zorder=3)
ax_map.add_patch(zoom_box2)
ax_map.text(extent2[0]-2.2, extent2[3]-0.4, "b", fontsize=fsize1, color='red', transform=ccrs.PlateCarree())
ax_inset2.text(extent2[0]+0.02, extent2[3]-0.1, "b", fontsize=fsize1, transform=ccrs.PlateCarree())

# Define KAN transect inset map
extent3 = [-51.1, -46.9, 66.88, 67.41]
ax_inset3 = fig.add_axes([0.3, -0.187, 0.69, 0.69], projection=ccrs.Mercator())
ax_inset3.set_extent(extent3, crs=ccrs.PlateCarree())
ax_inset3.add_feature(coastline, zorder=0)
ax_inset3.add_feature(ice_margin, zorder=1)
zoom_box3 = mpatches.Rectangle(xy=[extent3[0]-0.5, extent3[2]-0.5], width=5, height=1.2,
                              edgecolor='red', facecolor='none',
                              linewidth=1.5, transform=ccrs.PlateCarree(), zorder=3)
ax_map.add_patch(zoom_box3)
ax_map.text(extent3[0]-1.8, extent3[3]-0.2, "d", fontsize=fsize1, color='red', transform=ccrs.PlateCarree())
ax_inset3.text(extent3[0]+0.01, extent3[3]-0.06, "d", fontsize=fsize1, transform=ccrs.PlateCarree())

# Define THU transect inset map
extent4 = [-68.32, -68.08, 76.35, 76.45]
ax_inset4 = fig.add_axes([0.03, 0.5224, 0.25, 0.25], projection=ccrs.Mercator())
ax_inset4.set_extent(extent4, crs=ccrs.PlateCarree())
ax_inset4.add_feature(coastline, zorder=0)
ax_inset4.add_feature(ice_margin, zorder=1)
zoom_box4 = mpatches.Rectangle(xy=[extent4[0]-0.65, extent4[2]-0.65], width=2, height=1.1,
                              edgecolor='red', facecolor='none',
                              linewidth=1.5, transform=ccrs.PlateCarree(), zorder=3)
ax_map.add_patch(zoom_box4)
ax_map.text(extent4[0]-3, extent4[3]-0.1, "a", fontsize=fsize1, color='red', transform=ccrs.PlateCarree())
ax_inset4.text(extent4[0]+0.005, extent4[3]-0.005, "a", fontsize=fsize1, transform=ccrs.PlateCarree())

# Plot station location
for s in range(len(stations)):

    # Open file as xarray dataset
    inf = "https://thredds.geus.dk/thredds/dodsC/aws/l3sites/netcdf/month/" + stations[s] + "_month.nc"
    print('Opening '+inf)
    ds = xr.open_dataset(inf)

    # Determine point style based on project
    if ds.attrs['project'].lower() == 'gc-net':
        style='s'
        color=gcnet_color
    elif ds.attrs['project'].lower() == 'glaciobasis':
        style='^'
        color=glaciobasis_color
    else:
        if stations[s]=='KAN_U':
            style = 's'
            color = gcnet_color
        else:
            style='o'
            color=promice_color

    # Plot station location on map
    lat = float(ds.latitude)
    lon = float(ds.longitude)
    ax_map.plot(lon, lat, style, markeredgecolor='k', transform=ccrs.PlateCarree(),
                label=ds.attrs['project'].upper(), color=color, markersize=pt_size, zorder=3)

    # Reassign name for labelling
    station_name = stations[s].replace('_', '-')
    # Useful print statements
    print(station_name)
    print(ds.attrs['project'])
    print(lon)
    print(lat)
    print(list(ds['time'].values)[-1])

    # Plot in QAS inset map
    if extent1[0] <= lon <= extent1[1] and extent1[2] <= lat <= extent1[3]:
        print('Plotting location to ax_inset1')
        ax_inset1.plot(lon, lat, style, markeredgecolor='k', transform=ccrs.PlateCarree(),
                       color=color, markersize=pt_size)
        ax_inset1.text(lon+0.04, lat-0.01, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())

    # Plot in NUK inset map
    elif extent2[0] <= lon <= extent2[1] and extent2[2] <= lat <= extent2[3]:
        print('Plotting location to ax_inset2')
        ax_inset2.plot(lon, lat, style, markeredgecolor='k', transform=ccrs.PlateCarree(),
                       color=color, markersize=pt_size)
        if stations[s]=="NUK_L":
            ax_inset2.text(lon-0.35, lat-0.12, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s]=="NUK_K":
            ax_inset2.text(lon, lat+0.08, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s]=="NUK_U":
            ax_inset2.text(lon-0.65, lat+0.15, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        else:
            ax_inset2.text(lon-0.3, lat+0.08, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())

    # Plot in KAN inset map
    elif extent3[0] <= lon <= extent3[1] and extent3[2] <= lat <= extent3[3]:
        print('Plotting location to ax_inset2')
        ax_inset3.plot(lon, lat, style, markeredgecolor='k', transform=ccrs.PlateCarree(),
                       color=color, markersize=pt_size)
        if stations[s] =="KAN_U":
            ax_inset3.text(lon-0.4, lat+0.04, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s]  == "KAN_M":
            ax_inset3.text(lon - 0.3, lat+0.05, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s]  == "KAN_L":
            ax_inset3.text(lon-0.3, lat-0.1, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s]  == "KAN_B":
            ax_inset3.text(lon-0.55, lat-0.02, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        else: #KAN_T
            ax_inset3.text(lon-0.2, lat + 0.04, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())

    # Plot in THU inset map
    elif extent4[0] <= lon <= extent4[1] and extent4[2] <= lat <= extent4[3]:
        print('Plotting location to ax_inset3')
        ax_inset4.plot(lon, lat, style, markeredgecolor='k', transform=ccrs.PlateCarree(), color=color,
                       markersize=pt_size)
        if stations[s] =="THU_L2":
            ax_inset4.text(lon-0.03, lat-0.008, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] =="THU_L":
            ax_inset4.text(lon-0.03, lat+0.005, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        else: #station_name=="THU_U:
            ax_inset4.text(lon-0.03, lat+0.005, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())

    # Define station names in main map
    else:

        if stations[s]=="KPC_U":
            ax_map.text(lon-10, lat-0.4, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "KPC_L":
            ax_map.text(lon+1.9, lat+0.2, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "SCO_U":
            ax_map.text(lon-6.5, lat+0.7, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s]== "SCO_L":
            ax_map.text(lon-1.5, lat-0.6, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s]== "UPE_U":
            ax_map.text(lon+0.9, lat-0.3, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s]== "UPE_L":
            ax_map.text(lon-6, lat-0.8, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s]== "TAS_A":
            ax_map.text(lon-4, lat-1.8, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s]== "TAS_L":
            ax_map.text(lon-4, lat-1.1, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s]== "TAS_U":
            ax_map.text(lon-4, lat-0.6, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "DY2" or stations[s] == "SDL" or stations[s] == "EGP" or stations[s] == "JAR":
            ax_map.text(lon-1.5, lat-0.7, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "NSE":
            ax_map.text(lon-1.1, lat+0.4, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "LYN":
            ax_map.text(lon-1.1, lat+0.5, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "SWC":
            ax_map.text(lon-2.3, lat+0.35, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "ZAC_U":
            ax_map.text(lon-6, lat+1.5, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "ZAC_L":
            ax_map.text(lon-6, lat+0.8, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "FRE":
            ax_map.text(lon+1.2, lat-0.5, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "ZAC_A":
            ax_map.text(lon+1.3, lat+0.1, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "LYN_T":
            ax_map.text(lon-3.2, lat-1, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "LYN_L":
            ax_map.text(lon-4, lat+0.15, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "SDM":
            ax_map.text(lon+0.8, lat-0.5, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif stations[s] == "JAR":
            ax_map.text(lon-1.5, lat-1.2, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        else:
            ax_map.text(lon+1.1, lat-0.5, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())

# Manually add Summit and Petermann stations from local files
# Open file as xarray dataset
infs = ["Summit_daily.csv", "PetermannGlacier_daily.csv", "PetermannELA_daily.csv"]
skip=[21, 20, 21]
names = ["SUM", "PET", "PET-ELA"]
for i in range(len(infs)):
    print('Opening '+infs[i])
    df = pd.read_csv(infs[i], skiprows=skip[i], header=0)
    style='s'
    color=gcnet_color
    lat = float(list(df['lat'])[-1])
    lon = float(list(df['lon'])[-1])
    ax_map.plot(lon, lat, style, markeredgecolor='k', transform=ccrs.PlateCarree(),
                label='GC-Net', color=color, markersize=pt_size, zorder=3)
    if names[i] == "PET":
        ax_map.text(lon+1.8, lat-0.2, names[i], fontsize=fsize2, transform=ccrs.PlateCarree())
    elif names[i] == "PET-ELA":
        ax_map.text(lon+1.1, lat-0.6, names[i], fontsize=fsize2, transform=ccrs.PlateCarree())
    else:
        ax_map.text(lon+1.1, lat-0.5, names[i], fontsize=fsize2, transform=ccrs.PlateCarree())
    print(names[i])
    print(lon)
    print(lat)


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
add_scalebar(ax_inset1, 10)
add_scalebar(ax_inset2, 40)
add_scalebar(ax_inset3, 20)
add_scalebar(ax_inset4, 2)

# Create manual symbols for legend
gcnet_color = "#004949"
promice_color = "#b66dff"
glaciobasis_color = "#db6d00"
pt_size=8

pt1 = Line2D([0], [0], label='GC-Net station', marker='s', markersize=pt_size,
         markeredgecolor='k', markerfacecolor=gcnet_color, linestyle='')
pt2 = Line2D([0], [0], label='PROMICE station', marker='o', markersize=pt_size,
         markeredgecolor='k', markerfacecolor=promice_color, linestyle='')
pt3 = Line2D([0], [0], label='GlacioBasis/Asiaq station', marker='^', markersize=pt_size,
         markeredgecolor='k', markerfacecolor=glaciobasis_color, linestyle='')
ax_map.legend(loc=2, handles=[pt1, pt2, pt3], fontsize=fsize3)

# Show/save
plt.subplots_adjust(wspace=0.2, hspace=0.1, left=0.3, right=0.99)
#plt.tight_layout()
#plt.show()
#plt.savefig('/home/pho/Desktop/promice_station_locations.pdf', dpi=600)
plt.savefig('/home/pho/Desktop/promice_station_locations.png', dpi=600)
