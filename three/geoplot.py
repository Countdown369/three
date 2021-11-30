#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 20:42:29 2021

@author: cabrown802
"""


import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon

data = pd.read_pickle("output.pkl")
data = data.drop(data[data.long > 0].index)

servicetypes = []
for servicetype in data['service_name']:
    if servicetype not in servicetypes:
        servicetypes.append(servicetype)

print(servicetypes)
print(len(servicetypes))
crs={'init':'epsg:4326'}
geometry=[Point(xy) for xy in zip(data["long"], data["lat"])]

geodata = gpd.GeoDataFrame(data,crs=crs, geometry=geometry)
geodata.plot(column = 'service_name', markersize = 1)