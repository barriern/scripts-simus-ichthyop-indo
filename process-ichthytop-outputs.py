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
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from glob import glob
import os
import re
import pandas as pd

newpath = 'processed-outputs'
if not os.path.exists(newpath):
    os.makedirs(newpath)

filelist = glob('output/*nc')
filelist.sort()
filelist


def process_file(f):

    print(f"--------------------------------Process file {f}")
    
    prefix = os.path.basename(re.split('_ichthyop', f)[0])
    prefix
    
    data = xr.open_mfdataset(f)
    data
    
    N = len(data['recruitment_zone'])
    N
    
    release_zone = data['release_zone'].values
    release_zone
    
    unique_rel_zone = np.unique(release_zone)
    N_rel_zone = len(unique_rel_zone)
    N_rel_zone
    
    recruited_zone = data['recruited_zone'].values  # time, nparticles, nzones
    recruited_zone.shape
    
    N_rec_zone = recruited_zone.shape[-1]
    N_rec_zone
    
    rec_names = [data['recruited_zone'].attrs[f'recruitment_zone_{i}'] for i in range(N_rec_zone)]
    # for i in range(len(rec_names)):
    #     print(i, rec_names[i])
    
    data['release_zone']
    
    rel_names = [data['release_zone'].attrs[f'release_zone_{i}'] for i in range(N_rel_zone)]
    # for i in range(len(rel_names)):
    #     print(i, rel_names[i])
    
    itime = -1
    
    output = np.zeros((N_rel_zone, N_rec_zone))
    mort = data['mortality'].values[itime, :]
    
    # Loop over the release zones
    for rel_zone in range(0, N_rel_zone):
        # Get the index of particles releases in this specific zone
        irel = np.nonzero(release_zone == rel_zone)[0]
        N_rel = len(irel)  # Get total number of particles released from zone
        irel = np.nonzero((release_zone == rel_zone) & (mort == 0))[0]
        rec_temp = recruited_zone[itime, irel, :]  # Get the recruitment matrix for the particles released in the zone
        for rec_zone in range(0, N_rec_zone):
            # get whether the particles released in the specific release zone
            # have been recruited in the particular recruitment zone
            temp = rec_temp[:, rec_zone]
            output[rel_zone, rec_zone] = np.sum(temp) / N_rel * 100
    output = np.ma.masked_where(output == 0, output)  # Nrelease, Nrecruitment
    
    dsout = pd.DataFrame(index=rel_names, columns=rec_names, data=output)
    foutname = os.path.join(newpath, f'recruitment-matrix-{prefix}.csv')
    dsout.to_csv(foutname)
    
    fig = plt.figure()
    index_rel = np.arange(N_rel_zone)
    index_rec = np.arange(N_rec_zone)
    ax = plt.gca()
    ax.set_ylabel('Release zones')
    ax.set_xlabel('Recruitment zones')
    cs = ax.pcolormesh(index_rec, index_rel, output, alpha=0.5)
    iy, ix = np.nonzero(output > 0)
    for j, i in zip(iy, ix):
        ax.text(i, j, f'{output[j, i]:.2f}', ha='center', va='center')
    
    cb = plt.colorbar(cs)
    cb.set_label('Recruitment (%)')
    ax.set_xticks(index_rec)
    ax.set_xticklabels(rec_names, ha='right', rotation=45)
    ax.set_yticks(index_rel)
    ax.set_yticklabels(rel_names)
    ax.grid(True, ls='--')
    ax.set_title(prefix)
    plt.savefig(os.path.join(newpath, f'percentage-recruitment-{prefix}.png'), bbox_inches='tight')
    plt.close(fig)


for f in filelist[:2]:
    process_file(f)


