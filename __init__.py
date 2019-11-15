#usr/bin/python
"""
Library libencapsulation

Implements the distinction between the 'public' and 'protected' attributes (to
which the access is denied), C++ static like class attributes, fixed data
structure of the classes and their instances, and introspection methods.

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

__project__ = 'Partial implementation of the encapsulation in Python'
__version_info__= (0, 0, 2)
__version_suffix__= '-dev1'
__version__= ''.join(['.'.join(map(str, __version_info__)), __version_suffix__])
__date__ = '14-11-2019'
__status__ = 'Development'
__author__ = 'Anton Azarov'
__maintainer__ = 'a.azarov@diagnoptics.com'
__license__ = 'LGPL-3.0'
__copyright__ = 'Diagnoptics Technologies B.V.'

#import all base classes and exceptions into the library's upper level namespace

from classes import ProtectedAttributes, FixedAttributes
from classes import CustomAttributeError, ConstantAttributeAssignment
from classes import NotExistingAttribute, PrivateAttributeAccess