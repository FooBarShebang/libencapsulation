# Library libencapsulation

Implements 'protected' attributes of classes and class instance objects, which are not 'visible' to a class\` client. Such attributes are not accessible either using dot notation or the standard *getattr*() and *setattr*() functions, therefore they are considered to be a 'private property' of a class, which are intended for the internal implemenation of the class\` mechanics and not as a part of the public API of the class. Unlike the real private attributes in the C++ sense, these attributes are inherited by the sub-classes of such class. Therefore 'protected attributes' is a more suitable name.

Note that such 'protected' attributes can still be accessed via class / instance dictionary ('magic' attribute **\_\_dict\_\_**) or using the 'original' attribute resolution 'magic' methods *\_\_getattribute\_\_*() and *\_\_setattr\_\_*() of the **type** and **object** classes respectively.
