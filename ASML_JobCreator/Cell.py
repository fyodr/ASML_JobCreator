"""
This file is part of the ASML_JobCreator package for Python 3.x.

Cell.py
    Contains class Cell, for setting Wafer Layout > Cell Structure properties.
    

- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *    # global variables/methods to the module.


####################################################




class Cell(object):
    """
    Class for defining Wafer Layout > Cell Structure
    
    Cell(  ):
        Creates empty object with default values.
        
    """
    
    def __init__(self, parent=None):
        '''Creates empty object.'''
        self.parent = parent    # parent Job object
        self.RoundEdgeClearance = Defaults.ROUND_EDGE_CLEARANCE
        self.FlatEdgeClearance = Defaults.FLAT_EDGE_CLEARANCE
        self.EdgeExclusion = Defaults.EDGE_EXCLUSION
    #end __init__
    
    
    def __str__(self, tab=0):
        '''Return string to `print` this object. Indent the text with the `tab` argument, which will indent by the specified number of spaces (defaults to 0).'''
        s = ""
        s += " "*tab + "ASML_JobCreator.Cell object:\n"
        s += " "*tab + " Cell Size = " + str( self.get_CellSize() ) + " mm\n"
        s += " "*tab + " Cell Matrix Shift = " + str( self.get_MatrixShift() ) + " mm\n"
        s += " "*tab + " Die Per Cell = %s; Minimum for exposure = %i die\n" %( str( self.get_NumberDiePerCell() ), self.get_MinNumberDie() )
        s += " "*tab + " Edge Exclusion = %0.6f mm\n" % self.get_EdgeExclusion()
        s += " "*tab + " Round/Flat Clearance = %0.6f mm / %0.6f mm\n" % ( self.get_RoundEdgeClearance() , self.get_FlatEdgeClearance() )
        return s
    #end __str__
    
    
    def copy(self):
        ''' Returns a copy of this object.  Uses copy.deepcopy() to ensure all pointers are actually copied instead of referenced.'''
        from copy import deepcopy   # to make copies instead of only references
        return deepcopy(self)
    #end copy()
    
    
    
    ##############################################
    #       Setters/Getters
    ##############################################
    def set_CellSize(self, xy=[10,10] ):
        '''Set the Cell Size in millimeters, [x,y].'''
        if len(xy)==2: 
            self.CellSize = (xy[0], xy[1])
        else:
            raise ValueError("Expected x,y pair of numbers, instead got: " + str(xy))
    #end
    
    def get_CellSize(self):
        '''Return Cell Size in mm, as two-valued list.'''
        try:
            return self.CellSize
        except AttributeError:
            if WARN(): print("Using default values for `CellSize`.")
            self.set_CellSize( Defaults.CELL_SIZE)
            return self.CellSize
    #end
    
    
    def set_MatrixShift(self, xy=[0,0] ):
        '''Set the Cell Matrix Shift in millimeters, [x,y].'''
        if len(xy)==2: 
            self.MatrixShift = (xy[0], xy[1])
        else:
            raise ValueError("Expected x,y pair of numbers, instead got: " + str(xy))
    #end
    
    def get_MatrixShift(self):
        '''Return Cell Matrix Shift in mm, as two-valued list.'''
        try:
            return self.MatrixShift
        except AttributeError:
            if WARN(): print("Using default values for `MatrixShift`.")
            self.set_MatrixShift( Defaults.MATRIX_SHIFT )
            return self.MatrixShift
    #end
    
    
    def set_NumberDiePerCell(self, cellCR):
        '''Set number of internal Die exposed per Cell, as two-valued integer iterable. Eg. (1,1) or [3,3]'''
        try:
            self.NumberDiePerCell = [1,1]
            self.NumberDiePerCell[0] = cellCR[0]
            self.NumberDiePerCell[1] = cellCR[1]
        except IndexError:
            errstr = "Expected `cellCR` to be two-valued integer iterable. Eg. (1,1) or [3,3].  Instead got '%s'." % cellCR
            raise IndexError(errstr)
        #end try
    #end
    
    def get_NumberDiePerCell(self):
        '''Return Number of Die per Cell, as two-valued Col/Row list.'''
        try:
            return self.NumberDiePerCell
        except AttributeError:
            if WARN(): print("Using default values for `NumberDiePerCell`.")
            self.NumberDiePerCell =  Defaults.NUMBER_DIES
            return self.NumberDiePerCell
    #end
    
    
    def set_MinNumberDie(self, num):
        '''Set minimum number of internal Die that must fit on the wafer in order for Cell to get an exposure, as integer.'''
        try:
            self.MinNumberDie = int(num)
        except ValueError:
            errstr = "Expected `num`` to be a single integer.  Instead got '%s'." % num
            raise ValueError(errstr)
        #end try
    #end
    
    def get_MinNumberDie(self):
        '''Return Minimum Number of Die on the wafer to force exposure.'''
        try:
            return self.MinNumberDie
        except AttributeError:
            if WARN(): print("Using default values for `MinNumberDie`.")
            self.MinNumberDie =  Defaults.MIN_NUMBER_DIES
            return self.MinNumberDie
    #end
    
    
    def set_RoundEdgeClearance(self, mm):
        '''Set Round Edge Clearance in mm.'''
        self.RoundEdgeClearance = float(mm)
    #end
    
    def get_RoundEdgeClearance(self):
        '''Return Round Edge Clearance in mm.'''
        return self.RoundEdgeClearance
    #end
    
    
    def set_FlatEdgeClearance(self, mm):
        '''Return Flat Edge Clearance in mm.'''
        self.FlatEdgeClearance = float(mm)
    #end
    
    def get_FlatEdgeClearance(self):
        '''Return Flat Edge Clearance in mm.'''
        return self.FlatEdgeClearance
    #end
    
    
    
    def set_EdgeExclusion(self, mm):
        '''Set Edge Exclusion in mm.'''
        self.EdgeExclusion = float(mm)
    #end
    
    def get_EdgeExclusion(self):
        '''Return Edge Exclusion in mm.'''
        return self.EdgeExclusion
    #end
    
    
    
    
    ##############################################
    #       Utility Functions
    ##############################################
    
    def Cell2Wafer(self, CellCR, ShiftXY=[0.0, 0.0]):
        '''Return the WaferXY coordinate pair corresponding to the CellCR [Col,Row] and ShiftXY ( [X,Y] offsets from Cell center).
        
        Parameters
        ----------
        CellCR : 2-valued iterable of integers
            Col,Row integers given in a 2-valued list, array, tuple etc.  Eg. [0,0] or [1,-2]
        ShiftXY : 2-valued iterable of floats
            X,Y shift from center of Cell, in a 2-valued list, array, tuple etc.
        '''
        pass
    #end Cell2Wafer()
    
    
    def Wafer2Cell(self, WaferXY=[0.0, 0.0]):
        '''Return the CellCR pair [Col,Row] and ShiftXY ( [X,Y] offset from Cell Center) corresponding to the given WaferXY coordinate pair.'''
        pass
    #end Wafer2Cell()
    
    
    
  
#end class(Cell)





################################################
################################################


