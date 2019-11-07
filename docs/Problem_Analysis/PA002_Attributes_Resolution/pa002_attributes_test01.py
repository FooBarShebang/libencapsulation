#!/usr/bin/python

#classes

class TestClass1(object):

    testNormalClassAttribute = "Normal class attribute"
    _testHiddenClassAttribute = "Hidden class attribute"

    def __init__(self):
        self.testNormalInstanceAttribute = "Normal instance attribute"
        self._testHiddenInstanceAttribute = "Hidden instance attribute"

    @classmethod
    def getFullName(cls):
        return "{0}.{1}".format(cls.__module__, cls.__name__)

    @classmethod
    def getNormalClassMethod(cls):
        return "Normal class method"

    @classmethod
    def _getHiddenClassMethod(cls):
        return "Hidden class method"

    def getNormalInstanceMethod(self):
        return "Normal instance method"

    def _getHiddenInstanceMethod(self):
        return "Hiden instance method"

    @property
    def MyProperty(self):
        return "Getter property"

    @MyProperty.setter
    def MyProperty(self, Value):
        print "Using setter property"

#testing area

if __name__ == "__main__":
    print "TestClass1 info {}".format(TestClass1.getFullName())
    print "Class dictionary {}".format(TestClass1.__dict__)
    print "Access to class attributes"
    stTemp = TestClass1.testNormalClassAttribute
    TestClass1.testNormalClassAttribute = stTemp
    print stTemp
    stTemp = TestClass1._testHiddenClassAttribute
    TestClass1._testHiddenClassAttribute = stTemp
    print stTemp
    print "Access to class methods"
    print TestClass1.getNormalClassMethod()
    print TestClass1._getHiddenClassMethod()
    objTest = TestClass1()
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

