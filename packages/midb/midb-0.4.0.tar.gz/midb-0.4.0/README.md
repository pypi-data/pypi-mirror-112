# Mostly Invisible Database

A database access layer that acts like python in-memory objects. 

---
Disclaimer: Only minimal attempts have been made at speed. And mainly
intended for personal projects. Deeply nested data structures will 
likely be slow.

---
Example:

``` python
>>> import midb
>>> root = midb.get_root('db_file.db')
>>> root['test'] = 1
>>> root['test2'] = {'test3': 3}
>>> exit()
```
later ...
``` python
>>> import midb
>>> root = midb.get_root('db_file.db')
>>> root['test']
1
>>> root['test2']['test3']
3
>>> root['test2']
PDict({'test3': 3}, _backend=SQLiteBackend(filename="db_file.db"), _id=1, _temp=None)
>>> root['test2'].in_memory()
{'test3': 3}
>>> exit()
```

---
### What's currently supported?
Currently, the types that are supported are:

* Simple types:
    * str
    * None
    * bool
    * int
    * float
    * datetime.datetime
    * datetime.date
    * datetime.time
    
* container types (must not contain unsupported types)
    * dict (silently converted to PDict)
    * tuple (silently convert to PTuple, currently can't be used as PDict keys.)
    * list (silently convert to PList)
    * custom objects (see below for example)
    
---
### Custom objects
Custom objects are still not fully tested, but the basics have been 
including property descriptors. The following has been tested and works.

``` python
import midb

# define or import an class
#   Note: subclassing midb.MemoryObject is not necessary but useful 
#         because it defines __repr__ and __eq__.
class MyObj(midb.MemoryObject):
    def __init__(self, a_value, b_value):
        self.a = a_value
        self.b = b_value

    def some_other_method(self, input):
        self.methods_may_set = input
        return f"{self.a}, {self.b}"

# define a persistent object with an _in_memory_class attribute set to the object you 
# want to have it emulate and decorate it with the @midb.setup_pobject decorator.
@midb.setup_pobject
class PMyObj(midb.PObject):
    _in_memory_class = MyObj
```
With those objects imported or defined:
``` python
# first run
root = midb.get_root("filename.db")

root['my object'] = MyObj(1, 2)
print(root['my object'].a)
print(root['my object'].b)
print(root['my object'].some_other_method(3))
print(root['my object'].methods_may_set)

```
Later (also with the above classes defined or imported) ...
``` python
root = midb.get_root("filename.db")

print(root['my object'].a)
print(root['my object'].b)
print(root['my object'].some_other_method(4))
print(root['my object'].methods_may_set)

```
If you encounter any problems with the classes you have defined, 
please file an issue at https://gitlab.com/gossrock/midb/-/issues.

---
### Up Next:
* Support for hashable objects such as tuples containing immutable data as dict keys.
---
### Future:

* Support for and/or documentation of additional or custom serializers.
* More examples and documentation
* Add support for other standard library classes that represent storable data.


---
### Bugs

Please report bugs at https://gitlab.com/gossrock/midb/-/issues 






