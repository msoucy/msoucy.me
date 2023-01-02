+++
title = "The D Programming Language: A new take on C++"
author = "Matt Soucy"
outputs = ["Reveal"]
+++

# The D Programming Language: A new take on C++

by Matt Soucy

---
# What is D?

> "Great, the last thing I need is another D in programming!" - Walter Bright

- Developed by:
    - Walter Bright (Digital Mars, first native C++ compiler)
    - Andrei Alexandrescu (_Modern C++ Design_, Facebook)
    - Many contributors (Phobos standard library)

---

- Designed to be "C++ Done Right"
- Compiles to native code
- Community driven, multi-paradigm, buzzword-filled (but in a good way!)

![D Logo](http://dlang.org/images/dlogo.png)

---

### Six instantly-useful features

- Garbage collection, unless you want manual memory management, in which case you can use it or turn the GC off.
- Arrays know their length, and assigning to their length resizes them.
- Strings are treated as arrays of characters, and have access to all array properties.

---

- `const` types are actually const, and you can't circumvent the type system to change this.
- Compile time is insanely short. (Downside is there's less time for shenanigans)
- Object-oriented, but only when you want it - doesn't limit you to a specific paradigm.
    - For example, use a functional style by marking functions as `pure`

---

# D derives much of its syntax from C

```d
import std.stdio;

// If main is void, it's the same as if it returns 0
void main() {
	// The developers understand the awesomeness of printf
	writef("Hello, world!\n");
}
```

---

# The "auto" keyword

Because expressions, especially those returned from some functions, can have long or complex names,
the `auto` keyword can be used to create variables where the exact type isn't needed or important.

---

```d
import std.algorithm;
import std.stdio;

void main() {
	auto x = "Hello, world!"; // string
	auto data = [1,2,3,4,5]; // int[]
	auto somefunc = (int x) {return x*x;}; // int function(int)
	// UHHHHH...don't worry about it! (It's int[])
	auto y = data.map!somefunc().filter!q{a % 2}().array();
	writef("%s", y); // %s prints this nicely!
}
```

---

# Variable declaration syntax

C is infamous for having an unintuitive syntax for complex function declaration.

---

```c
// C style:
int *x, *y;
	// * is required for both
int* x, y;
	// x is an int*, y is an int
int *p;
	// p is a pointer to an int
int *p[13];
	// p is an array[13] of pointers to an int
int *(p[13]);
	// p is an array[13] of pointers to an int
int **p;
	// p is a pointer to a pointer to an int
int (*p)[13];
	// p is a pointer to an array[13] of int
int *f();
	// f is a function returning pointer to int
int (*f)();
	// f is a pointer to a function returning int
int (*(*f())[13])();
	// f is a function returning a ptr to an array[13]
	// of pointers to functions to int
int (*(*x[3])())[5];
	// x is an array[3] of pointers to functions
	// returning pointers to array[5] to int
```

#### Examples from K&R Sec 5.12

---

Isn't it nicer to just do it the D way?

```d
// D style:
int* x, y;
	// D forbids declaring variables of different types in the same expression
int *x;
int y;
	// x is an int*, y is an int
int* p;
	// p is a pointer to an int
int*[13] p;
	// p is an array[13] of pointers to an int
int **p;
	// p is a pointer to a pointer to an int
int[13]* p;
	// p is a pointer to an array[13] of int
int* function() f;
	// f is a function returning pointer to int
int function() f;
	// f is a pointer to a function returning int
int function()[13]* function() f;
	// f is a function returning a ptr to an array[13]
	// of pointers to functions to int
int[5]* function()[3] x;
	// x is an array[3] of pointers to functions
	// returning pointers to array[5] to int
```

#### Examples from K&R Sec 5.12

---

# Properties

Properties are an extension of accessors, where a "variable" lookup is converted to a function call.

```d
@property string twice(string x) {
	return x~x;
}

void main() {
	"Hello".twice.writeln();
}
```

---

# Smart arrays

Arrays in D can behave more like C++'s `std::vector`

- Automatic bounds checking (optional)
- Resizable
- Length+data

C-style arrays are also supported:

```d
int* p; // Same as in C
int[5] x; // Same as C's "int x[5];"
int[] y; // Smart array

y.length = 2; // Resizes
writef("Length: %s", y.length); // Gets value - property
```

---

# Built-in associative arrays

D has a built-in associative array type as part of the syntax:

```d
import std.stdio;

void main() {
	string[string] x;
	x["what"] = "Hello";
	x["who"] = "world";
	x["emotion"] = "!";
	writefln("%s %s%s",x["what"],x["who"],x["emotion"]);
}
```

---

# Foreach loops

Foreach loops in D are kind of awesome:

```d
import std.stdio;

void main() {
	int[] arr = [1,3,5,7,9];
	foreach(x;arr) {
		writef("%s ",x); // %s automagically deduces the type
	}
	writef("\n");
	foreach_reverse(x;arr) {
		writef("%s ",x);
	}
	writef("\n");
	foreach(ref x;arr) {
		x *= x; // Poor man's map()
	}
	foreach(x;arr) {
		writef("%s ",x);
	}
}
```

---

Output:

```
1 3 5 7 9 
9 7 5 3 1 
1 9 25 49 81
```

---

# Scripting in D

D is designed so that you can even use it in scripts "without compiling"!

---

Example script:

```d
#!/usr/bin/dmd -run
// If you have multiple files, you can use /usr/bin/rdmd
import std.stdio;
import std.string;
import std.random;

void main(){
	// Simple raffle name reorderer
	char[] data;
	writeln("Enter names:");
	string[] names;
	do {
		write("==> ");
		stdin.readln(data);
		data = data.strip();
		if(data != "") names ~= data.idup;
	} while(data != "");
	writeln("--- OUTPUT ---");
	uint i=0;
	foreach(name;names.randomCover(Random(unpredictableSeed))) {
		writef("%s: `%s`\n", i, name);
		i++;
	}
}
```

---

D continues C's style of a switch statement, but with a few tricks:

```d
string s;
// ... Do stuff, assign s
// switch now works directly on strings!
switch(s) {
case "A":
	// Do stuff
	break;
case "B","C","E":
	// Do stuff if it matches any of those
	break;
default:
	// Same old, same old
}
switch(s[0]) {
case 'a' : .. case 'z': // Matches anything between a-z
}
```


---

# Templates

Templates, combined with compile-time duck typing, allow for some powerful and simple type manipulation.

Their syntax is significantly cleaner than in C++, due to using a single binary operator `!` instead of overloading `<>`

---

```d
template Foo(T, U) {
	class Bar { ... }
	T foo(T t, U u) { ... }
	T abc;
	typedef T* Footype; // any declarations can be templated
}

class Baz(T) {
	T t;
}

Foo!(int,char).Bar b;
Foo!(int,char).foo(1,2);
Foo!(int,char).abc = 3;
Baz!int baz; // If there's only one argument it doesn't need parenthesis
```

---

# Eponymous Templates

When you make an eponymous template, the template takes the value of a static variable with the same name inside it.

```d
template factorial(int n) {
	static if (n == 1) const factorial = 1;
	else const factorial = n * factorial!(n-1);
}

int x = factorial!5; // Same as "int x = 120;"
```

---

# CTFE

The factorial example is simple, but in a lot of cases you'd prefer to be able to do a calculation both at compile and run time.
For this reason, D allows compile-time function execution.
Any variable that is created with `enum` or `static` is determined at compile-time.

---

```d
int factorial(int n) {
	if (n == 1) return 1;
	else return n * factorial(n - 1);
}

int x = factorial(5); // x is initialized to 120 at runtime
static int x = factorial(5); // x is statically initialized to 120
```

---

# Iterators

D's standard library uses the concept of `Range`s instead of `Iterator`s like C++.

---

Iterators have some conceptual issues:

- There is no single, simple definition of what an iterator is
- Tied to pointer syntax
- Essential primitives:
    - At the end
    - Access value
    - Move (increment)
- Come in pairs (mostly)
    - Forced to use two if you want to get anything done

---

# Ranges!

A range is a single interface that allows for an alternative method of iteration.

```d
// Taken verbatim from std.range
template isInputRange(R)
{
	enum bool isInputRange = is(typeof(
	(inout int _dummy=0)
	{
		R r = void;       // can define a range object
		if (r.empty) {}   // can test for empty
		r.popFront();     // can invoke popFront()
		auto h = r.front; // can get the front of the range
	}));
}
```

---

More importantly, it simplifies iterating over things that may not be a "real" range.

```d
// Reverses iteration over a bidirectional range
struct Reversed
{
	int[] range;

	this(int[] range) { this.range = range; }

	@property bool empty() const { return range.empty; }

	@property int front() const { return range.back; } // <- reverse

	@property int back() const { return range.front; } // <- reverse

	void popFront() { range.popBack(); } // <- reverse

	void popBack() {range.popFront(); } // <- reverse
}
```

---

# Standard Library

The standard library (Phobos) takes a "batteries included" approach like python

---

Phobos contains many different modules, such as:

- `std.regex` or `std.conv` to handle string processing and conversion
- `std.csv`, `std.json`, `std.xml`, and `std.zip` to handle many different file formats
- `std.concurrency` and `std.process` for processes and tasks
- `std.socket` for network sockets

---

Much like C++'s STL and iterators, Phobos is designed almost entirely around ranges.

Because of this, any user-made range is instantly supported by the entire standard library,
including a large number of algorithms for acting on those ranges (`std.algorithm`)

---

# Uniform Function Call Syntax

There are often instances when one is using a library that for some reason they cannot alter,
but you want to add functionality to a certain class or type.

---

```d
// D allows this through the use of UFCS, which converts any call to:
x.foo()
// Into the actual call:
foo(x);
// This is used often in `std.algorithm`, which allows one to write code such as:
writeln(take(generator(5),10));
// As the much more legible (and easily maintainable):
generator(5).take(10).writeln();
```

---

# Voldemort Types

Andrei discovered an interesting interaction between `auto` and declaring structs inside a function:
**Voldemort types** are types that cannot be named.

---

```d
import std.stdio;
import std.range;

auto generator(uint seed) { 
  struct RandomNumberGenerator {
	  @property int front() {
		  return ((seed / 0x10000) * seed) >> 16;
	  }
	  void popFront() {
		  seed = seed * 1103515245 + 12345;
	  }
	  enum empty = false;
  }
 
  RandomNumberGenerator g;
  g.popFront();    // get it going
  return g;
}

void main() {
  generator(5).take(10).writeln();
}
```

---

# Mixins

```d
// Taken from my ZeroMQ wrapper
mixin template SocketOption(TYPE, string NAME, int VALUE) {
	/// Setter
	@property void SocketOption(TYPE value) {
		if(zmq_setsockopt(this.socket, VALUE, &value, TYPE.sizeof)) {
			throw new ZMQError();
		}
	}
	/// Getter
	@property TYPE SocketOption() {
		TYPE ret;
		size_t size = TYPE.sizeof;
		if(zmq_getsockopt(this.socket, VALUE, &ret, &size)) {
			throw new ZMQError();
		} else {
			return ret;
		}
	}
	mixin("alias SocketOption "~NAME~";");
}
mixin SocketOption!(ulong, "hwm", ZMQ_HWM);
```

---

# C Bindings

In addition to Phobos, D also has the external library Deimos.

Deimos is a set of D bindings to various C libraries, such as:

- ncurses
- 0MQ (zeroMQ)

---

Much like Phobos, Deimos is supported by the open source community, and is constantly updating.

**This means you can link (almost) any C library to D, and it will work normally.**

```d
extern(C) int someCrazyCFunction();

void main() {
	return someCrazyCFunction();
}
```

---

# Resources

- [D Programming Language's homepage (http://dlang.org)](http://dlang.org)
- [GDC (Planned integration into GCC 4.8) (https://bitbucket.org/goshawk/gdc/)](https://bitbucket.org/goshawk/gdc/)
- [LDC (LLVM-based D compiler) (https://github.com/ldc-developers/ldc)](https://github.com/ldc-developers/ldc)

---

- The D Programming Language (TDPL)
    - http://www.amazon.com/The-Programming-Language-Andrei-Alexandrescu/dp/0321635361
    - Published by one of the main developers

---

# Conclusion

---

```d
foreach(question; audience)
	presenter.answer(question);
```
