# Scripts to run the Indonesian simulations

## Dowloading Ichthyop

The Ichthyop version used here can be dowloaded [here](https://github.com/ichthyop/ichthyop/releases/download/3.3.17.3/ichthyop-3.3.17-jar-with-dependencies.jar)

## Script description

The scripts must be run in the following order:

1) `download_data.py`

This script allows to extract daily forcing fields for a given time-period.

In the current version, data are extracted from 2019 to 2021. This can be adapted if needed.

2) `generate-zone-files.py`

This script allows to generate Ichthyop zone files (XML format) based on the sampling locations (provided in `sampling-locations-diadema.csv`)

It takes the center of the sampling location and add a 1 degree squared bounding box around.

The size of the box can be adapted (`dx` and `dy` parameters)
