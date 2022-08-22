#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 11:57:28 2021

@author: cabrown802
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
import contextily as ctx

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

 # Reads geojson file into a GeoDataFrame and returns it
def makeCityGDF(city):
    
    bos = gpd.read_file(city + ".geojson")
    return bos

# Makes plot
def plotData(geodata, citydata, shapefile, filterr, name, thetitle, legendlabel, filtertrue, shptrue, basemap, boundary, save):
    """
    Parameters
    ----------
    geodata : GeoDataFrame
        Collection of points in GDF.
    citydata : GeoDataFrame
        Polygon of city boundary.
    shapefile : String indicating path of .dbf file
        DBF file containing shapes with different values.
    filterr : string
        Type of service request to produce a map for.
    name : string
        File name, if saving.
    thetitle : string
        title of plot.
    legendlabel : string
        label of legend, if using a shapefile.
    filtertrue : boolean
        Only filters geodata if True.
    shptrue : boolean
        Only plots DBF-based data if True.
    basemap : boolean
        Only adds basemap image of city if true.
    boundary : boolean
        Only adds citydata boundary if True.
    save : boolean
        Only saves plot to file if true.

    Returns
    -------
    None, but plots.

    """
    
    
    """
    If you want to plot more layers, use the plot function, as is done with
    citydata and geodata down below.
    """
    # Setup bounds for plot
    minx, miny, maxx, maxy = citydata.geometry.total_bounds
    
    # Create Axes object (ax)
    f, ax = plt.subplots()
    
    # Add city boundary to plot
    if boundary:
        citydata.plot(ax=ax, color='green', alpha = 0.5)
    
    # If filtering, filter the service_name category
    if filtertrue:
        geodata = geodata[geodata.service_name == filterr]
        
    # Add service call points to plot
    geodata.plot(ax=ax, color = 'black', marker='o', markersize=1, legend = False)
    
    # If plotting census tracts, plot them (differently based on income value)
    if shptrue:
        income = gpd.read_file(shapefile)
        income = income.dropna(0)
        
        # Drop park areas (Franklin Park Zoo, Roslindale parks)
        income = income.drop([171, 174])
        
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        
        income.plot(ax=ax, cmap='OrRd', column = 'VALUE0', alpha = 0.61, legend = True, cax = cax)
    
    
    # Set bounds for plot
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    
    # Add basemap if wanted
    if basemap:
        import pdb; pdb.set_trace()
        ctx.add_basemap(ax, crs=citydata.crs.to_string(), source=ctx.providers.CartoDB.Voyager)
        
    # Labels
    plt.title(thetitle, loc = 'right')
    plt.xlabel("Longitude")
    if shptrue:
        plt.ylabel(legendlabel, loc = 'center')
    else:
        plt.ylabel("Latitude")
    
    # Save map to file as PNG if wanted
    if save:
        plt.savefig(name, dpi = 300, bbox_inches='tight')
        
    plt.show()
    
def issueFrequency(geodata):
    # For our "Most Common Requests" bar chart
    myObj = geodata['service_name'].value_counts()[:10]
    myObj.plot(kind = 'bar', title = 'Most Common Boston 311 Service Requests, 2019-2021', ylabel = 'Frequency')
    plt.savefig("barchart.png", dpi = 300, bbox_inches = 'tight')

def main():
    
    geodata = servicecallGDF("output.pkl")
    bos = makeCityGDF("boston")
    
    # This example prints out the education-based map.
    # See plotData() for info on arguments.
    plotData(geodata, bos, "education/edu.dbf", 'Street Lights', "ack1.png", "2019-2021 Boston 311 Service Requests by Education", "Educational Attainment", False, True, True, False, True)
    
    # issueFrequency(geodata)
    
main()

