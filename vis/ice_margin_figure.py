#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Color-blind–friendly update
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

# =====================================================================
# 1. Define PROMICE stations
# =====================================================================

stations = [
    'KAN_B', 'KAN_L', 'KAN_M', 'KAN_T', 'KAN_U',
    'KPC_L', 'KPC_U',
    'MIT',
    'NUK_L', 'NUK_U',
    'QAS_L', 'QAS_M', 'QAS_U',
    'SCO_L', 'SCO_U',
    'TAS_A', 'TAS_L',
    'THU_L', 'THU_L2', 'THU_U',
    'UPE_L', 'UPE_U'
]

# =====================================================================
# 2. Color-blind–safe color palette
# =====================================================================
#  Paul Tol “Bright”
colors_by_group = {
    "KAN": "#4477AA",
    "KPC": "#EE6677",
    "MIT": "#228833",
    "NUK": "#CCBB44",
    "QAS": "#66CCEE",
    "SCO": "#AA3377",
    "TAS": "#BBBBBB",
    "THU": "#009988",
    "UPE": "#0072B2",
}

# Paul Tol "Muted" palette — 9 categorical colors
#colors_by_group = {
#    "KAN": "#332288",   # dark blue
#    "KPC": "#88CCEE",   # light cyan
#    "MIT": "#44AA99",   # teal/green
#    "NUK": "#117733",   # dark green
#    "QAS": "#999933",   # olive
#    "SCO": "#DDCC77",   # sand
#    "TAS": "#CC6677",   # rose
#    "THU": "#882255",   # wine / burgundy
#    "UPE": "#AA4499",   # purple-magenta
#}


# =====================================================================
# 3. Line styles by suffix
# =====================================================================
linestyles_by_suffix = {
    "_L": "-",
    "_M": "-.",
    "_U": "--",
    "_B": ":",
    "_T": ":",
    "_A": ":",
    "L2": (0, (3, 5, 1, 5)),  # custom pattern for THU_L2
}

def get_group(station):
    return station.split("_")[0]

def get_suffix(station):
    p = station.split("_", 1)
    return "_" + p[1] if len(p) > 1 else ""

# =====================================================================
# 4. Figure Layout
# =====================================================================

fig = plt.figure(figsize=(20, 10))
gs = gridspec.GridSpec(2, 2, width_ratios=[1, 2.5], height_ratios=[1, 1])
ax_map = plt.subplot(gs[:, 0], projection=ccrs.Stereographic(central_latitude=70, central_longitude=-42))
ax1 = plt.subplot(gs[0, 1])
ax2 = plt.subplot(gs[1, 1])

fsize1 = 20
fsize2 = 16
fsize3 = 12
fsize4 = 10

# =====================================================================
# 5. Map Layers
# =====================================================================

coastline = cfeature.NaturalEarthFeature(
    category='physical', name='land', scale='10m',
    edgecolor='darkgray', facecolor='lightgray'
)
ice_margin_50m = cfeature.NaturalEarthFeature(
    category='physical', name='glaciated_areas', scale='50m',
    edgecolor='darkgray', facecolor='white'
)
ice_margin_10m = cfeature.NaturalEarthFeature(
    category='physical', name='glaciated_areas', scale='10m',
    edgecolor='darkgray', facecolor='white'
)

ax_map.set_extent([-58, -25, 58.1, 85], crs=ccrs.PlateCarree())
ax_map.add_feature(coastline, zorder=0)
ax_map.add_feature(ice_margin_50m, zorder=1)

gls = ax_map.gridlines(draw_labels=True)
gls.bottom_labels = False
gls.left_labels = False
gls.xlabel_style = {'size': fsize4, 'color': '#787878'}
gls.ylabel_style = {'size': fsize4, 'color': '#787878'}

# =====================================================================
# 6. Inset Maps (unchanged)
# =====================================================================

extent1 = [-46.95, -46.45, 60.85, 61.35]
ax_inset1 = fig.add_axes([-0.07, 0.19, 0.3, 0.3], projection=ccrs.Mercator())
ax_inset1.set_extent(extent1, crs=ccrs.PlateCarree())
ax_inset1.add_feature(coastline, zorder=0)
ax_inset1.add_feature(ice_margin_10m, zorder=1)
zoom_box1 = mpatches.Rectangle([extent1[0]-0.75, extent1[2]-0.75], 2, 2.1,
                               edgecolor='red', facecolor='none',
                               linewidth=1.5, transform=ccrs.PlateCarree(), zorder=3)
ax_map.add_patch(zoom_box1)

