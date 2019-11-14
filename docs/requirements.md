# Requirements for the libencapsulation library

## Conventions

Requirements listed in this document are constructed according to the following structure:

**Requirement ID:** REQ-UVW-XYZ

**Title:** Title / name of the requirement

**Description:** Descriprion / definition of the requirement

**Verification Method:** I / A / T / D

The requirement ID starts with the fixed prefix 'REQ'. The prefix is followed by 3 letters abbreviation (in here 'UVW'), which defines the requiement type - e.g. 'FUN' for a functional and capability requirement, 'AWM' for an alarm, warnings and operator messages, etc. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the requirement ordering number for this object. E.g. 'REQ-FUN-112'. Each requirement type has its own counter, thus 'REQ-FUN-112' and 'REQ-AWN-112' requirements are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Functional and capability requirements

**Requirement ID:** REQ-FUN-000

**Title:** C++ like static class fields

**Description:** The library should implement classes with the modified attributes resolution scheme such that the C++ static members is emulated, i.e. the assignement to an attribute defined as *class attribute* of a super class does not create an entry in the object's own dictionary (instance or class) but changes the value of that attribute of the super class. Thus, the changes made in the sub-class or its instance propagate upwards along the MRO chain up to the super class, where the corresponding attribute is last (re-) defined; and these changes are visible to all sub-classes extending this super class as well to their instances.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-001

**Title:** Full support of the descriptors

**Description:** The modification of the attributes resolution scheme should also ensure that the getter and setter descriptor methods of the class attributes are envoked upon access via a class without instantiation. Also the getter and setter descriptor methods of the instance attributes should be called upon access via a class' instance.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-002

**Title:** Protected class attributes

**Description:** The modification of the attributes resolution scheme should also ensure that the *class attributes* (data fields; class, static and instance methods) with the names starting with a single underscore ('_') but not two or more undescores are considered to be *private*, internal implementation details of the class, although they should be inherited by the sub-classes. In C++ terms such attributes are *protected*. These attributes should not be accessible to the class' clients neither via dot notation nor using the standard functions *getattr*(), *setattr*() and *delattr*(). The standard function *hasattr*() should return **False** concerning such attributes. However, it should be possible to define such attributes within the class's body definition itself using the dot notation.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-003

**Title:** Protected instance attributes

**Description:** The modification of the attributes resolution scheme should also ensure that the *instance attributes* (stored in the instance's own dictionary) with the names starting with a single underscore ('_') but not two or more undescores are considered to be *private* to this specific object. These attributes should not be accessible to the object's clients neither via dot notation nor using the standard functions *getattr*(), *setattr*() and *delattr*(). The standard function *hasattr*() should return **False** concerning such attributes. However, it should be possible to define such attributes using the dot notation during the instantiation.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-004

**Title:** Creation and deletion of the class and instance attributes during the run-time

**Description:** The modification of the attributes resolution scheme should implement two modes of operation: one mode should allow creation and deletion of the new class or instance attributes on demand as within the standard Python data model, whereas the second mode should not allow creation of new class attributes outside the class' definition or new instance attributes after the class' instantiation as well as deletion of the attributes. **Note**: *delattr*(obj, attr) and *del obj.attr* should allow deletion of only the *local* class or instance attributes, i.e. those stored in the object's own dictionary.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-005

**Title:** Introspection functionality

**Description:** Due to the non-trivial modifications introduced to the arguments resolution scheme the classes implemented in the library should provide the methods to list the *public class data fieds* (all attributes defined along MRO chain which are not explicitely defined as class, static of instance methods or property and can be accessed with and without instantiation), the *public class methods* (all attributes defined along MRO chain which are explicitely defined as class or static methods), the *public instance data fields* (all 'public' attributes stored in the instance dictionary), the *public instance methods* (all attributes defined along MRO chain which are explicitely defined as instance methods) and the *public properties* (all attributes defined along MRO chain which are explicitely defined as properties). The 'public' attributes are those, which names do not start with any amount of underscores. Note that the instance 'data attributes' can store callable objects: functions, classes or instances of the classes with the defined *\_\_call\_\_*() method - which will behave as if methods, i.e. object.attribute() call is completely legal. The class 'data attributes' can store classes or instances of the classes with the defined *\_\_call\_\_*() method but not the functions with the same behaviour. Functions stored as the class attributes must be explicitely converted into *static methods* to work properly. It is left up to the class' client to define if the 'data field' contain a callable object or not.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-006

**Title:** Singleton behaviour

**Description:** All classes derived from those defined in the library should behave as singletons, i.e. they cannot be instantiated and have only class level attributes, unless they re-define the special, *protected* instance method, which is called during the instantiation and is responsible for the creation of the instance attributes.

**Verification Method:** T

## Alarms, warnings and operator messages

**Requirement ID:** REQ-AWM-000

**Title:** Customised exceptions

**Description:** Instead of the generic, standard Python exception **AttributeError** the customized exceptions **CustomAttributeError**, **NotExistingAttribute** and **PrivateAttributeAccess** should be raised, which are defined in the library *libexceptions* and are sub-classes of the **AttributeError** exception.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-001

**Title:** Protected attribute access exception

**Description:** The **PrivateAttributeAccess** exception should be raised in response to read / modification or deletion of any *protected* class or instance attribute.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-002

**Title:** Missing attribute access exception

**Description:** The **NotExistingAttribute** exception should be raised in response to read access to an attribute not defined in the instance dictionary or in any of the (super) classes along the MRO chain. The same exception should be raised upon deletion requirest concerning an instance attribute not defined in the instance's dictionary or a class attribute not defined in the class' own dictionary when envoked on the class level without instantiation. The same exception should be raised in response to the attribute modification if the attribute is not found in neither the instance's dictionary or in any of the super classes' dictionary and the creation of the attributes 'on the fly' is not allowed.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-003

**Title:** Forbidden deletion or modification of an attribute

**Description:** The **CustomAttributeError** exception should be raised in response to an attempt of deletion of a 'public', *magic* or name mangling attribute of a class or instance of a class with the fixed data structure. The same error should be raised if the attributed to be deleted or modified is a method (class, static, instance) or a property access without instantiation of a class. Finally, the same exception should be raised if the descriptors of a class data attribute or instance attribute.

**Verification Method:** T
