# ---
# jupyter:
#   jupytext:
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

import numpy as np
import re

with open('ichthyop-mpi.txt', 'r') as fin:
    mpi_list = fin.readlines()
mpi_list[:4]

with open('processed.txt', 'r') as fin:
    processed = fin.readlines()
processed[:5]

regex = re.compile(".*(output-start-.*)_ichthyop.*")

i = 0


list_out = []
for line in mpi_list:
    include = True
    for i in range(len(processed)):
        temp = regex.match(processed[i])
        prefix = temp.groups()[0]
        if prefix in line:
            include = False
    if include: list_out.append(line)
len(list_out)

with open('clean-ichthyop-mpi.txt', 'w') as fout:
    for l in list_out:
        fout.write(l)


