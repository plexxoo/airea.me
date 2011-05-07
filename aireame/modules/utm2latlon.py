# -*- coding: utf-8 -*- 
import math

#
# Used explanation from "Converting UTM to Latitude and Longitude (Or Vice Versa)"
# http://www.uwgb.edu/dutchs/usefuldata/utmformulas.htm
#

def utmTolatlon(zone, xutm, yutm, northernHemisphere=True):
    """
    Translate UTM coordinates to Latitude-Longitude Coordinates
    
    Parameters:
    + zone: UTM zone
    + xutm: UTM X Coordinate (easting)
    + yutm: UTM Y Coordinate (northing)
    
    Returns Longitude-Latitude coordinates (tuple).
    """
    # Northern Hemisphere control
    if not northernHemisphere:
        yutm = 10000000 - yutm

    # Constants
    a = 6378137
    e = 0.081819191
    e1sq = 0.006739497
    k0 = 0.9996

    # Calculate the Meridional Arc
    arc = yutm / k0
    
    # Calculate Footprint Latitude
    mu = arc / (a * (1 - math.pow(e, 2) / 4.0 - 3 * math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))
    ei = (1 - math.pow((1 - e * e), (1 / 2.0))) / (1 + math.pow((1 - e * e), (1 / 2.0)))
    
    # Constants
    j1 = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0
    j2 = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
    j3 = 151 * math.pow(ei, 3) / 96
    j4 = 1097 * math.pow(ei, 4) / 512
    
    # Footprint Latitude
    fp = mu + j1 * math.sin(2 * mu) + j2 * math.sin(4 * mu) + j3 * math.sin(6 * mu) + j4 * math.sin(8 * mu)
    
    # Calculate Latitude
    # Previous calculus
    n1 = a / math.pow((1 - math.pow((e * math.sin(fp)), 2)), (1 / 2.0))
    r1 = a * (1 - e * e) / math.pow((1 - math.pow((e * math.sin(fp)), 2)), (3 / 2.0))
    q1 = n1 * math.tan(fp) / r1

    tmp1 = 500000 - xutm
    dd0 = tmp1 / (n1 * k0)
    q2 = dd0 * dd0 / 2

    t0 = math.pow(math.tan(fp), 2)
    Q0 = e1sq * math.pow(math.cos(fp), 2)
    q3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 - 9 * e1sq) * math.pow(dd0, 4) / 24

    q4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 * e1sq - 3 * Q0 * Q0) * math.pow(dd0, 6) / 720

    # Latitude
    latitude = 180 * (fp - q1 * (q2 + q3 + q4)) / math.pi

    if not northernHemisphere:
        latitude = -latitude
        
    # Calculate Latitude and Longitude
    # Previous calculus
    q5 = tmp1 / (n1 * k0)
    q6 = (1 + 2 * t0 + Q0) * math.pow(dd0, 3) / 6.0
    q7 = (5 - 2 * Q0 + 28 * t0 - 3 * math.pow(Q0, 2) + 8 * e1sq + 24 * math.pow(t0, 2)) * math.pow(dd0, 5) / 120
    tmp2 = (q5 - q6 + q7) / math.cos(fp)
    tmp3 = tmp2 * 180 / math.pi

    # Longitude
    longitude = ((zone > 0) and (6 * zone - 183.0) or 3.0) - tmp3

    # Returns tuple
    return (latitude, longitude)
 
