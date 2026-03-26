# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import xarray as xr
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import numpy as np

mask = xr.open_dataset('data/laura-indonesie-GLO-MFC_001_030_mask_bathy.nc').isel(depth=0)
mask = mask['mask']
mask
lon = mask['longitude'].values
lat = mask['latitude'].values
lonmin, lonmax = lon.min(), lon.max()
latmin, latmax = lat.min(), lat.max()

data = pd.read_csv('sampling-locations-diadema.csv')
# data = data.loc[data['Genetic cluster'] < 3]
data

# +
dx = 0.3
dy = 0.3
zones = {}
for i in range(data.shape[0]):
    temp = data.iloc[i, :]
    lon = temp['Longitude']
    lat = temp['Latitude']
    name = temp['Locations']
    lonzones = [lon - dx, lon + dx, lon + dx, lon - dx, lon - dx]
    latzones = [lat - dy, lat - dy, lat + dy, lat + dy, lat - dy]
    if((lonzones[0] < lonmin) | (lonzones[1] > lonmax) | (latzones[0] < latmin) | (latzones[3] > latmax)):
        print('zone is discarded')
    else:
        zones[name] = {'lon': lonzones, 'lat': latzones}

plt.figure()
cmap = plt.get_cmap('jet')
ax = plt.axes(projection=ccrs.PlateCarree())
ax.pcolormesh(mask['longitude'], mask['latitude'], mask, transform=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE, color='red')
i = 0
for z in zones.values():
    col = cmap(i / (len(zones) - 1))
    ax.plot(z['lon'], z['lat'], color=col, transform=ccrs.PlateCarree())
    i += 1

# +
upper_depth = 0
lower_depth = 200

strout = '<?xml version="1.0" encoding="UTF-8"?>\n'
strout += '<zones>\n'
i = 0
for name, z in zones.items():
    col = cmap(i / (len(zones) - 1))
    print(col)

    strout += '<zone>\n'
    strout += f'<key>Release-{name}</key>\n'
    strout += '<type>release</type>\n'
    strout += '<enabled>true</enabled>\n'
    strout += f'<color>[r={int(np.floor(col[0] * 255))},g={int(np.floor(col[1] * 255))},b={int(np.floor(col[2] * 255))}]</color>\n'
    strout += '<polygon>\n'
    lontmp = z['lon']
    lattmp = z['lat']
    for k in range(len(lontmp)):
        strout += '  <point>\n'
        strout += f'    <index>{k}</index>\n'
        strout += f'    <lon>{lontmp[k]}</lon>\n'
        strout += f'    <lat>{lattmp[k]}</lat>\n'
        strout += f'  </point>\n'
    strout += '</polygon>\n'
    strout += '<bathy_mask>\n'
    strout += '  <enabled>false</enabled>\n'
    strout += '  <line_inshore>200.0</line_inshore>\n'
    strout += '  <line_offshore>500.0</line_offshore>\n'
    strout += '</bathy_mask>\n'
    strout += '<thickness>\n'
    strout += '  <enabled>true</enabled>\n'
    strout += f'  <upper_depth>{upper_depth}</upper_depth>\n'
    strout += f'  <lower_depth>{lower_depth}</lower_depth>\n'
    strout += '</thickness>\n'
    strout += '</zone>\n'

    strout += '<zone>\n'
    strout += f'<key>Recruitment-{name}</key>\n'
    strout += '<type>recruitment</type>\n'
    strout += '<enabled>true</enabled>\n'
    strout += f'<color>[r={int(np.floor(col[0] * 255))},g={int(np.floor(col[1] * 255))},b={int(np.floor(col[2] * 255))}]</color>\n'
    strout += '<polygon>\n'
    lontmp = z['lon']
    lattmp = z['lat']
    for k in range(len(lontmp)):
        strout += '  <point>\n'
        strout += f'    <index>{k}</index>\n'
        strout += f'    <lon>{lontmp[k]}</lon>\n'
        strout += f'    <lat>{lattmp[k]}</lat>\n'
        strout += f'  </point>\n'
    strout += '</polygon>\n'
    strout += '<bathy_mask>\n'
    strout += '  <enabled>false</enabled>\n'
    strout += '  <line_inshore>200.0</line_inshore>\n'
    strout += '  <line_offshore>500.0</line_offshore>\n'
    strout += '</bathy_mask>\n'
    strout += '<thickness>\n'
    strout += '  <enabled>true</enabled>\n'
    strout += f'  <upper_depth>{upper_depth}</upper_depth>\n'
    strout += f'  <lower_depth>{lower_depth}</lower_depth>\n'
    strout += '</thickness>\n'
    strout += '</zone>\n'
    i += 1

strout += '</zones>\n'

with open('laura-zones.xml', 'w') as fout:
    fout.write(strout)
