+++
title = "Python for RIT Students"
author = "Matt Soucy"
outputs = ["Reveal"]
date = "November 6, 2015"
+++

# Python for RIT Students

by Matt Soucy

---

# Topics

---

- Environments
- Tuples
- Magic functions
- Comprehensions
- Generators
- `with` blocks
- First class functions
- Closures
- Lambdas
- Decorators

---

# Environments

---

Stop using IDLE, it's not sufficient for your needs

- Jupyter (formerly IPython)
    - Powerful scripting abilities - `!`-commands allow for shell-scripting like syntax, but 10x better
- BPython
    - Another nice REPL, ncurses-based and provides useful "view source" functionality
- Spyder
	- Somewhat useful GUI usable in Windows
	- Also part of Anaconda, which is useful for math processing and packaging

---

# Tuples

---

Basically, an immutable collection of data:

```python
tup = (1,3,5)
print type(tup) # tuple
```

---

Different from lists how?

- Immutable - can't reassign to an item
- Fixed size
- Faster to operate on
- Can be used as dictionary keys (due to immutability)
- By convention, position is meaningful
- By convention, heterogenous data
- Can convert using the list() and tuple() constructors

---

# Tuple Packing and Unpacking

---

You can create tuples "containing" lvalues.

#### For those who are unfamiliar, lvalues are "things you can assign to"

---

```python
x, y = 5, 7 # same as `x=5;y=7`
x, y = y, x # Swaps the values of x and y
for root, dirs, files in os.walk("."): pass
```

---

# Functions you might not know about

---

```python
# Gives index, value pairs
enumerate(seq[, start])

# Applies a function to each element in a sequence
map(function, sequence[, sequence, ...])

# Gives only elements for which the given function is true
# (uses the identity function if None)
filter(function or None, sequence)

# Applies a function to reduce a sequence to a single value
reduce(function, sequence[, initial])

# Give a list of attributes within an object
dir([object])

# "zip up" several sequences
zip(seq1, seq1 [...]]) # -> [(seq1[0], seq2[0], ...), (...)]
```

---

# Special syntax

---

You can unzip a sequence when passing as arguments:

```python
data = (1,5)
def add(a, b):
	return a+b
print(add(*data))
```

---

It's also possible to have a function take an arbitrary number of arguments:

```python
def sayAll(*args):
	for arg in args:
		print(arg)
sayAll("hello", "world", 5, 42 "stuff")
```

---

A similar syntax also works with keyword arguments:

```python
def keywords(**kwargs):
	print(kwargs)
keywords(hello="world", this="that")
```

---

# Magic functions

---

How the CS department has taught classes:

```python
class Vector(object):
	__slots__ = ("x", "y")
def mkVector(x, y):
	v = Vector()
	v.x = x
	v.y = y
	return v
def addVectors(a, b):
	return mkVector(a.x+b.x, a.y+b.y)
def strVector(vec):
	return "({0}, {1})".format(vec.x, vec.y)
a = mkVector(3,4)
b = mkVector(1,1)
print(strVector(addVectors(a,b)))
```

---

If you do this in the real world, you will be laughed out of any workplace.

---

Python supports constructors and operator overloading:

```python
class Vector(object):
	# Slots are used to specifically limit members to those names
	# Most real-world classes don't really use them...
	def __init__(self, x, y):
		self.x, self.y = x, y
	def __add__(self, other):
		return Vector(self.x+other.x, self.y+other.y)
	def __str__(self):
		return "({0}, {1})".format(self.x, self.y)
a = Vector(3,4)
b = Vector(1,1)
print(a+b)
```

---

Some of the most useful magic functions are:

- `__lt__`: Comparison, less than
- `__eq__`: Comparison, equality
- `__len__`: Provides implementation for `len()` for the class
- `__str__`: Generate a string representation
- `__getitem__`: Support `seq[key]`
- `__call__`: Allow support for treating the object as a function
- `__iter__`: Return an iterator, support `for x in y`

---

# RITlib

RIT has `rit_lib`, which is a janky version of `namedtuple`

```python
from rit_lib import struct
class Vector(struct):
	_slots = ("x", "y")
```

---

`rit_lib`'s `struct` is like a mutable `namedtuple` that you can't iterate over

```python
from collections import namedtuple
Vector = namedtuple("Vector", ["x", "y"])
```

---

# Statements vs. Expressions

---

```python
# An expression is basically "something that has a value"
None
"Hello, world!"
2+2
[1,3,5]

# A statement is "something that does something"
# All expressions are also statements
# Anything that involves blocks is a statement
for i in range(10): pass
try: pass
except: pass
```

---

# Comprehensions

---

Comprehensions help convert large blocks that build lists or dictionaries into single expressions.

---

```python
# Let's implement a "map"-like function
def doubleItems(seq):
	results = []
	for i in seq:
		results.append(i*2)
	return results

# And now as a comprehension
def doubleItems(seq):
	return [i*2 for i in seq]

# Return a generator instead of a list
def doubleItems(seq):
	return (i*2 for i in seq)
```

