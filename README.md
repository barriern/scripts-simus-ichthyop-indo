# Scripts to run the Indonesian simulations

## Dowloading Ichthyop

The Ichthyop version used here can be dowloaded [here](https://github.com/ichthyop/ichthyop/releases/download/3.3.17.3/ichthyop-3.3.17-jar-with-dependencies.jar)

## Script description

In this section, the scripts used to generate the Indonesian simulations are described.

> [!WARNING]
> The scripts need to be run in the order below

> [!CAUTION]
> You will need to update the scripts to change the paths

1) `download_data.py`

This script allows to extract daily forcing fields for a given time-period.

In the current version, data are extracted from 2019 to 2021. This can be adapted if needed.

On Datarmor, this script must be launched by submitting the `download_files.pbs` job:

```bash
qsub download_files.pbs
```

2) `generate-zone-files.py`

This script allows to generate Ichthyop zone files (XML format) based on the sampling locations (provided in `sampling-locations-diadema.csv`)

It takes the center of the sampling location and add a 1 degree squared bounding box around.

The size of the box can be adapted (`dx` and `dy` parameters)

3) `generate_configuration_files.py`

This script allows to build multiple configuration files from the `config-laura-indo.xml` template. It allows to control:

- Release date
- Simulation duration
- Lethal temperatures

4) `generate-mpi-text-file.py`

This script allows to create the text file that comes as an argument to the [ichthyop-mpi](https://github.com/ichthyop/ichthyop-mpi) tool.

This script contains the multiple lines that will send to each MPI process on High Performance Computation (HPC) centers.

5) `run_ichythyop_mpi.pbs`

When the zone files, the configuration files and the Ichthyop MPI input files are ready, the next step is to run the simulations.
This is done by submitting the `run_ichythyop_mpi.pbs` job to Datarmor.

```bash
qsub run_ichythyop_mpi.pbs4
```

This will run the model by batches of 14 simulations in parralel.

6) `process-ichthytop-outputs.py`

This script allows to post-process Ichthyop outputs to build connectivity matrix. They are exported as PNG and as CSV files
