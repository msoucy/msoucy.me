+++
title = "Evil C++: C and C++ Standard tricks to bemuse and befuddle"
author = "Matt Soucy"
outputs = ["Reveal"]
+++

# Prerequisites

Some of these tricks may require knowledge of the following:

 - Basic C syntax
    - Variable initialization and creation
    - Loops and control flow
    - Logical operators
    - Statements vs. Expressions
 - Familiarity with pointers and references
 - Basic bit manipulation (the `&`, `|`, `^`, `~` operators)
 - Base-8 and Base-16

---

# Warnings

The tricks involved in this presentation may exploit definitions found in the standard, or they may merely be things that aren't commonly known.
Either way, in 99.9999% of the cases where you wonder if you need to use them, you definitely don't.

> The people who actually need them know with certainty that they need them, and don't need an explaination about why

>> Python Guru Tim Peters

This presentation is designed to show the effects of:

 - Different language features interacting
 - The programmer having complete control over how an individual segment of memory is used
 - Manipulating the build system (such as the preprocessor)

It is NOT meant to demonstrate things that should be used for anything more than messing around and learning.
If you use these in production code, you will be ***REDACTED***.

---

# Harmless

---

# String Concatenation

Two string literals, placed "next to" each other, will be treated as one:

```cpp
printf("abc" "def"); // same as printf("abcdef")
```

This is useful for long strings (such as insanely complex printf formatting strings) that you can extend onto more than one line

---

# Octal
There is a HUGE difference between the following:

```cpp
int x = 10; // decimal 10
int y = 010; // decimal 8
int z = 0x10; // decimal 16
```

There are very few uses for this syntax, but it's important to know about it to avoid issues.

---

# Void pointers

Can be used as any pointer type, and point to any data type
In order to use it as anything other than just a pointer, it must be cast

```cpp
#include <stdio.h>
void printPtr(void* p) {
	*(char*)p += 1;
	printf("%p",p); // Pointer printf
}
int main() {
	char c = 'A';
	char* p = &c;
	printPtr(p);
}
```

Many C library functions use void* to accept pointers because they implicitly cast to any other pointer type.

---

# Commenting out/testing values
If you need to change a value really quick to test something:

```cpp
int x =
	//Actual_value
	Testing_value
	;
```

Debug versions of code can use different values:

```cpp
int x =
#if DEBUG
	DEBUG_VALUE
#else
	ACTUAL_VALUE
#endif
	;
```

---

# Tricky

---

# sizeof
Most people have heard of the sizeof command, however, they are unaware that sizeof doesn't actually evaluate its contents.

The entire thing is performed at compile time, but not executed - it returns the size of the result of the expression, and compiles that in.

The original code doesn't actually make it to the executable.

```cpp
// Notice the lack of a body there
template <typename T, int N> char ( &Array( T(&)[N] ) )[N];
int x[5];
printf("Length of an array: %d\n",sizeof(Array(x)));
```

---

# The comma operator

Commas are useful for more than just separating function arguments:

```cpp
int foo() {return 5;}
int bar() {return 6;}
int baz() {return 7;}

int x = (foo(),bar(),baz());
cout << x; // Outputs 7
```

You may be familiar with the comma in for loops and variable declarations:

```cpp
int x=2,y=3;
for(int i=0,j=2;i<j;i++) { /*do stuff*/}
```

Now try sticking them in, say, an if statement:

```cpp
int x=0;
if(cin>>x,x*=2,x<8) { /*do stuff*/}
```

---

# Conditional Scope

Conditionals require *expressions*.
The difference between expressions and statements is that expressions have a value.
Variable declarations are expressions, not statements.

This means that this is possible, limiting the scope of the variable to the body of the if statement and its else clause(s)

```cpp
if(int ret = someFunction()) {
	// Use ret
} else {
	// ret is 0
}
```

---

# Bitfields

It's possible to compact a group of variables into the size of a single variable.
This is called bitfields.
Care must be taken to arrange bitfields to end on a WORD boundry.

```cpp
struct Bitfield {
	unsigned x:2; // 2 bits
	unsigned y:16; // 16 bits
	unsigned z:14; // 14 bits
};
```

---

# Devious

---

# Array and pointer indexing
Given:

