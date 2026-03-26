# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import re
import xarray as xr
from glob import glob
import datetime
import calendar
import numpy as np

# Open the configuration template as a text file and read all the lines

with open("config-laura-indo.xml", "r") as fin:
    constant_lines = fin.readlines()
constant_lines[:5], constant_lines[-5:]
nlines = len(constant_lines)

for y in range(2019, 2021):
    for m in range(1, 13):
        ndays = np.arange(calendar.monthrange(y, m)[-1]) + 1
        for d in ndays[::5]:
            for mld in [30, 35, 40, 45]:
                for t in [31, 32, 33, 34]:

                    lines = constant_lines.copy()

                    # Replace time settings
                    fout_string1 = f"year {y:04d} month {m:02} day {d:02d} at 12:00"
                    fout_string1
                    
                    # Replace MLD settings
                    fout_string2 = f"{mld:04d} day(s) 00 hour(s) 00 minute(s)"
                    fout_string2    
                    
                    fout_string3 = f"output-start-{y:04d}-{m:02d}-{d:02d}-mld-{mld:02d}-Temp_max-{t:02d}"
                    fout_string3
                    
                    for i in range(nlines):
                        lines[i] = lines[i].replace("TRANSPORT_DURATION", fout_string2)
                        lines[i] = lines[i].replace("OUTPUT_PATH", fout_string3)
                        lines[i] = lines[i].replace("FILE_PREFIX", fout_string3)
                        lines[i] = lines[i].replace("SIMULATION_START", fout_string1)
                        lines[i] = lines[i].replace("LETHAL_HOT", str(t))
                    
                    with open('configuration-files/' + fout_string3 + '.xml', 'w') as fout:
                        for l in lines:
                            fout.write(l)


