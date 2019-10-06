# blenderplotter
plot images using chiplotle straight form blender using freestyle svg rendering

## references
### general intro to what blender is capable of in terms of creative coding
https://medium.com/@behreajj/creative-coding-in-blender-a-primer-53e79ff71e
### blender python API
https://docs.blender.org/api/current/


## using 
### chiplotle
http://sites.music.columbia.edu/cmc/chiplotle/
with python 2.7 

### blender
with python 3.5.3 API

so using call from the blender script to comunicate with chiplotle
### svgPathTools (python)
https://github.com/mathandy/svgpathtools

## install extra python libraries in blender



###  current use
#### masterscript.sh
we use bash to chain it together
#### open a python 2.7 env
source activate magenta
- make sure plotter is connected or use virtual
./masterscript.sh -Bplotrendertemplate -b "-g multicubegeom(20,'union') --render png -r svg -r size=10" -ftesting -g"masterscript is upandrunning" -t"smooth testing" -c"virtual both"


#### older way
$ /Applications/Blender/blender.app/Contents/MacOS/blender stroketesting.blend --background --python generateandrender.py -- mysvg.svg

this produces an SVG named mysvg.svg
then we pass it on to the next script in a python2.7 env

(python2.7)$ python plotrender.py mysvg.svg




## TODO
### pipeline template
* run script that generates geometry in blender
* render the script  (preferably in the background) to SVG lines
* use differnt linestyles for hidden lines
* pipe the output to chiplotle
* make a git commit

