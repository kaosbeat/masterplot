from chiplotle import *
from chiplotle.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from chiplotle.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
from chiplotle.geometry.core.label import Label
from chiplotle.core.interfaces.interface import _Interface
from chiplotle.plotters.margins.marginssoft import MarginsSoft
from chiplotle.plotters.margins.marginshard import MarginsHard
import random
import math


plotter = instantiate_virtual_plotter(type="DXY1300")
#plotter = instantiate_plotters()[0]
print(MarginsHard(plotter))
plotter.select_pen(1)
###drawbounds
#plotter.margins.hard.draw_outline()
#bounds = shapes.group([])
#bounds.append(shapes.rectangle(16158,11040))
#plotter.write(bounds)
maingroup = shapes.group([])
cubes = {}

def plotCube(size, x, y):
    points = [(x,y),
              (x + (0.8*size), y - (0.2*size)),
              (x - (0.2*size), y + (0.8*size)),
              (x + (0.3*size), y + (0.5*size)),
              (x + (1.1*size), y + (0.3*size)),
              (x + (0.6*size),y + (0.6*size)),
              (x + (0.9*size),y + (1.1*size)),
              (x + (0.1*size),y + (1.3*size))
    ]
    g = shapes.group([])
    for i in range(1000):
        #print(random.randint(0,7))
        g.append(shapes.line(points[random.randint(0,7)],points[random.randint(0,7)]))
    plotter.write(g)

def connectPoints(g,points,p1,p2):
  g.append(shapes.line(points[p1], points[p2]))
  #print (points[p1][0], points[p1][1])

def fillSquare(p1,p2,p3,p4, density, cubeID):  #parallel lines p1,p2 & p3,p4
    maingroup = shapes.group([])
    cubes[cubeID]["fillType"] = "parallel"
    f =  shapes.group([])
    intervalX = density
    totinterval = (p2[0] - p1[0])/density
#    for i in range(density):
    for i in range(int(totinterval)+1):
 #       vx1 = p1[0] + (p2[0] - p1[0])/density*i
        vx1 = p1[0] + intervalX*i
#        vy1 = p1[1] + (p2[1] - p1[1])/density*i
        vy1 = p1[1] + (p2[1] - p1[1])/totinterval*i
        #vx2 = p3[0] + (p4[0] - p3[0])/density*i
        vx2 = p3[0] + intervalX*i
        #vy2 = p3[1] + (p4[1] - p3[1])/density*i
        vy2 = p3[1] + (p4[1] - p3[1])/totinterval*i
        f.append(shapes.line((vx1,vy1),(vx2,vy2)))
        if (i == 0):
            cubes[cubeID]["vector"] = ((vx1,vy1),(vx2,vy2))
    if "fillSquares" in cubes[cubeID]:
        cubes[cubeID]["fillSquares"].append( [(p1,p2), (p3,p4)] )
    else:
        cubes[cubeID]["fillSquares"] = [(p1,p2), (p3,p4)]
    maingroup.append(f)
    return (maingroup)
    #print(cubes[cubeID])
    #plotter.write(f)

def fillSquareSlanted (p1,p2,p3,p4,density,cubeID,intersectingcubeID, offset):
    cubes[cubeID]["fillType"] = "slanted"
    ##get p1X

    ##get interval (if just one intersectinplaneID, this works, else update code)
    interval = cubes[intersectingcubeID]["fillSquares"][0]
    print(interval)

    ##get intersectioncubefill
    pass

def getKeyY(item):
        return item[1]

def getKeyX(item):
        return item[0]

def fillSquarePerpendicular(p1,p2,p3,p4,density,cubeID):
    maingroup = shapes.group([])
    cubes[cubeID]["fillType"] = "perpendicular"

    f = shapes.group([])
    ### get pointssequence X min  X max, other two  minY, maxY
    l = [p1,p2,p3,p4]
    #print l
    sortedl = sorted(l,key=getKeyX)
    print sortedl
    if (sortedl[1][0] == sortedl[0][0]):
        #do a parallel fill, we're done here
        print ("doinf parallel lines!!")
        return (fillSquare(sortedl[0], sortedl[2], sortedl[1],sortedl[3],density,cubeID))

    else:
        pass

    ## get interval
##    intervalX = ( sortedl[3][0] - sortedl[0][0] ) / density
    intervalX = density
    #get first series of Y coordinates at X interval
    normalvector01 = (sortedl[1][0] - sortedl[0][0], sortedl[1][1] - sortedl[0][1])
