import os

gadm_path = "gadm"
# for each folder in the directory gadm
for folder in os.listdir(gadm_path):

    # for each file in the folder 
    for file in os.listdir(f"{gadm_path}/{folder}"):

        # If file contains "gadm36_" in the name

        if "gadm36_" in file:
            # Remove the "gadm36_" part of the name
            os.rename(f"{gadm_path}/{folder}/{file}", f"{gadm_path}/{folder}/{file.replace('gadm36_', '')}")
            #Print the renamed file "Old name" -> "New name"
            print(f"{gadm_path}/{folder}/{file} -> {gadm_path}/{folder}/{file.replace('gadm36_', '')}")
            

        # If file contains "gadm41_" in the name
        if "gadm41_" in file:

            # Rename the file to remove the "gadm36_" part of the name
            os.rename(f"{gadm_path}/{folder}/{file}", f"{gadm_path}/{folder}/{file.replace('gadm41_', '')}")
            print(f"{gadm_path}/{folder}/{file} -> {gadm_path}/{folder}/{file.replace('gadm36_', '')}")


