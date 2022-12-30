---
Title: libfabd post update
Category: code
Date: "2015-02-03"
Tags:
- foss
---

When I wrote an [old post] about libfabd, I included a code sample:

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

I realized a little while later that the entire class was actually rather silly.
I was attempting to keep a pointer to the C string, but I had no guarantee that another C function wouldn't mess with the pointer.
The safest way, though not the fastest, would be to copy the source string.
This also helps by removing several duplication isues where I had an overload for `CString` and `string`.
Naturally, I wrapped the bulk of the code in a quick function:

```d
private string takeown(char* cptr)
{
	import core.stdc.string : strlen;
	import core.stdc.stdlib : free;
	auto dstr = cptr[0 .. strlen(cptr)].idup;
	free(cptr);
	return dstr;
}
```

*This doesn't use `fromStringz` found in the most recent version of phobos, as it's not available in all compilers yet.*

The function could be used easily, tacking it on the end of a call to a C function:

```d
string apply_color(String)(String text, Color c)
	if(isSomeString!String)
{
	// cfab is a reference to the direct C-style bindings
	return cfab.apply_color(c, text.toStringz).takeown;
}
```

[old post]: {{< ref "/blog/2014/12/16-libfabd-postmortem.md" >}}
