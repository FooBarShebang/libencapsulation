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

The class ProtectedAttributes introduces the following modifications to the data
model:
    * C++ like static fields based on the class attributes
    * Protected class and instance attributes
    * Support of the descriptors on the class and instance level
    * Class, static and instance methods and properties cannot be deleted or
        assigned to from a class object without instantiation
    * Class, static and instance methods cannot be deleted or assigned to from
        an instance of a class
    * Properties can be assigned to from an instance of a class if the property
        has __set__ descriptor
    * Properties can be deleted from an instance of a class if the property has
        __delete__ descriptor
The class FixedAttributes also adds the contant data structure of an object
during its lifetime, i.e.:
    * Neither class nor instance data attributes can be deleted or created
        during the lifetime of the object

Both classes implement singleton behaviour, i.e. their sub-classes cannot be
instantiated unless they re-define the protected method _onInit() without the
@abc.abstract decorator. This method is the only place inside the class'
definition, where the protected instance attributes can be defined using the
dot notation. It is supposed that all instance attributes are to be created
inside this _onInit() method. Do not modify the initialization magic method
__init__()!
"""

__version__ = "0.1.1.0"
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

from libexceptions import PrivateAttributeAccess, NotExistingAttribute
from libexceptions import CustomAttributeError, ConstantAttributeAssignment

#classes

#+ metaclasses

class ProtectedMeta(abc.ABCMeta):
    """
    Metaclass for the classes implementing the modified attributes access scheme
        * C++ like static fields based on the class attributes
        * Protected class and instance attributes
        * Support of the descriptors on the class and instance level
        * Class, static and instance methods and properties cannot be deleted
            or assigned to from a class object without instantiation
        * Class, static and instance methods cannot be deleted or assigned to
            from an instance of a class
        * Properties can be assigned to from an instance of a class if the
            property has __set__ descriptor
        * Properties can be deleted from an instance of a class if the property
            has __delete__ descriptor
    
    Version 0.1.1.0
    """
    
    #magic methods to hook attributes access on the class level
    
    def __getattribute__(objCaller, strAttrName):
        """
        Special magic method hooking the read access to an attribute on the
        class level using a class object (without instantiation). Does not allow
        access to the attributes with the names starting with a single
        underscore, excepting those starting with the '_abc_' string or more
        than one undescore.
        
        Signature:
            class A, str -> type A
        
        Args:
            objCaller: class A, the class object, to which this method is
                applied
            strAttrName: str, name of an attribute to access
        
        Returns:
            type A: the value of the attribute
        
        Raises:
            libexceptions.PrivateAttributeAccess: denied access to a protected
                attribute
            libexceptions.NotExistingAttribute: non-existing attribute is
                accessed
        
        Version 0.1.1.0
        """
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        bCond3 = not strAttrName.startswith('_abc_')
        if bCond1 and bCond2 and bCond3:
            raise PrivateAttributeAccess(strAttrName, objCaller, iSkipFrames= 1)
        try:
            gResult = type.__getattribute__(objCaller, strAttrName)
        except AttributeError:
            raise NotExistingAttribute(strAttrName, objCaller, iSkipFrames= 1)
        return gResult
    
    def __setattr__(objCaller, strAttrName, gValue):
        """
        Special magic method hooking the modification of an attribute access on
        the class level using a class object (without instantiation). Does not
        allow modification of the attributes with the names starting with a 
        single underscore, excepting those starting with the '_abc_' string or
        more than one undescore.
        
        Signature:
            class A, str, type A -> None
        
        Args:
            objCaller: class A, the class object, to which this method is
                applied
            strAttrName: str, name of an attribute to modify
            gValue: type A, the value to assign
        
        Raises:
            libexceptions.PrivateAttributeAccess: denied access to a protected
                attribute
            libexceptions.CustomAttributeError: an existing attribute cannot be
                modified, e.g. method, property or an instance of a class with
                __set__ descriptor preventing modification
        
        Version 0.1.1.0
        """
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        bCond3 = not strAttrName.startswith('_abc_')
        if bCond1 and bCond2 and bCond3:
            raise PrivateAttributeAccess(strAttrName, objCaller, iSkipFrames= 1)
        bModified = False
        for objParent in objCaller.__mro__:
            if strAttrName in objParent.__dict__.keys():
                gAttrValue = objParent.__dict__[strAttrName]
                bCond1 = hasattr(gAttrValue, '__set__')
                bCond2 = isinstance(gAttrValue, (classmethod, staticmethod,
                                                            types.FunctionType))
                bCond4 = isinstance(gAttrValue, property)
                if bCond1:
                    try:
                        gAttrValue.__set__(objParent, gValue)
                    except Exception as err:
                        if isinstance(err, ConstantAttributeAssignment):
                            raise ConstantAttributeAssignment(strAttrName,
                                                    objCaller, iSkipFrames = 1)
                        else:
                            raise CustomAttributeError(strAttrName, objCaller,
                                                            iSkipFrames= 1)
                elif (bCond4 and not bCond1) or (bCond2 and not bCond4):
                    raise CustomAttributeError(strAttrName, objCaller,
                                                            iSkipFrames= 1)
                else:
                    type.__setattr__(objParent, strAttrName, gValue)
                bModified = True
                break
        if not bModified:
            type.__setattr__(objCaller, strAttrName, gValue)
    
    def __delattr__(objCaller, strAttrName):
        """
        Special magic method hooking the deletion of an attribute on the class
        level using a class object (without instantiation). Does not allow
        deletion of the attributes with the names starting with a single
        underscore, excepting those starting with the '_abc_' string or more
        than one undescore.
        
        Signature:
            class A, str -> None
        
        Args:
            objCaller: class A, the class object, to which this method is
                applied
            strAttrName: str, name of an attribute to delete
        
        Raises:
            libexceptions.PrivateAttributeAccess: denied deletion of a protected
                attribute
            libexceptions.CustomAttributeError: denied deletion of a public or
                magic attribute, e.g. method, property or an instance of a class
                with __delete__ descriptor preventing deletion
            libexceptions.NotExistingAttribute: denied deletion of a
                non-existing attribute
        
        Version 0.1.1.0
        """
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        bCond3 = not strAttrName.startswith('_abc_')
        if bCond1 and bCond2 and bCond3:
            raise PrivateAttributeAccess(strAttrName, objCaller, iSkipFrames= 1)
        if strAttrName in objCaller.__dict__.keys():
            gAttrValue = objCaller.__dict__[strAttrName]
            bCond1 = hasattr(gAttrValue, '__delete__')
            bCond2 = isinstance(gAttrValue, (classmethod, staticmethod,
                                        types.FunctionType, types.MethodType))
            bCond4 = isinstance(gAttrValue, property)
            if bCond1:
                try:
                    gAttrValue.__delete__(objCaller)
                except Exception as err:
                        if isinstance(err, ConstantAttributeAssignment):
                            raise ConstantAttributeAssignment(strAttrName,
                                                    objCaller, iSkipFrames = 1)
                        else:
                            raise CustomAttributeError(strAttrName, objCaller,
                                                            iSkipFrames= 1)
                type.__setattr__(objCaller, strAttrName, None)
            elif (bCond4 and not bCond1) or (bCond2 and not bCond4):
                raise CustomAttributeError(strAttrName, objCaller,
                                                                iSkipFrames = 1)
            type.__delattr__(objCaller, strAttrName)
            del gAttrValue
        elif hasattr(objCaller, strAttrName):
            raise CustomAttributeError(strAttrName, objCaller, iSkipFrames = 1)
        else:
            raise NotExistingAttribute(strAttrName, objCaller, iSkipFrames = 1)
    
    def __new__(cls, strName, lstBases, dictAttributes):
        """
        Special 'constructor' magic method hooking the creation of the new
        classes based on this metaclass. Note, that the constructor of the class
        abc.ABCMeta is called instead of the type class. Due to the limitation
        implied by the access modification the list of the abstract methods of
        the class is reconstructed manually.
        
        Signature:
            type class A, str, list(class B), dict(str -> type A) -> class A
        
        Args:
            cls: type class A, factory for the class to be created, basically,
                this metclass itself
            strName: str, name of the class to be created
            lstBases: list(class B), list of the super classes
            dictAttributes: dict(str -> type A), dictionary of the class'
                attributes
        
        Returns:
            class A: a new class object
        
        Version 0.1.0.0
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
    
    def __del__(cls):
        """
        Special magic method hooking the destruction of a class. Ensures the
        deletion of all class attributes, especially the 'protected' ones.
        
        Signature:
            class A -> None
        
        Args:
            cls: class A, the class object to be destructed
        
        Version 0.1.0.0
        """
        strAttributes = cls.__dict__.keys()
        for strAttr in strAttributes:
            gAttrValue = cls.__dict__[strAttr]
            if hasattr(gAttrValue, '__delete__'):
                try:
                    gAttrValue.__delete__(cls)
                    type.__setattr__(cls, strAttr, None)
                except:
                    pass
            try:
                type.__delattr__(cls, strAttr)
                del gAttrValue
            except:
                pass

