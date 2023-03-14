

import geopandas as gpd
import rasterio 

from rasterio import mask

import os 

import numpy as np

# Extracts a list of all files in input folder: input_files
files_in_input_files = os.listdir("input_files")

# checks each item in input_files and if it is a file, it adds it to the list of files to be clipped
list_of_files_to_be_clipped = []
accepted_file_types = ["shp", "geojson" , "gpkg", "tif", "asc"]

# Define the country to be clipped to
list_of_countries_to_be_clipped_to = ["POL", "ITA", "DEU", "SWE"]


for file in files_in_input_files:
    if os.path.isfile("input_files/"+ file):
        # Check if the ending for the file is in the list: accepted_files, and if it is not, skip it
        if file.split(".")[-1] not in accepted_file_types:
            continue
        list_of_files_to_be_clipped.append(file)

for file_path in list_of_files_to_be_clipped:
    # Print a progress bar here
    
    filetype = file_path.split(".")[-1]

    print("Clipping file: {file_path}".format(file_path=file_path))

    # Check if the final file already exists, if it does, skip it
    if os.path.exists("clipped_files/{country}/{file_name}".format(country=list_of_countries_to_be_clipped_to[0], file_name=file_path.split(".")[0])):
        print("File already exists, skipping")
        continue

    
    # If the filetype is a vector type
    if filetype in ["shp", "geojson", "gpkg"]:
            
        # If the filetype is geojson, gpkg or shp 
        if filetype == "geojson":
            gdf = gpd.read_file("input_files/" + file_path, driver="GeoJSON")
        elif filetype == "shp":
            gdf = gpd.read_file("input_files/" + file_path)
        elif filetype == "gpkg":
            gdf = gpd.read_file("input_files/" + file_path, driver="GPKG")

        # check that geometries in the gdf is valid, and filter out those that are not
        # gdf = gdf[gdf.geometry.is_valid]

        if gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")

        print("Passed the CRS check")

        for country in list_of_countries_to_be_clipped_to:

            gdf_bounds = gpd.read_file("gadm/{country}/{country}_0.shp".format(country=country))
            # simplify the gdf_bounds to speed up the clipping process
            gdf_bounds = gdf_bounds.simplify(0.04)
            # clip the gdf to the gdf_bounds
            gdf_clipped = gpd.clip(gdf, gdf_bounds)

            # save the clipped gdf to a file
            # check if a path extists, if not create a folder
            if not os.path.exists("clipped_files/{country}/{file_name}".format(country=country, file_name=file_path.split(".")[0])):
                os.makedirs("clipped_files/{country}/{file_name}".format(country=country,file_name=file_path.split(".")[0]))

            gdf_clipped.to_file("clipped_files/{country}/{file_path}/{filename}.geojson".format(country=country ,file_path=file_path.split(".")[0]), driver="GeoJSON")

            # gdf_clipped.to_file("clipped_files/file.geojson".format(country=country ,file_path=file_path.split(".")[0]), driver="GeoJSON")
    

    # If the file is raster type    
    elif filetype in ["tif", "asc"]:

        # Open the file with rasterio
        with rasterio.open("input_files/" + file_path) as src:
            print("successfully opened the raster file")

            meta = src.meta

            for country in list_of_countries_to_be_clipped_to:
                
                # Print which country is being clipped to
                print("Clipping to country: {country}".format(country=country))

                gdf_bounds = gpd.read_file("gadm/{country}/{country}_0.shp".format(country=country))
                


                # simplify the gdf_bounds to speed up the clipping process
                gdf_bounds.geometry = gdf_bounds.simplify(0.04)



                out_image, _ = mask.mask(src, gdf_bounds["geometry"] , crop=True)

                # Get the bands of the out_image
                bbox = gdf_bounds.total_bounds

                transform_obj = rasterio.transform.from_bounds(*bbox, out_image.shape[2], out_image.shape[1])


                # check if a path extists, if not create a folder
                if not os.path.exists("clipped_files/{file_name}/{country}".format(country=country, file_name=file_path.split(".")[0])):
                    os.makedirs("clipped_files/{file_name}/{country}".format(country=country,file_name=file_path.split(".")[0]))
                

                # Save the out_image to a file 
                with rasterio.open("clipped_files/{file_name}/{country}/{file_name}.tif".format(country=country,file_name=file_path.split(".")[0]), 'w', driver='GTiff', height=out_image.shape[1], width=out_image.shape[2], count=1, dtype=out_image.dtype, crs=gdf_bounds.crs, transform=transform_obj, nodata=src.nodata) as dst:
                    dst.write(out_image)


                # Print success message
                print("Successfully clipped file: {file_path} to country: {country}".format(file_path=file_path, country=country))


