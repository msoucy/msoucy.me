---
Title: Experiencing Mastodon
Category: life
Tags:
- foss
---

Recently I made a few changes concerning my social media accounts.

Facebook
========

First of all, I uninstalled the Facebook app from my phone.
This was a long time coming, but I finally got fed up with the amount of advertisements that I saw on a regular basis, how much it spies on me, as well as how it was negatively affecting my mental health to have it so accessible.
I did keep the Messenger app, because a lot of my friends only use it to communicate, and I haven't put in the effort to get them to switch to something like [Signal][].
I've also started using Firefox's [Facebook Container][] addon, to better limit what it can see about my online habits.

Mastodon
========

More interestingly, I've started replacing my (admittedly limited) usage of Twitter with a more interesting alternative - [Mastodon][].
This site may seem a bit strange, but it fills the niche that Twitter has grown into, with a few neat features.

*Note: I say "grown into" because Twitter originally was meant to be used via SMS, hence its original character limit. For the most part, this role isn't used much anymore nowadays.*

Content Warnings
----------------

Mastodon has the concept of Content Warnings - ways to hide parts of your post behind a warning that the user has to explicitly click/tap on.
This has some good uses - hiding things that might be triggering to some, hiding content that isn't safe for work, or even just hiding the punchline of jokes.

Federation
----------

The real reason that Mastodon is so powerful, is that there isn't just one Mastodon.
There's an entire herd of them.

Mastodon is the name of [the software][Mastodon source] that powers the social networking site.
Anybody is able to download the source and run their own instance.
Users can refer to users on their own instance with `@username`, or refer to a user on another server with `@username@server.name`.
Not only can they mention users from other instances, but they can also follow them.
This is the primary draw to Mastodon's federated nature - any toot (Mastodon parlance for a post) that you make is propogated to your followers, regardless of where their actual instance is running.

This federated setup allows new instances to be set up for specific purposes - the Mastodon project homepage has a menu that allows one to search for instances that might suit them, filtering by language and interest.
There are instances set up for musicians, writers, LGBTQ+, gamers, developers, and many other demographics. This can help you connect with people with similar interests

Timelines
---------

On Twitter, you have one timeline, that contains "recommended" posts, and other tweets that are determined by some sort of magic.
Mastodon splits your timeline into several:

- Home, which is the closest to your Twitter feed, containing posts that people you follow have made or boosted (Mastodon's equivalent to "retweeting"), sorted strictly chronologically
- Notifications, which is somewhat configurable but generally shows when people follow or mention you
- Local timeline, which is a sometimes fast-paced feed of all posts that are made on your instance, allowing you to find interesting people to follow
- Federated timeline, which is like the local timeline but also for all users whom are followed by people on your instance

I generally find the federated timeline to be far too fast-moving to really follow, but it can be interesting for seeing what the world is talking about.

Toot controls
-------------

Much like Twitter posts, toots can be embedded:

{{< mastodon "https://mastodon.social/@msoucy/99825585254720557" >}}

Pictures can be attached, as well, and any particular instance can have their own nonstandard "emoji" that get displayed.
Naturally, topics (or for all those darn kids, "hashtags") also exist, and can be created with familiar `#topic` syntax.

One of the most interesting features, however, is that there are four modes for tooting:

- Public: Post to public timelines
- Unlisted: Do not post to public timelines
- Followers-only: Post to followers only
- Direct: Post to mentioned users only

This is nice, when combined with the fact that there's an option to lock down your account such that you have to approve new followers, and gives a nice level of control.

Suggested follows
-----------------

So far, I've found a few accounts that I follow that I'd like to shout out to:

- [Gargron](https://mastodon.social/@Gargron), the Mastodon lead developer
- [FSF](https://status.fsf.org/fsf), the Free Software Foundation
- [cwebber](https://octodon.social/@cwebber), a developer for ActivityPub, a technology used by Mastodon
- [rowletbot](https://mastodon.social/@rowletbot), a cute and open source Pokemon character bot that brightens your day

Conclusion
==========

Feel free to reach out and [follow me](https://mastodon.social/@msoucy), I might follow back.
I'm highly excited about a social platform with such levels of discoverability and freedom, especially one that's as robust as what I've experienced.

[Signal]: https://www.signal.org/
[Facebook Container]: https://addons.mozilla.org/en-US/firefox/addon/facebook-container/
[Mastodon]: https://joinmastodon.org/
[Mastodon source]: https://github.com/tootsuite/mastodon