class FixedMeta(ProtectedMeta):
    """
    Metaclass for the classes implementing the modified attributes access scheme
        * C++ like static fields based on the class attributes
        * Protected class and instance attributes
        * Support of the descriptors on the class and instance level
        * Class, static and instance methods and properties cannot be deleted
            or assigned to from a class object without instantiation
        * Class, static and instance methods cannot be deleted or assigned to
            from an instance of a class
        * Properties can be assigned to from an instance of a class if the
            property has __set__ descriptor
        * Properties can be deleted from an instance of a class if the property
            has __delete__ descriptor
        * Neither class nor instance data attributes can be deleted or created
            during the lifetime of the object
    
    Sub-classes ProtectedMeta.
    
    Version 0.1.1.0
    """
    
    #magic methods to hook attributes access on the class level
    
    def __delattr__(objCaller, strAttrName):
        """
        Special magic method hooking the deletion of an attribute on the class
        level using a class object (without instantiation). Does not allow
        deletion of any attribute.
        
        Signature:
            class A, str -> None
        
        Args:
            objCaller: class A, the class object, to which this method is
                applied
            strAttrName: str, name of an attribute to delete
        
        Raises:
            libexceptions.PrivateAttributeAccess: denied deletion of a protected
                attribute
            libexceptions.CustomAttributeError: denied deletion of a public or
                magic attribute
            libexceptions.NotExistingAttribute: denied deletion of a
                non-existing attribute
        
        Version 0.1.0.0
        """
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        bCond3 = not strAttrName.startswith('_abc_')
        if bCond1 and bCond2 and bCond3:
            raise PrivateAttributeAccess(strAttrName, objCaller, iSkipFrames= 1)
        if hasattr(objCaller, strAttrName):
            raise CustomAttributeError(strAttrName, objCaller, iSkipFrames = 1)
        else:
            raise NotExistingAttribute(strAttrName, objCaller, iSkipFrames = 1)
    
    def __setattr__(objCaller, strAttrName, gValue):
        """
        Special magic method hooking the modification of an attribute access on
        the class level using a class object (without instantiation). Does not
        allow modification of the attributes with the names starting with a 
        single underscore, excepting those starting with the '_abc_' string or
        more than one undescore.
        
        Signature:
            class A, str, type A -> None
        
        Args:
            objCaller: class A, the class object, to which this method is
                applied
            strAttrName: str, name of an attribute to modify
            gValue: type A, the value to assign
        
        Raises:
            libexceptions.PrivateAttributeAccess: denied access to a protected
                attribute
            libexceptions.CustomAttributeError: an existing attribute cannot be
                modified, or such argument does not exist
            libexceptions.NotExistingAttribute: the attribute does not exist
        
        Version 0.1.0.0
        """
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        bCond3 = not strAttrName.startswith('_abc_')
        if bCond1 and bCond2 and bCond3:
            raise PrivateAttributeAccess(strAttrName, objCaller, iSkipFrames= 1)
        bModified = False
        for objParent in objCaller.__mro__:
            if strAttrName in objParent.__dict__.keys():
                gAttrValue = objParent.__dict__[strAttrName]
                bCond1 = hasattr(gAttrValue, '__set__')
                bCond2 = isinstance(gAttrValue, (classmethod, staticmethod,
                                                            types.FunctionType))
                bCond4 = isinstance(gAttrValue, property)
                if bCond1:
                    try:
                        gAttrValue.__set__(objParent, gValue)
                    except Exception as err:
                        if isinstance(err, ConstantAttributeAssignment):
                            raise ConstantAttributeAssignment(strAttrName,
                                                    objCaller, iSkipFrames = 1)
                        else:
                            raise CustomAttributeError(strAttrName, objCaller,
                                                            iSkipFrames= 1)
                elif (bCond4 and not bCond1) or (bCond2 and not bCond4):
                    raise CustomAttributeError(strAttrName, objCaller,
                                                            iSkipFrames = 1)
                else:
                    type.__setattr__(objParent, strAttrName, gValue)
                bModified = True
                break
        if not bModified:
            raise NotExistingAttribute(strAttrName, objCaller, iSkipFrames = 1)

