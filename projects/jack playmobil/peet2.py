from chiplotle import *
from chiplotle.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from chiplotle.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
from chiplotle.geometry.core.label import Label
import numpy as np
import freetype
import math
import pickle
import random
#from texttools  import *
from svgpathtools import svg2paths, Path, Line, Arc, CubicBezier, QuadraticBezier
# from texttools import *

pltmax = [10320, 7920]
plotunit = 0.025 # 1 coordinate unit per plotter = 0.025 mm
#plotunits = (10320/432, 7920/297)
# print plotunits

plotsizemm = [626,309] #in mm breedte x hoogte
plotsize = [plotsizemm[0]/plotunit,plotsizemm[1]/plotunit]

#####configuratieopties
virtualplotting = True  ##False for real plotter, True for virtual
plotbounds = True


layer1scale = 4000   #should be integer factor of layer2scale, or not :)
layer1divs = 20  # lower = faster plotting, less detail, inverse factor of the above regarding to other layers

layer2scale = 4000
layer2divs = 10

layer3scale = 2000
layer3divs = 5

recordsize = 300 ### make this fit next lines sizes!!! (306 + 3 = 309)
backflap = [(6/plotunit,6/plotunit),(306/plotunit,306/plotunit)]
frontflap= [(318/plotunit,6/plotunit),(627/plotunit,306/plotunit)]
#record jackect size = 635mm,312mm
fullzone = [(0,0) , (plotsizemm[0]/plotunit,plotsizemm[1]/plotunit)]




globaloffset = (-10000,-4000) ### position the drwaing on the plotter here

#######CONFIG STOP, do not change below


if (virtualplotting == True):
        plotter = instantiate_virtual_plotter(type="DXY1300")
else:
        plotter = instantiate_plotters( )[0]




def plotchar(char, size, font, xpos, ypos):
#code adapted from freetype-py vector example
    global plotter
    if (char == " "):
        print "space"
        spacefactor = 30
        r = shapes.rectangle(size*spacefactor, size)
        transforms.offset(r, (size*spacefactor/2, 0))
        g = shapes.group([])
        
        g.append(r)
        
    else:
  
        face = freetype.Face(font)
        face.set_char_size( size*64 )
        face.load_char(char)
        slot = face.glyph
        outline = slot.outline
        points = np.array(outline.points, dtype=[('x',float), ('y',float)])
        x, y = points['x'], points['y']
        start, end = 0, 0
        VERTS, CODES = [], []
        # Iterate over each contour
        for i in range(len(outline.contours)):
            end    = outline.contours[i]
            points = outline.points[start:end+1]
            points.append(points[0])
            tags   = outline.tags[start:end+1]
            tags.append(tags[0])

            segments = [ [points[0],], ]
            for j in range(1, len(points) ):
                segments[-1].append(points[j])
                if tags[j] & (1 << 0) and j < (len(points)-1):
                    segments.append( [points[j],] )
            verts = [points[0], ]
            # codes = [Path.MOVETO,]
            for segment in segments:
                if len(segment) == 2:
                    verts.extend(segment[1:])
                    # codes.extend([Path.LINETO])
                elif len(segment) == 3:
                    verts.extend(segment[1:])
                    # codes.extend([Path.CURVE3, Path.CURVE3])
                else:
                    verts.append(segment[1])
                    # codes.append(Path.CURVE3)
                    for i in range(1,len(segment)-2):
                        A,B = segment[i], segment[i+1]
                        C = ((A[0]+B[0])/2.0, (A[1]+B[1])/2.0)
                        verts.extend([ C, B ])
                        # codes.extend([ Path.CURVE3, Path.CURVE3])
                    verts.append(segment[-1])
                    # codes.append(Path.CURVE3)
            VERTS.extend(verts)
            # CODES.extend(codes)
            start = end+1
        g = shapes.group([])
        g.append(shapes.path(VERTS))
    transforms.offset(g, (xpos, ypos))
    # print "size is ", g.width
    plotter.write(g)
    return g.width




  # print VERTS
def writeword(textstring, size, font, xpos, ypos):

	# print (textstring)
	tt = xpos + globaloffset[0]
	for char in textstring:
		tt = tt + plotchar(char, size, font, tt, ypos + globaloffset[1])






