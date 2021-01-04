import bpy
import bmesh
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
#            print("blasah")
            add_cube(location=[locx*1,locy*1,random.random()*3])



def multicubegeom(cubenum, union):
    add_cube = bpy.ops.mesh.primitive_cube_add
    #rot = [23,45,15]
    rot = [random.random()*90,random.random()*90,random.random()*90]
    for i in range(0,int(cubenum),1):
        loc = [random.random()*3, random.random()*3, random.random()*3]
        #rad = random.random()*2
        rad = random.random()*0.2+0.3
        add_cube(location=loc,rotation=rot)
    if (union == 'union'):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.booltool_auto_union()
#        bpy.ops.object.modifier_apply(modifier="Auto Boolean")


def multimulti(xx,yy):
    for x in range(xx):
        for y in range(yy):
            multicubegeom(x*3 + 3*y+1,"union")
    #    bpy.ops.select_all()
            bpy.ops.transform.transform(mode='TRANSLATION', value=(x*4, y*4, 0.0, 0.0))
    #        bpy.ops.btool.auto_union(solver='BMESH')
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


def gridTower(xs,ys,zs):
    grid = D.collections.new('grid')
    C.scene.collection.children.link(grid)
    cubesize=2
    x = 0.0
    y = 0.0
    z = 0.0
    for i in range(0,xs,1):
        for j in range(0,ys,1):
            cubesize=2
            cubeheight = 2
            z = 0.0
            tower = bpy.data.objects.new( 'tower' + str(i), None )
            grid.objects.link(tower)
            zs = random.randint(1,zs)
            for f in range(0,zs,1):
                rot = [0,0, 0]
                x = i*cubesize + random.random()*cubesize-cubesize/2
                y = j*cubesize + random.random()*cubesize-cubesize/3
                randz = random.random()
               
                z = z + random.random()*cubeheight

                loc = (x, y, z)
                bpy.ops.mesh.primitive_cube_add(size=cubeheight, enter_editmode=False, location=loc, rotation=rot)
                grid.objects.link(C.object) #link it with collection
                floor = C.object
                floor.parent = tower
                C.scene.collection.objects.unlink(C.object)
                cubeheight=cubeheight*0.9
    for ob in C.selected_objects:
        ob.select_set(False)
     



def bezierStack():
    add_curve = bpy.ops.curve.primitive_bezier_curve_add
    loc = [random.random()*3, random.random()*3, random.random()*3]
    add_curve(view_align=False, location=loc)
    pass


def addtextstuff(text, x, y, z, scale):
    print ("plottinhG: "+ text)
    bpy.ops.font.open(filepath="//../lib/rus.ttf", relative_path=True)
    for idx,letter in enumerate(text):
        print(idx,letter)
        bpy.ops.object.text_add(enter_editmode=False, location=(idx*scale,0,0))
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

#    bpy.ops.object.select_all(action='SELECT')
#    bpy.ops.object.modifier_apply(modifier="Auto Boolean")
#    bpy.ops.object.booltool_auto_union()
#    bpy.ops.btool.auto_union(solver='BMESH')
    #bpy.ops.mesh.remove_doubles()
    bpy.ops.transform.rotate(value=1.5708, constraint_axis=(True, False, False),  mirror=False, proportional_size=1)
    bpy.ops.transform.rotate(value=-1.5708, constraint_axis=(False, False, True),  mirror=False, proportional_size=1)
    bpy.ops.transform.translate(value=(x, y, z))
   # bpy.context.object.data.extrude = 1
 #   v = bpy.context.object.dimensions
    
