Title: Playing with Golang
Category: code
Tags: hackathons

As part of the Spring 2014 [Hack Upstate][], my team decided to create our project in Go (AKA Golang, AKA [Issue 9][]). [One friend][] will be using it for an upcoming co-op, and [the other friend][] and I figured that it would be an interesting language to learn. Here are some of the random thoughts we have on the language:

- Lack of generics wasn't much of an issue, despite my using them frequently in other languages
- A lack of a standardized constructor is limiting - sometimes the "0-value" is less than useful, but there's no standard way to make a new instance of a struct without having special `NewT()` or `MakeT()` functions, which don't play nicely with `make([]T, N)` and `new([]T)`.
- Speaking of, not much plays nicely with `make` and `new`
- The code looks so empty as a C-like language with a significant reduction in  semicolons
- `s/warning/error/` is a bit annoying when you WANT to have something like an unused (for the moment) variable
- "At least they didn't do the same broken switch-case that everyone who bases their syntax on C does"
- Some warnings just don't seem to exist online ("Cannot embed C type? How has nobody online ever encountered this problem?")
- Apparently installing via yum does weird things like not set $GOROOT?
- Multiple return is used to "handle" errors - a lot of code becomes more verbose because they have to handle exceptions immediately instead of in one centralized place. This is "better than errno because it forces you to look at them, but not by much"
- "`panic()` and `recover()` are the worst error handling ever"
- That said, `defer` is wonderful (and reminiscent of `scope(exit)` in D, which is very nice)
- The placement of the return value, plus the requirement that the `{` is on the same line, makes it easy to forget to add the return type
- You better use `go fmt`, or there's no guarantee that your code works
- Variable declaration syntax is clean and straightforward (a little too clean, as I mentioned above), and only becomes confusing on occasion, inside function parameters
- Why does `len(x)` return a signed int?
- "And yes, I DO come from a language where integers are arbitrary-precision by default, thank you very much for asking. As it SHOULD be."
- `map[string]int` is slightly prettier than `map<int, string>`, but still not as nice as `int[string]`. Unfortunately, because of the "read-left-to-right" requirement, this isn't possible. `[string]int` might work, but also could add some weird edge cases to the compiler
- Interface "mixing in" is too similar to member declaration
- Semicolon insertion is a poor way to enforce single-line conventions
- Using `:=` for the first, and only the first, assignment to a variable is odd, because it changes the entire operator used, as opposed to `var x = foo()`
- Case sensitivity to denote export status feels like needlessly forcing a particular idiom - and since there's no difference in convention between types and functions, it gets a bit annoying. (I have this same complaint with C#, but there it's a convention not a constraint)
- `type` (the rough equivalent to C's `typedef`), creates a type that BEHAVES identically to the original type, but is distinct so that the user can overload on a "new" type, which is awesome and useful
- "Since Go 1 the runtime randomizes map iteration order, as programmers relied on the stable iteration order of the previous implementation." WHY. Isn't that really slow?
- Go doesn't have generics...so why is there `type Type int` in the documentation for builtins? Oh, wait, to represent ANY TYPE. Doesn't that sound familiar?
- When what I wanted to do was directly doable by the language, it was usually relatively intuitive
- Is there really no convenient way to iterate over a sequence in reverse?
- "Oh yeah, that's right... Go's `while` loop is called `for`."
- I understand why `append` works the way it does, but it's rather annoying having to use `foo = append(foo, bar)` all the time.
- Don't even bother trying to store things in a map if you want to mutate them. `map[string]Item` became `map[string]*Item`, as it was the only way to properly handle them.

Some of these are just "change your way of thinking", some are "personal preference", and some are "who in the world considers this a good idea?"

[Hack Upstate]: http://hackupstate.com/
[Issue 9]: https://code.google.com/p/go/issues/detail?id=9
[One friend]: http://blog.gonyeo.com
[the other friend]: http://github.com/robgssp
