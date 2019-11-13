#usr/bin/python
"""
Module libencapsulation.test

Implements a set of unit-tests for the library.
"""

__version__ = "0.1.0.0"
__date__ = "13-11-2019"
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

from libexceptions import PrivateAttributeAccess

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
    
    def __get__(self, obj, objType = None):
        """
        Returns the internally stored string with an exclamation mark attached.
        
        Signature:
            type A/, type type A OR None/ -> str
        
        Args:
            obj: type A, 'parent' object requesting value of its attributes,
                which is an instance of this class
            objType: (optional) type type A, the type (class) of the 'parent'
                object
        
        Returns:
            str: the internally stored string with an exclamation mark attached
        
        Version 0.1.0.0
        """
        return '{}!'.format(self.Value)
    
    def __set__(self, obj, gValue):
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
        return "property"
    
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
        return "property"
    
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
    REQ-FUN-002, REQ-FUN-003, REQ-FUN-004, REQ-FUN-005, REQ-AWM-000,
    REQ-AWM-001, REQ-AWM-002, REQ-AWM-003
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = ProtectedTop
        cls.PublicOnClass = ['ClassMethod', 'StaticMethod', 'MyProperty',
                                                        'MyMethod', 'A', 'B']
        cls.PublicOnInstance = list(cls.PublicOnClass)
        cls.PublicOnInstance.extend(['D', 'E'])
        cls.HiddenOnClass = ['_ClassMethod', '_StaticMethod', '_MyProperty',
                                                            '_MyMethod', '_C']
        cls.HiddenOnInstance = list(cls.HiddenOnClass)
        cls.HiddenOnInstance.extend(['_F'])
    
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
        class attributes accessed from a class.
        
        Tests REQ-FUN-002
        """
        for strAttr in self.HiddenOnClass:
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
        getattr() built-in function should return the proper value of the public
        class attributes accessed from a class.
        
        Tests REQ-FUN-001, REQ-FUN-002
        """
        #methods
        self.assertEqual(self.TestClass.ClassMethod(), 'class method')
        self.assertEqual(self.TestClass.StaticMethod(), 'static method')
        #fields
        self.assertEqual(self.TestClass.A, 1)
    
    def test_instance_getattr_ok(self):
        """
        getattr() built-in function should return the proper value of the public
        class and instance attributes accessed from an instance.
        
        Tests REQ-FUN-001, REQ-FUN-003
        """
        objTest = self.TestClass()
        #methods
        self.assertEqual(objTest.ClassMethod(), 'class method')
        self.assertEqual(objTest.StaticMethod(), 'static method')
        self.assertEqual(objTest.MyMethod(), 'instance method')
        #property
        self.assertEqual(objTest.MyProperty, 'property')
        #fields
        self.assertEqual(objTest.A, 1)
        self.assertEqual(objTest.D, 1)
        del objTest
    
    def test_class_getattr_nok(self):
        """
        getattr() built-in function should raise the PrivateAttributeAccess
        exception upon access of the protected class attributes accessed from a
        class. NotExistingAttribute exception should be raised if a non-
        existing attributed is accessed.
        
        Tests REQ-FUN-001, REQ-FUN-002, REQ-AWM-000, REQ-AWM-001, REQ-AWM-002
        """
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = self.TestClass._ClassMethod()
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = self.TestClass._StaticMethod()
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = self.TestClass._C
    
    def test_instance_getattr_nok(self):
        """
        getattr() built-in function should raise the PrivateAttributeAccess
        exception upon access of the protected class and instance attributes
        accessed from a class. NotExistingAttribute exception should be raised
        if a non-existing attributed is accessed.
        
        Tests REQ-FUN-001, REQ-FUN-003, REQ-AWM-000, REQ-AWM-001, REQ-AWM-002
        """
        objTest = self.TestClass()
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = objTest._ClassMethod()
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = objTest._StaticMethod()
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = objTest._MyMethod()
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = objTest._MyProperty
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = objTest._C
        with self.assertRaises(PrivateAttributeAccess):
            gTemp = objTest._F
        del objTest

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_Singleton)

TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_ProtectedTop)

TestSuite = unittest.TestSuite()

TestSuite.addTests([TestSuite1, TestSuite2])

if __name__ == "__main__":
    sys.stdout.write("Conducting libencapsulation library tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)