def plotzonebounds(zone):
#	plotter.select_pen(1)
    x1,y1 = zone[0]
    x2,y2 = zone[1]
    r = shapes.rectangle((x2-x1), (y2-y1))
    transforms.offset(r,((x2-x1)/2,(y2-y1)/2))
    transforms.offset(r,(x1,y1))
    transforms.offset(r,globaloffset)
    plotter.write(r)


def calculatesvggroup(svg):
	print "PLOTTING stuff"
	# plotter.select_pen(pen)
	g = shapes.group([])
	paths, attributes = svg2paths(svg)
	# print dir(paths[0][0].start.real)
	for path in paths:
		for segment in path:
			if isinstance(segment, Line):
				# print "Line found"
				g.append(shapes.line((segment.start.real,segment.start.imag),(segment.end.real,segment.end.imag)))
			if isinstance(segment, CubicBezier):
				g.append(shapes.bezier_path([(segment.start.real,segment.start.imag),(segment.control1.real,segment.control1.imag),(segment.control2.real,segment.control2.imag),(segment.end.real,segment.end.imag)],0))
	bb = get_bounding_rectangle(g)
	bb = get_minmax_coordinates(bb.points)
	print bb
	print (svg + " is " + str(g.width*plotunit) + "mm")
	print (svg + " is " + str(g.height*plotunit) + "mm")
	# plotter.write(g)
	transforms.offset(g, (-bb[0][0], -bb[0][1] ))
	return({'group': g, 'bounds': bb})
	# io.view(g)

def plotgroup(g,paddingfactor,zone,noisexy,pen):
	plotter.select_pen(pen)
	x1,y1 = zone[0]
	x2,y2 = zone[1]
	maxx = abs(x2-x1)
	maxy = abs(y2-y1)
	xfactor = maxx / g.width/paddingfactor
	yfactor = maxy / g.height/paddingfactor
	if (yfactor <= xfactor):
		scale = yfactor
		transforms.scale(g, scale)
		# transforms.offset(g,((recordsize/plotunit - g.width)/2 , (recordsize/plotunit - g.height)/2))

	else:
		scale = xfactor
		transforms.scale(g, scale)
                # transforms.offset(g,((recordsize/plotunit - g.width)/2 , (recordsize/plotunit - g.height)/2))

		# transforms.offset(g,(0,(y2-y1+g.height)/2))

	print ("SCALE = " + str(scale))
	transforms.offset(g, (x1,y1))
	if not noisexy == (0,0):
		transforms.noise(g,noisexy)
	# plotter.write(g)
	return g


def prismSquare(x,y,scale,divs):
        g = shapes.group([])
        x1 = 0.0
        x2 = 0.0
        div = 1.0 / divs
        for j in xrange(divs + 1):
                p0 = (0,0)
                p1 = (div*j,1)
                q0 = (1,1)
                q1 = (div*j,0)
                #print(p1)
                g.append(shapes.line(p0,p1))
                g.append(shapes.line(q0,q1))

        transforms.scale(g,scale)
        transforms.offset(g,(x,y))
        #plotter.write(g)
        return(g)


def drawheadrays(x,y,i,size,growrate):

#	g.append(shapes.line((0,0),(100,200)))
        for j in xrange(i):
                g = shapes.group([])
                plotter.select_pen((j % 4)+2)
                g.append(shapes.circle(size+j*growrate, segments=500))
                transforms.offset(g, (x,y))
                plotter.write(g)


def dosomeprisms(gx,gy,scale,divs):
        s = shapes.group([])
        for i in xrange(gx):
                for j in xrange(gy):
                        dice = random.randint(0,4)
                        s.append(prismSquare(i*scale,j*scale,scale,divs))
                        transforms.rotate(s,math.radians(dice*90))

        transforms.offset(s,(gx*scale,gy*scale))
        return (s)





#
#########3done with function defs ###### start drawing

if plotbounds:
        ##disable to not plot bounds
        plotter.select_pen(1)
        plotzonebounds(fullzone)
        plotter.select_pen(2)
        plotzonebounds(backflap)
        plotter.select_pen(1)
        plotzonebounds(frontflap)




