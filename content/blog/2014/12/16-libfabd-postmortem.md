---
title: "Postmortem: libfabd"
categories: [code]
Date: "2014-12-16"
Tags:
- advfoss
---

My final project for advfoss, [libfabd], was different than the first two.

With the previous ideas, I had existing code that I was adapting into a new form.
RESTZZZ had the existing 0mq libraries that I adapted for the web.
PrettyWeb had `commonmark.js`, which I adapted for a browser plugin.

I was kind of getting sick of writing things for browsers.

[libfabd] was an interesting project - I wanted to start writing in [D] again, and I wanted to work on a command-line project.
By nature, I dislike writing things that the user can see, preferring to focus on things behind-the-scenes that allow developers to make cool things.

Naturally, the project I ended up doing was based on making pretty interfaces.

My friend and classmate [rossdylan] had been kicking around an idea for a rewrite of a Python library called [fabulous].
His reasoning was that the original development was halted, and the library had more features than belonged there.
His project was written in C, so naturally a [D] binding was not only possible, but straightforward.

Since the binding was straightforward, I spent a lot more time reading through [libfab]'s C code and pointing out issues.
There were a few efficiency problems and some confusion with the way C works, but overall [rossdylan] and I got some decent work done.

There were two big issues on D's side.
First of all, libfab allocated C strings that it expected the caller to take ownership of.
Converting this to a D string would make it more convenient for D, but then there's the issue of cleaning up after the allocated string.
I didn't see a good way to do that in the standard library, so I had to write a quick wrapper:

```d
class CString {
	this(char* ptr) {
		raw = ptr;
	}
	void toString(scope void delegate(const(char)[]) sink) const
	{
		sink(raw.to!string);
	}
	immutable(char)* toStringz() pure nothrow
	{
		return cast(immutable(char)*)(raw);
	}
	~this() {
		core.stdc.stdlib.free(raw);
	}
	char* raw;
	alias raw this;
}
```

This relies on using `std.conv.to` only for printing, which I was fine with, and converts the C string into a garbage-collected object.

The other issue I had was one that still isn't solved.
For some reason, wrapping the function `xterm_to_rgb` failed. I came to the conclusion that it was an issue with the sizes of C structs vs D structs (somehow), but this only seemed to happen at the C-to-D conversion. To fix this, I had to write a quick hack:

```d
cfab.rgb_t xterm_to_rgb(int xcolor)
{
	auto res = cfab.xterm_to_rgb_i(xcolor);
	return cfab.rgb_t(
		(res>>16) & 0xFF,
		(res>>8) & 0xFF,
		res & 0xFF
	);
}
```

This ends up calling `cfab.xterm_to_rgb`, converting that to an `int` to get it past the C-to-D conversion, and then unwrapping it again, which is **slightly** less efficient, but works. I'll probably spend some time later figuring out how to fix it more cleanly.

As of now, [libfabd] is [released on dub][release], which is pretty cool. Hopefully over the upcoming break I'll be tweaking it and posting an announcement to the D newsgroups.

Special thanks go out to [rossdylan] for starting the "libfab ecosystem" for the class!

[libfabd]: http://github.com/msoucy/libfabd
[D]: http://dlang.org/
[rossdylan]: http://blog.helixoide.com/
[fabulous]: https://github.com/jart/fabulous/
[libfab]: https://github.com/rossdylan/libfab/
[release]: http://code.dlang.org/packages/fabd