#    v[0]
#    bpy.ops.view3d.camera_to_view_selected()
    bpy.ops.view3d.camera_to_view_selected()
    bpy.ops.transform.resize(value=(0.99, 0.99, 0.99), constraint_axis=(False, False, False), mirror=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

def addtext(text, x, y, z, scale):
    bpy.ops.font.open(filepath="//../lib/rus.ttf", relative_path=True)
    bpy.ops.object.text_add(enter_editmode=True, location=(idx*scale,0,0))
    C.object.data.body = text
    bpy.ops.object.editmode_toggle()
    bpy.context.object.data.font = bpy.data.fonts["Russian"]
    bpy.context.object.data.extrude = 0.1
    bpy.context.object.data.bevel_depth = 0.1
    bpy.ops.object.convert(target='MESH')
#    for idx,letter in enumerate(text):
#        print(idx,letter)
       #        bpy.ops.object.editmode_toggle()
#        bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
#        bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
#        bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
#        bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
        
        
        

#    bpy.ops.object.select_all(action='SELECT')
#    bpy.ops.object.modifier_apply(modifier="Auto Boolean")
#    bpy.ops.object.booltool_auto_union()
#    bpy.ops.btool.auto_union(solver='BMESH')
    #bpy.ops.mesh.remove_doubles()
    bpy.ops.transform.rotate(value=1.5708, constraint_axis=(True, False, False),  mirror=False, proportional_size=1)
    bpy.ops.transform.rotate(value=-1.5708, constraint_axis=(False, False, True),  mirror=False, proportional_size=1)
    bpy.ops.transform.translate(value=(x, y, z))
   # bpy.context.object.data.extrude = 1
 #   v = bpy.context.object.dimensions
    
#    v[0]
#    bpy.ops.view3d.camera_to_view_selected()
#    bpy.ops.view3d.camera_to_view_selected()
#    bpy.ops.transform.resize(value=(0.99, 0.99, 0.99), constraint_axis=(False, False, False), mirror=False, proportional_edit_falloff='SMOOTH', proportional_size=1)


def extrudesome(x,y,z,i):
    cursor = (x,y,z)
    master_collection = C.scene.collection
    C.scene.cursor.location = cursor
    strudecube = D.collections.new('strudecube' + str(i))
    C.scene.collection.children.link(strudecube)
    cube = bpy.data.objects.new( 'cube' + str(i), None )
    strudecube.objects.link(cube)
    cubesize = random.random()
    loc = (x, y, z)
    rot = random.random()*90
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=True, location=loc)
    strudecube.objects.link(C.object) #link it with collection
    bpy.ops.object.modifier_add(type='BEVEL')
    C.object.modifiers["Bevel"].width = random.random()*0.5 + 0.1
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier='Bevel')
    
#    list(D.objects['extrudecube'].data.polygons)
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(C.object.data)
#    bpy.ops.object.mode_set(mode='EDIT')
#    bm = bmesh.from_edit_mesh(D.objects['etrudecube' + str(i)].data)
    for face in bm.faces:
        r = random.random()
        if r > 0.2:
            face.select = False
        else:
            face.select = True
#            bmesh.ops.extrude_discrete_faces(bm)
#    
#           
#            bmesh.update_edit_mesh(D.objects['extrudecube'].data, True)
    #bm.faces[1].select = True

    # Show the updates in the viewport
    bmesh.update_edit_mesh(C.object.data, True)
    bpy.ops.mesh.extrude_faces_move(MESH_OT_extrude_faces_indiv={"mirror":False}, TRANSFORM_OT_shrink_fatten={"value":random.random()*2, "use_even_offset":True, "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":False})

    
    
    
    bpy.ops.object.modifier_add(type='WIREFRAME')
    C.object.modifiers["Wireframe"].thickness = random.random() + 0.2
#    bpy.ops.object.select_all(action='SELECT')
#    bpy.ops.editmode_toggle
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier='Wireframe')
#    


