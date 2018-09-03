---
Title: PyCon 2015: Beyond PEP8
Category: code
Tags: python,bizlegfoss,foss,d
Series: PyCon 2015
---

One of the talks I attended at [PyCon 2015][] was called [Beyond PEP8][].

The basic ideas that Raymond Hettinger talked about were relatively simple, but highly worth talking about.
The basic idea is to seperate business logic from boring behind-the-scenes logic.

Many Python programmers, when they first encounter PEP8, take it as the end-all-be-all solution to legible Python.
Unfortunately, it actually CAUSES more problems than it fixes, because of that.
People will make pull requests reformatting the code, so **obviously** it's better now because it's PEP8 compliant.
They miss the obvious problem that not only is it barely more legible than before (less so in some cases, due to the short line length restriction), but now tools like `git blame` will show that person as the most recent person to touch those lines, which makes it impossible to tell who to contact about any potential bugs.
In fact, in the process of PEP8-ifying, one can accidentally introduce bugs, as Hettinger demonstrates.

Going "[Beyond PEP8][]", as he puts it, is about making code not just look nicer with whitespace, but more idiomatic, easier to maintain and duplicate, and WAY more legible.

Some of the ways he proposes, and my thoughts on them:

> Using named tuples instead of ordinary tuples to increase legibility

I admit I haven't used these too much, but they seem handy for some use cases.
I know situations where all we want is a list of tuples, since making a full class has extra visual overhead.
In cases like this, we get the benefits of descriptive names without the overhead.

One special situation I can think of is when you want special printing, however as I tested the following works in both Python 2 and 3:

```pycon
>>> from collections import namedtuple
>>> Color = namedtuple("Color", ["red", "green", "blue"])
>>> Color.__str__ = lambda self: "<{0.red}, {0.green}, {0.blue}>".format(self)
>>> str(Color(255, 255, 0))
'<255, 255, 0>'
```

This can be done with standalone functions, as well, not just lambdas.

> Using [context managers][] to handle setup and breakdown code

I talked a bit about this in my [Python with C Library][cpy seminar] lightning talk.
The basic idea is that [context managers][] implement something in Python similar to C++'s [RAII][].
This essentially means that it runs some code on startup, and more code when that block exits.

The stereotypical example is file handling, though I've used the same system for connections to sockets, external processes...

```python
from __future__ import print_function  # Use Python 3 already!

with open("foo.txt") as outputfile:
	print("A line", file=outputfile)
	print(1/0, file=outputfile)  # Always errors
	print("Never printed", file=outputfile)
# At this point, outputfile is safely flushed and closed
```

> Avoid "getters" and "setters", prefer properties

This has been a peeve of mine for years, though mainly I've seen it in Java.
My example will be in [D][], which is similar syntactically to Java but supports properties.

```d
// Imitating his Python example
class Route {
public:

	this(string name, string ip)
	{
		this.name = name;
		this.ip = ip;
	}

	public string getName() {
		return name;
	}

	public string getIP() {
		return ip;
	}

private:
	string name;
	string ip;
}
```

What's wrong with this?

Well, what if later down the line I want to store the IP as a [std.socket.Address][]?
As a simple fix I can `return ip.toString();`, but then I lose the benefits of storing it as an `Address` in the first place.
If I change it to `public InetInterface getIP() {return ip;}`, then now I have to change it (almost) everywhere I use `getIP`.

The best way to fix this solution is to not get into it in the first place.
In the example, he uses `Route` data for printing.
To make this work nicely, a `toString` could be added that formats it properly.

"But wait!" you might say, "Python isn't statically typed!".
"Yes," I'll respond, "but changing the interface is bound to cause problems regardless."

By seperating a class's members from its business data, the class better encapsulates its business logic.
It's the only thing that can change (or even access) its members, so it can ensure consistency.

Let's pretend that making an `Address` is expensive (this example might work better with `Regex`), but we don't need an `Address` for every `Route`.
For example, string comparison of the original string is considered "proper", and sometimes we only want to check if a route is already "in the system".
We're storing the routes as a `Route[]`, instead of `Address[string]`, because of the expensive Address creation.

```d
class Route {
public:

	this(string name, string ip)
	{
		this.name = name;
		this.ip = ip;
	}

	public string getName() {
		return name;
	}

	public Address getIP() {
		if(_addr is null) {
			// Pretend that we're using a real class and not the abstract Address
			_addr = Address(ip);
		}
		return _addr;
	}

	override bool opEquals(Object other) {
		if(Route r2 = other) {
			// Down-cast to Route, null if other isn't a Route
			// Doesn't create an expensive Address if it doesn't need to
			return name == r2.name && ip == r2.ip;
		} else {
			return false;
		}
	}

private:
	string name;
	string ip;
	Address _addr = null;
}
```

Sorry about all the pretending - it's hard to come up with a good example, normally one only finds them too late.

Now, what's this about properties?

In some languages, (Python and D among them), you can "disguise" a function call as member access.
(In C++ you can do some clever hacks with `operator->`, but it's not quite the same)
Moving the example (which is now straightforward) to Python, let's make this a little cleaner.
I'll substitute `Address` with Python 3.3's `ipaddress.ip_address`, which makes a v4 or v6 address.

```python
class Route(object):
	def __init__(self, name, ip):
		self.name = name
		self._ip = ip
	@property
	def ip(self):
		if self._addr is None:
			self._addr = ipaddress.ip_address(self._ip)
		return self._addr
	def __eq__(self, other):
		if not isinstance(other, Route):
			return False
		return self.name == other.name and self._ip = other._ip
```

Now, one can use `func(r.ip)`, and the `ip_address` only gets created if it needs to.
The actual behind-the-scenes work is hidden, and it acts just like an ordinary member.

> Using `len()` and magic methods

In the above examples, I used several magic functions: `__init__`, `__eq__`.

As I've mentioned in my [Fixing the Python Curriculum][] presentation, magic functions can change the code from:

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

Into the following, much nicer code:

```python
class Vector(object):
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

This is cleaner, and the class encapsulates the intended functionality.
The code _looks like_ what it does, as opposed to lots of visual noise with explicit function calls.

> Avoid unnecessary packaging

Nobody likes to `import some.crazy.long.namespace`.
At that point, either you're compartmentalizing too much (a file for every class), or your library tries to do WAY too much and should be broken up.

> Create custom exceptions to better enable tracking

Throwing a `ValueError` isn't too helpful, it could come from anywhere.
Throwing a `JSONDecodeError` is more descriptive and can be caught while unrelated errors propogate up

> Use keyword arguments

His example is clear enough:

```python
# Oh, so descriptive
ts("obama", 20, False, True)
# This is much nicer
twitter_search("obama", numtweets=20, retweets=False, unicode=True)
```

This has additional benefits:

- Being nonpositional, they can be placed in an order that's most convenient for the user
- Keyword arguments can have default arguments more easily

---

Overall, the talk was excellent, it covers a variety of things that beginning-to-intermediate Python developers won't immediately think of.
Legible code isn't just about formatting, but about creating a clean API and good documentation.

[Pycon 2015]: http://us.pycon.org/2015
[Beyond PEP8]: http://pyvideo.org/video/3511/beyond-pep-8-best-practices-for-beautiful-inte
[cpy seminar]: /seminars/cpy
[context managers]: https://en.wikibooks.org/wiki/Python_Programming/Context_Managers
[RAII]: https://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization
[D]: http://dlang.org
[std.socket.Address]: http://dlang.org/phobos/std_socket.html#.Address
[Fixing the Python Curriculum]: /seminars/python
