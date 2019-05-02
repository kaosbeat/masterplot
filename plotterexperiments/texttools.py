# from chiplotle import *
# from chiplotle.tools.plottertools import instantiate_virtual_plotter
import freetype
# import math
# import numpy as np



def plotchar(char, size, font, xpos, ypos):
#code adapted from freetype-py vector example
  global plotter
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
  print "size is ", g.width
  plotter.write(g)
  return g.width




  # print VERTS
def writeword(textstring, size, font, xpos, ypos):
	print (textstring)
	tt = xpos
	for char in textstring:
		tt = tt + plotchar(char, size, font, tt, ypos)






# tt = plotchar('s', 12, 0, 0)
# tt = tt + plotchar('t', 40, tt, 0)
# tt = tt + plotchar('_', 80, tt, 0)
# tt = tt + plotchar('s', 12, tt, 0)
# tt = tt + plotchar('s', 12, tt, 0)
# io.view(plotter)