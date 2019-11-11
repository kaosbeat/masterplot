from chiplotle import *
import datetime
import math

def sign(filename):
    now = datetime.datetime.now()
    t = shapes.label(str(filename + "    " + now.strftime("%Y-%m-%d %H:%M")),0.15, 0.15, None, None, 'bottom-left')
    transforms.rotate(t, math.radians(90))
    transforms.offset(t, (16000,0))
    return t
