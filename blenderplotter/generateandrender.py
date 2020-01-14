import bpy
C = bpy.context 
D = bpy.data

import random
import sys
import argparse
#import tracery
#from tracery.modifiers import base_english
from math import pi



layers = [False]*20
layers[0] = True
print(sys.argv)
sysargvoffset = 5




############################################################################################
######## GEOMETRY FUNCTIONS ## to be called in order with -g or --geom  ####################
############################################################################################
def dosomegeom():
    add_cube = bpy.ops.mesh.primitive_cube_add
    for locx in range(0,15,3):
        for locy in range(0,15,5):
            print("blasah")
            add_cube(location=[locx*1,locy*1,random.random()*3])



def multicubegeom(cubenum, union):
    add_cube = bpy.ops.mesh.primitive_cube_add
    #rot = [23,45,15]
    rot = [random.random()*90,random.random()*90,random.random()*90]
    for i in range(0,int(cubenum),1):
        loc = [random.random()*3, random.random()*3, random.random()*3]
        #rad = random.random()*2
        rad = random.random()*0.2+0.3
        add_cube(location=loc,rotation=rot, radius=rad)
    if (union == 'union'):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.modifier_apply(modifier="Auto Boolean")
        bpy.ops.btool.auto_union(solver='BMESH')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.view3d.camera_to_view_selected()


def star(num_arms, arms_length):
    x = 0.0
    y = 0.0
    z = 0.0
    yrot = 0
    cursor = (x,y,z)
    master_collection = C.scene.collection
    C.scene.cursor.location = cursor
    #add_cube = bpy.ops.mesh.primitive_cube_add
    p_up = 0.0
    star = D.collections.new('star')
    C.scene.collection.children.link(star)
    rotmod = num_arms/6
    
    #bpy.ops.outliner.collection_new(nested=True)
    
    for i in range(0,num_arms,1):
        cubesize=2
        x = 0.0
        y = 0.0
        z = 0.0
        arm = bpy.data.objects.new( 'arm' + str(i), None )
        #layer_collection = D.collections.new('arm' + str(j))
        #C.scene.collection.children.link(layer_collection)
        #C.scene.collection.objects.link(arm)
        star.objects.link(arm)
        p_up = 1/num_arms * i
        p_up = random.random()
        for j in range(0,arms_length,1):
            #layer_collection = bpy.data.collections['arm' + str(j)]
            rot = [0,0, 2*pi/arms_length*j]
            x = x + random.random()*cubesize-cubesize/2
            y = y + cubesize
            randz = random.random()
            if (randz > p_up):
                z = z + random.random()*cubesize
            else:
                z = z - random.random()*cubesize
            loc = (x, y, z)
            bpy.ops.mesh.primitive_cube_add(size=cubesize, enter_editmode=False, location=loc, rotation=rot)
            star.objects.link(C.object) #link it with collection
            armstep = C.object
            armstep.parent = arm
            master_collection.objects.unlink(C.object)
            cubesize=cubesize*0.8
        for ob in C.selected_objects:
            ob.select_set(False)
        print(int(i%rotmod))
        D.objects['arm' + str(i)].select_set(True)
        #C.scene.objects.active = D.objects['arm' + str(i)]
        if (int(i%rotmod) == int(rotmod-1)):
            print("rotmod =" + str(rotmod) + ", i =" + str(i))
            yrot = yrot+1
            print("yrot = " + str(yrot))
        bpy.ops.transform.rotate(value = 2*pi/6*yrot, orient_axis='X' )
        bpy.ops.transform.rotate(value = 2*pi/rotmod*i, orient_axis='Z' )

    bpy.ops.object.select_all(action='SELECT')
    # use booltool addon
    bpy.ops.object.booltool_auto_union()
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.view3d.camera_to_view_selected()


def gridTower():
    grid = D.collections.new('grid')
    C.scene.collection.children.link(grid)
    cubesize=2
    x = 0.0
    y = 0.0
    z = 0.0
    for i in range(0,3,1):
        for j in range(0,3,1):
            cubesize=2
            Zz = 0.0
            tower = bpy.data.objects.new( 'tower' + str(i), None )
            grid.objects.link(tower)
            for f in range(0,3,1):
                rot = [0,0, 0]
                x = i*cubesize + random.random()*cubesize-cubesize/2
                y = j*cubesize 
                randz = random.random()
                if (randz > 0.1):
                    z = z + random.random()*cubesize
                else:
                    z = z - random.random()*cubesize
                loc = (x, y, z)
                bpy.ops.mesh.primitive_cube_add(size=cubesize, enter_editmode=False, location=loc, rotation=rot)
                grid.objects.link(C.object) #link it with collection
                floor = C.object
                floor.parent = tower
                C.scene.collection.objects.unlink(C.object)
                cubesize=cubesize*0.8
    for ob in C.selected_objects:
        ob.select_set(False)
     




