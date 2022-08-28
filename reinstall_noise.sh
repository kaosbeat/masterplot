#git clone if needed git clone https://github.com/caseman/noise.git
#run python2.7 setup.py build
rm -rf  /home/kaos/Documents/kaotec/masterplot/plotter/lib/python2.7/site-packages/noise-1.2.2.dist-info/
rm -rf  /home/kaos/Documents/kaotec/masterplot/plotter/lib/python2.7/site-packages/noise/
cp -r /home/kaos/Documents/kaotec/masterplot/noise/build/lib.linux-x86_64-2.7/noise/ /home/kaos/Documents/kaotec/masterplot/plotter/lib/python2.7/site-packages/
