+++
title = "Build Systems Suck"
author = "Matt Soucy"
outputs = ["Reveal"]
+++

# Build Systems Suck

by Matt Soucy

---

# In the beginning...

...there were basic commands.

```bash
$CC -c main.c -o main.o
$CC -c lib.c -o lib.o
$CC -o prog lib.o main.o
# $CC is a variable that holds "C compiler of your choice"
```

---

# More arguments

What happens when we want more arguments added?

```bash
$CC -c main.c -o main.o -I../somelib
$CC -c lib.c -o lib.o -I../somelib
$CC -o prog lib.o main.o
```

This is silly...

---

# Variables

Can we store values in shell variables?

```bash
export CFLAGS=-I../somelib -DFOO=5
$CC -c main.c -o main.o $CFLAGS
$CC -c lib.c -o lib.o $CFLAGS
$CC -o prog lib.o main.o $CFLAGS
```

---

# Loops?

More "condensing"

```bash
export cfiles=main lib
export CFLAGS=-I../somelib -DFOO=5
for i in $cfiles; do
	$CC -c ${i}.c -o ${i}.o ${CFLAGS}
done
$CC -o prog $(cfiles// /.o ).o
# Fails if multiple spaces are in cfiles, like 'a  b'
```

Still rebuilds everything EVERY TIME.

---

# Rule-based

What rules to we have?

- Build a `.o` from a `.c` with `$CC -o ${name}.o ${name}.c ${CFLAGS}`
- Build an executable from a list of `.o` files with `$CC -o ${name} ${files}`

Introducing `make`!

---

# Introducing `make`

Back to the "beginning"...so no variables (yet) or optimization

```makefile
prog: main.o lib.o
	${CC} -o prog main.o lib.o -I../somelib -DFOO=5

main.o: main.c
	${CC} -o main.o -c main.c -I../somelib -DFOO=5

lib.o: lib.c
	${CC} -o lib.o -c lib.c -I../somelib -DFOO=5
```

---

# Using some variables

```makefile
CFLAGS:=-I../somelib -DFOO=5

prog: main.o lib.o
	${CC} -o prog main.o lib.o ${CFLAGS}

main.o: main.c
	${CC} -o main.o -c main.c ${CFLAGS}

lib.o: lib.c
	${CC} -o lib.o -c lib.c ${CFLAGS}
```

---

# Rule matching

```makefile
CFLAGS+=-I../somelib -DFOO=5

prog: main.o lib.o
	${CC} -o prog main.o lib.o ${CFLAGS}

%.o: %.c
	${CC} -o $@ -c $< ${CFLAGS}
```

---

# Implicit Rules

Make actually has support for C, C++, Fortran, Lex, Yacc...

```makefile
CFLAGS+=-I../somelib -DFOO=5
proc: main.o lib.o
```

---

# Cleanup and tests

```makefile
CFLAGS+=-I../somelib -DFOO=5
OBJS=main.o foo.o

all: prog

prog: ${OBJS}

# Test target depends on the program existing
test: prog
	./prog 1 2 > test.out
	diff test.out actual.out

clean:
	rm -rf ${OBJS}

# Tell make that "clean" doesn't generate anything,
# so is always out of date
.PHONY: clean test
```

---

# `make` is magic

If you have just a test file `main.c`, you can run `make main` without a makefile at all, and the built-in rules will operate on it!

---

# `make` Awesomeness

- Specify rules to build one of several potential targets
- Useful for configurations ("release" vs "debug")
- Used everywhere
- Not just building, but also test targets, cleanup...general purpose "command group run utility"

---

# `make` Problems

- Syntax is rather arcane at times
- Not the best on Windows
- Need to list out every dependency
- Output-file-based
- External dependencies require `autotools`, which gets messy

---

# Alternatives?

- Language-specific
- `tup`
- `scons`
- `ninja`
- `cmake`

---

Language | Tool
---------|-----
D        | dub (JSON)
Java     | ant (xml)
Java     | Maven (xml)
Python   | Python (pip, setuptools, pbr...)
Go       | `go build` (builtin)
Haskell  | Cabal

Most of these also do some sort of dependency management, as well as build management.

---

# `tup`

Graph-based system that promises that builds are always "as if from clean"

```tupfile
# Tupfile
CFLAGS += -I../somelib
CFLAGS += -DFOO=5
!cc = |> $(CC) $(CFLAGS) -c %f -o %o |> %B.o
: foreach main.c lib.c |> !cc |>
: main.o lib.o |> $(CC) %f -o %o |> prog
```

---

# `tup` Awesomeness

- Fast as `****`.
- Syntax is directed: `: inputs |> commands |> outputs`
- Variables make sense
- Many features of `make`, with different syntax
- Build from anywhere in the tree
- No need to clean
- Generate build graphs
- Dependency handling

---

# `tup` Problems

- Nested Tupfiles have some quirks
- Nobody's heard of it
- Support for `make install`-like commands is nonexistent
- Build configurations are a bit weird

---

# `scons`

`cons` (perl) -> `sccons` (Python) -> `scons` (Python)

Basically a build-system-in-a-library

```python
env = Environment(CPPPATH=["#../somelib"],
                  CPPDEFINES={"FOO": "5"})
prog = env.Program(target="prog", source=["main.c", "lib.c"])
Default(prog)
```

---

# `scons` Awesomeness

- Uses Python syntax and libraries
- Supports many languages and compilers
- Self-contained
- Dependency tracking
- Can ship `scons-local`, so just depends on Python

---

# `scons` Problems

- Requires extra code for some simple tasks
- Slow
- Lots of documentation to wade through
- UnPythonic API


---

# `ninja`

- Best. Name. Ever.
- Like `make`, but with a bit nicer syntax.

```ninja
cc = gcc
cflags = -I../somelib -DFOO=5
rule cc
  command = $cc -c $in -o $out $cflags
rule link
  command = $cc $in -o $out $cflags

build main.o: cc main.c
build lib.o: cc lib.c
build prog: link main.o lib.o
```

---

# `ninja` Awesomeness

- Fantastic name
- Similar to `make` syntax
	- Easier to read
- Lightweight
- Generate build graphs
- Splits rules and files
- Supports dependency handling
- Paralell by default

---

# `ninja` Problems

- Not much control flow
- Doesn't take in environment variables
- No inline rules allowed
- Not (very) human-writable

---

# `cmake`

A meta-build system that generates:

- Makefiles
- Ninja files
- MSBuild files
- IDE project files
- etc.

Write one bit of cross-platform code, build for all platforms

---

# `cmake` Example

```cmake
cmake_minimum_required(VERSION 2.8.12)

project(MyProgram)

include_directories(../somelib)
add_definitions(-DFOO=5)

add_executable(prog main.c lib.c)
```

---

# `cmake` Awesomeness

- Cross-platform
- Supports major compilers, languages, IDEs
- Describes the build structure
- Based on "input files", not "output files"
- Built-in test, install support
- Multiple build trees (out-of-source builds)

---

# `cmake` Problems

- The language
- The language
- Seriously, the language

---

# `cmake` Problems

- No lists (list == semicolon-delimited string)
- Conditionals/loops look like function calls
- Scoping is really weird
- "Fake" functions (no return values)
- Everything is controlled by "magic" variables with long names

---

# Conclusion

All build systems have huge problems, but some have nice features

Find the system that works best for your use case

Desire   | Possible build system
---------|----------------------
Simple   | make, ninja
Fast     | tup
Portable | cmake, SCons

---

```bash
for q in ${questions}; do
	try-answer $q
done
```
