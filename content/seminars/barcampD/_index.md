+++
title = "The D Programming Language - Barcamp"
author = "Matt Soucy"
outputs = ["Reveal"]
date = "April 14, 2012"
+++

# The D Programming Language - A new take on C++

by Matt Soucy

---

# What is D?

> "Great, the last thing I need is another D in programming!" - Walter Bright

- Developed by:
    - Walter Bright (Digital Mars, first native C++ compiler)
    - Andrei Alexandrescu (_Modern C++ Design_, Facebook)
    - Many developers (Phobos standard library)

---

- Designed to be "C++ Done Right"
- Compiles to native code
- Community driven, multi-paradigm, buzzword-filled

![D Logo](http://dlang.org/images/dlogo.png)

---

# D derives much of its syntax from C

```d
import std.stdio;

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
// Examples from K&R Sec 5.12
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

---

# Variable declaration syntax (D style)

Isn't it nicer to just do it the D way?

---

```d
// D style:
int* x, y;
	// D forbids declaring variables of different types in the same expression
int *x;
int y;
	// x is an int*, y is an int
// Examples from K&R Sec 5.12
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

---

# Smart arrays

Arrays in D can behave more like C++'s `std::vector`

- Automatic bounds checking (optional)
- Resizable
- Length+data

C-style arrays are also supported

---

```d
int* p; // Same as in C
int[5] x; // Same as C's "int x[5];"
int[] y; // Awesome array

y.length = 2; // Resizes
writef("Length: %s", y.length); // Gets value - property magic
```

---

# Built-in associative arrays

D has a built-in associative array type as part of the syntax:

```d
import std.stdio;

void main() {
	string[int] x;
	x[2] = "World!";
	x[0] = "Hello";
	x[1] = ", ";
	writefln("%s%s%s",x[0],x[1],x[2]);
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

D is nice enough that you can even use it in scripts "without compiling"!

---

```d
#!/usr/bin/dmd -run
// Yup. That's totally legit.
import std.stdio;
import std.random;
import std.algorithm;

void main(){
	// Simple raffle name reorderer
	writef("Enter names:\n==> ");
	char[] data;
	stdin.readln(data);
	string[] names;
	while(data != "") {
		names ~= cast(string)data;
		write("==> ");
		stdin.readln(data);
	}
	writeln("--- OUTPUT ---");
	auto rnd = Random(unpredictableSeed);
	uint i=0;
	foreach(name;randomCover(names,rnd)) {
		writef("%s: %s\n", i, name);
		i++;
	}
}
```

---

# Switch statements

D continues C's style of a switch statement, but with a few tricks

---

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
```

---

# WORLD-WIDE AWESOMENESS

D source text can be in one of the following formats:

 *  ASCII
 *  UTF-8
 *  UTF-16BE
 *  UTF-16LE
 *  UTF-32BE
 *  UTF-32LE

 ---

Copied verbatim from the D newsgroups:

```d
int main()
{
	int ﺎﻠﻋﺮﺒﻳﺓ = 42; // <- I really love this mind-fuck !!!
	return العربية;
}
```

(In case you're wondering, "العربية" means "Arabic")

---

# Templates

D has an interesting, simple template syntax, which I have absolutely no time to write an example for.

However, they are significantly more awesome than C++'s.

---

# Standard Library

The standard library (Phobos) takes a "batteries included" approach like python

---

Phobos contains many different modules, such as:

- `std.regex` or `std.conv` to handle string processing and conversion
- `std.csv`, `std.json`, `std.xml`, and `std.zip` to handle many different file formats
- `std.concurrency` and `std.process`, and `std.socket` for processes and tasks
- `std.socket` for network sockets

---

As if this wasn't awesome enough, you can do crazy function calls at compile time:

```d
import std.stdio;
import std.array;
import std.algorithm;

struct Roman {
	@property static auto opDispatch(string number)() {
		enum num = number.replace("IV", "IIII")
						 .replace("IX", "VIIII")
						 .replace("XL", "XXXX")
						 .replace("XC", "LXXXX");

		enum value = num.count('I')
				   + num.count('V') * 5
				   + num.count('X') * 10
				   + num.count('L') * 50
				   + num.count('C') * 100;

		return value;
	}
}

void main() {
	writeln(Roman.XV);
	writeln(Roman.IIX);
	writeln(Roman.VXCII);
}
```

(This code was taken from "Romans, Rubies, and the D Programming Language")

---

# C Bindings

In addition to Phobos, D also has the external library Deimos.

Deimos is a set of D bindings to various C libraries, such as:

- ncurses
- 0MQ (zeroMQ)

---

Much like Phobos, Deimos is supported by the open source community, and is constantly updating.

*This means you can link any C library to D, and it will work fine!*

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
- I may do a full presentation in a future Barcamp

