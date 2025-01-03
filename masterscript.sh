#!/bin/bash
### call from python2.7 env
### using gnu-getopt (brew install gnu-getopt > then >   echo 'export PATH="/usr/local/opt/gnu-getopt/bin:$PATH"' >> ~/.bash_profile)
##examples
#  ./masterscript.sh -b "-g multicubegeom(20,'union') --render png -r svg -r size=10"  -ftesting -g"masterscript is upandrunning" -t"smooth testing" -c"real both"
#  ./masterscript.sh -fcircklemess -s"circkles.py"
#detect if we have all arguments
# "-f" filename (mandatory)
    ## png (option)
# "-b" blender options
    ## geom "comma, seperated, list, of, geomfunctions(and their arguments)"
    ## render
        ### png
        ### svg
        ### fssvg (freestyle SVG)
# "-i" inkscape options (scour included)
    ## none (default)
    ## simplify
    ## scour (mandatory if other then none)
# "-c" chiplotle options 
    ## virtual / real
    ## layers
        ### hidden / unhidden
    ## scale (plotsize)
# "-g" git options
    ## if supplied commit with default message
    ## if supplied with argument include it in commit message
# "-p" plot options
    ## virtual or real

# "-P" projectname
    ## required, name of directory where project specific files live, such as blender file, and blendpython function fiel and chiplotle files etc


####https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash
# saner programming env: these switches turn some bugs into errors
set -o errexit -o pipefail -o noclobber -o nounset

! getopt --test > /dev/null 
if [[ ${PIPESTATUS[0]} -ne 4 ]]; then
    echo 'I’m sorry, `getopt --test` failed in this environment.'
    exit 1
fi

OPTIONS=f:b:B:i::c:g::t::s:p:P:
LONGOPTS=file:,blender:,blenderfile:,inkscape::,chiplotle:,git::,twitter::,script:,plot:,project:

! PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTS --name "$0" -- "$@")
if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
    # e.g. return value is 1
    #  then getopt has complained about wrong arguments to stdout
    exit 2
fi
# read getopt’s output this way to handle the quoting right:
eval set -- "$PARSED"

echo "$PARSED"
f=nf B=nB b=nb c=nc ink=ni g=ng t=nt chip=0 s=ns githash='' script=0 blend=0 p=np P=nP
# now enjoy the options in order and nicely split until we see --

while true; do
    case "$1" in
        -f|--file)
            echo "encounterd F $2"
            basename=$2
            f="$2_$(date +"%m_%d_%Y_%H%M")"
            #var=$(expr $iter + $varoffset)
            echo $f
            shift 2
            ;;
        -b|--blender)
            echo "encounterd b $2"
            blend=1
            b="$2"
            shift 2
            ;;
        -B|--blenderfile)
            echo "encounterd B $2"
            B="$2"
            shift 2
            ;;
        -i|--inkscape)
            echo "$1" "$2"
            echo "encounterd I $2"
            case "$2" in
                "") ink='some default value' ; shift 2 ;;
                *) ink=$2 ; shift 2 ;;
            esac ;;
        -c|--chiplotle)   ### specify virtual or real plotter anyways, until resolved
            echo "encounterd C $2"
            c="$2"
            chip=1
            shift 2
            ;;
        -s|--script)
            echo "encounterd S $2"
            s="$2"
            script=1
            shift 2
            ;;
        -g|--git)
            echo "$1" "$2"
            echo "encounterd G $2"
            g=dogit
            case "$2" in
                "") gitmsg='default commit message, not feeling creative' ; shift 2 ;;
                *) gitmsg=$2 ; shift 2 ;;
            esac ;;
        -t|--twitter)
            echo "$1" "$2"
            echo "encounterd T $2"
            t=dotweet
            case "$2" in
                "") tweet='default tweetmessage, not feeling creative, look at the picture' ; shift 2 ;;
                *) tweet=$2 ; shift 2 ;;
            esac ;;
        -p|--plot)
            echo "encounterd p $2"
            p="$2"
            shift 2
            ;;
        -P|--project)
            echo "encounterd Project $2"
            P="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Programming error"
            exit 3
            ;;
    esac
    #iter=$(expr $iter + 1)
