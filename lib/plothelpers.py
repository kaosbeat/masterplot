from chiplotle import *
import datetime
import math

def sign(filename,x,y):
    now = datetime.datetime.now()
    t = shapes.label(str(filename + "    " + now.strftime("%Y-%m-%d %H:%M")),0.15, 0.15, None, None, 'bottom-left')
    transforms.rotate(t, math.radians(90))
    transforms.offset(t, (x,y)) #used to be 160000
    return t
