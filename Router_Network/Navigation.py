#############################################
#
#   Navigation.py
#
#   Support point to point navigation
#
############################################

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

def ComputeHeading():
    heading = 0

    return heading