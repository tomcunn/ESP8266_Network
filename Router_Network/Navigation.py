#############################################
#
#   Navigation.py
#
#   Support point to point navigation
#
############################################

import math

def Navigation(current_position, list_of_points):
    current_point = 0
    left_speed = 0
    right_speed = 0 

    return current_point, left_speed, right_speed


def ComputeOffset(current_position,desired_position):
    offset = current_position[0] - desired_position[0]
    return offset

def ComputeSpeed():
    speed = 0

    return speed

def ComputeHeading(pointA,pointB):
    #Code from
    #https://gist.github.com/jeromer/2005586

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def ComputeDistance(pointa,pointb):
    distance = math.sqrt(((pointa[0]-pointb[0])**2) + ((pointa[1]-pointb[1])**2))
    return distance

def ComputeTurnDirection(CurrentHeading, DesiredHeading):
    Turn_Direction = "null"
    difference = DesiredHeading - CurrentHeading
    if(difference > 180 ):
        difference = difference - 360
    elif(difference < -180):
        difference = difference +360

    if(difference > 0):
        Turn_Direction = "Right"
    else:
        Turn_Direction = "Left"

    return Turn_Direction