```cpp
int arr[100];
```

We know that:

 * `arr` is a specific type: an array
 * `&arr` is a pointer to an array
 * `&arr[0]` is the location of/a pointer to the first element of the array

Therefore, each of these is equivalent:

```cpp
arr[5]
*(arr+5)
5[arr]
```

This is assuming, of course, that arr is a pointer/array, and not a class with `operator[]` overloaded

---

# By extension

String literals have a type of `const char*`.

It's perfectly legal to index a `const char*`.

Because of this, you're allowed to do something like this:

```cpp
// Gets the lowest hex value of a variable
"0123456789abcdef"[x & 0xf];
// Indexes into the string, but does the same thing
(x & 0xf)["0123456789abcdef"];
```

---

# The ternary operator

The ternary operator, using the format `(x?y:z)`, becomes `y` if `x` is true, otherwise `z`

Here's a simple example:

```cpp
#include <stdio.h>

int main() {
	int x = (1>2)?printf("Fail"):printf("Expected");
	printf("\n%d\n",x);
}
```

However, it actually much more diabolical uses:

```cpp
int x,y,z;
cin>>x>>y;
z = (x>y)?x:y; // Sets z to the higher of x and y
```

Or, if you want to get REALLY crazy:

```cpp
int x,y;
cin>>x>>y;
// Sets the lower of x and y to the inverse of the other
((x<y)?x:y) = -((x>y)?x:y);
```

---

# Abusing destructors

Destructors are called when a class (or struct) leaves scope.

This includes when the program is cleaning up after itself when it's exiting main.

```cpp
#include <iostream>
using namespace std;

struct ProgramWrapper {
	~ProgramWrapper() {
		cin.sync();cin.ignore();
	}
} wrapper;

int main() {
	return 0;
}
```

---

# Function Pointers

Since you can create a pointer to a variable, it makes sense that you can create a pointer to a function.
The syntax is rather ugly though...

```cpp
#include <stdio.h>

int f(int x) {
	return x+1;
}
int g(int x) {
	return x*2;
}
int h(int x) {
	return x-3;
}

typedef int(*FunctionPointer)(int); // Create a type FunctionPointer
// This type points to a function taking an int and returning an int
int main() {
	FunctionPointer todo[3] = {f,g,h}; // Array of function pointers
	int x=10;
	for(unsigned i=0;i < 3;i++) {
		x = todo[i](x);
	}
	// Result should be 19
	printf("Result>\t%d\n",x);
	return 0;
}
```

---

# Unions

Unions are a C++ construct that seem to be horribly misused.
Their purpose is to *save memory*, by placing several variable types in the same block of memory.
The behavior of writing to one type and reading from another is undefined.

```cpp
union Number {
	int integer;
	float decimal;
};
```

This undefined behavior is often abused for type punning, or the rough equivalent of:

```cpp
*(float*)&integer;
```

Don't use unions for this, though.
Undefined behavior is so named for a reason, you have no guarantee that it'll work.

Unions can also contain constructors and member functions -
basically, anything a struct can contain that doesn't involve inheritance or virtual functions.

---

# Const References

Everyone knows that you can't make a reference to the return value of a function.
That's because the return value is a temporary, and once it leaves the function's scope the temporary is invalid.

Unless it's `const`.

When you create a `const` reference to a temporary variable,
it extends the lifetime of the temporary to the lifetime of the reference.
What this means is, this is completely valid:

```cpp
const int & cir = 1+1; // OK to use cir = 2 after this line
```

Andrei Alexandrescu used this to create a "Scope Guard", to allow cleanup inside scope blocks.
He even described it as "the most important **const** I ever wrote."

The most useful trick is that it directly calls the class's destructor.

```cpp
Derived factory(); // construct a Derived object

void g() {
  const Base& b = factory(); // calls Derived::Derived here
  // … use b …
} // calls Derived::~Derived directly here — not Base::~Base + virtual dispatch!
```

