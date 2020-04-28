"""
This file is part of the ASML_JobCreator package for Python 3.x.

Alignment.py
    Contains class 'Alignment', which imports classes 'Marks' and 'Strategy'.
    
- - - - - - - - - - - - - - -

Demis D. John, Univ. of California Santa Barbara; Nanofabrication Facility; 2019

"""

####################################################
# Module setup etc.

from .__globals import *        # global variables/methods to the module.
from .Mark import Mark as _Mark # Alignment Marks class
from .Strategy import Strategy  # Alignment Strategy class

####################################################




class Alignment(object):
    """
    Class for ALignment info, containing Alignment Marks (Mark objects) and 
    Alignment Strategies (class Strategy).
    
    
    Attributes
    ----------
    MarkList : List of Mark objects added to this Job/Alignment.
    StrategyList : List of Strategy objects added to this Job/Alignment.
    parent : The parent Job object, that this Alignment belongs to.
        
    """
    
    def __init__(self, parent=None):
        '''Create empty Alignment object, with pointers to the Mark and Strategy classes.'''
        self.parent = parent    # parent Job object
        self.MarkList = []
        self.StrategyList = []
    #end __init__
    
    
    def __str__(self):
        '''Return string to `print` this object.'''
        s = ""
        s += "ASML_JobCreator.Alignment object:\n"
        for m in self.MarkList:
            s += str(m)
            s += " - - - - - - -"
        s+= "----------------"
        for a in self.StrategyList:
            s += str(s)
            s += " - - - - - - -"
        return s
    #end __str__
    
    
    def __len__(self):
        '''Returns number of Marks defined. Use this to determine whether Alignment is used at all in this Job.'''
        return len(self.MarkList)
    #end __len__
    
    
    def copy(self):
        ''' Returns a copy of this object.  Uses copy.deepcopy() to ensure all pointers are actually copied instead of referenced.'''
        from copy import deepcopy   # to make copies instead of only references
        return deepcopy(self)
    #end copy()
    
    
    
    ##############################################
    #       Classes
    ##############################################
    def Mark(self, MarkID, MarkType="PM", waferXY=None):
        '''Define a new alignment mark.
        Only waferXY (on-wafer coordinates) are implemented.
            
        Parameters
        ----------
        MarkID : string
            Name of the Mark
        
        MarkType : {"PM", "SPM_X", "SPM_Y" etc.}, optional
            Type of mark. Defaults to Primary Mark with both X/Y gratings, "PM".  See `help(Mark.set_marktype)` for full options.
        
        waferXY : two-valued iterable
            Wafer [X,Y] coordinates for this mark, relative to wafer center.
        
        Returns
        -------
        Returns the new Mark object, for later use in the Job.Alignment etc.
        
        ''' 
        return _Mark(MarkID, MarkType, waferXY=waferXY, parent=self)
    #end Mark()
        
    
    
    def add_marks(self, *marks):
        """
        Add Mark objects to the Job associated with this Alignment object.
    
        Parameters
        ----------
        *marks : Mark objects
            Pass Mark objects, each as it's own argument. To pass an array-like/iterable containing the Mark objects, use star dereferencing.  
        """
        
        for i,ii in enumerate(marks):
            if isinstance(ii, _Mark):
                self.MarkList.append( ii )
                ii.parent = self
            else:
                raise ValueError( "Expected `Mark` object, instead got: " + str(type(ii)) + " at argument #%i"%(i) )
        #end for(marks)
    #end
    
    
    def Strategy(self, ID, marks=None):
        '''
        Parameters
        ----------
        StrategyID : string
            Name of the strategy
        
        marks : iterable of Mark objects, optional
            Iterable containing Mark objects to add to this strategy. Can instead add later with `add_mark()`.
        '''
        m = Strategy(ID, marks, parent=self)
        return m
    #end Mark()
    
    
    def add_Strategy(self, *strat):
        """
        Add Strategy objects to this Alignment.
    
        Parameters
        ----------
        *strat : Strategy objects
            Pass Strategy objects each as it's own argument. To pass an array-like/iterable containing Strategy objects, use start-deferencing.
        """
        for i,ii in enumerate(strat):
            if isinstance(ii, Strategy):
                self.StrategyList.append( ii )
            else:
                raise ValueError( "Expected `Strategy` object, instead got: " + str(type(ii)) + " at argument #%i"%(i) )
        #end for(StrategyList)
    #end add_strategy()
    
    
    
    
  
#end class(Alignment)





################################################
################################################


