from chiplotle import *


from chiplotle.tools.plottertools import instantiate_virtual_plotter
plotter =  instantiate_virtual_plotter(type="DXY1300")


# interesting https://en.wikipedia.org/wiki/3D_projection#Perspective_projection

import math
import random


#helpers
def fib(n):
    return ((1+math.sqrt(5))**n-(1-math.sqrt(5))**n)/(2**n*math.sqrt(5))

def expd(base, height, inc, maxn):
    divlist = []
    curheight = base
    for i in range(maxn):
        if (sum(divlist) < height):
            divlist.append(curheight)
            curheight = curheight*inc
    return divlist


def baselines(vpx,vpy, width, height, denx,deny,base,inc,maxdiv ):
    """
    vpx, vpy vanishing point
    denx, deny density (0,1)
    maxdiv absolute max divisions
    """
    perspectivegrid = []
    #caclulate horizontal lines
    horlinelist = []
    ystart = 0
#    xstart = 0 - width
    prevy = ystart
    divlist = []
    curheight = base
    xstart = -width/2
    xend = width/2
#    calculate horizontal lines
    for i in range(maxdiv):
        if (sum(divlist) < height):
            horlinelist.append([(xstart,prevy), (xend,prevy)])
            divlist.append(curheight)
            curheight = curheight*inc
            prevy = prevy + curheight
    perspectivegrid.append(horlinelist)

    xhop = width/maxdiv
    vertlinelist = []
    for i in range(maxdiv):
        vertlinelist.append([(vpx,vpy),(xstart+xhop*i,ystart)])

    perspectivegrid.append(vertlinelist)

    return perspectivegrid





def sun(draw, radius, visiblepart, xpos, ypos):
    """
    if draw == true add lines to plotter.write, else return
    radius = duh, radius
    visiblepart = % above horizon as 0-1
    """
    print()

def filledcircle(cx,cy,radius,rate, full):

    a = np.linspace(0, 2*np.pi, rate)
    g = shapes.group([])
    for i in xrange(1,rate):
        # print((x[i-1]*radius,y[i]*radius),(x[i]*radius, y[i]*radius))
	# g.append(shapes.line())
	# g.append(shapes.line((x[i-1]*radius,y[i]*radius),(x[i]*radius, y[i]*radius)))
	# g.append(shapes.line(
	# 	( cx + radius * np.cos(a[i-1]) , cy + radius * np.sin(a[i-1]) ),
	# 	( cx + radius * np.cos(a[i]),cy + radius * np.sin(a[i]) )))
	#figure out how to get point at certin y-value
	# x^2 + y^2 = r^2
	x0 = radius * np.cos(a[i-1])
	# y0 = np.sqrt(radius^2 - int(x0)^2)
	y0 = np.sqrt(radius**2 - x0**2)

	# x1 = np.sqrt(radius^2 - y0^2)

	g.append(shapes.line((x0,y0),(-x0,y0)))
	if (full == 1):
	    g.append(shapes.line((x0,-y0),(-x0,-y0)))
    transforms.offset(g, (cx,cy))
    plotter.write(g)





def plot():
    plotter.clear()
    plotter.select_pen(2)
    plotter.write(shapes.line((0,-10000),(0,10000)))
    plotter.select_pen(3)
    plotter.write(shapes.line((-10000,0),(10000,0)))
    plotter.select_pen(1)
    plotter.write(shapes.rectangle(14158,9040))
    plotter.set_plot_window((2000,2000), (6000,6000))
    g = shapes.group([])
    # prevy = 0
#    for y in (expd(300,12000,0.9,23)):
 #       g.append(shapes.line((-3000,prevy),(3000,prevy)))
  #      prevy = prevy + y
   #     print(prevy)
    width = 12000
    grid = baselines(0,15000,width,4000, 0.5,0.5,300,0.8,50)
    hgridmaxy = grid[0][-1][1][1]
    yvec = 0.0
    for l in grid[0]:
        g.append(shapes.line(l[0],l[1]))
    for l in grid[1]:
        #get x = y/xfactor
        if (l[1][0] == 0):
            yvec = 0.0
        else:
            yvec = float(l[1][0])/float(l[0][1])
        print(l[0][1], l[1][0], yvec)
        if (l[1][0] > width/2):
            pass
        g.append(shapes.line((yvec * hgridmaxy ,hgridmaxy),l[1]))

    print(grid[1])

    plotter.write(g)

    plotter.select_pen(2)
    filledcircle(0,hgridmaxy,500,100,0)




plot()
io.view(plotter)
