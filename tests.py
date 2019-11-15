#usr/bin/python
"""
Module libencapsulation.test

Implements a set of unit-tests for the library.
"""

__version__ = "1.0.0.0"
__date__ = "15-11-2019"
__status__ = "Testing"

#imports

import sys
import os
import unittest

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if not (ROOT_FOLDER) in sys.path:
    sys.path.append(ROOT_FOLDER)

import libencapsulation.classes as testmodule

from libexceptions import PrivateAttributeAccess, NotExistingAttribute
from libexceptions import CustomAttributeError, ConstantAttributeAssignment

#classes

#+ helper classes

class Descripted(object):
    """
    Implementation of the objects with the descriptor methods.
    """
    
    def __init__(self, gValue):
        """
        Initializes the internal storage with the passed value converted into
        a string.
        
        Signature:
            type A -> None
        
        Args:
            gValue: type A, any value to be stored as a string
        
        Version 0.1.0.0
        """
        self.Value  = str(gValue)
    
    def __get__(self, objCaller, objType = None):
        """
        Returns the internally stored string with an exclamation mark attached.
        
        Signature:
            type A/, type type A OR None/ -> str
        
        Args:
            objCaller: type A, 'parent' object requesting value of its
                attributes, which is an instance of this class
            objType: (optional) type type A, the type (class) of the 'parent'
                object
        
        Returns:
            str: the internally stored string with an exclamation mark attached
        
        Version 0.1.0.0
        """
        return '{}!'.format(self.Value)
    
    def __set__(self, objCaller, gValue):
        """
        Changes the internally stored value to a string representation of the
        passed value.
        
        Signature:
            type A, type B -> None
        
        Args:
            obj: type A, 'parent' object requesting value of its attributes,
                which is an instance of this class
             gValue: type B, any value to be stored as a string
        """
        self.Value = str(gValue)
    
    def __delete__(self, objCaller):
        """
        Raises libexceptions.CustomAttributeError upon attemped deletion of
        an instance of this class as an attribute of another class.
        
        Signature:
            type A -> None
        
        Args:
            obj: type A, 'parent' object requesting value of its attributes,
                which is an instance of this class
        
        Raises:
            ConstantAttributeAssignment: always, the desired functionality
        """
        if hasattr(objCaller, '__class__'):
            _objCaller = objCaller.__class__
        else:
            print objCaller
            _objCaller = objCaller
        raise ConstantAttributeAssignment(self.__class__.__name__, _objCaller,
                                                                iSkipFrames = 1)

class ProtectedSingleton(testmodule.ProtectedAttributes):
    pass

class FixedSingleton(testmodule.FixedAttributes):
    pass

class ProtectedTop(testmodule.ProtectedAttributes):
    
    #class fields
    
    A = 1
    
    B = Descripted(1)
    
    _C = 1
    
    #instance fields
    
    def _onInit(self, *args, **kwargs):
        """
        Define the instance attributes here!
        """
        self.D = 1
        
        self.E = Descripted(1)
        
        self._F = 1
    
    #class methods
    
    @classmethod
    def ClassMethod(cls):
        return "class method"
    
    @classmethod
    def _ClassMethod(cls):
        pass
    
    #static methods
    
    @staticmethod
    def StaticMethod():
        return "static method"
    
    @staticmethod
    def _StaticMethod():
        pass
    
    #properties
    
    @property
    def MyProperty(self):
        return str(self.__dict__['_F'])
    
    @MyProperty.setter
    def MyProperty(self, gValue):
        self.__dict__['_F'] = gValue
    
    @property
    def FixedProperty(self):
        return 'property'
    
    @property
    def _MyProperty(self):
        pass
    
    #instance methods
    
    def MyMethod(self):
        return "instance method"
    
    def _MyMethod(self):
        pass

class ProtectedMiddle(ProtectedTop):
    pass

class ProtectedBottom(ProtectedMiddle):
    pass

class FixedTop(testmodule.FixedAttributes):
    
    #class fields
    
    A = 1
    
    B = Descripted(1)
    
    _C = 1
    
    #instance fields
    
    def _onInit(self, *args, **kwargs):
        """
        Define the instance attributes here!
        """
        self.D = 1
        
        self.E = Descripted(1)
        
        self._F = 1
    
    #class methods
    
    @classmethod
    def ClassMethod(cls):
        return "class method"
    
    @classmethod
    def _ClassMethod(cls):
        pass
    
    #static methods
    
    @staticmethod
    def StaticMethod():
        return "static method"
    
    @staticmethod
    def _StaticMethod():
        pass
    
    #properties
    
    @property
    def MyProperty(self):
        return str(self.__dict__['_F'])
    
    @MyProperty.setter
    def MyProperty(self, gValue):
        self.__dict__['_F'] = gValue
    
    @property
    def FixedProperty(self):
        return 'property'
    
    @property
    def _MyProperty(self):
        pass
    
    #instance methods
    
    def MyMethod(self):
        return "instance method"
    
    def _MyMethod(self):
        pass

class FixedMiddle(FixedTop):
    pass

class FixedBottom(FixedMiddle):
    pass

#+ test cases