def plotcover(start,end):
        t = shapes.label(str(start) + "/" + str(end), 0.5, 0.5)
        transforms.offset(t,(200,400))
        transforms.offset(t,globaloffset)
        plotter.write(t)
        plotter.select_pen(2)
        file = "jackpeet.svg"
        shape = calculatesvggroup(file.encode('utf-8'))
        # transforms.rotate(shape,math.radians(random.randint(0,360)))
        # transforms.scale(shape, 0.9)
        #transforms.scale(shape,-1)
        pivotx = 9000
        pivoty = 0
        plotter.select_pen(2)
        # r = shapes.rectangle(1000,1000)
        # transforms.offset(r,(pivotx,pivoty))
        # plotter.write(r)
        jacksize = 100
        jacksizefactor = jacksize*15
        minX = random.randint(318/plotunit,500/plotunit)
        minY = random.randint(6/plotunit,306/plotunit)
        size = random.randint(50,100)
        maxX = random.randint(minX,(627-size)/plotunit)
        maxY = random.randint(6/plotunit,(306-size)/plotunit)
        jackflap= [(minX,minY),(maxX,maxY)]
        jackflap= [(21000,0), (22000,5000)]
        peet = plotgroup(shape['group'],1.2,jackflap,(0,0),2)
        
        transforms.offset(peet,globaloffset)
        bb = get_bounding_rectangle(peet)
        bb = get_minmax_coordinates(bb.points)
        sizeX = (bb[1][0]-bb[0][0]) 
        sizeY = (bb[1][1] -bb[0][1])
        
        transforms.rotate(peet, math.radians(random.randint(0,360)), pivot=(pivotx, pivoty))
        
        transforms.offset(peet, (0, sizeY/2))
        # transforms.offset(peet,(xoff,yoff))

        print(bb)
        print (jackflap)

        plotter.write(peet)

        rec = shapes.rectangle(sizeX,sizeY)
        transforms.offset(rec, (bb[0][0] + sizeX/2, bb[0][1] + sizeY/2))
        # plotter.write(rec)
        # transforms.rotate(peet, math.radians(random.randint(0,360)), pivot=(pivotx, pivoty))
        # plotter.write(peet)

        # shape = calculatesvggroup(file.encode('utf-8'))
        # peet = plotgroup(shape['group'],1.2,frontflap,(0,0),3)
        # transforms.offset(peet,globaloffset)
        # transforms.offset(peet,(3800,1000))
        # transforms.rotate(peet, math.radians(random.randint(0,360)), pivot=(pivotx, pivoty))
        # plotter.write(peet)
        # transforms.rotate(peet, math.radians(random.randint(0,360)), pivot=(pivotx, pivoty))
        # plotter.write(peet)


        # shape = calculatesvggroup(file.encode('utf-8'))
        # peet = plotgroup(shape['group'],1.2,frontflap,(0,0),4)
        # transforms.offset(peet,globaloffset)
        # transforms.offset(peet,(3800,1000))
        # transforms.rotate(peet, math.radians(random.randint(0,360)), pivot=(pivotx, pivoty))
        # plotter.write(peet)
        # transforms.rotate(peet, math.radians(random.randint(0,360)), pivot=(pivotx, pivoty))
        # plotter.write(peet)


        # shape = calculatesvggroup(file.encode('utf-8'))
        # peet = plotgroup(shape['group'],1.2,frontflap,(0,0),5)
        # transforms.offset(peet,globaloffset)
        # transforms.offset(peet,(3800,1000))
        # transforms.rotate(peet, math.radians(random.randint(0,360)), pivot=(pivotx, pivoty))
        # plotter.write(peet)
        # transforms.rotate(peet, math.radians(random.randint(0,360)), pivot=(pivotx, pivoty))
        # plotter.write(peet)
        # transforms.offset(peet,globaloffset)  
        # transforms.rotate(peet, math.radians(random.randint(0,360)), pivot=(pivotx, pivoty))
        # plotter.write(peet)

        # transforms.offset(peet,globaloffset)
        # transforms.rotate(peet, math.radians(random.randint(0,360)), pivot=(pivotx, pivoty))
        # plotter.write(peet)

        # transforms.offset(peet,globaloffset)
        # transforms.rotate(peet, math.radians(random.randint(0,360)), pivot=(pivotx, pivoty))
        # plotter.write(peet)

        # transforms.offset(peet,globaloffset)
        # transforms.rotate(peet, math.radians(random.randint(0,360)), pivot=(pivotx, pivoty))
        # plotter.write(peet)

        # transforms.offset(peet,globaloffset)
        # transforms.rotate(peet, math.radians(random.randint(0,360)), pivot=(pivotx, pivoty))
        # plotter.write(peet)

        # prisms = dosomeprisms(4,4,layer1scale ,layer1divs)
        # scaledprisms = plotgroup(prisms,1,frontflap,(0,0),1)
        # plotter.write(scaledprisms)
        # prisms = dosomeprisms(8,8,layer2scale,layer2divs)
        # scaledprisms = plotgroup(prisms,1,frontflap,(0,0),2)
        # plotter.write(scaledprisms)
        # # prisms = dosomeprisms(16,16,layer3scale,layer3divs)
        # scaledprisms = plotgroup(prisms,1,frontflap,(0,0),4)
        # plotter.write(scaledprisms)

        #drawheadrays(4900,2000,40,60,80)
        #drawheadrays(5000,2000,40,70,70)
        plotter.select_pen(1)
        writeword("S", 40, "3dlet.ttf", 800,10200)
        writeword("ondervan", 18, "powerpuff.ttf", 2600,10700)
        plotter.select_pen(2)
        writeword("M", 20, "3dlet.ttf", 500,9000)
        writeword("ouche", 9, "powerpuff.ttf", 1400,9250)
        writeword("D", 20, "3dlet.ttf", 5000,9000)
        writeword("rouhin", 10, "powerpuff.ttf", 5900,9250)
        # writeword("aa", 16, "neon.ttf", 3500,8300)
        writeword("B", 20, "3dlet.ttf", 500,7500)
        writeword("arocci", 9, "powerpuff.ttf", 1400,7750)
        writeword("M", 20, "3dlet.ttf", 5750,7500)
        writeword("ejami", 9, "powerpuff.ttf", 6650,7750)
        # writeword("eew", 16, "sqd.ttf", 3500,6300)
        writeword("C", 20, "3dlet.ttf", 500,6000)
        writeword("entre", 9, "powerpuff.ttf", 1400,6250)
        writeword("D", 20, "3dlet.ttf", 4750,6000)
        writeword("ata", 9, "powerpuff.ttf", 5650,6250)
        writeword("X", 20, "3dlet.ttf", 8000,6000)
        writeword("D", 20, "3dlet.ttf", 500,4500)
        writeword("ry", 9, "powerpuff.ttf", 1400,4750)
        writeword("D", 20, "3dlet.ttf", 2750,4500)
        writeword("ocks", 9, "powerpuff.ttf", 3650,4750)
        writeword("B", 20, "3dlet.ttf", 500,3000)
        writeword("arocci", 9, "powerpuff.ttf", 1400,3250)
        writeword("M", 20, "3dlet.ttf", 5750,3000)
        writeword("ejami", 9, "powerpuff.ttf", 6650,3250)
        writeword("R", 20, "3dlet.ttf", 5750,2100)
        writeword("eprise", 9, "powerpuff.ttf", 6650,2350)
        # plotter.select_pen(3)
        # writeword("uncomment", 26, "3dlet.ttf", 2000,300)
        plotter.select_pen(random.randint(1,4))

        xpos = 13000
        xoff = 1100
        jacksize = 60
        positions = []
        plotter.select_pen(random.randint(1,4))
        ypos = random.randint(300,7700)
        
        for l in "UNCOMMENT":
            plotter.select_pen(random.randint(1,4))
            ypos = safeYpos(ypos)
            positions.append((xpos,ypos))
            writeword(l, jacksize, "3dlet.ttf", xpos,ypos )
            xpos= xpos + xoff


        p = shapes.path(positions)
        transforms.offset(p,globaloffset)
        transforms.offset(p,(jacksize*24, jacksize*24))

        plotter.write(p)
        
        io.view(plotter)



#plotcover(1,300)

#io.view(plotter)

def safeYpos(ypos):
    newypos = random.randint(300,7700)
    while (abs(newypos - ypos) < 1500 ):
        newypos = random.randint(300,7700)
    return newypos

print('startnumber/stopnumber will be plotted')
startnumber = input('enter startnumber: ')
stopnumber = input('enter stopnumber (eg. 300): ')
#plotter.clear()
for x in xrange(startnumber,stopnumber):
        ready = input('is record ready? press 1 to continue, press 2 for wordtest :')
        print(ready)
        if(ready == 1):
                print x
                plotcover(x, stopnumber)
                # plotter.clear()

        if(ready == 2):
                print x
                plotter.select_pen(4)
                writeword("Triangle_Yur", 10, "USSR.ttf", 1000, 10000)
        else:
                print('press CTRL-C')
