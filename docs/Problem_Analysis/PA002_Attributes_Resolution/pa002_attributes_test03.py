#!/usr/bin/python

#classes

class TestClass1(object):

    testNormalClassAttribute = "Normal class attribute"
    _testHiddenClassAttribute = "Hidden class attribute"

    def __init__(self):
        self.testNormalInstanceAttribute = "Normal instance attribute"
        try:
            self.__dict__[
                "_testHiddenInstanceAttribute"] = "Hidden instance attr"
        except Exception as err:
            print err

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

class PrivateFieldMeta(type):
    #special methods

    def __getattribute__(self, stAttrName):
        objClass = type.__getattribute__(self, "__class__")
        stModule = type.__getattribute__(objClass, "__module__")
        stClassName = type.__getattribute__(objClass, "__name__")
        stCaller = "{0}.{1}.__getattribute__()".format(stModule,
                                                            stClassName)
        stMessage = "{} cannot access to get a".format(stCaller)
        if stAttrName.startswith("_"):
            if not stAttrName.startswith("__"):
                stMessage = "{0} hidden attribute or method {1}".format(
                                                stMessage, stAttrName)
                raise Exception(stMessage)
        try:
            result = type.__getattribute__(self, stAttrName)
        except AttributeError:
            stMessage = "{0} normal attribute or method {1}".format(
                                                stMessage, stAttrName)
            raise Exception(stMessage)
        return result

    def __setattr__(self, stAttrName, *args):
        objClass = type.__getattribute__(self, "__class__")
        stModule = type.__getattribute__(objClass, "__module__")
        stClassName = type.__getattribute__(objClass, "__name__")
        stCaller = "{0}.{1}.__setattr__()".format(stModule,
                                                            stClassName)
        stMessage = "{} cannot access to set a".format(stCaller)
        if stAttrName.startswith("_"):
            if not stAttrName.startswith("__"):
                stMessage = "{0} hidden attribute or method {1}".format(
                                                stMessage, stAttrName)
                raise Exception(stMessage)
        try:
            type.__setattr__(self, stAttrName, *args)
        except AttributeError:
            stMessage = "{0} normal attribute or method {1}".format(
                                                stMessage, stAttrName)
            raise Exception(stMessage)

class PrivateFieldsClass(TestClass1):

    __metaclass__ = PrivateFieldMeta

    #special methods

    def __getattribute__(self, stAttrName):
        stClassName = super(PrivateFieldsClass, self).__getattribute__(
                                                        "getFullName")()
        stCaller = "{}.__getattribute__()".format(stClassName)
        stMessage = "{} cannot access to get a".format(stCaller)
        if stAttrName.startswith("_"):
            if not stAttrName.startswith("__"):
                stMessage = "{0} hidden attribute or method {1}".format(
                                                stMessage, stAttrName)
                raise Exception(stMessage)
        try:
            result = super(PrivateFieldsClass, self).__getattribute__(
                                                            stAttrName)
        except AttributeError:
            stMessage = "{0} normal attribute or method {1}".format(
                                                stMessage, stAttrName)
            raise Exception(stMessage)
        return result

    def __setattr__(self, stAttrName, *args):
        stClassName = super(PrivateFieldsClass, self).__getattribute__(
                                                        "getFullName")()
        stCaller = "{}.__setattr__()".format(stClassName)
        stMessage = "{} cannot access to set a".format(stCaller)
        if stAttrName.startswith("_"):
            if not stAttrName.startswith("__"):
                stMessage = "{0} hidden attribute or method {1}".format(
                                                stMessage, stAttrName)
                raise Exception(stMessage)
        try:
            super(PrivateFieldsClass, self).__setattr__(stAttrName, *args)
        except AttributeError:
            stMessage = "{0} normal attribute or method {1}".format(
                                                stMessage, stAttrName)
            raise Exception(stMessage)

class TestClass2(PrivateFieldsClass):
    pass

#testing area

if __name__ == "__main__":
    print "TestClass2 info {}".format(TestClass2.getFullName())
    print "Class dictionary {}".format(TestClass2.__dict__)
    print "Access to class attributes"
    stTemp = TestClass2.testNormalClassAttribute
    print stTemp
    TestClass2.testNormalClassAttribute = stTemp
    try:
        stTemp = TestClass2._testHiddenClassAttribute
        print stTemp
    except Exception as err:
        print err, "\tError !"
    try:
        TestClass2._testHiddenClassAttribute = stTemp
    except Exception as err:
        print err, "\tError !"
    print "Access to class methods"
    print TestClass2.getNormalClassMethod()
    try:
        print TestClass2._getHiddenClassMethod()
    except Exception as err:
        print err, "\tError !"
    objTest = TestClass2()
    print "Instance dictionary {}".format(objTest.__dict__)
    print "Access to class attributes"
    print objTest.testNormalClassAttribute
    try:
        stTemp = objTest._testHiddenClassAttribute
        print stTemp
    except Exception as err:
        print err, "\tError !"
    try:
        objTest._testHiddenClassAttribute = stTemp
    except Exception as err:
        print err, "\tError !"
    print "Access to class methods"
    print objTest.getNormalClassMethod()
    try:
        print objTest._getHiddenClassMethod()
    except Exception as err:
        print err, "\tError !"
    print "Access to instance attributes"
    print objTest.testNormalInstanceAttribute
    try:
        stTemp = objTest._testHiddenInstanceAttribute
        print stTemp
    except Exception as err:
        print err, "\tError !"
    try:
        objTest._testHiddenInstanceAttribute = stTemp
    except Exception as err:
        print err, "\tError !"
    print "Access to instance methods"
    print objTest.getNormalInstanceMethod()
    try:
        print objTest._getHiddenInstanceMethod()
    except Exception as err:
        print err, "\tError !"
    print "Access to properties"
    print objTest.MyProperty
    objTest.MyProperty = 1