class Test_Singleton(unittest.TestCase):
    """
    Test cases for the checking the Singleton behaviour
    
    Test id: TEST-T-000. Covers the requirements: REQ-FUN-006.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.Singletons = [ProtectedSingleton, FixedSingleton]
        cls.NotSingletons = [ProtectedTop, ProtectedMiddle, ProtectedBottom,
                                            FixedTop, FixedMiddle, FixedBottom]
    
    def test_Singleton(self):
        """
        Checks that the classes designed to act as singleton cannot be
        instantiated.
        
        Test REQ-FUN-006.
        """
        for clsName in self.Singletons:
            with self.assertRaises(TypeError):
                objTemp = clsName()
    
    def test_NotSingleton(self):
        """
        Checks that the classes with the overriden abstract methods can be
        instantiated
        
        Test REQ-FUN-006
        """
        for clsName in self.NotSingletons:
            objTemp = clsName()
            del objTemp

class Test_ProtectedTop(unittest.TestCase):
    """
    Test cases for the checking the implementation of the protected attributes
    and static class attributes as well as the introspection functionality.
    
    Test id: TEST-T-001. Covers the requirements: REQ-FUN-000, REQ-FUN-001,
    REQ-FUN-002, REQ-FUN-003, REQ-AWM-000, REQ-AWM-001, REQ-AWM-002, REQ-AWM-003
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = ProtectedTop
        #relation with other classes
        cls.DownHill = [ProtectedMiddle, ProtectedBottom]
        cls.UpHill = []
        #attributes groups
        cls.PublicClassMethods = ['ClassMethod', 'StaticMethod']
        cls.HiddenClassMethods = ['_ClassMethod', '_StaticMethod']
        cls.PublicInstanceMethods = ['MyMethod']
        cls.HiddenInstanceMethods = ['_MyMethod']
        cls.PublicProperties = ['MyProperty', 'FixedProperty']
        cls.HiddenProperties = ['_MyProperty']
        cls.PublicClassFields = ['A', 'B']
        cls.HiddenClassFields = ['_C']
        cls.PublicInstanceFields = ['D', 'E']
        cls.HiddenIstanceFields = ['_F']
        #aggregated
        cls.PublicOnClass = list(cls.PublicClassMethods)
        cls.PublicOnClass.extend(cls.PublicInstanceMethods)
        cls.PublicOnClass.extend(cls.PublicProperties)
        cls.PublicOnClass.extend(cls.PublicClassFields)
        cls.HiddenOnClass = list(cls.HiddenClassMethods)
        cls.HiddenOnClass.extend(cls.HiddenInstanceMethods)
        cls.HiddenOnClass.extend(cls.HiddenProperties)
        cls.HiddenOnClass.extend(cls.HiddenClassFields)
        cls.PublicOnInstance = list(cls.PublicOnClass)
        cls.PublicOnInstance.extend(cls.PublicInstanceFields)
        cls.HiddenOnInstance = list(cls.HiddenOnClass)
        cls.HiddenOnInstance.extend(cls.HiddenIstanceFields)
    
    def test_class_hasattr_ok(self):
        """
        hasattr() built-in function should return True concerning the public
        class attributes accessed from a class.
        
        Tests REQ-FUN-002
        """
        for strAttr in self.PublicOnClass:
            self.assertTrue(hasattr(self.TestClass, strAttr))
    
    def test_instance_hasattr_ok(self):
        """
        hasattr() built-in function should return True concerning the public
        class and instance attributes accessed from an instance.
        
        Tests REQ-FUN-003
        """
        objTest = self.TestClass()
        for strAttr in self.PublicOnInstance:
            self.assertTrue(hasattr(objTest, strAttr))
        del objTest
    
    def test_class_hasattr_nok(self):
        """
        hasattr() built-in function should return False concerning the protected
        class attributes accessed from a class or instance.
        
        Tests REQ-FUN-002
        """
        for strAttr in self.HiddenOnInstance:
            self.assertFalse(hasattr(self.TestClass, strAttr))
    
    def test_instance_hasattr_nok(self):
        """
        hasattr() built-in function should return False concerning the protected
        class and instance attributes accessed from an instance.
        
        Tests REQ-FUN-003
        """
        objTest = self.TestClass()
        for strAttr in self.HiddenOnInstance:
            self.assertFalse(hasattr(objTest, strAttr))
        del objTest
    
    def test_class_getattr_ok(self):
        """
        Read access to a public attribute using the dot notation or the
        getattr() built-in function should return the proper value of the public
        class attributes accessed from a class.
        
        Tests REQ-FUN-001, REQ-FUN-002
        """
        #methods
        self.assertEqual(self.TestClass.ClassMethod(), 'class method')
        self.assertEqual(getattr(self.TestClass, 'ClassMethod')(),
                                                                'class method')
        self.assertEqual(self.TestClass.StaticMethod(), 'static method')
        self.assertEqual(getattr(self.TestClass, 'StaticMethod')(),
                                                                'static method')
        #fields
        self.assertEqual(self.TestClass.A, 1)
        self.assertEqual(getattr(self.TestClass, 'A'), 1)
        self.assertEqual(self.TestClass.B, '1!')
        self.assertEqual(getattr(self.TestClass, 'B'), '1!')
    
    def test_instance_getattr_ok(self):
        """
        Read access to a public attribute using the dot notation or the
        getattr() built-in function should return the proper value of the public
        class and instance attributes accessed from an instance.
        
        Tests REQ-FUN-001, REQ-FUN-003
        """
        objTest = self.TestClass()
        #methods
        self.assertEqual(objTest.ClassMethod(), 'class method')
        self.assertEqual(getattr(objTest, 'ClassMethod')(), 'class method')
        self.assertEqual(objTest.StaticMethod(), 'static method')
        self.assertEqual(getattr(objTest, 'StaticMethod')(), 'static method')
        self.assertEqual(objTest.MyMethod(), 'instance method')
        self.assertEqual(getattr(objTest, 'MyMethod')(), 'instance method')
        #property
        self.assertEqual(objTest.MyProperty, '1')
        self.assertEqual(getattr(objTest, 'MyProperty'), '1')
        self.assertEqual(objTest.FixedProperty, 'property')
        self.assertEqual(getattr(objTest, 'FixedProperty'), 'property')
        #fields
        self.assertEqual(objTest.A, 1)
        self.assertEqual(getattr(objTest, 'A'), 1)
        self.assertEqual(objTest.B, '1!')
        self.assertEqual(getattr(objTest, 'B'), '1!')
        self.assertEqual(objTest.D, 1)
        self.assertEqual(getattr(objTest, 'D'), 1)
        self.assertEqual(objTest.E, '1!')
        self.assertEqual(getattr(objTest, 'E'), '1!')
        del objTest
    
    def test_class_getattr_nok(self):
        """
        Read access to a protected attribute using the dot notation or the
        getattr() built-in function should raise the PrivateAttributeAccess
        exception upon access of the protected class attributes accessed from a
        class. NotExistingAttribute exception should be raised if a non-
        existing attributed is accessed.
        
        Tests REQ-FUN-001, REQ-FUN-002, REQ-AWM-000, REQ-AWM-001, REQ-AWM-002
        """
        #protected attributes
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = self.TestClass._ClassMethod()
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = self.TestClass._StaticMethod()
        for strAttr in self.HiddenClassMethods:
            with self.assertRaises(PrivateAttributeAccess):
                gTemp = getattr(self.TestClass, strAttr)()
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = self.TestClass._C
        for strAttr in self.HiddenClassMethods:
            with self.assertRaises(PrivateAttributeAccess):
                gTemp = getattr(self.TestClass, strAttr)
        #instance methods - TypeError should be raised
        with self.assertRaises(TypeError):
            gTemp = self.TestClass.MyMethod()
        with self.assertRaises(TypeError):
            gTemp = getattr(self.TestClass,'MyMethod')()
        #not existing attributes
        for strAttr in self.PublicInstanceFields:
            with self.assertRaises(NotExistingAttribute):
                gTemp = getattr(self.TestClass, strAttr)
        with self.assertRaises(NotExistingAttribute):
            gTemp = self.TestClass.SomeSuperWierdName
        with self.assertRaises(NotExistingAttribute):
            gTemp = self.TestClass.SomeSuperWierdName()
        with self.assertRaises(NotExistingAttribute):
            gTemp = getattr(self.TestClass, 'SomeSuperWierdName')
        with self.assertRaises(NotExistingAttribute):
            gTemp = getattr(self.TestClass, 'SomeSuperWierdName')()
    
    def test_instance_getattr_nok(self):
        """
        Read access to a protected attribute using the dot notation or the
        getattr() built-in function should raise the PrivateAttributeAccess
        exception upon access of the protected class and instance attributes
        accessed from a class. NotExistingAttribute exception should be raised
        if a non-existing attributed is accessed.
        
        Tests REQ-FUN-001, REQ-FUN-003, REQ-AWM-000, REQ-AWM-001, REQ-AWM-002
        """
        #protected attributes
        objTest = self.TestClass()
        lstHiddenMethods = list(self.HiddenClassMethods)
        lstHiddenMethods.extend(self.HiddenInstanceMethods)
        lstHiddenFields = list(self.HiddenClassFields)
        lstHiddenFields.extend(self.HiddenProperties)
        lstHiddenFields.extend(self.HiddenIstanceFields)
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = objTest._ClassMethod()
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = objTest._StaticMethod()
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = objTest._MyMethod()
        for strAttr in lstHiddenMethods:
            with self.assertRaises(PrivateAttributeAccess):
                gTemp = getattr(objTest, strAttr)()
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = objTest._MyProperty
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = objTest._C
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = objTest._F
        for strAttr in lstHiddenFields:
            with self.assertRaises(PrivateAttributeAccess):
                gTemp = getattr(objTest, strAttr)
        #not existing attributes
        with self.assertRaises(NotExistingAttribute):
            gTemp = objTest.SomeSuperWierdName
        with self.assertRaises(NotExistingAttribute):
            gTemp = objTest.SomeSuperWierdName()
        with self.assertRaises(NotExistingAttribute):
            gTemp = getattr(objTest, 'SomeSuperWierdName')
        with self.assertRaises(NotExistingAttribute):
            gTemp = getattr(objTest, 'SomeSuperWierdName')()
        del objTest
    
    def test_class_setattr_ok(self):
        """
        Checks the proper modification of the existing class attributes, and
        the preservation of the resolution order and attribute visibility scope.
        
        Tests REQ-FUN-001
        """
        lstClasses = list(self.UpHill)
        lstClasses.extend(self.DownHill)
        lstObjects = [clsItem() for clsItem in lstClasses]
        self.TestClass.A = 42
        self.TestClass.B = 42
        for clsItem in lstClasses:
            self.assertEqual(clsItem.A, 42)
            self.assertEqual(clsItem.B, '42!')
        for objItem in lstObjects:
            self.assertEqual(objItem.A, 42)
            self.assertEqual(objItem.B, '42!')
        self.TestClass.A = 1
        self.TestClass.B = 1
        for clsItem in lstClasses:
            self.assertEqual(clsItem.A, 1)
            self.assertEqual(clsItem.B, '1!')
        for objItem in lstObjects:
            self.assertEqual(objItem.A, 1)
            self.assertEqual(objItem.B, '1!')
        while len(lstObjects):
            del lstObjects[0]
    
    def test_instance_setattr_ok(self):
        """
        Checks the proper modification of the existing class and instance
        attributes, and the preservation of the resolution order and attribute
        visibility scope.
        
        Tests REQ-FUN-001
        """
        objTest = self.TestClass()
        objTest2 = self.TestClass()
        #instance attributes and properties
        objTest.D = 42
        objTest.E = 42
        objTest.MyProperty = 42
        self.assertEqual(objTest.D, 42)
        self.assertEqual(objTest.E, '42!')
        self.assertEqual(objTest.MyProperty, '42')
        self.assertEqual(objTest2.D, 1)
        self.assertEqual(objTest2.E, '1!')
        self.assertEqual(objTest2.MyProperty, '1')
        self.assertFalse(hasattr(self.TestClass, 'D'))
        self.assertFalse(hasattr(self.TestClass, 'E'))
        objTest.D = 1
        objTest.E = 1
        objTest.MyProperty = 1
        del objTest2
        #class attributes
        lstClasses = list(self.UpHill)
        lstClasses.extend(self.DownHill)
        lstObjects = [clsItem() for clsItem in lstClasses]
        objTest.A = 42
        objTest.B = 42
        self.assertEqual(objTest.A, 42)
        self.assertEqual(objTest.B, '42!')
        for clsItem in lstClasses:
            self.assertEqual(clsItem.A, 42)
            self.assertEqual(clsItem.B, '42!')
        for objItem in lstObjects:
            self.assertEqual(objItem.A, 42)
            self.assertEqual(objItem.B, '42!')
        objTest.A = 1
        objTest.B = 1
        for clsItem in lstClasses:
            self.assertEqual(clsItem.A, 1)
            self.assertEqual(clsItem.B, '1!')
        for objItem in lstObjects:
            self.assertEqual(objItem.A, 1)
            self.assertEqual(objItem.B, '1!')
        while len(lstObjects):
            del lstObjects[0]
        del objTest
    
    def test_class_setattr_nok(self):
        """
        Checks the proper modification of the existing class attributes, and
        the preservation of the resolution order and attribute visibility scope.
        
        PrivateAttributeAccess should be raised upon assignment to any protected
        attribute
        
        CustomAttributeError should be raised upon assignment to a class, static
        or instance method as well as to a property
        
        Tests REQ-FUN-001, REQ-FUN-002, REQ-AWN-000, REQ-AWM-001, REQ-AWM-002,
        REQ-AWM-003
        """
        #protected attributes
        for strAttr in self.HiddenOnInstance:
            with self.assertRaises(PrivateAttributeAccess):
                setattr(self.TestClass, strAttr, 1)
        with self.assertRaises(PrivateAttributeAccess):
            self.TestClass._C = 1
        with self.assertRaises(PrivateAttributeAccess):
            self.TestClass._F = 1
        with self.assertRaises(PrivateAttributeAccess):
            self.TestClass._MyMethod = 1
        with self.assertRaises(PrivateAttributeAccess):
            self.TestClass._ClassMethod = 1
        with self.assertRaises(PrivateAttributeAccess):
            self.TestClass._StaticMethod = 1
        with self.assertRaises(PrivateAttributeAccess):
            self.TestClass._MyProperty = 1
        #methods and properties
        for strAttr in self.PublicClassMethods:
            with self.assertRaises(CustomAttributeError):
                setattr(self.TestClass, strAttr, 1)
        for strAttr in self.PublicProperties:
            with self.assertRaises(CustomAttributeError):
                setattr(self.TestClass, strAttr, 1)
        for strAttr in self.PublicInstanceMethods:
            with self.assertRaises(CustomAttributeError):
                setattr(self.TestClass, strAttr, 1)
        with self.assertRaises(CustomAttributeError):
            self.TestClass.MyMethod = 1
        with self.assertRaises(CustomAttributeError):
            self.TestClass.MyProperty = 1
        with self.assertRaises(CustomAttributeError):
            self.TestClass.ClassMethod = 1
        with self.assertRaises(CustomAttributeError):
            self.TestClass.StaticMethod = 1
    
    def test_instance_setattr_nok(self):
        """
        Checks the proper modification of the existing class attributes, and
        the preservation of the resolution order and attribute visibility scope.
        
        PrivateAttributeAccess should be raised upon assignment to any protected
        attribute
        
        CustomAttributeError should be raised upon assignment to a class, static
        or instance method as well as to a property without a setter descriptor
        
        Tests REQ-FUN-001, REQ-FUN-002, REQ-FUN-003, REQ-AWN-000, REQ-AWM-001,
        REQ-AWM-002, REQ-AWM-003
        """
        objTest = self.TestClass()
        #protected attributes
        for strAttr in self.HiddenOnInstance:
            with self.assertRaises(PrivateAttributeAccess):
                setattr(objTest, strAttr, 1)
        with self.assertRaises(PrivateAttributeAccess):
            objTest._C = 1
        with self.assertRaises(PrivateAttributeAccess):
            objTest._F = 1
        with self.assertRaises(PrivateAttributeAccess):
            objTest._MyMethod = 1
        with self.assertRaises(PrivateAttributeAccess):
            objTest._ClassMethod = 1
        with self.assertRaises(PrivateAttributeAccess):
            objTest._StaticMethod = 1
        with self.assertRaises(PrivateAttributeAccess):
            objTest._MyProperty = 1
        #methods and read-only properties
        for strAttr in self.PublicClassMethods:
            with self.assertRaises(CustomAttributeError):
                setattr(objTest, strAttr, 1)
        for strAttr in self.PublicInstanceMethods:
            with self.assertRaises(CustomAttributeError):
                setattr(objTest, strAttr, 1)
        with self.assertRaises(CustomAttributeError):
            objTest.MyMethod = 1
        with self.assertRaises(CustomAttributeError):
            objTest.ClassMethod = 1
        with self.assertRaises(CustomAttributeError):
            objTest.StaticMethod = 1
        with self.assertRaises(CustomAttributeError):
            objTest.FixedProperty = 1
        del objTest
    
    def test_class_delattr_ok(self):
        """
        Checks the proper creation and deletion of the class attributes, i.e.
        that the resolution order and attribute visibility are preserved
        
        Tests REQ-FUN-001, REQ-FUN-002
        """
        #checking that the delete descriptor is called
        with self.assertRaises(CustomAttributeError):
            del self.TestClass.B
        #check the proper creation and deletion of a class data field
        lstUpHill = [clsItem() for clsItem in self.UpHill]
        lstDownHill = [clsItem() for clsItem in self.DownHill]
        self.TestClass.SomeSuperWierdName = 43
        for lstObjects in [self.DownHill, lstDownHill]:
            for objTemp in lstObjects:
                self.assertTrue(hasattr(objTemp, 'SomeSuperWierdName'))
                self.assertEqual(objTemp.SomeSuperWierdName, 43)
        for lstObjects in [self.UpHill, lstUpHill]:
            for objTemp in lstObjects:
                self.assertFalse(hasattr(objTemp, 'SomeSuperWierdName'))
        del self.TestClass.SomeSuperWierdName
        for lstObjects in [self.DownHill, lstDownHill]:
            for objTemp in lstObjects:
                self.assertFalse(hasattr(objTemp, 'SomeSuperWierdName'))
        for lstObjects in [self.UpHill, lstUpHill]:
            for objTemp in lstObjects:
                self.assertFalse(hasattr(objTemp, 'SomeSuperWierdName'))
        while len(lstUpHill):
            del lstUpHill[0]
        while len(lstDownHill):
            del lstDownHill[0]
    
    def test_instance_delattr_ok(self):
        """
        Checks the proper creation and deletion of the intance attributes, i.e.
        that the resolution order and attribute visibility are preserved
        
        Tests REQ-FUN-001, REQ-FUN-002
        """
        objTest = self.TestClass()
        #checking that the delete descriptor is called
        with self.assertRaises(CustomAttributeError):
            del objTest.E
        objTest2 = self.TestClass()
        objTest.SomeSuperWierdName = 42
        self.assertTrue(hasattr(objTest, 'SomeSuperWierdName'))
        self.assertFalse(hasattr(objTest2, 'SomeSuperWierdName'))
        self.assertFalse(hasattr(self.TestClass, 'SomeSuperWierdName'))
        self.assertEqual(objTest.SomeSuperWierdName, 42)
        del objTest.SomeSuperWierdName
        self.assertFalse(hasattr(objTest, 'SomeSuperWierdName'))
        del objTest
    
    def test_class_delattr_nok(self):
        """
        Checks the deletion of the class attributes.
        
        PrivateAttributeAccess should be raised with a protected attribute being
        deleted.
        
        NotExistingAttribute should be raised with a deletion of an unknown to
        the object attribute.
        
        CustomAttributeError should be raised if an attribute cannot be deleted,
        i.e. not defined in the object directly, or it is a method or property.
        
        Tests REQ-FUN-001, REQ-FUN-002, REQ-AWM-000, REQ-AWM-001, REQ-AWM-002,
        REQ-AWM-003
        """
        #protected attributes
        for strAttr in self.HiddenOnInstance:
            with self.assertRaises(PrivateAttributeAccess):
                delattr(self.TestClass, strAttr)
        with self.assertRaises(PrivateAttributeAccess):
            del self.TestClass._ClassMethod
        with self.assertRaises(PrivateAttributeAccess):
            del self.TestClass._C
        with self.assertRaises(PrivateAttributeAccess):
            del self.TestClass._MyProperty
        with self.assertRaises(PrivateAttributeAccess):
            del self.TestClass._StaticMethod
        with self.assertRaises(PrivateAttributeAccess):
            del self.TestClass._MyMethod
        #not existing attribues
        for strAttr in self.PublicInstanceFields:
            with self.assertRaises(NotExistingAttribute):
                delattr(self.TestClass, strAttr)
        with self.assertRaises(NotExistingAttribute):
            del self.TestClass.D
        with self.assertRaises(NotExistingAttribute):
            del self.TestClass.E
        with self.assertRaises(NotExistingAttribute):
            del self.TestClass.SomeSuperWierdName
        #methods and properties
        for strAttr in self.PublicClassMethods:
            with self.assertRaises(CustomAttributeError):
                delattr(self.TestClass, strAttr)
        for strAttr in self.PublicProperties:
            with self.assertRaises(CustomAttributeError):
                delattr(self.TestClass, strAttr)
        for strAttr in self.PublicInstanceMethods:
            with self.assertRaises(CustomAttributeError):
                delattr(self.TestClass, strAttr)
        with self.assertRaises(CustomAttributeError):
            del self.TestClass.ClassMethod
        with self.assertRaises(CustomAttributeError):
            del self.TestClass.StaticMethod
        with self.assertRaises(CustomAttributeError):
            del self.TestClass.ClassMethod
        with self.assertRaises(CustomAttributeError):
            del self.TestClass.MyMethod
        with self.assertRaises(CustomAttributeError):
            del self.TestClass.MyProperty
        with self.assertRaises(CustomAttributeError):
            del self.TestClass.FixedProperty
        #class attributes not defined in the class itself
        for strAttr in self.PublicClassFields:
            if not (strAttr in self.TestClass.__dict__.keys()):
                with self.assertRaises(CustomAttributeError):
                    delattr(self.TestClass, strAttr)
    
    def test_instance_delattr_nok(self):
        """
        Checks the deletion of the class and instance attributes.
        
        PrivateAttributeAccess should be raised with a protected attribute being
        deleted.
        
        NotExistingAttribute should be raised with a deletion of an unknown to
        the object attribute.
        
        CustomAttributeError should be raised if an attribute cannot be deleted,
        i.e. not defined in the object directly, or it is a method or property.
        
        Tests REQ-FUN-001, REQ-FUN-002, REQ-FUN-003, REQ-AWM-000, REQ-AWM-001,
        REQ-AWM-002, REQ-AWM-003
        """
        #protected attributes
        objTest = self.TestClass()
        for strAttr in self.HiddenOnInstance:
            with self.assertRaises(PrivateAttributeAccess):
                delattr(objTest, strAttr)
        with self.assertRaises(PrivateAttributeAccess):
            del objTest._ClassMethod
        with self.assertRaises(PrivateAttributeAccess):
            del objTest._C
        with self.assertRaises(PrivateAttributeAccess):
            del objTest._MyProperty
        with self.assertRaises(PrivateAttributeAccess):
            del objTest._StaticMethod
        with self.assertRaises(PrivateAttributeAccess):
            del objTest._MyMethod
        #not existing attribues
        with self.assertRaises(NotExistingAttribute):
            del objTest.SomeSuperWierdName
        #methods and properties without delete descriptor
        for strAttr in self.PublicClassMethods:
            with self.assertRaises(CustomAttributeError):
                delattr(objTest, strAttr)
        for strAttr in self.PublicProperties:
            with self.assertRaises(CustomAttributeError):
                delattr(objTest, strAttr)
        for strAttr in self.PublicInstanceMethods:
            with self.assertRaises(CustomAttributeError):
                delattr(objTest, strAttr)
        with self.assertRaises(CustomAttributeError):
            del objTest.ClassMethod
        with self.assertRaises(CustomAttributeError):
            del objTest.StaticMethod
        with self.assertRaises(CustomAttributeError):
            del objTest.ClassMethod
        with self.assertRaises(CustomAttributeError):
            del objTest.MyMethod
        with self.assertRaises(CustomAttributeError):
            del objTest.MyProperty
        with self.assertRaises(CustomAttributeError):
            del objTest.FixedProperty
        #class attributes not instance attributes!
        for strAttr in self.PublicClassFields:
            with self.assertRaises(CustomAttributeError):
                delattr(objTest, strAttr)
        del objTest

