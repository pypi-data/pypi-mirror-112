# MIT License
#
# Copyright (c) 2021 Peter Goss
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import cast, Any, Type, Mapping, Sequence
import itertools
from midb.backend import SQLiteBackend
from midb.persistent_objects._basepersistentobject import BasePersistentObject
from midb.persistent_objects._basepersistentobject import register_persistent_object_class_with_serializer


def setup_pobject(cls: Type):
    """
        Class Decorator that does the work of setting up a custom persistent object.
    """
    cls_defined_attrs = set(itertools.chain.from_iterable([cls.__dict__ for cls in cls.mro()[:-1]])) # pragma: no mutate
    copy_class = cls._in_memory_class
    for key, value in copy_class.__dict__.items():
        if key not in cls_defined_attrs and (callable(value) or type(value) is property):
            setattr(cls, key, value)
    register_persistent_object_class_with_serializer(cls)
    return cls


class MemoryObject:
    """
        A simple class that can be used (but not required to be used) as the foundation of objects that
        will be persisted.
    """
    def __init__(self, **kwargs: Mapping[str, Any]) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        """ implement: repr(self) """
        attribute_strings = [f"{key} = {repr(value)}" for key, value in self.__dict__.items()]
        return f'{self.__class__.__name__}({", ".join(attribute_strings)})'

    def __eq__(self, other: Any) -> bool:
        """ implement: self == value """
        if type(self) != type(other):
            return False
        else:
            if len(self.__dict__) != len(other.__dict__):
                return False
            for attribute in self.__dict__.keys():
                if not hasattr(other, attribute):
                    return False
                elif getattr(self, attribute) != getattr(other, attribute):
                    return False
        return True

@register_persistent_object_class_with_serializer
class PObject(BasePersistentObject):
    """ The base object for implementing custom persistent object classes.  """
    _in_memory_class: Type = MemoryObject

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super_init_args = {}
        if '_backend' in kwargs.keys():
            super_init_args['_backend'] = kwargs['_backend']
            del kwargs['_backend']
        if '_id' in kwargs.keys():
            super_init_args['_id'] = kwargs['_id']
            del kwargs['_id']
        if '_init_temp' in kwargs.keys():
            super_init_args['_init_temp'] = kwargs['_init_temp']
            del kwargs['_init_temp']
        elif '_id' not in super_init_args or super_init_args['_id'] is None:
            super_init_args['_init_temp'] = self._in_memory_class(*args, **kwargs)

        super(PObject, self).__init__(**super_init_args)

    def in_memory(self) -> Any:
        """
            Returns an object that contains all the attributes of the persistent object but in memory
            instead of on disk.
        """
        if self.still_temp():
            return self._temp
        else:
            _backend = cast(SQLiteBackend, self._backend)
            _id = cast(int, self._id)
            new_in_memory = self._in_memory_class.__new__(self._in_memory_class, object())
            for key, value in _backend.get_items(_id):
                new_in_memory.__dict__[key] = value
            return new_in_memory

    def _init_temp(self, initial: Any) -> None:
        """
            This is called by '__init__' to initialize a temporary object.
        """
        if isinstance(initial, self._in_memory_class):
            self._temp = initial
        else:
            self._temp = None

    def _move_temp_to_backend(self) -> None:
        """
            When an object has been fully initialized this is called to move what is being held in '_temp'
            into the database.
        """
        if not self.still_temp():
            for key, value in self._temp.__dict__.items():
                self._set(key, value)
            self._temp = None

    def _not_reserved_setattr(self, key: str, value: Any) -> None:
        """
            This must be implemented by each subclass and is called by "__setattr__" to give the Subclass a chance to
            do something that it sees as appropriate. In the case of PObject that means to set the attribute to the value.
        """
        if self.still_temp():
            setattr(self._temp, key, value)
        else:
            self._set(key, value)

    def __delattr__(self, key: str) -> None:
        """
            Called when deleting an attribute (del self.key)
        """
        if key in self._reserved_attributes():
            super(PObject, self).__delattr__(key)
        else:
            self._del(key)

    def _set_temp(self, key: str, value: Any) -> None:
        """
            Used by '_set' when the object is not fully initialized
            and data is still being held in the '_temp' object.
        """
        self._temp.__setattr__(key, value)

    def _get_temp(self, key: str) -> Any:
        """
            Used by '_get' when an object is not fully initialized
            and data is still being held in the '_temp' object.
        """
        return self._temp.__getattribute__(key)

    def _del_temp(self, key: str) -> None:
        """
            Used by '_del' when the object is not fully initialized
            and data is still being held in the '_temp' object.
        """
        self._temp.__delattr__(key)

    def __eq__(self, other: Any) -> bool:
        """ implement: self == value """
        self = self.in_memory()
        if isinstance(other, PObject):
            other = other.in_memory()
        return self == other
