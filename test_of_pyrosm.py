


from pyrosm import OSM


osm = OSM("italy_latest.pbf")

# open

print(osm.conf.tags.available)


extract_power = ["substation"]


goedata_of_interest  = osm.get_data_by_custom_criteria(custom_filter={'power': ["substation"]},
                                                                            osm_keys_to_keep=['power'],
                                                                            filter_type="keep",
                                                                            keep_nodes=True, 
                                                                            keep_ways=False, 
                                                                            keep_relations=False)

# print(goedata_of_interest.head())
goedata_of_interest.to_file("clipped_files/ITA/power_substation.geojson", driver="GeoJSON")
