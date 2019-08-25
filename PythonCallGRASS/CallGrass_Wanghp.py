# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:21:26 2015

Modify startcmd on 2019/8/25

@author: think99

"""

import os
import sys
import subprocess
import binascii
import random
import string
import shutil
import grass.script as gscript
import grass.script.setup as gsetup

grass7bin = r'C:\Program Files\GRASS GIS 7.6\grass76.bat'
myfile = r'H:\pycharm\Grass\Code\clip7.tif'

# Set GISBASE environment variable
gisbase = os.environ['GISBASE'] = 'C:\Program Files\GRASS GIS 7.6'
os.environ['PATH'] += os.pathsep + os.path.join(gisbase, 'extrabin')

# add path to GRASS addons
home = os.path.expanduser("C:\Program Files\GRASS GIS 7.6")
os.environ['PATH'] += os.pathsep + os.path.join(home, 'scripts')
os.environ['PATH'] += os.pathsep + os.path.join(home, 'bin')
# Set GISDBASE environment variable
gisdb = os.path.join(r'C:\Users\HP\Documents', 'grassdata')
location = 'newLocation1'
mapset = 'PERMANENT'

# define GRASS-Python environment
gpydir = os.path.join(gisbase, 'etc', 'python')
sys.path.append(gpydir)

# query GRASS 7 itself for its GISBASE
startcmd = [grass7bin, '--config', 'path']
 
p = subprocess.Popen(startcmd, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
if p.returncode != 0:
        print >>sys.stderr, "ERROR: Cannot find GRASS GIS 7 start script (%s)" % startcmd
        sys.exit(-1)

# location/mapset: use random names for batch jobs
string_length = 4
location = binascii.hexlify(os.urandom(string_length))
mapset   = 'PERMANENT'
location_path = os.path.join(gisdb, location)

# Create new location
startcmd = "\"{0}\" -c \"{1}\" -e \"{2}\"".format(grass7bin, myfile, location_path)

p = subprocess.Popen(startcmd, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
if p.returncode != 0:
    print >>sys.stderr, 'ERROR: %s' % err
    print >>sys.stderr, 'ERROR: Cannot generate location (%s)' % startcmd
    sys.exit(-1)
else:
    print 'Created location %s' % location_path

# Now the location with PERMANENT mapset exists.
os.environ['GISDBASE'] = gisdb
path = os.getenv('PYTHONPATH')
dirr = os.path.join(gisbase, 'etc', 'python')
if path:
    path = dirr + os.pathsep + path
else:
    path = dirr
os.environ['PYTHONPATH'] = path
 
# launch session
gsetup.init(gisbase,gisdb, location, mapset)
gscript.message('Current GRASS GIS 7 environment:')
print gscript.gisenv()

def test_grass(inputdata, outputdata):
    try:
        #input raster map
        output_result1=''.join(random.sample(string.letters,8))
        gscript.run_command("r.in.gdal",input=inputdata,output=output_result1)
        #generate contour vector map
        output_result2=''.join(random.sample(string.letters,8))
        gscript.run_command("r.contour",input=output_result1,output=output_result2,step=300)
        #convert vector map into raster map
        output_result3=''.join(random.sample(string.letters,8))
        gscript.run_command("v.to.rast",input=output_result2,output=output_result3,use="val")
        #overlay raster maps
        output_result4=''.join(random.sample(string.letters,8))
        gscript.run_command("r.patch",input=[output_result3,output_result1],output=output_result4)
        #output raster map
        gscript.run_command("r.out.gdal",overwrite=True,input=output_result4,output=outputdata,format="GTiff")
    finally:
        #delete temporary Location
        shutil.rmtree(os.path.join(gisdb , location))


Inputdata = r'H:\pycharm\Grass\Code\clip7.tif'
Outputdata = r'H:\pycharm\Grass\Code\clip7_output.tif'

test_grass(Inputdata, Outputdata)