#+ classes to be used

class ProtectedAttributes(object):
    """
    Abstract base class implementing the modified attributes access scheme
        * C++ like static fields based on the class attributes
        * Protected class and instance attributes
        * Support of the descriptors on the class and instance level
        * Class, static and instance methods and properties cannot be deleted
            or assigned to from a class object without instantiation
        * Class, static and instance methods cannot be deleted or assigned to
            from an instance of a class
        * Properties can be assigned to from an instance of a class if the
            property has __set__ descriptor
        * Properties can be deleted from an instance of a class if the property
            has __delete__ descriptor
    
    Sub-classes should re-define as not abstract the protected instance method
    _onInit(), there the instance attributes are supposed to be created. Do not
    change the __init__() method! If the _onInit() method is not re-defined the
    sub-class cannot be instantiated and will act as a singleton.
    
    Version 0.1.1.0
    """
    
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
        
        Signature:
            /type A/, type B/, ...// -> None
        
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
        Special magic method hooking the read access to an attribute on the
        class instance level. Does not allow access to the attributes with the
        names starting with a single underscore, excepting those starting with
        more than one undescore.
        
        Signature:
            str -> type A
        
        Args:
            strAttrName: str, name of an attribute to access
        
        Returns:
            type A: the value of the attribute
        
        Raises:
            libexceptions.PrivateAttributeAccess: denied access to a protected
                attribute
            libexceptions.CustomAttributeError: denied read access to an
                existing attribute, i.e. by its own desriptor
            libexceptions.NotExistingAttribute: the attribute does not exist
        
        Version 0.1.1.0
        """
        objClass = object.__getattribute__(self, '__class__')
        bLocked = object.__getattribute__(self, '__dict__').get('_bLocked',
                                                                        False)
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        if bCond1 and bCond2 and bLocked:
            raise PrivateAttributeAccess(strAttrName, objClass, iSkipFrames = 1)
        try:
            gResult = object.__getattribute__(self, strAttrName)
        except AttributeError:
            raise NotExistingAttribute(strAttrName, objClass, iSkipFrames = 1)
        #check if a descriptor but not a method
        if (hasattr(gResult, '__get__') and 
                            (not isinstance(gResult, types.FunctionType))):
            try:
                gResult = gResult.__get__(self, objClass)
            except:
                raise CustomAttributeError(strAttrName, objClass,
                                                                iSkipFrames = 1)
        return gResult
    
    def __setattr__(self, strAttrName, gValue):
        """
        Special magic method hooking the modification of an attribute access on
        the class instance level. Does not allow modification of the attributes
        with the names starting with a single underscore, excepting those
        starting with more than one undescore.
        
        Signature:
            str, type A -> None
        
        Args:
            strAttrName: str, name of an attribute to modify
            gValue: type A, the value to assign
        
        Raises:
            libexceptions.PrivateAttributeAccess: denied access to a protected
                attribute
            libexceptions.CustomAttributeError: denied modification of an
                existing attribute due to its own desriptor limitation, or
                deletion of an instance, class or static method
        
        Version 0.1.1.0
        """
        objClass = object.__getattribute__(self, '__class__')
        bLocked = object.__getattribute__(self, '__dict__').get('_bLocked',
                                                                        False)
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        if bCond1 and bCond2 and bLocked:
            raise PrivateAttributeAccess(strAttrName, objClass, iSkipFrames = 1)
        if strAttrName in self.__dict__.keys():
            if hasattr(self.__dict__[strAttrName], '__set__'):
                self.__dict__[strAttrName].__set__(self, gValue)
            else:
                self.__dict__[strAttrName] = gValue
        elif hasattr(self, strAttrName):
            for objParent in self.__class__.__mro__:
                if strAttrName in objParent.__dict__.keys():
                    gAttrValue = objParent.__dict__[strAttrName]
                    bCond1 = hasattr(gAttrValue, '__set__')
                    bCond2 = isinstance(gAttrValue, (classmethod, staticmethod,
                                                    property, types.MethodType,
                                                    types.FunctionType))
                    if bCond1:
                        try:
                            gAttrValue.__set__(self, gValue)
                        except Exception as err:
                            if isinstance(err, ConstantAttributeAssignment):
                                raise ConstantAttributeAssignment(strAttrName,
                                                    objClass, iSkipFrames = 1)
                            else:
                                raise CustomAttributeError(strAttrName, objClass,
                                                                iSkipFrames= 1)
                    elif bCond2:
                        raise CustomAttributeError(strAttrName, objClass,
                                                                iSkipFrames = 1)
                    else:
                        type.__setattr__(objParent, strAttrName, gValue)
        else:
            self.__dict__[strAttrName] = gValue
    
    def __delattr__(self, strAttrName):
        """
        Special magic method hooking the deletion of an attribute on the class
        instance level. Does not allow deletion of the attributes with the names
        starting with a single underscore, excepting those starting with more
        than one undescore.
        
        Signature:
            str -> None
        
        Args:
            strAttrName: str, name of an attribute to delete
        
        Raises:
            libexceptions.PrivateAttributeAccess: denied access to a protected
                attribute
            libexceptions.CustomAttributeError: denied delition of an existing
                class attribute, or of an existing instance attribute due to its
                own desriptor limitation
            libexceptions.NotExistingAttribute: the attribute does not exist
        
        Version 0.1.1.0
        """
        objClass = object.__getattribute__(self, '__class__')
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        if bCond1 and bCond2:
            raise PrivateAttributeAccess(strAttrName, objClass, iSkipFrames = 1)
        if strAttrName in self.__dict__.keys():
            gAttrValue = self.__dict__[strAttrName]
            if hasattr(gAttrValue, '__delete__'):
                try:
                    gAttrValue.__delete__(self)
                except Exception as err:
                    if isinstance(err, ConstantAttributeAssignment):
                        raise ConstantAttributeAssignment(strAttrName,
                                                    objClass, iSkipFrames = 1)
                    else:
                        raise CustomAttributeError(strAttrName, objClass,
                                                                iSkipFrames= 1)
                self.__dict__[strAttrName] = None
            object.__delattr__(self, strAttrName)
            del gAttrValue
        elif hasattr(self, strAttrName):
            raise CustomAttributeError(strAttrName, objClass, iSkipFrames = 1)
        else:
            raise NotExistingAttribute(strAttrName, objClass, iSkipFrames = 1)
    
    def __del__(self):
        """
        Special magic method hooking the destruction of a class's instance.
        Ensures the deletion of all instance attributes, especially the
        'protected' ones.
        
        Signature:
            None -> None
        
        Version 0.1.0.0
        """
        strAttributes = self.__dict__.keys()
        for strAttr in strAttributes:
            gAttrValue = self.__dict__[strAttr]
            if hasattr(gAttrValue, '__delete__'):
                try:
                    gAttrValue.__delete__(self)
                    self.__dict__[strAttrName] = None
                except:
                    pass
            try:
                object.__delattr__(self, strAttr)
                del gAttrValue
            except:
                pass

class FixedAttributes(ProtectedAttributes):
    """
    Abstract base class implementing the modified attributes access scheme
        * C++ like static fields based on the class attributes
        * Protected class and instance attributes
        * Support of the descriptors on the class and instance level
        * Class, static and instance methods and properties cannot be deleted
            or assigned to from a class object without instantiation
        * Class, static and instance methods cannot be deleted or assigned to
            from an instance of a class
        * Properties can be assigned to from an instance of a class if the
            property has __set__ descriptor
        * Properties can be deleted from an instance of a class if the property
            has __delete__ descriptor
        * Neither class nor instance data attributes can be deleted or created
            during the lifetime of the object
    
    Sub-classes ProtectedAttributes.
    
    Sub-classes should re-define as not abstract the protected instance method
    _onInit(), there the instance attributes are supposed to be created. Do not
    change the __init__() method! If the _onInit() method is not re-defined the
    sub-class cannot be instantiated and will act as a singleton.
    
    Version 0.1.1.0
    """
    
    __metaclass__ = FixedMeta
    
    #magic instance methods
    
    def __delattr__(self, strAttrName):
        """
        Special magic method hooking the deletion of an attribute on the class
        instance level. Does not allow deletion of the attributes with the names
        starting with a single underscore, excepting those starting with more
        than one undescore.
        
        Signature:
            str -> None
        
        Args:
            strAttrName: str, name of an attribute to delete
        
        Raises:
            libexceptions.PrivateAttributeAccess: denied access to a protected
                attribute
            libexceptions.CustomAttributeError: denied delition of an existing
                attribute
            libexceptions.NotExistingAttribute: the attribute does not exist
        
        Version 0.1.0.0
        """
        objClass = object.__getattribute__(self, '__class__')
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        if bCond1 and bCond2:
            raise PrivateAttributeAccess(strAttrName, objClass, iSkipFrames = 1)
        if hasattr(self, strAttrName):
            raise CustomAttributeError(strAttrName, objClass, iSkipFrames = 1)
        else:
            raise NotExistingAttribute(strAttrName, objClass, iSkipFrames = 1)
    
    def __setattr__(self, strAttrName, gValue):
        """
        Special magic method hooking the modification of an attribute access on
        the class instance level. Does not allow modification of the attributes
        with the names starting with a single underscore, excepting those
        starting with more than one undescore.
        
        Signature:
            str, type A -> None
        
        Args:
            strAttrName: str, name of an attribute to modify
            gValue: type A, the value to assign
        
        Raises:
            libexceptions.PrivateAttributeAccess: denied access to a protected
                attribute
            libexceptions.NotExistingAttribute: assignment to a non-existing
                attribute, i.e. denied creation of a new attribute
            libexceptions.CustomAttributeError: denied modification of an
                existing attribute, i.e. by its own desriptor
        
        Version 0.1.0.0
        """
        objClass = object.__getattribute__(self, '__class__')
        bLocked = object.__getattribute__(self, '__dict__').get('_bLocked',
                                                                        False)
        bCond1 = strAttrName.startswith('_')
        bCond2 = not strAttrName.startswith('__')
        if bCond1 and bCond2 and bLocked:
            raise PrivateAttributeAccess(strAttrName, objClass, iSkipFrames = 1)
        if strAttrName in self.__dict__.keys():
            if hasattr(self.__dict__[strAttrName], '__set__'):
                self.__dict__[strAttrName].__set__(self, gValue)
            else:
                self.__dict__[strAttrName] = gValue
        elif hasattr(self, strAttrName):
            for objParent in self.__class__.__mro__:
                if strAttrName in objParent.__dict__.keys():
                    gAttrValue = objParent.__dict__[strAttrName]
                    bCond1 = hasattr(gAttrValue, '__set__')
                    bCond2 = isinstance(gAttrValue, (classmethod, staticmethod,
                                                    property, types.MethodType,
                                                    types.FunctionType))
                    if bCond1:
                        try:
                            gAttrValue.__set__(self, gValue)
                        except Exception as err:
                            if isinstance(err, ConstantAttributeAssignment):
                                raise ConstantAttributeAssignment(strAttrName,
                                                    objClass, iSkipFrames = 1)
                            else:
                                raise CustomAttributeError(strAttrName, objClass,
                                                                iSkipFrames= 1)
                    elif bCond2:
                        raise CustomAttributeError(strAttrName, objClass,
                                                                iSkipFrames = 1)
                    else:
                        type.__setattr__(objParent, strAttrName, gValue)
        else:
            if bLocked:
                raise NotExistingAttribute(strAttrName, objClass,
                                                                iSkipFrames = 1)
            else:
                self.__dict__[strAttrName] = gValue
