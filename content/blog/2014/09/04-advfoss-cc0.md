---
title: "Community Contribution: Rebase Gone Wrong"
Category: code
Tags:
- advfoss
---

"Just rebase, it won't be that bad!"

Said nobody. Ever.

For my community contribution, I attempted to bring [an old pull request] up to date. Unfortunately, I didn't expect it to be so far from master.

Merging was fine, until I ran across the dreaded words: "This could use a rebase." OK, let's rebase.

As you can tell from [my pull request], it's not that simple.

My original goal was to merge master onto a pull, so that the pull can be read more conveniently. This backfired when there were commits going back eight months. I tried to clean up by rebasing the commits, though I forgot that that would lose a lot of data, and so the merge won't work easily.

[an old pull request]: https://github.com/D-Programming-Language/phobos/pull/1797
[my pull request]: https://github.com/WebDrake/phobos/pull/6
