from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta

infile = "dataverse_ice_discharge_downloads_by_month.csv"

df = pd.read_csv(infile, skiprows=0)
df['datetime'] = pd.to_datetime(df['date'])
df['cumulative_count'] = df['count']

count = list(df['count'])
abs_count = []
abs_count.append(np.nan)
for i in list(range(len(count)))[1:]:
    abs_count.append(count[i]-count[i-1])
df['absolute_count'] = abs_count

print(df)
print('Average monthly downloads:',str(np.mean(df['absolute_count'])))
print('Most monthly downloads:',str(np.max(df['absolute_count'])))
print('Total downloads:',str(np.max(df['cumulative_count'])))

fig, ax = plt.subplots(1, figsize=(10, 6))
fsize1 = 14
fsize2 = 12
fsize3 = 10
fsize4 = 8
fsty = 'arial'
pad = 1.
lw = 1
col = '#128c4f'
fcol = '#404040'
props = dict(boxstyle='round', edgecolor="#666699", facecolor="#FFFFFF",
             lw=2, alpha=1,fill=True,zorder=2000)

ax.bar(df['datetime'], df['absolute_count'], color=col, width=10)
ax.set_xlim([dt.datetime(2022,12,15), dt.datetime(2025,1,15)])
ax.set_xticks([dt.datetime(2023,1,1), dt.datetime(2023,2,1),
               dt.datetime(2023,3,1), dt.datetime(2023,4,1),
               dt.datetime(2023,5,1), dt.datetime(2023,6,1),
               dt.datetime(2023,7,1), dt.datetime(2023,8,1),
               dt.datetime(2023,9,1), dt.datetime(2023,10,1),
               dt.datetime(2023,11,1), dt.datetime(2023,12,1),
               dt.datetime(2024, 1, 1), dt.datetime(2024, 2, 1),
               dt.datetime(2024, 3, 1), dt.datetime(2024, 4, 1),
               dt.datetime(2024, 5, 1), dt.datetime(2024, 6, 1),
               dt.datetime(2024, 7, 1), dt.datetime(2024, 8, 1),
               dt.datetime(2024, 9, 1), dt.datetime(2024, 10, 1),
               dt.datetime(2024, 11, 1), dt.datetime(2024, 12, 1),
               dt.datetime(2025,1,1),dt.datetime(2025, 2, 1),
               dt.datetime(2025, 3, 1), dt.datetime(2025, 4, 1),
               dt.datetime(2025, 5, 1), dt.datetime(2025, 6, 1),
               dt.datetime(2025, 7, 1), dt.datetime(2025, 8, 1),
               dt.datetime(2025, 9, 1), dt.datetime(2025, 10, 1),
               dt.datetime(2025, 11, 1), dt.datetime(2025, 12, 1)])
ax.set_xticklabels(['Jan 2023', '', 'Mar', '', 'May', '', 'Jul','', 'Sep','','Nov','',
                    'Jan 2024', '', 'Mar', '', 'May', '', 'Jul', '', 'Sep', '', 'Nov', '',
                    'Jan 2025', '', 'Mar', '', 'May', '', 'Jul', '', 'Sep', '', 'Nov', '',],
                    fontsize=fsize3, rotation=45, color=fcol)
ax.set_ylim([0, 600])
ax.set_yticks([0, 100, 200, 300, 400, 500, 600])
ax.set_yticklabels(['0', '100', '200', '300', '400', '', ''], fontsize=fsize3, color=fcol)
ax.tick_params(axis='y', which='both', length=0)

ax1 = ax.twinx()
ax1.set_xlim([dt.datetime(2022,12,15), dt.datetime(2025,12,31)])
ax1.plot(df['datetime'], df['cumulative_count'], color=col, linewidth=1.5, marker='s', markersize=3)
ax1.set_ylim([0, 60000])
ax1.set_yticks([0, 10000, 20000, 30000, 40000, 50000, 60000])
ax1.set_yticklabels(['', '', '', '30.000', '40.000', '50.000', '60.000'], fontsize=fsize3, color=fcol)
ax1.tick_params(axis='y', which='both', length=0)

#labels = [str(s) for s in df['cumulative_count']]
labels = ["{:,.0f}".format(s).replace(',','.') for s in df['cumulative_count']]
print(labels)
#for l in labels:
#    s1 = l.replace(",", ".")
for a in range(len(labels))[::3]:
    ax1.annotate(labels[a], xy=(list(df['datetime'])[a], list(df['cumulative_count'])[a]+1000), fontsize=fsize3, color=col)
ax1.annotate(labels[a], xy=(list(df['datetime'])[a]-timedelta(days=45), list(df['cumulative_count'])[a]+10000), fontsize=fsize3, color=col)

ax.set_xlabel('Month', fontsize=fsize2, color=fcol, labelpad=5)
ax.set_ylabel('Downloads per month', fontsize=fsize2, color=fcol)
ax.yaxis.set_label_coords(-0.08, 0.3)
ax1.set_ylabel('Cumulative downloads', rotation=270, fontsize=fsize2, color=fcol)
ax1.yaxis.set_label_coords(1.11, 0.7)
ax.set_title('Ice Discharge Dataverse downloads by month', fontsize=fsize1, color=fcol, pad=20)

ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)

for a in [ax, ax1]:
    a.spines["top"].set_visible(False)
    a.spines["right"].set_visible(False)
    a.spines["left"].set_visible(False)

plt.savefig('dataverse_ice_discharge_downloads.png', dpi=300)