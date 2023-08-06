# Constant Properties Protector Package

With the help of this module, you can protect some of properties in a class. Protecting means avoiding to change them but keep them publicly available.

```python
from constant_properties_protector import CPP
    
class A(CPP):
    def __init__(self):
        CPP.__init__(self, protecteds=[
            'initialized_protected',
            'uninitialized_protected'
        ])
        self._initialized_protected = 12
        
a = A()
print(a.initialized_protected)
# >>> 12
a.t = 2
print(a.t)
# >>> 2
a.initialized_protected += 1
# Exception: Can not modify constant property: initialized_protected
a.uninitialized_protected = 10
# Exception: Can not modify constant property: uninitialized_protected
```

NOTE: 

* You can use `CPP` along with other base classes.
* `CPP` will override `__getattribute__` and `__setattr__`. So where these functions somehow are overrided or are going to be overridden, don't use it .
* Use `_` first of the protected property name to get fully access to it.

## Installation
```pip install constant-properties-protector```