import copernicusmarine
import os

#copernicusmarine.login()


offx = 10
offy = 10 
lon_min = 94 - offx
lon_max = 129 + offx
lat_min = -9 - offy
lat_max = 6 + offy

dirout = "/home/datawork-marbec-scenlab/ICHTHYOP/laura-indonesie/"
dirout = "/home1/scratch/nbarrier/data-indo"

for year in range(2019, 2022):
    for month in range(1, 13):
        for day in range(1, 32):

            start_datetime = "%.4d-%.2d-%.2dT00:00:00" %(year, month, day)
            end_datetime = "%.4d-%.2d-%.2dT23:59:59" %(year, month, day)
            print(start_datetime)
            print(end_datetime)
            foutname =  os.path.join(dirout, "indonisia-current-%.4d-%.2d-%.2d.nc" %(year, month, day))
            print("Processing ", foutname)
            if(os.path.isfile(foutname)):
                print("--------------------- %.4d-%.2d-%.2d is skipped." %(year, month, day))
                continue
            try:
                copernicusmarine.subset(
                dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
                variables=["uo", "vo", "thetao"],
                minimum_longitude=lon_min,
                maximum_longitude=lon_max,
                minimum_latitude=lat_min,
                maximum_latitude=lat_max,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                minimum_depth=0,
                maximum_depth=6000,
                output_filename = foutname,
                output_directory = dirout
                )
            except:
                pass
