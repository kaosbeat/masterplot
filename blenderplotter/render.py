import bpy
import sys
import random

layers = [False]*20
layers[0] = True


print(sys.argv)
sysargvoffset = 5

def dosomegeom():
    for locx in range(0,15,3):
        for locy in range(0,15,5):
            add_cube(location=[locx*1,locy*1,random.random()*3])

def multicubegeom():
    #rot = [23,45,15]
    cubenum = sys.argv[sysargvoffset+2]
    rot = [random.random()*90,random.random()*90,random.random()*90]
    for i in range(0,int(cubenum),1):
        loc = [random.random()*3, random.random()*3, random.random()*3]
        rad = random.random()*0.2+0.3
        add_cube(location=loc,rotation=rot, radius=rad)


def setFreestyleContext():
    bpy.context.scene.render.layers["fressstylelayer"].use_solid = False
    bpy.context.scene.render.layers["fressstylelayer"].use_halo = False
    bpy.context.scene.render.layers["fressstylelayer"].use_zmask = False
    bpy.context.scene.render.layers["fressstylelayer"].use_all_z = False
    bpy.context.scene.render.layers["fressstylelayer"].use_ztransp = False
    bpy.context.scene.render.layers["fressstylelayer"].invert_zmask = False
    bpy.context.scene.render.layers["fressstylelayer"].use_sky = False
    bpy.context.scene.render.layers["fressstylelayer"].use_edge_enhance = False
    bpy.context.scene.render.layers["fressstylelayer"].use_strand = False
    bpy.context.scene.render.layers["fressstylelayer"].use_freestyle = True

    bpy.context.scene.render.use_freestyle = True
    #change to script mode
    rl = bpy.context.scene.render.layers.active
    rl.freestyle_settings.mode = 'EDITOR'



def setRenderParams():
    
    bpy.context.scene.render.resolution_y = 1500 
    bpy.context.scene.render.resolution_x = 1500
    bpy.context.scene.render.resolution_percentage = 50
    


def renderStuff():
    #render image
    bpy.context.scene.render.filepath = './' + sys.argv[sysargvoffset+1]
    bpy.ops.render.render( write_still=True )

def renderStuff():
    #render image
    bpy.context.scene.render.filepath = './'
    bpy.ops.render.render( write_still=True )   



# dosomegeom()
setFreestyleContext()
setRenderParams()
renderStuff()

