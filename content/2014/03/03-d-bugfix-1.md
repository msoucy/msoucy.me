---
Title: Fixing Bugs: D/Phobos
Category: code
Tags: hfoss
---

A large part of open development is giving back to projects that you use.

As a semicasual D programmer, I jumped at the opportunity to get class credit for using it. The HFOSS course has an assignment that requires us to submit a (reasonable) pull request to an open source project. After browsing through the bugs, I discovered [Issue 4391]. Due to my recent adventures with functional programming, I figured that it would be an exciting request to try.

That was when the compiler attacked.

One of my largest complaints with DMD and D compilers in general is that some things that "should work" seem to break for strange reasons. In this case, I admit that my code was a slight edge case, but still relevant.

Deriving some of the code from [Philippe Sigaud] in the issue, I set forth to create a slightly more modern implementation. There were a few issues I had with the initial code:

- `Init!T` doesn't exist, but `T.init` works for these purposes
- Several helpers that seemed to just clutter the namespace
- Uses string mixins, which I felt were overkill for this situation (templates are sufficient)

I was able to get the code mostly working, thanks in part to the sample code and leveraging `std.functional.partial`, except for one irritating edge case:

- A templated delegate
- Within a unittest or function
- That isn't marked as static

Removing the template, or marking it as static, or moving it outside the unittest, makes everything work cleanly. Despite double-checking with a couple of other D developers, it appeared that this wasn't an issue with my code directly, but rather relating to the context pointer and where templates are instantiated.

[My pull request], therefore, was reduced to "rename and fix documentation for curry", so that it has a name that matches what it actually DOES - partial application. I left a `deprecated alias curry = partial` in the code (with documentation) to preserve backwards compatibility, in the hopes that if/when I can complete the FULL intended pull, the name change won't be as complex.

[Issue 4391]: https://d.puremagic.com/issues/show_bug.cgi?id=4391
[Philippe Sigaud]: https://github.com/PhilippeSigaud
[My pull request]: https://github.com/D-Programming-Language/phobos/pull/1979
