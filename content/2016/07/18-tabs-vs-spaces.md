---
Title: Tabs vs Spaces
Category: code
Tags: humor
---

In honor of the fantastic [Silicon Valley][] third season, I felt like posting to show that not only have I not completely vanished off the face of the earth, but I also have an opinion on one of the greatest (and most useless) debates of computing: [tabs vs spaces][].

... I lied, this is entirely a ploy to share that video.

Honestly though, I can see how developers change their opinions over time.

When a dev is starting out, it seems reasonable to want to use tabs, because it lets people see code the way they feel most comfortable.
This breaks down, though, for that exact reason.
When tabs are used for alignment, something that appears aligned for the author will often be horribly skewed for people who prefer a different tab size.
Then, *nobody* likes how it looks, and any time someone maintains it you end up with a ton of whitespace changes.

So, if tabs are bad for alignment, what about "tabs for indentation and spaces for alignment"?
... Yeah, no. That's kind of terrible. It's a hassle for editors to manage, you can't rely on autoindent, and it confuses the reader who now has to hold the indentation state in their mind (though to be fair this is mitigated by editors that display whitespace in some form, such as vim).

Therefore, spaces are the most sane option for any project, especially one that involves several developers.
With certain editor support, substantially simpler than the aforementioned mixing support, using spaces is seamless for the user (pressing tab gives you a variable number of spaces) and backspace behaves as though a tab was used - but code still shows up as expected.

[Silicon Valley]: http://www.hbo.com/silicon-valley
[tabs vs spaces]: https://youtu.be/SsoOG6ZeyUI
