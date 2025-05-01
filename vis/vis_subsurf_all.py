#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:15:18 2024

@author: pho
"""

import glob
import xarray as xr
import pandas as pd
import datetime, sys
import matplotlib.pyplot as plt

infile = [
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/CEN1/CEN1_day.csv',
    'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/CEN2/CEN2_day.csv'],
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/HUM/HUM_day.csv'],
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/NEM/NEM_day.csv'],
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_L/THU_L_day.csv',
    'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_L2/THU_L2_day.csv'],
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_U/THU_U_day.csv',
    'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_U2/THU_U2_day.csv']
    ]

all_names = []
dfs = []
for inf in infile: 
    if len(inf)>1:
        all_df = []
        names = []
        for f in range(len(inf)):
            all_df.append(pd.read_csv(inf[f], comment='#', index_col=0,
                                      na_values=['','nan'], parse_dates=True,
                                      sep=',', 
                                      skip_blank_lines=True))    
            names.append(inf[f].split('/')[-1].split('_day')[0])
        name = names[0]+' '+names[1]
        df = pd.concat(all_df)
    else:        
        name = inf[0].split('/')[-1].split('_day')[0]
        df = pd.read_csv(inf[0], comment='#', index_col=0,
                             na_values=['','nan'], parse_dates=True,
                             sep=',', 
                             skip_blank_lines=True)   

    print('Loaded '+name)
    all_names.append(name)
    dfs.append(df)


# plt.figure(figsize=(w, h), dpi=d)
fig, ax = plt.subplots(5, 1, figsize=(10,10), sharex=True)
fsize1 = 9
fsize2 = 10
fsize3 = 12
fsize4 = 14
fsty = 'arial'
pad=1.
lloc=4
lw=1

for i in range(len(dfs)):

    # Fourth plot
    clrs = [None, '#FF0018', '#FFA52C', '#FFFF41', '#008018','#0000F9', '#86007D', '#5BCEFA', '#F5A9B8', '#FFF200', '#8548A6']
    for r in list(range(1,11)):
        n = 't_i_' + str(r)
        if n in dfs[i]:
            dfs[i][n].plot(ax=ax[i], c=clrs[r], linewidth=lw, label= str(r) + ' m subsurf. temp.')
    ax[i].set_ylim([-30, 10])  
    ax[i].set_yticks([-30,-20,-10,0,10])
    if i == range(len(dfs))[0]:
        ax[i].set_yticklabels(['-30','-20','-10','0','10']) 
    else:
        ax[i].set_yticklabels(['-30','-20','-10','0','']) 
    # ax[i].legend(loc=lloc, ncol=2, fontsize=fsize2, bbox_to_anchor=(1.285, -0.07))
    ax[i].set_xlim([datetime.date(2021,1,1), datetime.date(2024,1,1)])

    props = dict(boxstyle='round', facecolor='#FFEAB0', alpha=0.7)
    ax[i].text(datetime.date(2021,1,20), 3, all_names[i], fontsize=fsize2, 
           horizontalalignment='left', bbox=props)#, transform=ax[2].transAxes)
    ax[i].set_xlabel('', fontsize=0)


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

    a.tick_params(which='both', labelsize=fsize2)    
    a1.tick_params(which='both', labelsize=fsize2)  
    
ax[1].legend(bbox_to_anchor=(0.5, -3.7), loc='center', ncol=3)    
    
    # for i in list(range(df.index[0].date().year,df.index[-1].date().year)):
    #     a.vlines(x=datetime.date(i,1,1),ymin=lims[0], ymax=lims[1], linewidth=1, color='#636363')

fig.text(0.06, 0.5, 'Subsurface temperature $^\circ$C', va='center', rotation='vertical', fontsize=fsize3)
fig.text(0.94, 0.5, 'Subsurface temperature $^\circ$C', va='center', rotation=270, fontsize=fsize3)

# # First plot
# if 't_l' in df:
#     df['t_l'].plot(ax=ax[0], c='#3F8BD7',  linewidth=lw, linestyle='-', label='Lower')
# df['t_u'].plot(ax=ax[0], c='#3FC0D7', linestyle='-', linewidth=lw, label='Upper')
# # df['t_surf'].scatter(ax=ax[0], linestyle='-', label='Air temperature (at surface)')
# ax[0].set_ylabel('Air temp.\n$^\circ$C', fontsize=fsize1)
# ax[0].set_ylim([-50, 10])
# ax[0].set_yticks([-50,-30,-10, 10])
# ax[0].set_yticklabels(['','-30','10',''])import glob
# import xarray as xr
# import pandas as pd
# import datetime, sys
# import matplotlib.pyplot as plt
# if 't_l' in df:
#     ax[0].legend(loc=lloc, fontsize=fsize2)

# # Second plot
# if 'p_l' in df:
#     df['p_l'].plot(ax=ax[1], c='#267E56', linewidth=lw, label='Lower')
# df['p_u'].plot(ax=ax[1], c='#39B87E', linewidth=lw, label='Upper')
# ax[1].set_ylabel('Air press.\nhPa', fontsize=fsize1, labelpad=pad)
# ax[1].set_ylim([700, 1150])
# ax[1].set_yticks([700, 850, 1000, 1150])
# ax[1].set_yticklabels(['','850','1000',''])
# if 'p_l' in df:
#     ax[1].legend(loc=lloc, fontsize=fsize2)

# # Third plot
# if 'rh_l' in df:
#     df['rh_l'].plot(ax=ax[2], c='#BC3737', linewidth=lw, label='Lower')
# df['rh_u'].plot(ax=ax[2], c ='#D78F3F', linewidth=lw, label='Upper')
# ax[2].set_ylabel('Rel. humid.\n%', fontsize=fsize1)
# ax[2].set_ylim([25, 100])
# ax[2].set_yticks([25,50,75,100])
# ax[2].set_yticklabels(['','50','75',''])
# if 'rh_l' in df:
#     ax[2].legend(loc=lloc, fontsize=fsize2)

# # Fourh plotax[3].legend(loc=1, fontsize=fsize2)
# if 'precip_l' in df:
#     df['precip_l'].plot(ax=ax[3], c='#B8B8B8', linewidth=lw, label='Lower')
# df['precip_u'].plot(ax=ax[3], c='#6E6E6E', linewidth=lw, label='Upper')
# ax[3].set_ylabel('Precip. mm', fontsize=fsize1, labelpad=pad)
# ax[3].set_ylim([0, 9000])
# ax[3].set_yticks([0,3000,6000,9000])
# ax[3].set_yticklabels(['','3000','6000',''])
# ax[3].yaxis.set_label_coords(-0.07, 0.5)
# if 'precip_l' in df:
#     ax[3].legend(loc=lloc, fontsize=fsize2)

# # Fifth plot
# if 'wspd_l' in df:
#     df['wspd_l'].plot(ax=ax[4], c='#98E023', linewidth=lw, label='Lower')
# df['wspd_u'].plot(ax=ax[4], c='#DDE023', linewidth=lw, label='Upper')
# ax[4].set_ylabel('Wind spd.\nm s-1', fontsize=fsize1)
# ax[4].set_ylim([0, 21])
# ax[4].set_yticks([0,7,14,21])
# ax[4].set_yticklabels(['','7','14',''])
# if 'wspd_l' in df:   
#     ax[4].legend(loc=lloc, fontsize=fsize2)

# # Sixth plot
# if 'wdir_l' in df:
#     df['wdir_l'].plot(ax=ax[5], c='#00A714', linewidth=lw, label='Lower')
# df['wdir_u'].plot(ax=ax[5], c='#7FA383', linewidth=lw, label='Upper')
# ax[5].set_ylabel('Wind dir. $^\circ$', fontsize=fsize1, labelpad=pad)
# ax[5].set_ylim([0, 360])
# ax[5].set_yticks([0,120,240,360])
# ax[5].set_yticklabels(['','120','240',''])
# ax[5].yaxis.set_label_coords(-0.07, 0.5)
# if 'wdir_l' in df:
#     ax[5].legend(loc=lloc, fontsize=fsize2)



# # Fifth plot
# df['dsr_cor'].plot(ax=ax[7], c='#B7B8E1', linewidth=lw, label='Downwelling shortwave')
# df['usr_cor'].plot(ax=ax[7], c='#393DDE', linewidth=lw, label='Upwelling shortwave')
# df['dlr'].plot(ax=ax[7], c='#E1B7DE', linewidth=lw, label='Downwelling longwave')
# df['ulr'].plot(ax=ax[7], c='#DF50D5', linewidth=lw, label='Upwelling longwave')
# ax[7].set_ylabel('Radiation\nW m-2', fontsize=fsize1)
# ax[7].set_ylim([-100, 500]) 
# ax[7].set_yticks([-100,100,300,500])
# ax[7].set_yticklabels(['','100','300',''])
# ax[7].legend(loc=lloc, fontsize=fsize2, bbox_to_anchor=(1.33, -0.07))  
    
    
# if 'dlhf_l' in df:
#     df['dlhf_l'].plot(ax=ax[8], c='#1A9BA1', linewidth=lw, label='Latent lower')
# df['dlhf_u'].plot(ax=ax[8], c='#8FDDE1', linewidth=lw, label='Latent upper')
# if 'dshf_l' in df:
#     df['dshf_l'].plot(ax=ax[8], c='#785252', linewidth=lw, label='Sensible lower')
# df['dshf_u'].plot(ax=ax[8], c='#F6D09D', linewidth=lw, label='Sensible upper')
# ax[8].set_ylabel('Heat flux\nW m-2', fontsize=fsize1, labelpad=pad)
# ax[8].set_ylim([-60, 60])   
# ax[8].set_yticks([-60,-20,20,-60])
# ax[8].set_yticklabels(['','-20','20',''])
# ax[8].yaxis.set_label_coords(-0.054, 0.5)
# ax[8].legend(loc=lloc, fontsize=fsize2, bbox_to_anchor=(1.255, -0.07))

# for a in ax:
#     a.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
#     a.xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)

#     a1=a.twinx()
#     lims = a.get_ylim()
#     a1.set_ylim(lims)
#     tx = a.get_yticks()
#     lab = a.get_yticklabels()
#     a1.set_yticks(tx)
#     a1.set_yticklabels(lab, fontsize=fsize2)

#     a.tick_params(labelsize=fsize2)    
#     a1.tick_params(labelsize=fsize2)  
    
#     a.set_xlim([df.index[0].date(), df.index[-1].date()])

#     for i in list(range(df.index[0].date().year,df.index[-1].date().year)):
#         a.vlines(x=datetime.date(i,1,1),ymin=lims[0], ymax=lims[1], linewidth=1, color='#636363')

    
# ax[8].set_xlabel('', fontsize=0)
# # ax[8].set_xticks()
# # ax[8].set_xticklabels(['Jul','Oct','Jan 2022','Apr','Jul','Oct','Jan 2023','Apr','Jul','Oct'], fontsize=fsize2)
# ax[8].tick_params(axis='x', which='minor', bottom=False)

# # a1 = ax[0].twiny()
# # a1.set_xlim([df.index[0].date(), df.index[-1].date()])
# # a1.set_xlabel('', fontsize=0)
# # a1.tick_params(axis='x', which='minor', bottom=False)
# # xticks = ax[8].get_xticks()
# # a1.set_xticks(xticks)
# # a1.set_xticklabels(['Jul','Oct','Jan 2022','Apr','Jul','Oct','Jan 2023','Apr','Jul','Oct'], fontsize=fsize2)


# # ax[8].text(0.25, -0.6, '2021', fontsize=fsize3, horizontalalignment='center', transform=ax[8].transAxes)
# # ax[8].text(0.75, -0.6, '2022', fontsize=fsize3, horizontalalignment='center', transform=ax[8].transAxes)

# props = dict(boxstyle='round', facecolor='#CAA84F', alpha=0.3)
# ax[0].text(1.195, 1.1, name, fontsize=fsize4, horizontalalignment='center', 
#             bbox=props, transform=ax[0].transAxes)

# newax = fig.add_axes([0.71,0.62,0.24,0.24], anchor='NE', zorder=1)
# i = glob.glob('/home/pho/python_workspace/promice/pypromice/src/pypromice/local/vis/'+name.split(' ')[0]+'*_2023.jpg')[0]
# im = plt.imread(i)
# newax.imshow(im)
# newax.axis('off')

# props = dict(boxstyle='round', facecolor='#FFFFFF', edgecolor='#DFDFDF', alpha=0.8)
# start=str(df.index[0].date())
# size=str(len(df.index))
# lat=str(df.loc[df['gps_lat'].isnull() == False]['gps_lat'][-1])
# lon=str(df.loc[df['gps_lon'].isnull() == False]['gps_lon'][-1])
# if 'dlhf_l' in df: 
#     design = 'Two boom'
# else:
#     design = 'One boom'
# ax[0].text(1.2, -3.9, 'Active since: ' + start +
#            '\n\nPosition: ' + lat[0:5] + lon[0:5] +
#            '\n\nStation design: ' + design + 
#            '\n\nNr. measurements: ' + size + 
#            '\n\nData type: RAW/TX', fontsize=fsize2, horizontalalignment='center', 
#             bbox=props, transform=ax[0].transAxes)

plt.subplots_adjust(wspace=1,hspace=0)#, left=0.1, right=0.75)
plt.show()
plt.savefig('subsurface_data.jpg', dpi=300)