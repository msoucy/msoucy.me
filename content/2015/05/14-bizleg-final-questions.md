---
title: "BizLegFOSS: Answers to Final Questions"
Category: class
Tags: foss,bizlegfoss
---

As a group, the [bizlegfoss][] class decided on the questions that we wanted to have on the final.
These questions aren't submitted in class, though, but as a blog post.
This wasn't to make it "easier", but to allow us to choose the most important questions from the class and let us share our knowledge.

> When does code you create become copyrighted?

As soon as you save it and it's stored somewhere

> If you could wave a magic wand, and open source any piece of proprietary software, what software would you choose?

I would say the development toolkits for either Nintendo's WiiU or 3DS lines.

> If the software above was open sourced, would it’s company remain stable? How would the company continue to make money?

The company would remain stable, because they could license the ability to put games on an official cart instead of licensing the development kit itself.
Even if they implemented some sort of check (As in, "this game was officially released by Nintendo"), it would open up the potential to find new developers, and allow many more people to develop for the platforms.

> What do you feel was the most beneficial thing to learn in the class?

I would say the nuances of licensing, because any open source developer will have to deal with those issues regularly.

> Explain some of the motivations a company may have to open source software.

- "Free" bug reports and work from users, following "Linus' Law" - "Given enough eyeballs, all bugs are shallow"
	- With an appropriate license, the company can avoid problems with utilizing this workforce
- Excellent advertising for the company
	- Shows that the company wants to give to the community
	- Developers will be more likely to want to work for a company that visibly helps developers
- Can help the company find new talent
	- Someone is making a lot of useful contributions to a project? It seems like they really care, it might be worth hiring them to work on it full-time.

> Are there any changes you would suggest making to the profile template? What parts did you find most interesting or important?

A lot of the questions were about a specific project that the organization makes, which is problematic for Open Hardware companies.
More emphasis should be placed on the actual business and community portions.

> If you could have spent more time, say an extra week, on any topic, which would you have liked to cover more in depth?

Covering noncompete and nondisclosure agreements would have been extremely helpful.

> Why are you using license insert license X here for your open source project?

I actually had an [interesting situation][issue 38] with this recently, where I received a request to relicense [dproto][] from [BSD-3 clause][] to the [Boost Software License][BSL-1].
The reasoning behind this request, which at first I was against but later changed my mind, was that [dproto][] generates code that is meant to be used for (de)serialization, and requiring a copy of the BSD license to be shipped with every product that includes generated code would provide little-to-no benefit for end users who most likely don't even know about the language that the software is written in.

> If you would suggest a video to be watched as part of this course, what would it be?

Other than [Hackers][]?
I'd have to say [The Internet's Own Boy][], though since one has to pay it might be better suited for a class movie night.
Alternatively, either [Gabriella Coleman's keynote][biella] or [Open Source for Newcomers][], both of which I was fortunate enough to see in person.

[bizlegfoss]: http://bizlegfoss-ritigm.rhcloud.com/
[issue 38]: https://github.com/msoucy/dproto/issues/38
[dproto]: http://github.com/msoucy/dproto
[BSD-3 clause]: http://choosealicense.com/licenses/bsd-3-clause/
[BSL-1]: http://www.boost.org/users/license.html
[Hackers]: http://www.imdb.com/title/tt0113243/
[The Internet's Own Boy]: http://www.takepart.com/internets-own-boy
[biella]: http://pyvideo.org/video/3493/keynote-gabriella-coleman
[Open Source for Newcomers]: http://pyvideo.org/video/3405/open-source-for-newcomers-and-the-people-who-want
