#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 08:34:09 2022

@author: pho
"""
import xarray as xr
import pandas as pd
import datetime
import matplotlib.pyplot as plt

infile = '/home/pho/Downloads/SDM_day.csv'
    
df = pd.read_csv(infile, comment='#', index_col=0,
                     na_values=['','nan'], parse_dates=True,
                     sep=',', 
                     skip_blank_lines=True)        

# plt.figure(figsize=(w, h), dpi=d)
fig, ax = plt.subplots(9, 1, figsize=(10,10), sharex=True)

fsize1 = 9
fsize2 = 8
fsize3 = 10
fsize4 = 14
fsty = 'arial'
pad=1.
lloc=4
lw=1

# First plot
df['t_l'].plot(ax=ax[0], c='#3F8BD7',  linewidth=lw, linestyle='-', label='Lower')
df['t_u'].plot(ax=ax[0], c='#3FC0D7', linestyle='-', linewidth=lw, label='Upper')
# df['t_surf'].scatter(ax=ax[0], linestyle='-', label='Air temperature (at surface)')
ax[0].set_ylabel('Air temp.\n$^\circ$C', fontsize=fsize1)
ax[0].set_ylim([-50, 10])
ax[0].set_yticks([-50,-30,-10, 10])
ax[0].set_yticklabels(['','-30','10',''])
ax[0].legend(loc=lloc, fontsize=fsize2)

# Second plot
df['p_l'].plot(ax=ax[1], c='#267E56', linewidth=lw, label='Lower')
df['p_u'].plot(ax=ax[1], c='#39B87E', linewidth=lw, label='Upper')
ax[1].set_ylabel('Air press.\nhPa', fontsize=fsize1, labelpad=pad)
ax[1].set_ylim([650, 750])
ax[1].set_yticks([600,650, 700, 750])
ax[1].set_yticklabels(['','650','700',''])
ax[1].legend(loc=lloc, fontsize=fsize2)

# Third plot
df['rh_l'].plot(ax=ax[2], c='#BC3737', linewidth=lw, label='Lower')
df['rh_u'].plot(ax=ax[2], c ='#D78F3F', linewidth=lw, label='Upper')
ax[2].set_ylabel('Rel. humid.\n%', fontsize=fsize1)
ax[2].set_ylim([25, 100])
ax[2].set_yticks([25,50,75,100])
ax[2].set_yticklabels(['','50','75',''])
ax[2].legend(loc=lloc, fontsize=fsize2)

# Fourh plotax[3].legend(loc=1, fontsize=fsize2)
df['precip_l'].plot(ax=ax[3], c='#B8B8B8', linewidth=lw, label='Lower')
df['precip_u'].plot(ax=ax[3], c='#6E6E6E', linewidth=lw, label='Upper')
ax[3].set_ylabel('Precip. mm', fontsize=fsize1, labelpad=pad)
ax[3].set_ylim([0, 9000])
ax[3].set_yticks([0,3000,6000,9000])
ax[3].set_yticklabels(['','3000','6000',''])
ax[3].yaxis.set_label_coords(-0.07, 0.5)
ax[3].legend(loc=lloc, fontsize=fsize2)

# Fifth plot
df['wspd_l'].plot(ax=ax[4], c='#98E023', linewidth=lw, label='Lower')
df['wspd_u'].plot(ax=ax[4], c='#DDE023', linewidth=lw, label='Upper')
ax[4].set_ylabel('Wind spd.\nm s-1', fontsize=fsize1)
ax[4].set_ylim([0, 21])
ax[4].set_yticks([0,7,14,21])
ax[4].set_yticklabels(['','7','14',''])
ax[4].legend(loc=lloc, fontsize=fsize2)

# Sixth plot
df['wdir_l'].plot(ax=ax[5], c='#00A714', linewidth=lw, label='Lower')
df['wdir_u'].plot(ax=ax[5], c='#7FA383', linewidth=lw, label='Upper')
ax[5].set_ylabel('Wind dir. $^\circ$', fontsize=fsize1, labelpad=pad)
ax[5].set_ylim([0, 360])
ax[5].set_yticks([0,120,240,360])
ax[5].set_yticklabels(['','120','240',''])
ax[5].yaxis.set_label_coords(-0.07, 0.5)
ax[5].legend(loc=lloc, fontsize=fsize2)

# Fourth plot
clrs = [None, '#FF0018', '#FFA52C', '#FFFF41', '#008018','#0000F9', '#86007D', '#5BCEFA', '#F5A9B8', '#FFF200', '#8548A6']
for i in list(range(1,11)):
    n = 't_i_' + str(i)
    df[n].plot(ax=ax[6], c=clrs[i], linewidth=lw, label=str(i) + ' m')
ax[6].set_ylabel('Subsurf.\ntemp. $^\circ$C', fontsize=fsize1)
ax[6].set_ylim([-25, 5])  
ax[6].set_yticks([-25,-15,-5,5])
ax[6].set_yticklabels(['','-15','-5','']) 
ax[6].legend(loc=lloc, ncol=2, fontsize=fsize2, bbox_to_anchor=(1.285, -0.07))

# Fifth plot
df['dsr_cor'].plot(ax=ax[7], c='#B7B8E1', linewidth=lw, label='Downwelling shortwave')
df['usr_cor'].plot(ax=ax[7], c='#393DDE', linewidth=lw, label='Upwelling shortwave')
df['dlr'].plot(ax=ax[7], c='#E1B7DE', linewidth=lw, label='Downwelling longwave')
df['ulr'].plot(ax=ax[7], c='#DF50D5', linewidth=lw, label='Upwelling longwave')
ax[7].set_ylabel('Radiation\nW m-2', fontsize=fsize1)
ax[7].set_ylim([-100, 500]) 
ax[7].set_yticks([-100,100,300,500])
ax[7].set_yticklabels(['','100','300',''])
ax[7].legend(loc=lloc, fontsize=fsize2, bbox_to_anchor=(1.33, -0.07))  


df['dlhf_l'].plot(ax=ax[8], c='#1A9BA1', linewidth=lw, label='Latent lower')
df['dlhf_u'].plot(ax=ax[8], c='#8FDDE1', linewidth=lw, label='Latent upper')
df['dshf_l'].plot(ax=ax[8], c='#785252', linewidth=lw, label='Sensible lower')
df['dshf_u'].plot(ax=ax[8], c='#F6D09D', linewidth=lw, label='Sensible upper')
ax[8].set_ylabel('Heat flux\nW m-2', fontsize=fsize1, labelpad=pad)
ax[8].set_ylim([-60, 60])   
ax[8].set_yticks([-60,-20,20,-60])
ax[8].set_yticklabels(['','-20','20',''])
ax[8].yaxis.set_label_coords(-0.054, 0.5)
ax[8].legend(loc=lloc, fontsize=fsize2, bbox_to_anchor=(1.255, -0.07))

for a in ax:
    a.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
    a.xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)

    a1=a.twinx()
    lims = a.get_ylim()
    a1.set_ylim(lims)
    tx = a.get_yticks()
    lab = a.get_yticklabels()
    a1.set_yticks(tx)
    a1.set_yticklabels(lab, fontsize=fsize2)

    a.tick_params(labelsize=fsize2)    
    a1.tick_params(labelsize=fsize2)  
    
    a.set_xlim([datetime.date(2021, 7, 1), datetime.date(2023, 10, 1)])

    a.vlines(x=datetime.date(2022,1,1),ymin=lims[0], ymax=lims[1], linewidth=1, color='#636363')
    a.vlines(x=datetime.date(2023,1,1),ymin=lims[0], ymax=lims[1], linewidth=1, color='#636363')
    
ax[8].set_xlabel('', fontsize=0)
ax[8].set_xticklabels(['Jul','Oct','Jan 2022','Apr','Jul','Oct','Jan 2023','Apr','Jul','Oct'], fontsize=fsize2)
ax[8].tick_params(axis='x', which='minor', bottom=False)

a1 = ax[0].twiny()
a1.set_xlim([datetime.date(2021, 7, 1), datetime.date(2023, 10, 1)])
a1.set_xlabel('', fontsize=0)
a1.tick_params(axis='x', which='minor', bottom=False)
# xticks = ax[8].get_xticks()
# a1.set_xticks(xticks)
a1.set_xticklabels(['Jul','Oct','Jan 2022','Apr','Jul','Oct','Jan 2023','Apr','Jul','Oct'], fontsize=fsize2)

plt.subplots_adjust(wspace=1,hspace=0, left=0.1, right=0.75)
# ax[8].text(0.25, -0.6, '2021', fontsize=fsize3, horizontalalignment='center', transform=ax[8].transAxes)
# ax[8].text(0.75, -0.6, '2022', fontsize=fsize3, horizontalalignment='center', transform=ax[8].transAxes)

props = dict(boxstyle='round', facecolor='#CAA84F', alpha=0.3)
ax[0].text(1.195, 1.1, 'SDM', fontsize=fsize4, horizontalalignment='center', 
           bbox=props, transform=ax[0].transAxes)

newax = fig.add_axes([0.71,0.62,0.24,0.24], anchor='NE', zorder=1)
im = plt.imread('/home/pho/Downloads/SDM 2021 06 21a GEUS AWS J Box.jpg')
newax.imshow(im)
newax.axis('off')

props = dict(boxstyle='round', facecolor='#FFFFFF', edgecolor='#DFDFDF', alpha=0.8)
ax[0].text(1.2, -3.8, 'Active since: June 2021\n\nPosition: 63.15, -44.82\n\nStation design: Two-boom\n\nNr. transmissions: 20.000\n\nData type: RAW/TX\n\nLast visit: 2023-06-11', fontsize=fsize2, horizontalalignment='center', 
           bbox=props, transform=ax[0].transAxes)

plt.savefig('/home/pho/Desktop/SDM_data.jpg', dpi=300)
