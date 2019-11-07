#!/usr/bin/python

#imports

from pa002_attributes_test01 import TestClass1

class TestClass2(TestClass1):
    pass

#testing area

if __name__ == "__main__":
    print "TestClass2 info {}".format(TestClass2.getFullName())
    print "Class dictionary {}".format(TestClass2.__dict__)
    print "Access to class attributes"
    stTemp = TestClass2.testNormalClassAttribute
    TestClass2.testNormalClassAttribute = stTemp
    print stTemp
    stTemp = TestClass2._testHiddenClassAttribute
    TestClass2._testHiddenClassAttribute = stTemp
    print stTemp
    print "Access to class methods"
    print TestClass2.getNormalClassMethod()
    print TestClass2._getHiddenClassMethod()
    objTest = TestClass2()
    print "Instance dictionary {}".format(objTest.__dict__)
    print "Access to class attributes"
    stTemp = objTest.testNormalClassAttribute
    objTest.testNormalClassAttribute = stTemp
    print stTemp
    stTemp = objTest._testHiddenClassAttribute
    objTest._testHiddenClassAttribute = stTemp
    print stTemp
    print "Access to class methods"
    print objTest.getNormalClassMethod()
    print objTest._getHiddenClassMethod()
    print "Access to instance attributes"
    stTemp = objTest.testNormalInstanceAttribute
    objTest.testNormalInstanceAttribute = stTemp
    print stTemp
    stTemp = objTest._testHiddenInstanceAttribute
    objTest._testHiddenInstanceAttribute = stTemp
    print stTemp
    print "Access to instance methods"
    print objTest.getNormalInstanceMethod()
    print objTest._getHiddenInstanceMethod()
    print "Access to properties"
    print objTest.MyProperty
    objTest.MyProperty = 1