done

#handle non-option arguments
if [[ $f == nf ]]; then
    echo "output filename is required. set it using -f and do it like -fMyFile and not -f MyFile"
    exit 4
fi

if [[ $P == nf ]]; then
    echo "project name == subdirectory of projects is required"
    exit 4
fi

echo "filename: $f, blenderopts: $b, inkscapeopts: $ink, chiplotleopts: $c, Blendfile: $B, Project: $P"


pngname=$f.png
###calling BLENDER

#### ['/Applications/Blender.app/Contents/MacOS/Blender', '--log-file', 'logfile', 'projects/blenderplotter/plotrendertemplate.blend', '--background', '--python', 'projects/blenderplotter/generateandrender.py', '--', '-g', "multicubegeom(2,'union')", '--render', 'png', '-r', 'svg', '-r', 'size=10', '-f', 'testing_03_08_2021_1738', '-P', 'blenderplotter']
echo $b
if [ $blend == 1 ]; then
    echo "we're doing blender"
    if [ $B == nB ]; then
        echo "no blenderfile supplied, please specify using -B / -blenderfile, use filename, not path, file should be in same directory"
        exit
    fi
    # linux

    # osx
    /Applications/Blender.app/Contents/MacOS/Blender --log-file logfile projects/$P/$B.blend --background --python projects/$P/generateandrender.py -- $b -f $f -P $P
    # svgfilename=$f.svg
    svgfilename=$f
    svgfilename+=0000.svg ### blender appends this.... need to keep it in sync
    echo $svgfilename
else
    echo "we're not doing blender"
    svgfilename=$f.svg
    echo $svgfilename
fi

tweetimg=$pngname

#### calling inkscape  <<<<< needs filenamefixing
if [ $ink != ni ]; then
    cp $PWD/$filename $PWD/processed_$filename
    /usr/local/bin/inkscape $PWD/processed_$filename --verb EditSelectAll --verb SelectionSimplify --verb FileSave --verb FileQuit
    # python plotrender.py $PWD/processed_$filename $3 $5
fi


#### calling additional script
### the script must accept a filename (absolute path) as argument and write a jpg using chiplotle.tools.io.export(plotter, filename, fmt='jpg')
if [ $script == 1 ]; then
echo "projects/$P/$s $PWD/projects/$P/output/$f $p"
    python projects/$P/$s $PWD/output/$f $p
    if [ $t != nt ]; then
        tweetimg=$PWD/tmp/$f.jpg
    fi
fi


#### calling chiplotle with the svgplotter arguments are in order!! real/virtual hidden/unhidden/both so pass as -c"real both" or --chiplotle"real unhidden"
if [ $chip == 1 ]; then
    # python plotrender.py $PWD/projects/$P/output/$svgfilename $c
    echo "CALLING CHIPLOTLE"
    echo $PWD/output/$svgfilename $c
    python plotrender.py $PWD/output/$svgfilename $c

fi
 

##call git
if [ $g == dogit ]; then
    echo "Now really doing GIT"
    echo `git add $PWD/projects/$P`
    git add $PWD/projects/$P
    FILE=$PWD/output/$svgfilename
    if test -f "$FILE"; then
        git add $PWD/output/$svgfilename
    fi
    FILE=$PWD/tmp/seed.txt
    if test -f "$FILE"; then
        # git add $PWD/tmp/seed.txt   
        SEED=`cat $PWD/tmp/seed.txt`
        git commit -a -m "plotting with seed $SEED"
    else
        git commit -a -m "$gitmsg"
    fi
   
    githash=`git rev-parse HEAD`
fi


##post to twitter? >>>> if calling extra script, $tweetimg might have correct filename, else use SVG > check format in in tweetplot.py
if [ $t != nt ]; then
    echo "$tweetimg"
    FILE=$PWD/tmp/seed.txt
    if test -f "$FILE"; then
        # git add $PWD/tmp/seed.txt 
        SEED=`cat $PWD/tmp/seed.txt`
        tweet+="the githash is $tweet and the seed to recreate is $SEED"
    fi
    python lib/tweetplot.py "$tweet $githash" $PWD/output/$svgfilename
fi