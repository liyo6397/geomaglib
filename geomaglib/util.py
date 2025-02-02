# Autogenerated with SMOP 0.29
#Modified by Adam
import numpy as np
import math
from geomaglib import geoid
from datetime import datetime
import calendar
    
def geod_to_geoc_lat(lat,alt,B=None):
    # [r, theta] = geod2geoc(alpha, h);
# [r, theta, B_r, B_theta] = geod2geoc(alpha, h, X, Z);
# conversion from geodetic X,Z components to geocentric B_r, B_theta
# Input:   geodetic latitude lat (deg)
#          altitude alt [km]
#          X, Z
# Output:  theta (rad)
#          r (km)
#          B_r, B_theta
    
    # Nils Olsen, DSRI Copenhagen, September 2001.
    # After Langel (1987), eq. (52), (53), (56), (57)
    # Converted to python by Adam (2017)
    
    # Latest changes: NIO, 170903 optional conversion of magnetic components
    #                 Update to WGS-84 ellipsoid    

    # WGS-84 Ellipsoid parameters
    a=6378.137
    f = 1/298.257223563
    b = a*(1-f)
    lat_rad = np.radians(lat)
    sin_alpha_2=np.sin(lat_rad) ** 2
    cos_alpha_2=np.cos(lat_rad) ** 2
    tmp=np.multiply(alt,np.sqrt(np.dot(a ** 2,cos_alpha_2) + np.dot(b ** 2,sin_alpha_2)))
    beta=np.arctan(np.multiply((tmp + b ** 2) / (tmp + a ** 2),np.tan(lat_rad)))
    theta= math.degrees(beta)
    r=np.sqrt(alt ** 2 + np.dot(2,tmp) + np.dot(a ** 2,(1 - np.dot((1 - (b / a) ** 4),sin_alpha_2))) / (1 - np.dot((1 - (b / a) ** 2),sin_alpha_2)))




    return r, theta


def alt_to_ellipsoid_height(alt,lat,lon):
    """
    This function converts altitude MSL in kilometers to ellipsoid height in
    kilometers

    Parameters:
    alt (int or float): The original altitude in kilometers in MSL
    lat (int or float): The latitude degree from -90 to 90
    lon (int or float): The longitude degree from -180 to 360

    Returns:
    (float): Height above ellipsoid in kilometers
    """
    offset_x = 0
    if lon < 0.0:
        offset_x = (lon + 360) * geoid.geoid["scale_factor"]
    else :
        offset_x = lon * geoid.geoid["scale_factor"]

    offset_y = (90- lat) * geoid.geoid["scale_factor"]


    post_x =  int(math.floor(offset_x))
    if post_x + 1 == geoid.geoid["cols"]:
        post_x = post_x -1
    
    post_y = int(math.floor(offset_y))
    if post_y + 1 == geoid.geoid["rows"]:
        post_y = post_y - 1

    index = post_y * geoid.geoid["cols"] + post_x
    elevation_NW = geoid.geoid["height_buffer"][index]
    elevation_NE = geoid.geoid["height_buffer"][index+1]

    index = (post_y +1) * geoid.geoid["cols"] + post_x
    elevation_SW = geoid.geoid["height_buffer"][index]
    elevation_SE = geoid.geoid["height_buffer"][index+1]

    delta_x = offset_x - post_x
    delta_y = offset_y - post_y

    upper_y = elevation_NW + delta_x * (elevation_NE - elevation_NW)
    lower_y = elevation_SW + delta_x * (elevation_SE - elevation_SW)

    delta_height = upper_y + delta_y * (lower_y - upper_y)

    #delta_height is in meters need to convert to kilometers
    ellipsoid_height = alt + delta_height/1000 

    return ellipsoid_height

def calc_dec_year(year, month,day):
    """
    Takes year, month, and day and calculates the decimal year from those inputs

    Parameters:
    year (int): The year fully written for example 2024
    month (int): The month from 1-12 where is 1 is January and 12 is December
    day (int): The day of the month from 1-31 

    Returns:
    (float): The decimal year

    """
    num_days_year = 365
    if calendar.isleap(year):
        num_days_year = 366
    date = datetime(year, month, day)
    day_of_year = date.timetuple().tm_yday
    return  year + ((day_of_year -1)/num_days_year)






