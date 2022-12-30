---
Title: Magic Set Editor
Category: code
Tags:
- linux-dev
- foss
- c++
- bizlegfoss
---

I haven't been able to post much about actual projects I've been working on lately, so I figured that I'd at least do a little introduction.

Back when I was in high school, some of my friends were really into [Magic the Gathering][].
More interestingly, they were fond of a tool called [Magic Set Editor][], which allows people to create their own custom cards and sets, as well as generate packs of cards based on rarity.
It seemed like a fairly usable program back then, for mocking up not just Magic cards but custom games as well.

I thought about the program again recently (brought on by some upcoming game-development events) and wondered about the feasibility of making it build in Linux - I had remembered that there was some preliminary work, but wasn't sure about its development status.

The last commit was in April 2012, and the last release February 2011.

What happened since then?

- C++11 was finalized and most of the commonly used compilers implement it. This deprecated a lot of boost usage:
	- `std::regex`
	- `std::unique_ptr`
	- `std::shared_ptr`
	- `std::mt19937` (pseudorandom number generation)
	- Range-based for loops
- libpng got stricter about iCCP profiles, which resulted in most of the images causing error popups
- The world really started catching on to [cmake][]

I got started on fixing these issues, as well as otherwise "cleaning up" the code.

One thing that did concern me a bit was that there seems to be some prior work that started around the same time:

- [kjoppy][] seems to be working on it, but I can't find the actual MSE code changes available anywhere - which goes completely against the GPLv2 that MSE is licensed under.
- [Ninzhan][] has a GitHub mirror, but there are no changes that aren't in the original SourceForge distribution

Overall my [progress][MSE] is coming along, though I still have some cleanup to do. I recently isolated a bug that's been in the code since 2008, so I can make a nice new fix.

Assuming I can make it build properly in Windows again...

[Magic the Gathering]: http://magic.wizards.com/
[Magic Set Editor]: http://magicseteditor.sourceforge.net/
[cmake]: http://cmake.org
[kjoppy]: http://magicseteditor.sourceforge.net/node/7072
[Ninzhan]: http://magicseteditor.sourceforge.net/node/9319
[MSE]: http://github.com/msoucy/MagicSetEditor