def bezierStack():
    add_curve = bpy.ops.curve.primitive_bezier_curve_add
    loc = [random.random()*3, random.random()*3, random.random()*3]
    add_curve(view_align=False, location=loc)
    pass


def addtextstuff(text, scale):
    print ("plottinhG: "+ text)
    #bpy.ops.font.open(filepath="//../plotterexperiments/rus.ttf", relative_path=True)
    for idx,letter in enumerate(text):
        print(idx,letter)
        bpy.ops.object.text_add(view_align=False, enter_editmode=False, location=(idx*scale,0,0))
        bpy.ops.object.editmode_toggle()
        bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
        bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
        bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
        bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
        bpy.ops.font.text_insert(text=letter)
        bpy.ops.object.editmode_toggle()
        bpy.context.object.data.font = bpy.data.fonts["Russian"]
        bpy.context.object.data.extrude = 0.1
        bpy.context.object.data.bevel_depth = 0.1
        bpy.ops.object.convert(target='MESH')

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.modifier_apply(modifier="Auto Boolean")
    bpy.ops.btool.auto_union(solver='BMESH')
    #bpy.ops.mesh.remove_doubles()
    bpy.ops.transform.rotate(value=1.22173, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.transform.translate(value=(-8.2, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True, use_accurate=False)
   # bpy.context.object.data.extrude = 1
 #   v = bpy.context.object.dimensions
    
#    v[0]
    bpy.ops.view3d.camera_to_view_selected()
    bpy.ops.transform.resize(value=(0.99, 0.99, 0.99), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

############################################################################################
######## RENDER FUNCTIONS ## to be called in order with -r or --render  ####################
############################################################################################



def setFreestyleContext():

    bpy.context.scene.render.use_freestyle = True
    #change to script mode
    # rl = bpy.context.scene.render.layers.active
    # rl.freestyle_settings.mode = 'EDITOR'

def setRenderSize():
    bpy.context.scene.render.resolution_y = 2970 
    bpy.context.scene.render.resolution_x = 4200
    bpy.context.scene.render.resolution_percentage = 50

def renderToSVG(filename):
    bpy.data.window_managers["WinMan"].ruta = "/Users/kaos/Documents/005_plotter/blenderplotter/algo3.svg"
    bpy.ops.export.svg()

def fitCam():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.view3d.camera_to_view_selected()
    
def renderStuff():
    #render image
    C.scene.svg_export.use_svg_export = True
    bpy.ops.render.render( write_still=True )
    


rules = {
    'origin': '#hello.capitalize#, #location#!',
    'hello': ['hello', 'greetings', 'howdy', 'hey'],
    'location': ['world', 'solar system', 'galaxy', 'universe']
}

#grammar = tracery.Grammar(rules)
#grammar.add_modifiers(base_english)

#def dostufff():
  #  print(grammar.flatten("#origin#"))  # prints, e.g., "Hello, world!"
#    return(grammar.flatten("#origin#"))


#dosomegeom()
#multicubegeom(sys.argv[sysargvoffset+2], sys.argv[sysargvoffset+3])

#bezierStack()

# #addtextstuff("errors and mistakes",0.7)
# text = dostufff()
# addtextstuff(text,0.7)
#addtextstuff(sys.argv[sysargvoffset+4],0.7)
#setFreestyleContext()
#setRenderParams()
#renderStuff()
# print("doing: " + sys.argv[sysargvoffset+3])


for idx,a in enumerate(sys.argv):
   if a == '-f':
       print('setting filepath')
       bpy.context.scene.render.filepath = './' + sys.argv[idx+1]

   if a == '-g' or a == '--geom':
       print("hell yeah")
       print(sys.argv[idx+1])
       eval(sys.argv[idx+1])

   if a == '-r' or a == '--render':

       print("rendering")
       fitCam()
       setFreestyleContext()
       setRenderSize()
       renderStuff()
# #dosomegeom()

#gridTower()    
# star(12,3)

# fitCam()

# setFreestyleContext()
# setRenderSize()
# renderStuff()