class Test_FixedTop(Test_ProtectedTop):
    """
    Test cases for the checking the implementation of the protected attributes
    and static class attributes as well as the introspection functionality.
    
    Test id: TEST-T-002. Covers the requirements: REQ-FUN-000, REQ-FUN-001,
    REQ-FUN-002, REQ-FUN-003, REQ-FUN-004, REQ-AWM-000, REQ-AWM-001,
    REQ-AWM-002, REQ-AWM-003
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super(Test_FixedTop, cls).setUpClass()
        cls.TestClass = FixedTop
        #relation with other classes
        cls.DownHill = [FixedMiddle, FixedBottom]
        cls.UpHill = []
    
    def test_class_delattr_ok(self):
        """
        Deletion of the attributes is not allowed, skip this test, everything
        is covered by test_class_delattr_nok
        
        Tests REQ-FUN-004
        """
        pass
    
    def test_instance_delattr_ok(self):
        """
        Deletion of the attributes is not allowed, skip this test, everything
        is covered by test_instance_delattr_nok
        
        Tests REQ-FUN-004
        """
        pass
    
    def test_instance_delattr_nok(self):
        """
        Checks the deletion of the class and instance attributes.
        
        PrivateAttributeAccess should be raised with a protected attribute being
        deleted.
        
        NotExistingAttribute should be raised with a deletion of an unknown to
        the object attribute.
        
        CustomAttributeError should be raised with a deletion of an existing
        public attribute
        
        Tests REQ-FUN-001, REQ-FUN-002, REQ-FUN-003, REQ-FUN-004, REQ-AWM-000,
        REQ-AWM-001, REQ-AWM-002, REQ-AWM-003
        """
        super(Test_FixedTop, self).test_instance_delattr_nok()
        objTest = self.TestClass()
        for strAttr in self.PublicInstanceFields:
            with self.assertRaises(CustomAttributeError):
                delattr(objTest, strAttr)
        del objTest
    
    def test_class_delattr_nok(self):
        """
        Checks the deletion of the class attributes.
        
        PrivateAttributeAccess should be raised with a protected attribute being
        deleted.
        
        NotExistingAttribute should be raised with a deletion of an unknown to
        the object attribute.
        
        CustomAttributeError should be raised with a deletion of an existing
        public attribute
        
        Tests REQ-FUN-001, REQ-FUN-002, REQ-AWM-000, REQ-AWM-001, REQ-AWM-002,
        REQ-AWM-003
        """
        super(Test_FixedTop, self).test_class_delattr_nok()
        for strAttr in self.PublicClassFields:
            if strAttr in self.TestClass.__dict__.keys():
                with self.assertRaises(CustomAttributeError):
                    delattr(self.TestClass, strAttr)
    
    def test_class_setattr_nok(self):
        """
        Checks the proper modification of the existing class attributes, and
        the preservation of the resolution order and attribute visibility scope.
        
        PrivateAttributeAccess should be raised upon assignment to any protected
        attribute
        
        CustomAttributeError should be raised upon assignment to a class, static
        or instance method as well as to a property
        
        NotExistingAttribute should be raised upon assigment to a non-existing
        attribute
        
        Tests REQ-FUN-001, REQ-FUN-002, REQ-AWN-000, REQ-AWM-001, REQ-AWM-002,
        REQ-AWM-003
        """
        super(Test_FixedTop, self).test_class_setattr_nok()
        with self.assertRaises(NotExistingAttribute):
            self.TestClass.SomeSuperWierdName = 1
    
    def test_instance_setattr_nok(self):
        """
        Checks the proper modification of the existing class attributes, and
        the preservation of the resolution order and attribute visibility scope.
        
        PrivateAttributeAccess should be raised upon assignment to any protected
        attribute
        
        CustomAttributeError should be raised upon assignment to a class, static
        or instance method as well as to a property without a setter descriptor
        
        NotExistingAttribute should be raised upon assigment to a non-existing
        attribute
        
        Tests REQ-FUN-001, REQ-FUN-002, REQ-FUN-003, REQ-AWN-000, REQ-AWM-001,
        REQ-AWM-002, REQ-AWM-003
        """
        super(Test_FixedTop, self).test_instance_setattr_nok()
        objTest = self.TestClass()
        with self.assertRaises(NotExistingAttribute):
            objTest.SomeSuperWierdName = 1
        del objTest

class Test_FixedMiddle(Test_FixedTop):
    """
    Test cases for the checking the implementation of the protected attributes
    and static class attributes as well as the introspection functionality.
    
    Test id: TEST-T-002. Covers the requirements: REQ-FUN-000, REQ-FUN-001,
    REQ-FUN-002, REQ-FUN-003, REQ-FUN-004, REQ-AWM-000, REQ-AWM-001,
    REQ-AWM-002, REQ-AWM-003
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super(Test_FixedMiddle, cls).setUpClass()
        cls.TestClass = FixedMiddle
        #relation with other classes
        cls.DownHill = [FixedBottom]
        cls.UpHill = [FixedTop]

