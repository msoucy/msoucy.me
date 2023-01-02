+++
title = "Injecting Code with Python"
author = "Matt Soucy"
outputs = ["Reveal"]
date = "October 9, 2014"
+++

---

# Getting Dirty

Assume we have a code sample:

```python
# somemod.py
def __call__(mod):
	# Using "mod" as if it were "self", which makes sense
	print("Called module", mod)
```

```python
# driver.py
import somemod

somemod() # Error, module is not callable
```

---

# What can we do?

Well, many things in Python are flexible...

> Why would you want to call a module?

Not my problem.

---

# What if we make a new module?

```python
# modulehack.py
try:
    import __builtin__
except ImportError:
    import builtins as __builtin__
_imp = __builtin__.__import__

class Module(object):
    def __init__(self, name, *args):
        super(Module, self).__setattr__("_mod", _imp(name, *args))
    def __getattr__(self, name, default=None):
        return getattr(self._mod, name, default)
    def __setattr__(self, name, value):
        return setattr(self._mod, name, value)
    def __delattr__(self, name):
        return delattr(self._mod, name)
    def __call__(self, *args, **kwargs):
        if hasattr(self._mod, '__call__'):
            return self._mod.__call__(self._mod, *args, **kwargs)
        raise TypeError("'module' object is not callable")

__builtin__.__import__ = Module

```

---

# No, stop that.

I don't think so.

```python
import modulehack
import somemod

somemod() # Prints out a message
```

---

# Magic.
