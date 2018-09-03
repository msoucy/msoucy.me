---
Title: D, or "C++ Done Right(er)"
Category: code
---

One of the languages that I spend a lot of time using is the [D Programming Language](http://dlang.org).
I've gotten quite a bit of (mostly) good-natured ribbing at my choice of language, but I normally just respond by showing people some of the more interesting features that I consider to be a huge improvement over C++, such as:

* Templates that are actually easily usable
* Compile-Time Function Execution, to do heavy processing at compile time instead of at run time
* United Function Call Syntax, allowing developers to simulate extending classes using a natural syntax

As a small example, last night another D programmer was asking about a way to do something similar to Python's `setdefault` for dictionaries.
After a short setup period, I produced the following code:

```d
import std.stdio;

ref T setdefault(T, U)(ref T[U] aa, U key, lazy T defaultvalue)
{
    if(key !in aa) aa[key] = defaultvalue();
    return aa[key];
}

class A
{
    this(int i)
    {
            writeln("A's constructor ", i);
    }
}

void main()
{
    A[string] aa;
    aa.setdefault("t2", new A(3));
    aa.setdefault("t2", new A(4));

    auto b = aa.get("test", new A(2));
}
```

The key part is that my `setdefault` function could be used as if it were a member if the associative array - UFCS in action.

Some of my code examples and breakdowns will be in D, because it's an interesting language that has some cool capabilities.