class Test_FixedBottom(Test_FixedTop):
    """
    Test cases for the checking the implementation of the protected attributes
    and static class attributes as well as the introspection functionality.
    
    Test id: TEST-T-002. Covers the requirements: REQ-FUN-000, REQ-FUN-001,
    REQ-FUN-002, REQ-FUN-003, REQ-AWM-000, REQ-AWM-001, REQ-AWM-002, REQ-AWM-003
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super(Test_FixedBottom, cls).setUpClass()
        cls.TestClass = FixedBottom
        #relation with other classes
        cls.DownHill = []
        cls.UpHill = [FixedTop, FixedMiddle]

class Test_ProtectedMiddle(Test_ProtectedTop):
    """
    Test cases for the checking the implementation of the protected attributes
    and static class attributes as well as the introspection functionality.
    
    Test id: TEST-T-001. Covers the requirements: REQ-FUN-000, REQ-FUN-001,
    REQ-FUN-002, REQ-FUN-003, REQ-AWM-000, REQ-AWM-001, REQ-AWM-002, REQ-AWM-003
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super(Test_ProtectedMiddle, cls).setUpClass()
        cls.TestClass = ProtectedMiddle
        #relation with other classes
        cls.DownHill = [ProtectedBottom]
        cls.UpHill = [ProtectedTop]

