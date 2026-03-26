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

from glob import glob

filelist = glob('configuration-files/output-start-*xml')
filelist.sort()
filelist

prefix = 'java -jar ichthyop-3.3.17-jar-with-dependencies.jar'

lout = []
for f in filelist:
    fout = f.replace(".xml", ".log").replace("configuration-files/", "")
    lout.append(f"{prefix} {f} > {fout}")
lout

with open("ichthyop-mpi.txt", "w") as fout:
    for l in lout:
        fout.write(l + "\n")