---

Comprehensions, much like for loops, can be nested, possibly with conditionals:

```python
def getLines(allFilenames):
	data = []
	for filename in allFilenames:
		for line in open(filename):
			if ">>" in line:
				data.append(line.strip())
	return data

# Better done as a comprehension:
def getLines(allFilenames):
	return [line.strip()
			for filename in allFilenames
			for line in open(filename)
			if ">>" in line]
```

---

# Generators

---

Generators are basically a way to create and manipulate sequences without actually storing the full sequence in memory

They can almost be considered "functions that return several times as the function runs"

---

```python
def genDoubles(maxVal):
	for i in range(0, maxVal):
		yield i*2 # Sends the value out of the function

for i in genDoubles(20):
	print(i)

val = genDoubles(20)
print(val.next())
print(val.next())
```

---

# Comprehensions vs generators

---

Generators can also be produced in a similar syntax to comprehensions.

The main difference is that the generator is lazy and so needs to be iterated over to operate on it

---

```pycon
>>> gen = (x * 2 for x in range(10))
>>> gen
<generator object <genexpr> at 0x7fce54ecdd70>
>>> for i in gen:
...     print(i)
...
0
2
4
6
8
10
12
14
16
18
```

---

# Context managers

---

Sometimes, you want to be able to say "return to this state after doing this", without worrying about exceptions, etc:

- File handling/autoclosing
- Lock/unlock mutex
- Cleanup after a class

This concept exists in C++ as RAII, and in Python as Context Managers

---

```python
# Let's copy a file's contents!
# This is super verbose
inpfi = open("somefile")
outfi = open("newfile", "w")
outfi.write(inpfi.read()) # What if, we get an IOError?
inpfi.close()
outfi.close()
```

---

```python
# Let's copy a file's contents!
# This is still super verbose..
inpfi = open("somefile")
outfi = open("newfile", "w")
try:
	outfi.write(inpfi.read())
except IOError:
	inpfi.close()
	outfi.close()
```

---

```python
# Let's copy a file's contents!
# Let's use context managers!
with open("somefile") as inpfi:
	with open("newfile", "w") as outfi:
		outfi.write(inpfi.read())
```

---

```python
# Let's copy a file's contents!
# Why not use both together?
with open("somefile") as inpfi, open("newfile", "w") as outfi:
	outfi.write(inpfi.read())
```

---

# Creating context managers

---

Any custom class can get context manager functionality by adding two functions:

- `__enter__(self)`: do any "entry" code
- `__exit__(self, exc_type, exc_value, traceback)`: Any exit code, catches the exception given to it and passes it as arguments

There is also [contextlib](https://docs.python.org/3.4/library/contextlib.html), which makes it even simpler

---

# First Class Functions

---

Functions can be thought of like variables - you can pass them into functions, assign them, etc.

```python
def getAdder(x):
	def add(y):
		return x+y
	return add
add5 = getAdder(5)
print(add5(5)) # 10
```

Functions returned from other functions can retain information about their context.

---

# Lambdas

---

Lambda allows you to create a function inline.

There are limitations, the largest being that it only shows the "return value".

```python
def notALambda(x):
	return x+2
isALambda = lambda x: x+2 # Note there is no "return"
```

Lambdas can greatly reduce code required for some operations

```python
def getAdder(x):
	return lambda y: x+y
```

---

# Closures

---

You can pass functions into other functions...

```python
def compose(f, g):
	return lambda x: return f(g(x))
f = lambda x: x*2
g = lambda x: x+5
fog = compose(f, g)
print(fog(5)) # 20
```

Notice that the function returned relies on the function passed in.

---

# Decorators

---

Let's make a function that operates on other functions to provide debug information.

```python
def debugInfo(name, func):
	def runFunc(*args, **kwargs):
		print("Before", name)
		func(*args, **kwargs) # Forward all arguments
		print("After", name)
	return runFunc

def add(a, b):
	return a+b

# Let's use our debug add as add
if DEBUG:
	add = debugInfo("add", add)
```

---

In fact, Python provides some even better syntax for using decorators:

```python
def debugInfo(name)
	def _func(func):
		def runFunc(*args, **kwargs):
			print("Before", name)
			func(*args, **kwargs) # Forward all arguments
			print("After", name)
		return runFunc
	def _func

@debugInfo("add")
def add(a, b): return a+b
```

---

# Virtual Environments

---

Sometimes you'll want to install different versions of Python libraries.
Normally, a python app won't/can't specify the version of each library required.
This causes problems when one program only works with `libfoo==1.5`, but another requires `libfoo==2.0`.

To get around this, we use virtual environments.

The easiest way to set them up is via VirtualEnvWrapper or VirtualFish (depending on your shell).

---

# More info

---

Some fun links:

- http://www.dabeaz.com/coroutines/Coroutines.pdf
- http://stackoverflow.com/questions/101268/hidden-features-of-python