def extrudeprogression(seed,sizex,sizey):
    index = 0
    for x in range(sizex):
        for y in range(sizey):
            cursor = (x*8,0,y*8)
            master_collection = C.scene.collection
            C.scene.cursor.location = cursor
            strudecube = D.collections.new('strudecube' + str(x) + "_" +str(y))
            C.scene.collection.children.link(strudecube)
            cube = bpy.data.objects.new( 'cube' + str(x) + "_" +str(y), None )
            strudecube.objects.link(cube)
            cubesize = random.random()*2 + 1
            loc = cursor
            rot = (random.random()*3.14, 0, 0)
            bpy.ops.mesh.primitive_cube_add(size=cubesize, enter_editmode=True, location=loc, rotation=rot)
            strudecube.objects.link(C.object) #link it with collection
            bpy.ops.object.mode_set(mode='EDIT')
            random.seed(seed)
            for gen in range(y):
                for genx in range(x):
                    random.seed(genx)
                bpy.ops.mesh.select_all(action='DESELECT')
                bm = bmesh.from_edit_mesh(C.object.data)
                numfaces = random.randint(1,len(bm.faces))
                print("numfaces = " + str(numfaces))
                if numfaces > 15:
                    numfaces = 15
                for _ in range(numfaces):
                    bm.faces.ensure_lookup_table()
                    random.choice(bm.faces).select = True
                bmesh.update_edit_mesh(C.object.data, True)
                bpy.ops.mesh.extrude_faces_move(MESH_OT_extrude_faces_indiv={"mirror":False}, TRANSFORM_OT_shrink_fatten={"value":random.random()*0.8, "use_even_offset":True, "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":False})
                if gen == 1:
                    bpy.ops.object.modifier_add(type='SUBSURF')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.modifier_apply(modifier='Subdivision')
                    bpy.ops.object.mode_set(mode='EDIT')
                
            bpy.ops.object.mode_set(mode='OBJECT')
                 
#            make unique collection
#            addcube, position
#            select faces using seed


def soloxtrudeprogression(x,z,times,seed):
    #init
    cursor = (x,0,z)
    master_collection = C.scene.collection
    C.scene.cursor.location = cursor
    strudecube = D.collections.new('strudecube')
    C.scene.collection.children.link(strudecube)
    cube = bpy.data.objects.new( 'cube', None )
    strudecube.objects.link(cube)
    cubesize = random.random()
    loc = cursor
    rot = (random.random()*3.14, random.random()*3.14, random.random()*3.14)
    bpy.ops.mesh.primitive_cube_add(size=cubesize, enter_editmode=True, location=loc, rotation=rot)
    strudecube.objects.link(C.object) #link it with collection
    bpy.ops.object.mode_set(mode='EDIT')
    random.seed(seed)
    #start extrusion loop
    for _ in range(times):
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(C.object.data)
        numfaces = random.randint(1,len(bm.faces))
        print("numfaces = " + str(numfaces))
        bm.faces.ensure_lookup_table()
        random.choice(bm.faces).select = True
        bmesh.update_edit_mesh(C.object.data, True)
#        bpy.ops.transform.rotate(value=random.random()*0.5708, constraint_axis=(False, False, True),  mirror=False, proportional_size=1)
        bpy.ops.mesh.extrude_faces_move(MESH_OT_extrude_faces_indiv={"mirror":False}, TRANSFORM_OT_shrink_fatten={"value":random.random()*1.8, "use_even_offset":True, "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":False})
    bpy.ops.object.mode_set(mode='OBJECT')


    
    





############################################################################################
######## RENDER FUNCTIONS ## to be called in order with -r or --render  ####################
############################################################################################



def setFreestyleContext():

    bpy.context.scene.render.use_freestyle = True
    #change to script mode
    # rl = bpy.context.scene.render.layers.active
    # rl.freestyle_settings.mode =  'EDITOR'

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

#addtextstuff("errors and mistakes",0.7)
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
       bpy.context.scene.render.filepath = './output/' + sys.argv[idx+1]

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

#dosomegeom()
#multicubegeom(20,"union")
#multimulti(3,3)
#addtextstuff("errors and mistakes",0.7)
#gridTower(3,3,3)    
##star(12,3)


#i = 0
#for x in range(5):
#    for y in range(5):
#        i = i+1
#        extrudesome(7*x,0,7*y,i)

random.seed(45)
for x in range(2):
    for z in range(2):
        
        # soloxtrudeprogression(x*6,z*6, 30,random.randint(5,15+x*z+z))
        soloxtrudeprogression(x*6,z*6, 30,random.random())

#        addtext("",x*6,0,z*6, 10)
        

fitCam()

setFreestyleContext()
setRenderSize()
renderStuff()