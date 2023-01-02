+++
title = "Using Python for Prototyping off of a C Library"
author = "Matt Soucy"
outputs = ["Reveal"]
date = "November 18, 2014"
+++

# Using Python for Prototyping off of a C Library

by Matt Soucy

---

# So we have some C code...

```c
// CMI == Common Message Interface
typedef unsigned char ubyte;
typedef ubyte* Buffer;
Buffer cmi_alloc_buffer(size_t);
void cmi_dealloc_buffer(Buffer);
size_t cmi_buffer_length(Buffer);

typedef void* Router;
Router cmi_alloc_router(void);
void cmi_dealloc_router(Router);
```

---

# Echo server

Motivation: doing some testing on part of the framework. Tried to create a server that will just echo back what it receives.

---

```c
#include <cmi.h>
#include <stdio.h>

int main(int argc, char* argv)
{
	// Routers automagically find each other (don't ask)
	Router r = cmi_alloc_router();
	while(1) {
		Buffer buf = cmi_recv(r);
		printf("Buffer length: %u", cmi_buffer_length(buf));
		// We send the original buffer back
		// Right now this process "owns" the buffer's memory
		cmi_send(r, buf);
	}
	// Ignoring error handling...
	cmi_dealloc_router(r);
}
```

---

# Eew.

---

# Python translation

What would the nicest way to write it look like?

```python
import cmi

with cmi.Router() as r:
	while True:
		buf = r.recv()
		print("Buffer length:", len(buf))
		r.send(buf);
```

---

# Direct translation

Here's a transliteration of the C code:

```python
# ccmi is the direct bindings
import ccmi as cmi

r = cmi.alloc_router()
while True:
	buf = cmi.recv(r)
	print("Buffer length:", cmi.buffer_length(buf))
	cmi.send(r, buf)
cmi.dealloc_router(r)
```

Already looks a bit cleaner!

---

### Let's make a Buffer class

```python
# File: cmi.py
import ccmi

class Buffer(object):
	def __init__(self, data):
		self.data = data
	def __len__(self):
		if self.data is None:
			return 0
		return ccmi.buffer_length(self.data)
	def __repr__(self):
		return self.data
	@staticmethod
	def alloc(size):
		return Buffer(ccmi.alloc_buffer(size))
	def dealloc(self):
		if self.data is not None:
			ccmi.dealloc_buffer(self.data)
		self.data = None
```

---

# The Router helper

```python
class Router(object):
	def __enter__(self):
		self._r = ccmi.alloc_router()
		return self
	def __exit__(self, exc_type, exc_value, traceback):
		# Notice that it will automatically handle cleanup
		ccmi.dealloc_router(self._r)
	def send(self, buf):
		ccmi.send(self._r, buf.data)
	def recv(self):
		return Buffer(ccmi.recv(self._r))
```

Already, we can do everything the original code could!

---

# What is `ccmi`?

`ccmi` could be made in any number of ways:

- `ctypes`: Built in to the standard library
- `cffi`: Nonstandard, but much nicer

Just contains information about the C functions:

```python
# Using ctypes:
cmilib = CDLL("libcmi.so") # Pretend I handle Windows
Buffer = ctypes.c_void_p
buffer_length = cmilib.buffer_length
buffer_length.argtypes = (Buffer,)
buffer_length.restype = ctypes.c_uint
```

---

# Using `cffi`

```python
# cffi handles this for you
ffi = cffi.FFI()
# Could even use open("cmi.h").read() for this..?
ffi.cdef("void* buffer_length(unsigned int);")
C = ffi.dlopen("libcmi.so")
buffer_length = C.buffer_length
```

---

# Using the new CMI library

Yes, this is the original code.

```python
import cmi

with cmi.Router() as r:
	while True:
		buf = r.recv()
		print("Buffer length:", len(buf))
		r.send(buf);
```

---

# Why is this cool?

- It's super simple to create a wrapper!
- Rapid Prototyping
- Ease tool development
	- Communication written in C, but tools (GUIs, logic) done in Python
	- Existing tools were limited to Windows only, because of GUI
	- Python is more cross-platform for the tool-based stuff, only need to worry about the messaging

---

I made several tools based off of this on co-op:

- Echo server
- Byte-swapped echo server
- CMI-to-Ethernet bridge

---

# Issues with this

- Code may need to be changed to export symbols from a dynamic library
- Requires some boilerplate code (but `.h` files aren't much better)
- The echo server was SLIGHTLY slower...but only slightly
- Python couldn't be easily used to write any production-level code (embedded on a proprietary system)

---

# Questions?

- Slides at <http://msoucy.me/seminars/cpy>
- Contact me at <msoucy@csh.rit.edu>
