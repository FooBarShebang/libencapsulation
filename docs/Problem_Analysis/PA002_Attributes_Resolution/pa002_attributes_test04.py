#!/usr/bin/python

#imports

from pa002_attributes_test03 import TestClass2

#testing area

if __name__ == "__main__":
    print "TestClass2 info {}".format(TestClass2.getFullName())
    print "Class dictionary {}".format(TestClass2.__dict__)
    print "Access to class attributes"
    stTemp = TestClass2.testNormalClassAttribute
    print stTemp
    TestClass2.testNormalClassAttribute = stTemp
    try:
        stTemp = TestClass2.__dict__["_testHiddenClassAttribute"]
        print stTemp
    except Exception as err:
        print err, "\tError !"
    try:
        TestClass2.__dict__["_testHiddenClassAttribute"] = stTemp
    except Exception as err:
        print err, "\tError !"
    print "Access to class methods"
    print TestClass2.getNormalClassMethod()
    try:
        print TestClass2.__dict__["_getHiddenClassMethod"]()
    except Exception as err:
        print err, "\tError !"
    objTest = TestClass2()
    print "Instance dictionary {}".format(objTest.__dict__)
    print "Access to class attributes"
    print objTest.testNormalClassAttribute
    try:
        stTemp = objTest.__class__.__dict__["_testHiddenClassAttribute"]
        print stTemp
    except Exception as err:
        print err, "\tError !"
    try:
        objTest.__class__.__dict__["_testHiddenClassAttribute"] = stTemp
    except Exception as err:
        print err, "\tError !"
    print "Access to class methods"
    print objTest.getNormalClassMethod()
    try:
        print objTest.__class__.__dict__["_getHiddenClassMethod"]()
    except Exception as err:
        print err, "\tError !"
    print "Access to instance attributes"
    print objTest.testNormalInstanceAttribute
    try:
        stTemp = objTest.__dict__["_testHiddenInstanceAttribute"]
        print stTemp
    except Exception as err:
        print err, "\tError !"
    try:
        objTest.__dict__["_testHiddenInstanceAttribute"] = stTemp
    except Exception as err:
        print err, "\tError !"
    print "Access to instance methods"
    print objTest.getNormalInstanceMethod()
    try:
        print objTest.__class__.__dict__["_getHiddenInstanceMethod"]()
    except Exception as err:
        print err, "\tError !"
    print "Access to properties"
    print objTest.MyProperty
    objTest.MyProperty = 1
