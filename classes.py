#usr/bin/python
"""
Module libencapsulation.classes

Implements the full functionality of the library in two classes to be imported
by the other modules: distinction between the 'public' and 'protected'
attributes (to which the access is denied), C++ static like class attributes,
fixed data structure of the classes and their instances, and introspection
methods.

Classes:
    ProtectedAttributes
    FixedAttributes
"""

__version__ = "0.1.0.0"
__date__ = "13-11-2019"
__status__ = "Development"

#imports

import sys
import os
import abc
import types

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if not (ROOT_FOLDER) in sys.path:
    sys.path.append(ROOT_FOLDER)

from libexceptions import PrivateAttributeAccess

#classes

#+ metaclasses

class ProtectedMeta(abc.ABCMeta):
    
    #magic methods to hook attributes access on the class level
    
    def __getattribute__(objCaller, strAttrName):
        """
        """
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        bCond3 = not strAttrName.startswith('_abc_')
        if bCond1 and bCond2 and bCond3:
            raise PrivateAttributeAccess(strAttrName, objCaller,
                                                                iSkipFrames = 1)
        gResult = type.__getattribute__(objCaller, strAttrName)
        return gResult
    
    def __setattr__(objCaller, strAttrName, gValue):
        """
        """
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        bCond3 = not strAttrName.startswith('_abc_')
        if bCond1 and bCond2 and bCond3:
            raise PrivateAttributeAccess(strAttrName, objCaller,
                                                                iSkipFrames = 1)
        gResult = type.__setattr__(objCaller, strAttrName, gValue)
    
    def __new__(cls, strName, lstBases, dictAttributes):
        """
        """
        objResult = abc.ABCMeta.__new__(cls, strName, lstBases, dictAttributes)
        #walk around to preserve the virtuality of the inherited protected
        #+ abstract method without copying them into the class dictionary, in
        #+ short - recreate the list of the abstract methods manually
        lstAbstractMethods = []
        lstAllMethods = []
        objlstMRO = [objResult]
        objlstMRO.extend(objResult.__mro__)
        for objParent in objlstMRO:
            for strAttr, gAttr in objParent.__dict__.items():
                if type(gAttr) == types.FunctionType:
                    bAbstract= gAttr.__dict__.get('__isabstractmethod__', False)
                    bCond1 = not (strAttr in lstAbstractMethods)
                    bCond2 = not (strAttr in lstAllMethods)
                    if bAbstract and bCond1 and bCond2:
                        lstAbstractMethods.append(strAttr)
                    if not (strAttr in lstAllMethods):
                        lstAllMethods.append(strAttr)
        type.__setattr__(objResult, '__abstractmethods__',
                                                frozenset(lstAbstractMethods))
        return objResult

class FixedMeta(ProtectedMeta):
    pass

#+ classes to be used

class ProtectedAttributes(object):
    
    __metaclass__ = ProtectedMeta
    
    #protected class methods
    
    @abc.abstractmethod
    def _onInit(self, *args, **kwargs):
        """
        Virtual / abstract method to set the instance attributes. The
        sub-classes designed to be used as singletons should not re-define this
        method. Other sub-classes must re-define this method without the
        decorator, and to create the instance attributes there, not in the
        __init__() method.
        
        Note that the signature of the re-defined version of this method will
        define the signature of the class instantiation.
        
        Version 0.1.0.0
        """
        pass
    
    #magic instance methods
    
    def __init__(self, *args, **kwargs):
        """
        Special magic method to create and initialize the instance attributes
        and to trigger the modification of the attributes resolution scheme.
        
        The sub-classes should not modify this method. Instead, the protected
        instance method _onInit() should be redefined without the decorator
        @abc.abstractmethod. The instance attributes - public and protected -
        should be defined their using dot notation as is usually done within 
        the __init__(). All positional and keyword arguments passed into the 
        __init__() method will be passed into _onInit(). The signature of the
        re-defined _onInit() method will define the signature of the class'
        instantiation.
        
        Signature:
            /type A/, type B/, ...// -> None
        
        Args:
            args: type A, any number of any positional arguments
            kwargs: type B, any number of any keyword arguments
        
        Raises:
            TypeError: the abstract instance method _onInit() is not re-defined
                as not abstract, and the class cannot be instantiated
        
        Version 0.1.0.0
        """
        self._onInit(*args, **kwargs)
        self._bLocked = True
    
    def __getattribute__(self, strAttrName):
        """
        """
        objClass = object.__getattribute__(self, '__class__')
        bLocked = object.__getattribute__(self, '__dict__').get('_bLocked',
                                                                        False)
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        if bCond1 and bCond2 and bLocked:
            raise PrivateAttributeAccess(strAttrName, objClass, iSkipFrames = 1)
        gResult = object.__getattribute__(self, strAttrName)
        return gResult
    
    def __setattr__(self, strAttrName, gValue):
        """
        """
        objClass = object.__getattribute__(self, '__class__')
        bLocked = object.__getattribute__(self, '__dict__').get('_bLocked',
                                                                        False)
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        if bCond1 and bCond2 and bLocked:
            raise PrivateAttributeAccess(strAttrName, objClass, iSkipFrames = 1)
        gResult = object.__setattr__(self, strAttrName, gValue)
        return gResult

class FixedAttributes(ProtectedAttributes):
    
    __metaclass__ = FixedMeta
