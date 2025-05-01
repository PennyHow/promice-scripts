#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Penelope How, pho@geus.dk
"""

import datetime as dt
import xarray as xr
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.geodesic import Geodesic

# Prime plot layout
fig = plt.figure(figsize=(20, 10))
gs = gridspec.GridSpec(2, 2, width_ratios=[1, 2.5], height_ratios=[1, 1])
ax_map = plt.subplot(gs[:, 0], projection=ccrs.Stereographic(central_latitude=70, central_longitude=-42))
ax1 = plt.subplot(gs[0, 1])
ax2 = plt.subplot(gs[1, 1])#, sharex=ax1)
fsize1=20
fsize2=16
fsize3=12
fsize4=10

# Define PROMICE stations
stations = ['KAN_B', 'KAN_L', 'KAN_M', 'KAN_T', 'KAN_U',
            'KPC_L', 'KPC_U',
            'MIT',
            'NUK_L', 'NUK_U',
            'QAS_L', 'QAS_M', 'QAS_U',
            'SCO_L', 'SCO_U',
            'TAS_A', 'TAS_L',
            'THU_L', 'THU_L2', 'THU_U',
            'UPE_L', 'UPE_U']

# Define colour ramp
#https://stackoverflow.com/questions/65013406/how-to-generate-30-distinct-colors-that-are-color-blind-friendly
colors = ["#004949", "#009292", "#ff6db6", "#ffb6db",
"#490092", "#006ddb", "#b66dff", "#6db6ff", "#b6dbff",
"#920000", "#924900", "#db6d00", "#24ff24"]
colors=colors+colors

# Define map layers
coastline = cfeature.NaturalEarthFeature(
    category='physical',
    name='land',
    scale='10m',
    edgecolor='darkgray',
    facecolor='lightgray'
)
ice_margin_50m = cfeature.NaturalEarthFeature(
    category='physical',
    name='glaciated_areas',
    scale='50m',        #10m, 50m or 110m
    edgecolor='darkgray',
    facecolor='white'
)
ice_margin_10m = cfeature.NaturalEarthFeature(
    category='physical',
    name='glaciated_areas',
    scale='10m',        #10m, 50m or 110m
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
extent1 = [-46.95, -46.45, 60.85, 61.35]
ax_inset1 = fig.add_axes([-0.07, 0.19, 0.3, 0.3], projection=ccrs.Mercator())
ax_inset1.set_extent(extent1, crs=ccrs.PlateCarree())
ax_inset1.add_feature(coastline, zorder=0)
ax_inset1.add_feature(ice_margin_10m, zorder=1)
zoom_box1 = mpatches.Rectangle(xy=[extent1[0]-0.75, extent1[2]-0.75], width=2, height=2.1,
                              edgecolor='red', facecolor='none',
                              linewidth=1.5, transform=ccrs.PlateCarree(), zorder=3)
ax_map.add_patch(zoom_box1)

# Define KAN transect inset map
extent2 = [-51.1, -46.9, 66.9, 67.4]
ax_inset2 = fig.add_axes([0.125, 0.02, 0.2, 0.2], projection=ccrs.Mercator())
ax_inset2.set_extent(extent2, crs=ccrs.PlateCarree())
ax_inset2.add_feature(coastline, zorder=0)
ax_inset2.add_feature(ice_margin_10m, zorder=1)
zoom_box2 = mpatches.Rectangle(xy=[extent2[0]-0.5, extent2[2]-0.5], width=5, height=1.2,
                              edgecolor='red', facecolor='none',
                              linewidth=1.5, transform=ccrs.PlateCarree(), zorder=3)
ax_map.add_patch(zoom_box2)

# Define THU inset map
extent3 = [-68.3, -68.1, 76.35, 76.45]
ax_inset3 = fig.add_axes([-0.07, 0.50, 0.3, 0.3], projection=ccrs.Mercator())
ax_inset3.set_extent(extent3, crs=ccrs.PlateCarree())
ax_inset3.add_feature(coastline, zorder=0)
ax_inset3.add_feature(ice_margin_10m, zorder=1)
zoom_box3 = mpatches.Rectangle(xy=[extent3[0]-0.75, extent3[2]-0.4], width=2, height=1.1,
                              edgecolor='red', facecolor='none',
                              linewidth=1.5, transform=ccrs.PlateCarree(), zorder=3)
ax_map.add_patch(zoom_box3)

# Plotting function
def plot(station_name, style, a1, a2, col):
    # Open file as xarray dataset
    inf = "https://thredds.geus.dk/thredds/dodsC/aws/l3sites/netcdf/month/" + station_name + "_month.nc"
    ds = xr.open_dataset(inf)

    # Plot temperature and cloud cover
    ds['t_u'].plot(ax=a1, color=col, linestyle=style, label=station_name)
    ds['cc'].plot(ax=a2, color=col, linestyle=style, label=station_name)

    # Plot station location on map
    lat = float(ds.latitude)
    lon = float(ds.longitude)
    ax_map.plot(lon, lat, 'o', markeredgecolor='k', transform=ccrs.PlateCarree(), label=station_name, color=col,
                markersize=5, zorder=3)

    # Useful print statements
    print(station_name)
    print(lon)
    print(lat)
    print(list(ds['time'].values)[-1])

    # Plot in QAS inset map
    if extent1[0] <= lon <= extent1[1] and extent1[2] <= lat <= extent1[3]:
        print('Plotting location to ax_inset1')
        ax_inset1.plot(lon, lat, 'o', markeredgecolor='k', transform=ccrs.PlateCarree(), color=col, markersize=6)
        ax_inset1.text(lon+0.05, lat-0.01, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())

    # Plot in KAN inset map
    elif extent2[0] <= lon <= extent2[1] and extent2[2] <= lat <= extent2[3]:
        print('Plotting location to ax_inset2')
        ax_inset2.plot(lon, lat, 'o', markeredgecolor='k', transform=ccrs.PlateCarree(), color=col, markersize=6)
        if station_name=="KAN_U":
            ax_inset2.text(lon-0.8, lat+0.04, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif station_name == "KAN_M":
            ax_inset2.text(lon - 0.3, lat+0.05, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif station_name == "KAN_L":
            ax_inset2.text(lon-0.3, lat-0.1, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif station_name == "KAN_B":
            ax_inset2.text(lon-0.83, lat-0.02, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        else: #KAN_T
            ax_inset2.text(lon-0.2, lat + 0.04, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())

    # Plot in THU inset map
    elif extent3[0] <= lon <= extent3[1] and extent3[2] <= lat <= extent3[3]:
        print('Plotting location to ax_inset3')
        ax_inset3.plot(lon, lat, 'o', markeredgecolor='k', transform=ccrs.PlateCarree(), color=col, markersize=6)
        if station_name=="THU_L2":
            ax_inset3.text(lon-0.03, lat-0.01, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif station_name=="THU_L":
            ax_inset3.text(lon-0.03, lat+0.005, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        else: #station_name=="THU_U:
            ax_inset3.text(lon-0.1, lat+0.005, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())

    # Define station names in main map
    else:
        if station_name=="KPC_U":
            ax_map.text(lon-10, lat-0.8, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif station_name == "KPC_L":
            ax_map.text(lon+1.9, lat+0.2, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif station_name == "SCO_U":
            ax_map.text(lon-7.6, lat+1., station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif station_name == "SCO_L":
            ax_map.text(lon-7.3, lat-0.9, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif station_name == "UPE_U":
            ax_map.text(lon+0.9, lat-0.2, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif station_name == "UPE_L":
            ax_map.text(lon-11, lat-0.8, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif station_name == "TAS_A":
            ax_map.text(lon-3, lat+1, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif station_name == "TAS_L":
            ax_map.text(lon-3.2, lat-1.5, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif station_name == "NUK_U":
            ax_map.text(lon-6, lat+0.5, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        elif station_name == "NUK_L":
            ax_map.text(lon-7, lat-1.59, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())
        else: # MIT
            ax_map.text(lon+1.1, lat-0.5, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())

# Apply plotting function to all stations
for s in range(len(stations))[0:13]:
    plot(stations[s], '-', ax1, ax2, colors[s])
for s in range(len(stations))[13:]:
    plot(stations[s], '--', ax1, ax2, colors[s])

# Plot customization
for ax in [ax1, ax2]:
    ax.yaxis.grid(color='gray', linestyle='solid', linewidth=0.5)
    ax.xaxis.grid(color='gray', linestyle='solid', linewidth=0.5)
    # ax.set_xticks(ticks)
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.tick_params(axis='x', which='major', bottom=False)
    ax.axvline(dt.date(2022, 8, 15), linewidth=10, color='#878787', alpha=0.3)
    ax.set_xlim([dt.datetime(2019,1,1), dt.datetime(2024,1,1)])
    ax.set_xticks([dt.datetime(2019,1,1), dt.datetime(2020,1,1),
                   dt.datetime(2021,1,1), dt.datetime(2022,1,1),
                   dt.datetime(2023,1,1), dt.datetime(2024,1,1)])

ax1.set_xlabel(None)
ax1.set_xticklabels([])
ax2.set_xlabel("Datetime", fontsize=fsize2)
ax2.set_xticklabels(['2019','2020','2021','2022','2023','2024'], fontsize=fsize3, rotation=45)
ax1.text(dt.datetime(2022, 4, 15), -38.5, "August 2022", color='#878787', fontsize=fsize2)

ax1.set_ylim([-30, 10])
ax1.set_yticks([-35,-30,-25,-20,-15,-10,-5,0,5,10,15])
#ax1.set_yticklabels(['','-30','','-20','','-10','','0','','10',''],fontsize=fsize3)
ax1.set_yticklabels(['-35','','-25','','-15','','-5','','5','','15'],fontsize=fsize3)
ax2.set_ylim([0, 1.0])
ax2.set_yticks([0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
ax2.set_yticklabels(['0.0','','0.2','','0.4','','0.6','','0.8','','1.0'], fontsize=fsize3)
ax1.legend(loc=4, fontsize=fsize3, bbox_to_anchor=(1.15, -0.9))
ax1.set_ylabel("Air Temperature ($^\circ$C)", fontsize=fsize2)
ax2.set_ylabel("Cloud Cover (%)", fontsize=fsize2)

# Add scalebars to maps
import cartopy.crs as ccrs
import numpy as np

def add_scalebar(ax, length=None, location=(0.5, 0.05), linewidth=1.5):
    #Get the limits of the axis in lat long
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    #Make tmc horizontally centred on the middle of the map,
    #vertically at scale bar location
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]
    tmc = ccrs.TransverseMercator(sbllx, sblly)
    #Get the extent of the plotted area in coordinates in metres
    x0, x1, y0, y1 = ax.get_extent(tmc)
    #Turn the specified scalebar location into coordinates in metres
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    #Calculate a scale bar length if none has been given
    if not length:
        length = (x1 - x0) / 5000 #in km
        ndim = int(np.floor(np.log10(length))) #number of digits in number
        length = round(length, -ndim) #round to 1sf
        #Returns numbers starting with the list
        def scale_number(x):
            if str(x)[0] in ['1', '2', '5']: return int(x)
            else: return scale_number(x - 10 ** ndim)
        length = scale_number(length)

    #Generate the x coordinate for the ends of the scalebar
    bar_xs = [sbx - length * 500, sbx + length * 500]
    #Plot the scalebar
    ax.plot(bar_xs, [sby, sby], transform=tmc, color='#787878', linewidth=linewidth)
    #Plot the scalebar label
    ax.text(sbx, sby+0.1, str(length)+' km', color='#787878', fontsize=fsize3, transform=tmc,
            horizontalalignment='center', verticalalignment='bottom')

add_scalebar(ax_map, 400, (0.5, 0.02))
add_scalebar(ax_inset1, 10)
add_scalebar(ax_inset2, 20)
add_scalebar(ax_inset3, 2)

# Add figure numbering
ax_map.text(-95, 80., "a", fontsize=fsize1, transform=ccrs.PlateCarree())
ax_map.text(-70.6, 76.9, "i", fontsize=fsize2, color='red', transform=ccrs.PlateCarree())
ax_map.text(-49.9, 61.0, "ii", fontsize=fsize2, color='red', transform=ccrs.PlateCarree())
ax_map.text(-54.7, 67.34, "iii", fontsize=fsize2, color='red', transform=ccrs.PlateCarree())
ax1.text(dt.datetime(2019,1,15), 11, "b", fontsize=fsize1)
ax2.text(dt.datetime(2019,1,15), 0.93, "c", fontsize=fsize1)
ax_inset1.text(extent1[0]+0.01, extent1[3]-0.05, "ii", fontsize=fsize1, transform=ccrs.PlateCarree())
ax_inset2.text(extent2[0]+0.03, extent2[3]-0.11, "iii", fontsize=fsize1, transform=ccrs.PlateCarree())
ax_inset3.text(extent3[0]+0.005, extent3[3]-0.01, "i", fontsize=fsize1, transform=ccrs.PlateCarree())

# Show/save
plt.subplots_adjust(wspace=0.2, hspace=0.1)#, left=0.1, right=0.75)
#plt.tight_layout()
plt.show()
#plt.savefig('/home/pho/Desktop/promice_temp_cloud.png', dpi=300)
