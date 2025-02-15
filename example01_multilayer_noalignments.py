# -*- coding: utf-8 -*-
"""
ASML_JobCreator - Example 01
    Example usage, to export a text file for import into ASML PAS system.
    Multi-layer job, multiple images per layer, no alignments or mark exposure.
    Very basics of making a Job.

@author: Demis D. John
Univ. of California Santa Barbara
UCSB Nanofabrication Facility: http://www.nanotech.ucsb.edu
2020-01-18


All units are in millimeters.  
Coordinates and sizes are specified as two-valued iterables like [X,Y]
All sizes and shifts are specified at 1x wafer-scale (NOT 4x/5x reticle-scale)

For help: after running once, use commands like:
    help( asml ) -- print package info and contents
    help( MyJob ) -- list functions in the Job class.
    dir( MyJob.Cell ) -- list all options inside the Cell module.
    help( MyJob.Cell.set_CellSize ) -- help on a specific function.
"""

####################################################
# Module setup etc.

import matplotlib.pyplot as plt
import ASML_JobCreator as asml

####################################################

print('Running...')

MyJob = asml.Job()

MyJob.set_comment("Demo Job - Example 1", "Exported from ", "Python ASML_JobCreator")
#print( MyJob.get_comment(), "\n" )    # Return the current comment lines


## Cell Structure:
MyJob.Cell.set_CellSize( [4.00, 4.00] )    # cell size [X,Y] in millimeters
MyJob.Cell.set_MatrixShift( [2.00, 2.00] ) # shift by half a cell

MyJob.set_ExposeEdgeDie()  # allow exposure of die that partially fall off the wafer. See `help(MyJob.set_ExposeEdgeDie)` for more info.


## Image Definition:
#   MyJob.Image( <ImageID>, <ReticleID_Barcode>, sizeXY=coords, shiftXY=coords)
#   see `help( MyJob.Image )`
Res = MyJob.Image("UCSB_Res", "UCSB-OPC1", sizeXY=[3, 3], shiftXY=[4,5])
MA6 = MyJob.Image("UCSB_MA6", "UCSB-OPC1", sizeXY=[2, 2], shiftXY=[-4,-5])
GCA = MyJob.Image("UCSB_GCA", "UCSB-OPC1", sizeXY=[2, 2], shiftXY=[0,-2])


## Image Distribution
#   cellCR is integer pair of Col/Row specificiation
#   shiftXY is floating-point X/Y shift
#   Add each of these to a single exposure location only:
MA6.distribute( cellCR=[-5,-5], shiftXY=[-2.00, -2.00] )
GCA.distribute( cellCR=[5,5], shiftXY=[-2.00, -2.00] )

# Distribute Image "Res" in a 3x3 array with no shift:
for r in [-1,0,1]:
    for c in [-1,0,1]:
        Res.distribute( [c,r] )
    #end for(c)
#end for(r)


## Layer Definition & Reticle Data - 
# Add Zero layer - Required even if no alignments.
ZeroLyr = MyJob.Layer() # Empty Layer with default values

# Choose Images to expose on this Layer:
MetalLyr = MyJob.Layer( LayerID="Metal" )
MetalLyr.expose_Image( Res, Energy=21, Focus=-0.10 )
MetalLyr.expose_Image( MA6, Energy=22 )
MetalLyr.expose_Image( GCA, Energy=22 )

# Print all data added to this Job:
print(MyJob)

# Plot the wafer layout and distributed Images:
MyJob.Plot.plot_wafer()
MyJob.Plot.plot_reticles()
plt.show()

## Export the text file:
MyJob.export('examplejob01_multilayer_noalignments.txt')


print('done.')
