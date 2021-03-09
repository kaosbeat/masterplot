from chiplotle import *
from chiplotle.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
from chiplotle.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from xml.dom import minidom
# import xpath
from lib.plothelpers import sign
from svgpathtools import svg2paths, svg2paths2, Path, Line, Arc, CubicBezier, QuadraticBezier
import sys

exit

plotunit = 0.025
virtualplotting = sys.argv[2]
#print(virtualplotting)
if (virtualplotting == 'virtual'):
		plotter = instantiate_virtual_plotter(type="DXY1300")
if (virtualplotting == 'real'):
		plotter = instantiate_plotters( )[0]
		print("plotting for real")

envelopesizemm = [320,260]
paper = shapes.rectangle(envelopesizemm[0]/plotunit, envelopesizemm[1]/plotunit)
transforms.offset(paper,(envelopesizemm[0]/plotunit/2,envelopesizemm[1]/plotunit/2))
plotter.select_pen(2)
plotter.write(paper)
pltmax = [16158, 11040]
pltmax = [320/plotunit,260/plotunit]
bounds =shapes.rectangle(pltmax[0],pltmax[1])
transforms.offset(bounds,(pltmax[0]/2,pltmax[1]/2) )
#plotter.write(bounds)

def getGroup(svg, groupname):
	# doc = minidom.parse(svg)  # parseString also exists
	# group = doc.getElementsByID(groupname)
	# doc.unlink()

	# group = xpath.find("//*['id="+groupname+"]",l)
	# return group

#import minidom
# from xml.dom.minidom import parse as p
#parse your XML-document
	doc = minidom.parse(svg)
	#print(doc.childNodes[0].childNodes[1].getAttribute("id"))
	# print doc.getElementById('#fressstylelayer_LineSet')  #>> None
	#print(doc.childNodes[0].childNodes[1].nodeValue)
	# print doc.childNodes[1].childNodes[1].getAttribute("id")
	#Get all child nodes of your root-element or any element surrounding your "target" (in my example "cmmn:casePlanModel")
	nodelist = doc.getElementsByTagName("g")[0].childNodes
	#print(nodelist)
	# i=0
	# for i in range(len(nodelist)):
	# 	if nodelist[i].getAttribute("id") == groupname:
	# 		print ("found it!")
 # 			print nodelist[i]	
	return doc.childNodes[0].childNodes[1]
# #Now find the element via the id-tag
# def find_element(id):
#  #(or whatever you want to do)

#Call find_element with the id you are looking for
# find_element(id)

def calculatesvggroup(svg):
	print ("PLOTTING stuff")
	# plotter.select_pen(pen)
	g = shapes.group([])
	h = shapes.group([])
	paths, attributes, svg_attributes = svg2paths2(svg)
	# print paths
	#paths, attributes = svg2paths(svg)
#	print dir(paths[0][0].start.real)
	for idx, path in enumerate(paths):
		# print('\n')
		# print(idx)
		#print attributes[idx]['stroke']
		stroke = attributes[idx]['stroke']
		layer = h
		if stroke == 'rgb(157, 20, 170)':
			layer = g
		if stroke == '#f0f': 
			layer = g
		if stroke == 'rgb(0, 119, 0)': 
			layer = h
		if stroke == '#0f0': 
			layer = h
		p = []		
		if isinstance(path[0], Line):
			#print("Line instance found", path[0])
			p.append((path[0].start.real,path[0].start.imag))
			pathtype = "line"
		if isinstance(path[0], QuadraticBezier):
			#print("instance found")
			#print(path)
			pathtype = "qbezier"
			p.append((path[0].start.real,path[0].start.imag))
		for segment in path:
			if isinstance(segment, Line):
				p.append((segment.end.real,segment.end.imag))
				#print('still appending lines')
			#	layer.append(shapes.line((segment.start.real,segment.start.imag),(segment.end.real,segment.end.imag)))
			if isinstance(segment, QuadraticBezier):
				#print("Bezier found")
				# p.append(shapes.bezier_path([(segment.start.real,segment.start.imag),(segment.control1.real,segment.control1.imag),(segment.control2.real,segment.control2.imag),(segment.end.real,segment.end.imag)],0))
				p.append((segment.control.real,segment.control.imag))
				p.append((segment.end.real,segment.end.imag))
		# print(sys.argv)
#		if (sys.argv[3] == 'hidden' or sys.argv[3] == 'both'):
		if (layer == h):
			if pathtype == "line":
				layer.append(shapes.path(p))
			if pathtype == "qbezier":
				# print("bezier it is", p)
				layer.append(shapes.bezier_path(p,0.5))
#		if (sys.argv[3] == 'unhidden' or sys.argv[3] == 'both'):
		if (layer == g):
			if pathtype == "line":
				layer.append(shapes.path(p))
			if pathtype == "qbezier":
				# print("bezier it is", p)
				layer.append(shapes.bezier_path(p,0.5))	
	# print(g,h)
	bb = get_bounding_rectangle(g)
	bb = get_minmax_coordinates(bb.points)
	# print (bb)
	print (svg + " is " + str(g.width*plotunit) + "mm")
	print (svg + " is " + str(g.height*plotunit) + "mm")
	# plotter.write(g)
	transforms.offset(g, (-bb[0][0], -bb[0][1] ))
	transforms.offset(h, (-bb[0][0], -bb[0][1] ))
	#scale to fullsize
	# print(g)
	if len(h) > 0:
		sc = min( [12000/g.width, 15000/h.width, 9500/g.height, 9500/h.height])
	else:
		sc = min([12000/g.width, 9500/g.height])
	# print (sc)
	transforms.scale(g, sc)
	transforms.scale(h, sc)
	transforms.offset(g, (500,500))
	transforms.offset(h, (500,500))
	#io.view(g)
	print ("de groepen", len(g), len(h))
	return({'group': [g,h], 'bounds': bb})


def grabSVGandplotWithChiplotle(file):
	# shape = calculatesvggroup(getGroup(file.encode('utf-8'), 'fressstylelayer_LineSet'))
	shape = calculatesvggroup(file.encode('utf-8'))
	print (shape['group'][0])
	if (sys.argv[3] == 'hidden' or sys.argv[3] == 'both'):
		plotter.select_pen(2)
		plotter.write(shape['group'][1])
	if (sys.argv[3] == 'unhidden' or sys.argv[3] == 'both'):
		plotter.select_pen(1)
		plotter.write(shape['group'][0])
	# for idx, gr in enumerate(shape['group']):
	# 	print("plotting group", idx, len(gr))
	# 	plotter.select_pen(idx+1)
	# 	plotter.write(gr)
	




grabSVGandplotWithChiplotle(sys.argv[1])
print (sys.argv[1].rsplit('/')[-1])
plotter.write(sign(sys.argv[1].rsplit('/')[-1], 325/plotunit, 0))
io.export(plotter, "output/out2" , fmt='jpg') #> path needs to be fixed
io.view(plotter)
# io.view(plotter)