#    print normalvector01
    normalvector13 = (sortedl[3][0] - sortedl[1][0], sortedl[3][1] - sortedl[1][1])
    normalvector02 = (sortedl[2][0] - sortedl[0][0], sortedl[2][1] - sortedl[0][1])
    normalvector23 = (sortedl[3][0] - sortedl[2][0], sortedl[3][1] - sortedl[2][1])
    print ("normalvectopr")
    print (normalvector23)
    i = 0
    x1 = 0
    toplist = []
    while x1 < sortedl[1][0] - intervalX:
        x1 = sortedl[0][0] + i * intervalX
        if (normalvector01[0] == 0):
            y1 = sortedl[0][1]
        else:
            y1 = sortedl[0][1] + normalvector01[1] * (intervalX * i) / normalvector01[0]
        i = i + 1
        toplist.append((x1,y1))
        print (x1,y1)
        print("go down")
        print toplist
    j = 0
    print x1
    while x1 < sortedl[3][0] - intervalX:
        x1 = sortedl[0][0] + i * intervalX
        y1 = sortedl[1][1] + normalvector13[1] *   (intervalX * j) / normalvector13[0]
        i = i + 1
        j = j + 1
        toplist.append((x1,y1))
        print (x1,y1)

    i = 0
    x1 = 0
    bottomlist = []
    while x1 < sortedl[2][0] - intervalX:
        x1 = sortedl[0][0] + i * intervalX
        y1 = sortedl[0][1] + normalvector02[1] *   (intervalX * i) / normalvector02[0]
        i = i + 1
        bottomlist.append((x1,y1))
        print (x1,y1)
    print x1
    j = 0
    while x1 < sortedl[3][0] - intervalX:
        x1 = sortedl[0][0] + i * intervalX
        y1 = sortedl[2][1] + normalvector23[1] * (intervalX * (j+1)) / normalvector23[0]
#        y1 = 980 -  999 * 950/10
        i = i + 1
        j = j + 1
        bottomlist.append((x1,y1))
        print (x1,y1)

    for i in range(len(toplist)):
        x1 = toplist[i][0]
        y1 = toplist[i][1]
        x2 = bottomlist[i][0]
        y2 = bottomlist[i][1]
        f.append(shapes.line((x1,y1),(x2,y2)))
    maingroup.append(f)
    return (maingroup)



def oldfillsquares():

    if (p1[1] == p2[1]):
        #do a parallel fill, we're done here
        fillSquare(p1,p2,p3,p4,density,cubeID)
        return
    else:
        pass
#interval?
    print ("points")
    print(p1, p2, p3, p4 )
    normalvector12 = (p2[0] - p1[0], p2[1] - p1[1])
    normalvector14 = (p4[0] - p1[0], p4[1] - p1[1])
    interval = (p3[0] - p1[0]) / density
    print("interval =" + str(interval))
    print("normalvector12 " + str(normalvector12))
    print("normalvector14" + str(normalvector14))
    if (p2[1] == p1[1]):
        interval12Y = 0
    else:
        interval12Y = (normalvector12[1]) / (normalvector12[0]/interval)
    if (p4[1] == p1[1]):
        interval14Y = 0
    else:
        interval14Y = (normalvector14[1]) / ((p4[0]-p1[0])/interval)
    print("interval12Y" + str(interval12Y))
    for i in range(int(interval12Y)):
        x1 = p1[0] + i*interval
        y1 = p1[1] + (normalvector12[1]/normalvector12[0]) * i * interval12Y
        x2 = x1
        y2 = p1[1] + (normalvector14[1]/normalvector14[0]) * i * interval14Y
        f.append(shapes.line((x1,y1),(x2,y2)))
    maingroup.append(f)

def getXinterval (p1,p2,p3,p4):
    pass

