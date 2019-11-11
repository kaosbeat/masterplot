from chiplotle import *
from chiplotle.tools.io import export
# from PIL import Image
import math
import random
import sys
from plothelpers import sign

from chiplotle.tools.plottertools import instantiate_virtual_plotter
virtualplotting = sys.argv[2]

#print(virtualplotting)
if (virtualplotting == 'virtual'):
		plotter = instantiate_virtual_plotter(type="DXY1300")
if (virtualplotting == 'real'):
		plotter = instantiate_plotters( )[0]
		print("plotting for real")

pltmax = [16158, 11040]

pltmax = [10000, 10000]
bounds =shapes.rectangle(pltmax[0],pltmax[1])
transforms.offset(bounds,(pltmax[0]/2,pltmax[1]/2) )
plotter.select_pen(1)
plotter.write(sign(sys.argv[1]))
# plotter.write(bounds)

def fillsquare(xoffset,yoffset,width,height,angle,interval,outline):
    r = shapes.group([])
    if (outline == 1):
        o = shapes.rectangle(width,height)
        transforms.offset(o, (width/2,height/2))
        r.append(o)
    for x in xrange(int(width/interval)):
        r.append(shapes.line((x*interval,0),(x*interval,height)))
    transforms.offset(r,(xoffset,yoffset))
    return r
# plotter.write(fillsquare(5000,300,1000,1000,90,80,1))


def doPattern(totalwidth, totalheight, xdiv, ydiv):
    margin = 500
    xcursor = 0
    ycursor = 0
    avgwidth = totalwidth/xdiv
    avgheight = totalheight/ydiv
    interval = avgwidth/100
    p = shapes.group([])
    for x in xrange(xdiv):
        for y in xrange(ydiv):
            maxx = totalwidth - xcursor
            maxy = totalheight- ycursor
            w = avgwidth - margin/2 + random.randint(0,margin)
            h = avgheight - margin/2 + random.randint(0,margin)
            sqint = interval - margin/20 + random.randint(0,margin/10)
            if sqint < 0:
                print ("squint was only:", sqint)
                sqint = math.fabs(sqint)
            if sqint == 0:
                print ("squint was 0")
                sqint = 10
            if w > maxx: 
                w = maxx
            if y > maxy:
                h = maxy
        
            sq = fillsquare(0,0,w,h,90,sqint,1)
            transforms.offset(sq, (xcursor,ycursor))
            p.append(sq)
            ycursor=y*avgheight
        xcursor=x*avgwidth
    return p
# plotter.write(doPattern(15000,11000,4,4))

def progressivepattern(width,height):
    p = shapes.group([])
    done = 0 
    zones = []
    cursor = [0,0]
    while done == 0:
        xsq = random.randint(1000,3000)
        ysq = random.randint(2000,5000)
        zones.append([xsq,ysq])
        z = fillsquare(0,0,xsq,ysq,90,random.randint(20,35),0)
        transforms.offset(z,(cursor[0],cursor[1]))
        cursor[0] = cursor[0] + xsq
        if cursor[0] > width:
            done = 1
        p.append(z)
    return p        

# plotter.write( progressivepattern(15000,12000))


def subdivpattern(xoffset,yoffset,width,height,generations,numtypes):
    types = [60, 65, 75, 64, 80]
    p = shapes.group([])
    # zones = [[[0,0,width,height], [100,100,130,130]]]
    zones = [ [[0,0,width,height]] ]
    # zones = [ [[0, 0, 10000, 10000]], [[[0, 0, 8692, 6689], [0, 6689, 8692, 10000], [8692, 6689, 10000, 10000], [8692, 0, 10000, 6689]]]]

    for gen in xrange(generations):
        zones.append([])
        for sq in zones[gen]:
            #print(zones[gen])
            #print(sq[0], sq[1])
            # x = random.randint((sq[2]-sq[0])/2-width/10,(sq[2]-sq[0])/2+width/10)
            # y = random.randint((sq[3]-sq[1])/2-height/10 ,(sq[3]-sq[1])/2+height/10)
            print(sq[0],sq[2]-sq[0])
            print(sq[1],sq[3]-sq[1])
            # x = (sq[2]-sq[0])/2 + random.randrange(-500,500)
            # y = (sq[3]-sq[1])/2 + random.randrange(-500,500)
            x = random.randint(sq[0],sq[0]+(sq[2]-sq[0])/2)
            y = random.randint(sq[1],sq[1]+(sq[3]-sq[1])/2)

            zones[gen+1].append([sq[0],sq[1],x,y])
            zones[gen+1].append([sq[0],y,x,sq[3]])
            zones[gen+1].append([x,y,sq[2],sq[3]])
            zones[gen+1].append([x,sq[1],sq[2],y])
            print(zones)
    # for idx,z in enumerate(zones):
    for idx,s in enumerate(zones[generations]):
        if idx < 2:
            filltype = types[1]
        else:
            filltype = types[random.randint(0,4)]
        r = fillsquare(s[0],s[1],s[2]-s[0],s[3]-s[1],90,filltype,0)
        # transforms.offset(r, (s[0],s[1]))
        # p.append(r)
        # plotter.select_pen(idx+1)
        transforms.offset(r,(xoffset,yoffset))
        plotter.write(r)
    # return p

# plotter.write(subdivpattern(10000,10000,1,2))
# plotter.select_pen(1)
# subdivpattern(0,0,3000,10000,4,2)
# plotter.select_pen(2)
# subdivpattern(2500,0,10000,10000,3,2)
# plotter.select_pen(1)
# subdivpattern(7500,0,7500,10000,2,2)

for x in xrange(8):
    for y in xrange(5):
        xs = x*random.randint(0,100)
        ys = y*random.randint(0,100)
        w = random.randint(0,5000)
        h = random.randint(0,5000)
        subdivpattern(xs+(x*1000),ys+(y*1000),w,h,3,4)

export(plotter, sys.argv[1], fmt='jpg')
export(plotter, sys.argv[1], fmt='svg')
io.view(plotter)