extent2 = [-51.1, -46.9, 66.9, 67.4]
ax_inset2 = fig.add_axes([0.125, 0.02, 0.2, 0.2], projection=ccrs.Mercator())
ax_inset2.set_extent(extent2, crs=ccrs.PlateCarree())
ax_inset2.add_feature(coastline, zorder=0)
ax_inset2.add_feature(ice_margin_10m, zorder=1)
zoom_box2 = mpatches.Rectangle([extent2[0]-0.5, extent2[2]-0.5], 5, 1.2,
                               edgecolor='red', facecolor='none',
                               linewidth=1.5, transform=ccrs.PlateCarree(), zorder=3)
ax_map.add_patch(zoom_box2)

extent3 = [-68.3, -68.1, 76.35, 76.45]
ax_inset3 = fig.add_axes([-0.07, 0.50, 0.3, 0.3], projection=ccrs.Mercator())
ax_inset3.set_extent(extent3, crs=ccrs.PlateCarree())
ax_inset3.add_feature(coastline, zorder=0)
ax_inset3.add_feature(ice_margin_10m, zorder=1)
zoom_box3 = mpatches.Rectangle([extent3[0]-0.75, extent3[2]-0.4], 2, 1.1,
                               edgecolor='red', facecolor='none',
                               linewidth=1.5, transform=ccrs.PlateCarree(), zorder=3)
ax_map.add_patch(zoom_box3)

# =====================================================================
# 7. Updated Plotting Function
# =====================================================================

def plot_station(station_name, ax_temp, ax_cloud):
    # Determine color + line style
    group = get_group(station_name)
    suffix = get_suffix(station_name)

    color = colors_by_group.get(group, "#000000")
    style = linestyles_by_suffix.get(suffix, "-")

    # Load data
    url = f"https://thredds.geus.dk/thredds/dodsC/aws/l3sites/netcdf/month/{station_name}_month.nc"
    ds = xr.open_dataset(url)

    # Temperature
    ds["t_u"].plot(ax=ax_temp, color=color, linestyle=style, label=station_name)

    # Cloud cover (if present)
    try:
        ds["cc"].plot(ax=ax_cloud, color=color, linestyle=style, label=station_name)
    except:
        print(f"No cloud cover for {station_name}")

    # Map marker
    lat = float(ds.latitude)
    lon = float(ds.longitude)
    ax_map.plot(lon, lat, 'o', markersize=5,
                markeredgecolor='k', color=color,
                transform=ccrs.PlateCarree(), zorder=3)

    # Inset-map logic (unchanged)
    # -----------------------------------------------------------
    if extent1[0] <= lon <= extent1[1] and extent1[2] <= lat <= extent1[3]:
        ax_inset1.plot(lon, lat, 'o', color=color, markeredgecolor='k',
                       markersize=6, transform=ccrs.PlateCarree())
        ax_inset1.text(lon+0.05, lat-0.01, station_name, fontsize=fsize2,
                       transform=ccrs.PlateCarree())

    elif extent2[0] <= lon <= extent2[1] and extent2[2] <= lat <= extent2[3]:
        ax_inset2.plot(lon, lat, 'o', color=color, markeredgecolor='k',
                       markersize=6, transform=ccrs.PlateCarree())

        # original manual label positions preserved
        if station_name == "KAN_U":
            ax_inset2.text(lon-0.8, lat+0.04, station_name, fontsize=fsize2,
                           transform=ccrs.PlateCarree())
        elif station_name == "KAN_M":
            ax_inset2.text(lon-0.3, lat+0.05, station_name, fontsize=fsize2,
                           transform=ccrs.PlateCarree())
        elif station_name == "KAN_L":
            ax_inset2.text(lon-0.3, lat-0.1, station_name, fontsize=fsize2,
                           transform=ccrs.PlateCarree())
        elif station_name == "KAN_B":
            ax_inset2.text(lon-0.83, lat-0.02, station_name, fontsize=fsize2,
                           transform=ccrs.PlateCarree())
        else:
            ax_inset2.text(lon-0.2, lat+0.04, station_name, fontsize=fsize2,
                           transform=ccrs.PlateCarree())

    elif extent3[0] <= lon <= extent3[1] and extent3[2] <= lat <= extent3[3]:
        ax_inset3.plot(lon, lat, 'o', color=color, markeredgecolor='k',
                       markersize=6, transform=ccrs.PlateCarree())

        if station_name == "THU_L2":
            ax_inset3.text(lon-0.03, lat-0.01, station_name, fontsize=fsize2,
                           transform=ccrs.PlateCarree())
        elif station_name == "THU_L":
            ax_inset3.text(lon-0.03, lat+0.005, station_name, fontsize=fsize2,
                           transform=ccrs.PlateCarree())
        else:
            ax_inset3.text(lon-0.1, lat+0.005, station_name, fontsize=fsize2,
                           transform=ccrs.PlateCarree())

    else:
        # Main map labels unchanged
        if station_name == "KPC_U":
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
        else:
            ax_map.text(lon+1.1, lat-0.5, station_name, fontsize=fsize2, transform=ccrs.PlateCarree())