Example taken from [Herb Stutter's Guru of the Week (88)](http://herbsutter.com/2008/01/01/gotw-88-a-candidate-for-the-most-important-const/)

---

# Evil

---

# Trigraphs

In order to support those poor programmers who don't have access to such exotic keys as {}, C/C++ support the following:

| Trigraph | Equivalent | Trigraph | Equivalent | Trigraph | Equivalent |
|:--------:|:----------:|:--------:|:----------:|:--------:|:----------:|
| ??= | # | ??/ | \ | ??' | ^ |
| ??( | [ | ??) | ] | ??! | &#124; |
| ??< | { | ??> | } | ??- | ~ |

Important:

 * These require the `-trigraphs` flag in GCC.
 * `???` is not a valid trigraph
 * Replacements are made as the FIRST step of the preprocessor
 * Trigraphs within strings are replaced - to prevent this, do `"?""?-"` instead of `"??-"`
 * With the advent of raw strings (C++11), in order to safely remove all trigraphs you essentially need to write a complete C++ parser.

---

# Digraphs

There are also digraphs, meant to be more readable:

 Digraph | Equivalent
---------|-----------
 <: | [
 >: | ]
 <% | {
 %> | }
 %: | #

Differences between trigraphs and digraphs:

 * Digraphs within strings will NOT be replaced
 * `-trigraphs` isn't required for these
 * Checked during tokenization in the preprocessor
 * A digraph must represent a full token by itself, except for `%:%:`, which replaces the preprocessor `##`

---

# X-Macros

The preprocessor uses a textual replace for #include, replacing the #include with the (preprocessed) body of the file.

Someone unfamiliar with the preprocessor may be confused by this,
because it's common for beginners to assume that the preprocessor must produce complete tokens.
However, 

This means that the preprocesser can be used to generate some types of code.

---

# X-macros Example

### colors.def
```cpp
X(red)
X(green)
X(blue)
```

### main.cpp
```cpp
#include <stdio.h>

#define X(a) a,
enum COLOR {
  #include "colors.def"
};
#undef X

#define X(a) #a,
const char *color_name[] = {
  #include "colors.def"
};
#undef X

int main() {
  enum COLOR c = red;
  printf("c=%s\n", color_name[c]);
  return 0;
}
```

---

# X-Macros final result

### The end result:

```cpp
#include <stdio.h>

enum COLOR {
  red,
  green,
  blue
};

char *color_name[] = {
  "red",
  "green",
  "blue"
};

int main() {
  enum COLOR c = red;
  printf("c=%s\n", color_name[c]);
  return 0;
}
```

Example blatantly stolen from [Randy Meyers](http://www.drdobbs.com/the-new-c-x-macros/184401387)

---

# Supermacros

By using `#undef` within the X-macro file, any code that uses it won't have to clean up after itself.

You can use #define and X-macros together to simulate passing a parameter to the included header file.

---

# Unary + operator

Everyone knows that the + operator is used to sum two values.
However, it can also be used as a unary operator.

```cpp
int x = +1234;
printf("%d",+x);
```

Alone, it's somewhat useless, but it has some interesting side effects.

---

# Unary + on enums

When used on an enum, unary + is the same as a cast to int.

```cpp
enum X {
	a,b,c
};

X val = a;
printf("%d",+val); // +val is an int
```

---

# Unary + to create const ref

Sometimes, a function requires a const reference, but you want to pass it something else.
When this happens, you can use + to create a "temporary reference" to a value.

```cpp
struct Foo {
  static int const value = 42;
};

// This does something interesting...
template<typename T>
void f(T const&);

int main() {
  // fails to link - tries to get the address of "Foo::value"!
  f(Foo::value);

  // works - pass a temporary value
  f(+Foo::value);
}
```

Taken from [Johannes Schaub](http://stackoverflow.com/questions/75538/hidden-features-of-c)

---

# Unary + to convert arrays to pointers

On occasion, you'll need to send a pointer to a function. Typically, your options are:

```cpp
&arr[0];
(int*)arr[0];
```

However, using unary + you can convert any array into a pointer while remaining easy-to-read.

```cpp
// This does something interesting...
template<typename T>
void f(T const& a, T const& b);

int main() {
  int a[2];
  int b[3];
  f(a, b); // won't work! different values for "T"!
  f(+a, +b); // works! T is "int*" both times
}
```

Taken from [Johannes Schaub](http://stackoverflow.com/questions/75538/hidden-features-of-c)

---

# Switch Statements

How do switch statements work?

An ordinary switch statement might look something like this:

```cpp
switch( x ) {
case 0:
	printf("Case 0\n");
	break;
case 1:
	printf("Case 1\n");
	break;
case 2:
	printf("Case 2\n");
	break;
default:
	// do nothing
	break;
}
```

---

# Switch Statements (Fallthrough)

Regular switch statements, by default, have a unique scope for the whole switch (as shown by the {}).

However, if you want to pass through to the next case, this poses problems and will error:

```cpp
switch( x ) {
case 0:
	int y = 0;
	printf("int: %d\n",y);
case 1:
	char y = 'A'; // Error: y is already an int
	printf("char: %c\n",y);
case 2:
	float y = 1.66;
	printf("float: %f\n",y);
default:
	// do nothing
	break;
}
```

---

# Switch Statements (Blocks)

This can be used to properly handle scope for each case, as well as group statements together logically:

```cpp
switch(x) {
case 0: {
	int y = 0;
	printf("int: %d\n",y);
}
case 1: {
	char y = 'A'; // Error: y is already an int
	printf("char: %c\n",y);
}
case 2: {
	float y = 1.66;
	printf("float: %f\n",y);
}
default: {
	// do nothing
	break;
}
}
```

---

# Switch Interlacing

We're able to combine switch and if in some convoluted ways:

```cpp
switch(x) {
case 0: {
	int y = 0;
	printf("int: %d\n",y);
} if(0)
case 1: {
	char y = 'A'; // Error: y is already an int
	printf("char: %c\n",y);
} if(0)
case 2: {
	float y = 'A';
	printf("float: %f\n",y);
}
case 3: {
	printf("Gets run iff x is 0, 1, 2, or 3\n");
} if(0)
default: {
	// do nothing
	printf("Not a valid choice!\n");
	break;
}
}
```

---

# Switch Interlacing Example

This trick can be extended to work with if(){}else{}:

```cpp
switch(mode) {
case PARSE_MODE_COMMAND:
	// We have a null command!
	fprintf(stderr, "Illegal null command\n");
	return NULL;
	break;
case PARSE_MODE_PIPE:
case PARSE_MODE_ARGUMENT:
	if(allowLT) {
		// Set the mode
		mode = PARSE_MODE_INREDIR;
		allowLT = false;
	} else {
default:
		// It's a illegal redirect
		if(currentArg + 1 < argCount) {
			fprintf(stderr, "%s: Illegal input redirect\n",
				argList[currentArg + 1]);
		} else {
			fprintf(stderr, "Illegal input redirect\n");
		}
		return NULL;
	}
	break;
}
```

Credit to Ben Russel (benrr101) for this snippet

---

# Duff's Device

This trick was used with a for loop for this lovely, famous (but slightly modified) bit of code:

```cpp
void duff(char* to, char* from, short count)
{
	char n = (count + 7) / 8;
	switch(count % 8) {
	case 0:     do {     *to++ = *from++;
	case 7:              *to++ = *from++;
	case 6:              *to++ = *from++;
	case 5:              *to++ = *from++;
	case 4:              *to++ = *from++;
	case 3:              *to++ = *from++;
	case 2:              *to++ = *from++;
	case 1:              *to++ = *from++;
				} while(--n > 0);
	}
}
```

What does this code do?

---

# C++ Evil

---

# C++11 Warning

All examples marked with C++11 are part of the C++11 standard ONLY.

This requires the compiler to support at least those features of the standard.

For gcc, the switch to enable this is:

```bash
gcc -std=c++11 file.cpp
```

---

# Templates

Templates are a way to write code that can be adapted to work on any type, such as containers.
std::vector is a template, so `vector<T>` means roughly `vector of some type T`
The syntax for declaring a template is:

```cpp
template<typename T> struct MyType {
	T data;
	MyType(T data):data(data) {}
};
```

In this case, `T` is used as a type determined at compile time:

```cpp
MyType<int> x = MyType(5); // "typename T" matches "int"
```

---

# Template turing-completeness

C++ templates are turing-complete:

```cpp
#include <cstdio>

template<int N> void bin() {
	bin<(N>>1)>(); printf("%d",N%2);
}
template<> void bin<0>() {} // Base case

int main() {
	bin<42>(); // Print the binary representation of 42
	printf("\n");
	return 0;
}
```

---

# Templates on unions (C++11)

Templates can be done on the types in a union as well:

```cpp
template<typename From, typename To>
union union_cast {
	From from;
	To   to;

	union_cast(From from)
		:from(from) { }

	To getTo() const { return to; }
};
```

Type punning didn't stop being undefined, by the way.

---

# Templates on bitfields

Templates can be used for integral values, not just types.
They must be calculatable in compile-time.
This means that a template value can be used in the place of any other compile-time value.

```cpp
#include <cstdio>

template<int N> class BitField {
	unsigned x:N; // Generate a compiler error if N==0
};

int main() {
	Bitfield<2> x; // Booleans "graduate" to integers, so this is legal
	//Bitfield<(1>2)> y; // Creates a zero-width bitfield, so illegal
	return 0;
}
```

---

# Lambdas (C++11)

Lambda functions are basically anonymous functions.
These can make some of the standard library's functions much more usable.

```cpp
vector<int> x = vector<int>(10); // Vector with 10 values
generate(x.begin(),x.end(),[]() {
	return (rand() % 100); // Make a "random" value
});
printf("Number of odd values: ",count_if(x.begin(), x.end(), [](int i){
	return i%2;}));
```

However they can VERY easily confuse anyone who is unaware:

```cpp
#include <stdio.h>

int main() {
	// Harmless example
	printf("%d\n",[]{return 2+2;}());
	[](){}(); // Does absolutely nothing but scare future readers
	// And you can capture them with function pointers!
	int(*f)(int) = [](int x) {return x+2;};
	printf("%d\n",f(5));
	return 0;
}
```


---

# Range-based For Loops (C++11)

C++11 allows the use of foreach loops using a somewhat familiar syntax:

```cpp
vector<int> vec = ...; // Some values or whatever
for(int i : vec) {
	cout << i << endl;
}
```

The trick is that this can operate on C-style arrays, initializer lists, and types that have .begin() and .end() functions.

It's identical to writing:

```cpp
for(auto _iter = vec.begin(); _iter != vec.end(); _iter++) {
	auto i = *_iter;
	cout << i << endl;
}
```

---

# Exploiting ranges

This can be exploited to use foreach over things that aren't "real" collections.

```cpp
class Count {
	int val, step;
public:
	class iterator {
		int val, step;
	public:
		iterator(int val, int step) : val(val), step(step) {}
		iterator operator++() {
			val+=step;
			return *this;
		}
		bool operator!=(const iterator& other) const {
			return (val+step > other.val);
		}
		int operator*() const { return val; }
	};
	Count(int v, int step=1) : val(v), step(step) {}
	iterator begin() { return iterator(val, step); }
	iterator end() { return iterator(val-1, step); }
};

for(int i : Count(5,3)) {
	cout << i << endl;
}
```

---

# Eldritch Abomination

---

# Disclaimer

This last trick is NOT for the faint of heart.
If you are squeamish or think that you may be unable to handle this monstrosity, please stop reading.

It abuses some rules in the C++ syntax that should probably never be abused

---

# Void Type Expressions

A void function is normally assumed to not return anything.
In fact, you can leave the return out of the end of a void function.

However, technically a return expression can contain any expression that evaluates to a value of a type that can be coerced into the return type of the function.

```cpp
void f() { }
void g() { return f(); }
void h(void(*k)()) {
	return k();
}

int main() {
	h(g);
	return 0;
}
```

---

# Void Type Expression Details

Some common void-type expressions:

 - Functions returning void
 - Throw statements (Yes, the statement is an expression, it just returns void)

Other places a void-type expression can be used:

 - As either result of a ternary expression
 - Returning from a templated function, that returns the template type, that gets passed a void as the template

---

# Conclusion

I actually can't produce a piece of code that encorporates MOST of these tricks, let alone ALL.
Such code should probably never exist.

Reminder: Most of these should only be used if there is literally no other way to do what you want to do.
They give you more control over your code, at the expense of readability and maintainability.

Always remember that it's always a good idea to "Code for the Maintainer":

> Always code as if the person who ends up maintaining your code is a violent psychopath who knows where you live.

>> *I usually maintain my own code, so the as-if is true*

---

# return 0;
