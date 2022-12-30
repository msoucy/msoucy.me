---
Title: On "On Iteration"
Category: code
---

*This post was originally on an internal group for a class I'm in involving design patterns and architecture. It was slightly updated to suit this blog.*

Very few people would accuse C++ of being a well-thought-out language. It has quite a few inconsistencies, weird syntax rules, and [some rather strange things that it allows][evil C]. With that said, I feel that its attempt to be backwards-compatible with C caused one of the ugliest mistakes it has: Iterators.

Everyone here knows the GoF iterator, it basically looks like:

	:::cpp
	class Iterator<T> {
		T peek();
		bool hasNext();
		void getNext();
	}

A slight tweak would be to rename `peek` to `peekNext`, but that's irrelevant.

C++ developers, in an attempt to be backwards-compatible with C, apparently had this rough train of thought: "Well, in C we have pointers, and you can do p++ to advance it, and *p to get it, and you can compare with other pointers. Clearly, this means that we can adapt the existing interface to use it for C++'s iterators!"

Which is nice, in theory, after all it's "compatible" and C pointers are now magically "iterators", but fails horribly in practice.

Why is this? As [Andrei Alexandrescu states in his rather well-known article, "On Iteration"][On Iteration], which served as the basis for this post, you need two STL iterators to do anything useful - a single iterator has no equivalent to hasNext(). There is no guarantee that the iterators you use will be correctly paired. They also have a hierarchy based around types of iteration, but the semantics between several kinds are too similar. These deviations from the original GoF pattern are annoying not just because they're different from the "by-the-book" implementation, but because they actually cause problems with safety and control

As Alexandrescu proposed, a nicer implementation is to return to the GoF...and then deviate a different way. His section on ranges introduces another concept, one that I find much more convenient and expandable:

	:::cpp
	interface Iterator<T> {

		// "Input" range
		bool empty(); // Is there any more information available?
		T front(); // Get the "head" element
		void popFront(); // Move the "head" to the next element

		// "Forward" ranges, closest to GoF, based on Input
		Iterator<T> save(); // Return a copy of the iterator with identical current state

		// Double-ended ranges, based on Forward
		T back(); // Get the "last" element
		void popBack(); // Remove the "last" element

		// Random access - based on Forward, though "finite" ones are based on Double
		T at(int index); // Get a single element
		Iterator<T> slice(int start, int end); // Get an iterable collection of items

	}

Mouthful, right? Not really, actually. All of the functions are straightforward, and build off of each other.

Take a look at the "Experience with Ranges" and "Higher-Order Ranges" sections of the article to see some real-world applicability of this - from using them extensively, I feel that by sticking closer to the GoF, it resulted in a much more usable system, and gives extra power - it's difficult to implement something that matches a STL iterator but gives "lazy" support - something like D's [std.range.iota] or Python's [range (xrange in Python 2)][range], both of which compute numeric sequences without storing the entire sequence.

Basically, the point I'm trying to get at is that following the pattern, particularly the simple ones, usually helps create much nicer interfaces, but there are times when mixing it up can create something even more convenient.

[evil C]: http://msoucy.me/seminars/evilC.html "My Evil C Seminar"
[On Iteration]: http://www.informit.com/articles/printerfriendly/1407357
[std.range.iota]: http://dlang.org/phobos/std_range#iota
[range]: https://docs.python.org/2/library/functions.html#xrange
