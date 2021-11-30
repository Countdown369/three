#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 21:52:54 2021

@author: cabrown802
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon

# Crates GeoDataFrame out of service call data.
def servicecallGDF(datafile):
    
    # Reads service call data from PKL file.
    data = pd.read_pickle(datafile)
    
    # Removes all service calls with inaccurate coordinates.
    # (Some were in the Eastern hemisphere for some reason?)
    data = data.drop(data[data.long > 0].index)
    """
    You can use this type of statement to filter on whatever data you want.
    For example, you could make one DataFrame which only contains Graffiti
    service calls, or one which contains 3 certain call types, etc.
    """
    
    # Creates Point objects out of lat-long data for a GeoDataFrame.
    geometry=[Point(xy) for xy in zip(data["long"], data["lat"])]
    
    # Constructs GeoDataFrame of service call Points
    geodata = gpd.GeoDataFrame(data,crs={'init':'epsg:3857'}, geometry=geometry)
    
    return geodata

def main():
    geodata = servicecallGDF("output.pkl")
    print(geodata['service_name'])
    
main()