def plotDynamicCube(cubeID, size, x, y, a1, a2, a3, f1,f2,f3,f4, density):

    """a1,a2,a3 - slantvectors f1-f4 --fillcorners


#
#                           (6)
#                       _.-+.
#              (2) _.-""     '.
#              +:""            '.
#              J \               '.
#               \ \             _.-+ (5)
#               |  '.       _.-"   L
#               J    \  _.-"      /
#                L (1)+"          J
#           (3)  +    |           |
#                 \   |          .+  (4)
#                  \  |       .-'
#                   \ |    .-'
#                    \| .-'
#                (0)  +'
#


    """
    maingroup = shapes.group([])
    cubes[cubeID] = {}
    a1x = math.cos(a1)
    a1y = math.sin(a1)
    a2x = math.sin(a2)
    a2y = math.cos(a2)
    a3x = math.sin(a3)
    a3y = math.cos(a3)
    points = [(x,y),
              (x + (a3x*size), y + (a3y*size)),
              (x + ((a2x+a3x)*size), y + ((a2y+a3y)*size)),
              (x + (a2x*size), y + (a2y*size)),
              (x + (a1x*size), y + (a1y*size)),
              (x + ((a1x+a3x)*size),y + ((a1y+a3y)*size)),
              (x + ((a3x+a2x+a1x)*size),y + ((a1y+a2y+a3y)*size)),
              (x + ((a1x+a2x)*size),y + ((a1y+a2y)*size))
    ]
    g = shapes.group([])

    # for i in range(100):

    #     g.append(shapes.line(points[random.randint(0,7)],points[random.randint(0,7)]))

    connectPoints(g,points,0,1)
    connectPoints(g,points,1,2)
    connectPoints(g,points,2,3)
    connectPoints(g,points,3,0)
    connectPoints(g,points,0,4)
    connectPoints(g,points,1,5)
    connectPoints(g,points,2,6)
    connectPoints(g,points,3,7)
    connectPoints(g,points,4,5)
    connectPoints(g,points,5,6)
    connectPoints(g,points,6,7)
    connectPoints(g,points,4,7)

    print len(points)

    #for p in range(7):
    #    t = shapes.label("P"+str(p), 0.2, 0.2)
    #    transforms.offset(t, points[p])
    #    g.append(t)

    #fillSquare(points[f1],points[f2],points[f3],points[f4], density, cubeID)
    fill = fillSquarePerpendicular (points[f1],points[f2],points[f3],points[f4], density, cubeID)

    maingroup.append(g)
    maingroup.append(fill)
    return(maingroup)
    ###add cube to memory


#    plotter.write(g)



def cubeStudies():

    for i in range(7):
        # plotDynamicCube(500, i*500, 0, 0, math.radians(i*10), 10, i,i+1,i+2,i+3)
        # plotDynamicCube(500, i*500, 0, 0, math.radians(i*2), 10, 3,2,0,1)
        # plotDynamicCube(500, i*600, 0, random.randint(0,300),0, 100, 0,0,0,0)
        for t in range(5):
            v1 = random.randint(0,7)
            v2= random.randint(0,7)
            v3 = random.randint(0,7)
            v4 = random.randint(0,7)
            plotDynamicCube("cubeH"+str(i)+"V"+str(t),500, i*1000, t*1000, math.radians((t-2)*20), 0, math.radians((i-3)*30), v1,v2,v3,v4, 10)

# plotCube(300, 500, 600)


#plotDynamicCube(600, 100, 0, -20, 20, 10,0,1,3,2)
#plotDynamicCube(1000, 300, -500, 0, 20, 10, 1,2,5,6)
#plotDynamicCube(1000, 300, -500, 0, 20, 10, 4,3,5,6)

def intersectStudy():
    maingroup = shapes.group([])
    plotter.select_pen(1)
    maingroup.append(plotDynamicCube("cube1", 1000, 0,0, 0.1, 0.5, 0.2, 3,2,0,1, 30))
    plotter.write(maingroup)

    maingroup = shapes.group([])
    plotter.select_pen(2)
    maingroup.append(plotDynamicCube("cube2", 800, -600,-200, 0.2, 0, 0.5, 7,6,4,5,30))
    plotter.write(maingroup)


    maingroup = shapes.group([])
    plotter.select_pen(3)
    plotDynamicCube("cube3", 1800, -800,-800, 0.2,0,0.5, 2,6,1,5,30)
    plotter.write(maingroup)
intersectStudy()



#transforms.scale(maingroup, 0.8*11040/maingroup.height)
#transforms.offset(maingroup, (maingroup.width/10, maingroup.height/10))

#plotter.select_pen(2)
#plotter.write(shapes.line((0,0), (2500,0)))
#plotter.write(shapes.line((0,0), (0,2500)))

#print(cubes)
io.view(plotter)