# =====================================================================
# 8. Run plotting loop
# =====================================================================

for s in stations:
    plot_station(s, ax1, ax2)

# =====================================================================
# 9. Axes formatting (unchanged except for legend)
# =====================================================================

for ax in [ax1, ax2]:
    ax.yaxis.grid(color='gray', linestyle='solid', linewidth=0.5)
    ax.xaxis.grid(color='gray', linestyle='solid', linewidth=0.5)
    ax.axvline(dt.date(2022, 8, 15), linewidth=10, color='#878787', alpha=0.3)
    ax.set_xlim([dt.datetime(2019,1,1), dt.datetime(2024,1,1)])
    ax.set_xticks([dt.datetime(y,1,1) for y in [2019, 2020, 2021, 2022, 2023, 2024]])

ax1.set_xticklabels([])
ax1.set_xlabel(None)
ax1.set_ylim([-30, 10])
ax1.set_yticks([-35,-30,-25,-20,-15,-10,-5,0,5,10,15])
ax1.set_yticklabels(['-35','','-25','','-15','','-5','','5','','15'], fontsize=fsize3)

ax2.set_xlabel("Datetime", fontsize=fsize2)
ax2.set_xticklabels(['2019','2020','2021','2022','2023','2024'], fontsize=fsize3, rotation=45)
ax2.set_ylim([0,1.0])
ax2.set_yticks([i/10 for i in range(11)])
ax2.set_yticklabels(['0.0','','0.2','','0.4','','0.6','','0.8','','1.0'], fontsize=fsize3)

ax1.text(dt.datetime(2022, 4, 15), -38.5, "August 2022", fontsize=fsize2, color='#878787')

# OPTIONAL: smaller legend with two columns
ax1.legend(loc=4, fontsize=fsize3, bbox_to_anchor=(1.15, -0.9), ncol=1)

ax1.set_ylabel("Air Temperature ($^\circ$C)", fontsize=fsize2)
ax2.set_ylabel("Cloud Cover (%)", fontsize=fsize2)

# =====================================================================
# 10. Scalebars (unchanged)
# =====================================================================
from cartopy.crs import TransverseMercator

def add_scalebar(ax, length=None, location=(0.5, 0.05), linewidth=1.5):
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]
    tmc = TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    if not length:
        length = (x1 - x0) / 5000
        ndim = int(np.floor(np.log10(length)))
        length = round(length, -ndim)
        def scale_number(x):
            if str(x)[0] in ['1','2','5']: return int(x)
            else: return scale_number(x - 10**ndim)
        length = scale_number(length)

    bar_xs = [sbx - length*500, sbx + length*500]
    ax.plot(bar_xs, [sby, sby], transform=tmc, color='#787878', linewidth=linewidth)
    ax.text(sbx, sby+0.1, f"{length} km", fontsize=fsize3, color='#787878',
            transform=tmc, ha='center', va='bottom')

add_scalebar(ax_map, 400, (0.5,0.02))
add_scalebar(ax_inset1, 10)
add_scalebar(ax_inset2, 20)
add_scalebar(ax_inset3, 2)

# =====================================================================
# 11. Annotate main figure panels
# =====================================================================

ax_map.text(-95, 80., "a)", fontsize=fsize1, transform=ccrs.PlateCarree())
ax_map.text(-70.6, 76.9, "i", fontsize=fsize2, color='red', transform=ccrs.PlateCarree())
ax_map.text(-49.9, 61.0, "ii", fontsize=fsize2, color='red', transform=ccrs.PlateCarree())
ax_map.text(-54.7, 67.34, "iii", fontsize=fsize2, color='red', transform=ccrs.PlateCarree())
ax1.text(dt.datetime(2019,1,15), 11, "b)", fontsize=fsize1)
ax2.text(dt.datetime(2019,1,15), 0.93, "c)", fontsize=fsize1)

ax_inset1.text(extent1[0]+0.01, extent1[3]-0.05, "ii)", fontsize=fsize1, transform=ccrs.PlateCarree())
ax_inset2.text(extent2[0]+0.03, extent2[3]-0.11, "iii)", fontsize=fsize1, transform=ccrs.PlateCarree())
ax_inset3.text(extent3[0]+0.005, extent3[3]-0.01, "i)", fontsize=fsize1, transform=ccrs.PlateCarree())

# =====================================================================
# 12. Save figure
# =====================================================================

plt.subplots_adjust(wspace=0.2, hspace=0.1)
#plt.show()
plt.savefig("out/promice_temp_cloud_paul_tol_bright_colorblind_palette.png", dpi=300)