class Test_ProtectedBottom(Test_ProtectedTop):
    """
    Test cases for the checking the implementation of the protected attributes
    and static class attributes as well as the introspection functionality.
    
    Test id: TEST-T-001. Covers the requirements: REQ-FUN-000, REQ-FUN-001,
    REQ-FUN-002, REQ-FUN-003, REQ-FUN-004, REQ-AWM-000, REQ-AWM-001,
    REQ-AWM-002, REQ-AWM-003
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super(Test_ProtectedBottom, cls).setUpClass()
        cls.TestClass = ProtectedBottom
        #relation with other classes
        cls.DownHill = []
        cls.UpHill = [ProtectedTop, ProtectedMiddle]

class Test_Introspection(unittest.TestCase):
    """
    Test cases for the checking the introspection functionality
    
    Test id: TEST-T-003. Covers the requirements: REQ-FUN-005.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.AllClasses = [ProtectedTop, ProtectedMiddle, ProtectedBottom,
                                            FixedTop, FixedMiddle, FixedBottom]
        cls.PublicClassMethods = ['ClassMethod', 'StaticMethod',
                                    'getClassMethods', 'getClassFields',
                                        'getInstanceMethods', 'getProperties']
        cls.PublicInstanceMethods = ['MyMethod', 'getInstanceFields']
        cls.PublicProperties = ['MyProperty', 'FixedProperty']
        cls.PublicClassFields = ['A', 'B']
        cls.PublicInstanceFields = ['D', 'E']
    
    def test_getClassMethods(self):
        """
        Tests REQ-FUN-005. All classes and their instances must properly find
        all public class and static methods available to them.
        """
        for clsTest in self.AllClasses:
            lstReference = self.PublicClassMethods
            lstTest = clsTest.getClassMethods()
            self.assertItemsEqual(lstTest, lstReference)
            objTest = clsTest()
            lstTest = objTest.getClassMethods()
            self.assertItemsEqual(lstTest, lstReference)
            del objTest
    
    def test_getClassFields(self):
        """
        Tests REQ-FUN-005. All classes and their instances must properly find
        all public static class fields (not methods or properties).
        """
        for clsTest in self.AllClasses:
            lstReference = self.PublicClassFields
            lstTest = clsTest.getClassFields()
            self.assertItemsEqual(lstTest, lstReference)
            objTest = clsTest()
            lstTest = objTest.getClassFields()
            self.assertItemsEqual(lstTest, lstReference)
            del objTest
    
    def test_getProperties(self):
        """
        Tests REQ-FUN-005. All classes and their instances must properly find
        all public properties.
        """
        for clsTest in self.AllClasses:
            lstReference = self.PublicProperties
            lstTest = clsTest.getProperties()
            self.assertItemsEqual(lstTest, lstReference)
            objTest = clsTest()
            lstTest = objTest.getProperties()
            self.assertItemsEqual(lstTest, lstReference)
            del objTest
    
    def test_getInstanceMethods(self):
        """
        Tests REQ-FUN-005. All classes and their instances must properly find
        all public instance methods.
        """
        for clsTest in self.AllClasses:
            lstReference = self.PublicInstanceMethods
            lstTest = clsTest.getInstanceMethods()
            self.assertItemsEqual(lstTest, lstReference)
            objTest = clsTest()
            lstTest = objTest.getInstanceMethods()
            self.assertItemsEqual(lstTest, lstReference)
            del objTest
    
    def test_getInstanceFields(self):
        """
        Tests REQ-FUN-005. All classes' instances must properly find all public
        instance attributes.
        """
        for clsTest in self.AllClasses:
            lstReference = self.PublicInstanceFields
            objTest = clsTest()
            lstTest = objTest.getInstanceFields()
            self.assertItemsEqual(lstTest, lstReference)
            del objTest
    

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_Singleton)

TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_ProtectedTop)

TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_FixedTop)

TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_FixedMiddle)

TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_FixedBottom)

TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_ProtectedMiddle)

TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(Test_ProtectedBottom)

TestSuite8 = unittest.TestLoader().loadTestsFromTestCase(Test_Introspection)

TestSuite = unittest.TestSuite()

TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                                        TestSuite6, TestSuite7, TestSuite8])

if __name__ == "__main__":
    sys.stdout.write("Conducting libencapsulation library tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)