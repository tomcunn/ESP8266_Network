#################################################
#
#   Process the incoming IR Camera Data
#
#
#
#################################################

def ProcessCameraData(data):
    x1,y1,x2,y2 = 0,0,0,0
    if(data[0] == 0x80 and len(data) >= 13):
        x1 = data[1] + data[2]*256
        y1 = data[4] + data[5]*256

        x2 = data[7] + data[8]*256
        y2 = data[10] + data[11]*256
        #print(x1,y1)
    return (x1,y1,x2,y2)
