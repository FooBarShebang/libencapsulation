#!/usr/bin/python

#imports

from pa002_attributes_test03 import TestClass1, TestClass2

#classes

#testing area

if __name__ == "__main__":
    #initialization
    objTest1 = TestClass1()
    objTest2 = TestClass2()
    #class fields
    #+ public
    print 'TestClass1 public class field', TestClass1.testNormalClassAttribute
    print 'TestClass2 public class field', TestClass2.testNormalClassAttribute
    print 'objTest1 public class field', objTest1.testNormalClassAttribute
    print 'objTest2 public class field', objTest2.testNormalClassAttribute
    print 'Change value of the public class field on the instance objTest2'
    objTest2.testNormalClassAttribute = 'New normal class attribute'
    print 'TestClass1 public class field', TestClass1.testNormalClassAttribute
    print 'TestClass2 public class field', TestClass2.testNormalClassAttribute
    print 'objTest1 public class field', objTest1.testNormalClassAttribute
    print 'objTest2 public class field', objTest2.testNormalClassAttribute
    print 'Change value of the public class field on the class TestClass2'
    TestClass2.testNormalClassAttribute = 'Newer normal class attribute'
    print 'TestClass1 public class field', TestClass1.testNormalClassAttribute
    print 'TestClass2 public class field', TestClass2.testNormalClassAttribute
    print 'objTest1 public class field', objTest1.testNormalClassAttribute
    print 'objTest2 public class field', objTest2.testNormalClassAttribute
    print 'Create new instances of TestClass1 -> objTest3, TestClass2 -> objTest4'
    objTest3 = TestClass1()
    objTest4 = TestClass2()
    print 'objTest3 public class field', objTest3.testNormalClassAttribute
    print 'objTest4 public class field', objTest4.testNormalClassAttribute
    print 'Delete last two instances'
    del objTest3
    del objTest4
    #+ private
    print 'TestClass1 private class field', TestClass1._testHiddenClassAttribute
    try:
        print 'TestClass2 private class field', TestClass2._testHiddenClassAttribute
    except Exception as err:
        print '>', err.message
    print 'TestClass2 private class field', type.__getattribute__(TestClass2, '_testHiddenClassAttribute')
    print 'objTest1 private class field', objTest1._testHiddenClassAttribute
    try:
        print 'objTest2 private class field', TestClass2._testHiddenClassAttribute
    except Exception as err:
        print '>', err.message
    print 'objTest2 private class field', object.__getattribute__(objTest2, '_testHiddenClassAttribute')
    print 'Changing the values on the classes'
    TestClass1._testHiddenClassAttribute = "test 1"
    try:
        TestClass2._testHiddenClassAttribute = "test 2"
    except Exception as err:
        print '>', err.message
    type.__setattr__(TestClass2, '_testHiddenClassAttribute', 'test 2')
    print 'TestClass1 private class field', TestClass1._testHiddenClassAttribute
    try:
        print 'TestClass2 private class field', TestClass2._testHiddenClassAttribute
    except Exception as err:
        print '>', err.message
    print 'TestClass2 private class field', type.__getattribute__(TestClass2, '_testHiddenClassAttribute')
    print 'objTest1 private class field', objTest1._testHiddenClassAttribute
    try:
        print 'objTest2 private class field', TestClass2._testHiddenClassAttribute
    except Exception as err:
        print '>', err.message
    print 'objTest2 private class field', object.__getattribute__(objTest2, '_testHiddenClassAttribute')
    print 'Changing the values on the instances'
    objTest1._testHiddenClassAttribute = "test 3"
    try:
        objTest2._testHiddenClassAttribute = "test 4"
    except Exception as err:
        print '>', err.message
    object.__setattr__(objTest2, '_testHiddenClassAttribute', 'test 4')
    print 'TestClass1 private class field', TestClass1._testHiddenClassAttribute
    try:
        print 'TestClass2 private class field', TestClass2._testHiddenClassAttribute
    except Exception as err:
        print '>', err.message
    print 'TestClass2 private class field', type.__getattribute__(TestClass2, '_testHiddenClassAttribute')
    print 'objTest1 private class field', objTest1._testHiddenClassAttribute
    try:
        print 'objTest2 private class field', TestClass2._testHiddenClassAttribute
    except Exception as err:
        print '>', err.message
    print 'objTest2 private class field', object.__getattribute__(objTest2, '_testHiddenClassAttribute')
    objTest3 = TestClass1()
    objTest4 = TestClass2()
    print 'objTest3 private class field', objTest3._testHiddenClassAttribute
    try:
        print 'objTest4 private class field', objTest4._testHiddenClassAttribute
    except Exception as err:
        print '>', err.message
    print 'objTest4 private class field', object.__getattribute__(objTest4, '_testHiddenClassAttribute')
    print 'Delete last two instances'
    del objTest3
    del objTest4
    #instance fields
    #+ public
    try:
        print 'TestClass1 public instance attribute', TestClass1.testNormalInstanceAttribute
    except Exception as err:
        print '>', err.message
    try:
        print 'TestClass2 public instance attribute', TestClass2.testNormalInstanceAttribute
    except Exception as err:
        print '>', err.message
    print 'objTest1 public instance attribute', objTest1.testNormalInstanceAttribute
    print 'objTest2 public instance attribute', objTest2.testNormalInstanceAttribute
    print 'Change values...'
    objTest2.testNormalInstanceAttribute = 'test 1'
    print 'objTest1 public instance attribute', objTest1.testNormalInstanceAttribute
    print 'objTest2 public instance attribute', objTest2.testNormalInstanceAttribute
    objTest1.testNormalInstanceAttribute = 'test 2'
    print 'objTest1 public instance attribute', objTest1.testNormalInstanceAttribute
    print 'objTest2 public instance attribute', objTest2.testNormalInstanceAttribute
    try:
        print 'TestClass1 public instance attribute', TestClass1.testNormalInstanceAttribute
    except Exception as err:
        print '>', err.message
    try:
        print 'TestClass2 public instance attribute', TestClass2.testNormalInstanceAttribute
    except Exception as err:
        print '>', err.message
    #+ private
    try:
        print 'TestClass1 private instance attribute', TestClass1._testHiddenInstanceAttribute
    except Exception as err:
        print '>', err.message
    try:
        print 'TestClass2 private instance attribute', TestClass2._testHiddenInstanceAttribute
    except Exception as err:
        print '>', err.message
    print 'objTest1 private instance attribute', objTest1._testHiddenInstanceAttribute
    try:
        print 'objTest2 private instance attribute', objTest2._testHiddenInstanceAttribute
    except Exception as err:
        print '>', err.message
    print 'objTest2 private instance attribute', object.__getattribute__(objTest2, '_testHiddenInstanceAttribute')
    print 'Change values...'
    objTest1._testHiddenInstanceAttribute = 'test 1'
    print 'objTest1 private instance attribute', objTest1._testHiddenInstanceAttribute
    try:
        print 'objTest2 private instance attribute', objTest2._testHiddenInstanceAttribute
    except Exception as err:
        print '>', err.message
    print 'objTest2 private instance attribute', object.__getattribute__(objTest2, '_testHiddenInstanceAttribute')
    try:
        objTest2._testHiddenInstanceAttribute = 'test 2'
    except Exception as err:
        print '>', err.message
    object.__setattr__(objTest2, '_testHiddenInstanceAttribute', 'test 2')
    try:
        print 'TestClass1 private instance attribute', TestClass1._testHiddenInstanceAttribute
    except Exception as err:
        print '>', err.message
    try:
        print 'TestClass2 private instance attribute', TestClass2._testHiddenInstanceAttribute
    except Exception as err:
        print '>', err.message
    print 'objTest1 private instance attribute', objTest1._testHiddenInstanceAttribute
    try:
        print 'objTest2 private instance attribute', objTest2._testHiddenInstanceAttribute
    except Exception as err:
        print '>', err.message
    print 'objTest2 private instance attribute', object.__getattribute__(objTest2, '_testHiddenInstanceAttribute')
    #class methods
    #+ public
    print 'TestClass1 public class method', TestClass1.getNormalClassMethod()
    print 'TestClass2 public class method', TestClass2.getNormalClassMethod()
    print 'objTest1 public class method', objTest1.getNormalClassMethod()
    print 'objTest2 public class method', objTest2.getNormalClassMethod()
    #+ private
    print 'TestClass1 private class method', TestClass1._getHiddenClassMethod()
    try:
        print 'TestClass2 private class method', TestClass2._getHiddenClassMethod()
    except Exception as err:
        print '>', err.message
    print type.__getattribute__(TestClass2, '_getHiddenClassMethod')()
    print 'objTest1 private class method', objTest1._getHiddenClassMethod()
    try:
        print 'objTest2 private class method', objTest2._getHiddenClassMethod()
    except Exception as err:
        print '>', err.message
    print object.__getattribute__(objTest2, '_getHiddenClassMethod')()
    #instance methods
    #+ public
    try:
        print 'TestClass1 public instance method', TestClass1.getNormalInstanceMethod()
    except Exception as err:
        print '>', err.message
    try:
        print 'TestClass2 public instance method', TestClass2.getNormalInstanceMethod()
    except Exception as err:
        print '>', err.message
    print 'objTest1 instance class method', objTest1.getNormalInstanceMethod()
    print 'objTest2 instance class method', objTest2.getNormalInstanceMethod()
    #+ private
    try:
        print 'TestClass1 private instance method', TestClass1._getHiddenInstanceMethod()
    except Exception as err:
        print '>', err.message
    try:
        print 'TestClass2 private instance method', TestClass2._getHiddenInstanceMethod()
    except Exception as err:
        print '>', err.message
    print 'objTest1 private instance method', objTest1._getHiddenInstanceMethod()
    try:
        print 'objTest2 private instance method', objTest2._getHiddenInstanceMethod()
    except Exception as err:
        print '>', err.message
    print object.__getattribute__(objTest2, '_getHiddenInstanceMethod')()