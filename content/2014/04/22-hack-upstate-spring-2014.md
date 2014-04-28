Title: Hack Upstate: Spring 2014
Category: code
Tags: hackathons, hfoss

A couple of weeks ago, I attended yet another [Hack][] [Upstate][]. I already [posted about some of my experiences][Go Rant], and [Derek posted about our experience][Derek's Post], so I figured that I should do the same.

Our project was known as [Bootleg][], but until a late-night halfhearted name change, it was known as "MovieNet". The idea was that it would serve as a replacement for [plex.tv][], a pretty good utility that allows people to stream their media to other computers/tablets/etc. Though Derek mentioned a bit about what he did, my work was of a vastly different nature.

A proper media server needs to have a way to list all available media files - for our purposes, we assumed that the user would have no extraneous files.
My job was to create a system in Go to do the following:

- Create an initial list of files on the filesystem
- Watch for new or removed files
- Send information about the "library" along a socket

I encountered a few difficulties, but overall the hard part was just getting used to the language. With more time, it could have been perfectly functional and I could have started cleaning it up.

- The initial list was done with a manual traversal, which was slightly tedious but a good learning experience.
- We used the excellent [fsnotify][] library to detect changes in the filesystem - we only needed to detect adds and removes, as we felt that "attribute/modification" wasn't particularly useful for our purposes. A "move" was just an "add" at one place and a "remove" at the other.
- Sending information depended on a JSON hierarchy that we agreed on. The language has built-in support for JSON encoding, so that part was as simple as sending it along the socket.

My adventure was substantially simpler than Derek's or Rob's, but I feel that if we hadn't lost time that we needed to drive back, we could have had a decent presentable project.

Of course, the project isn't the sole reason to go to a hackathon.

I met up with some hackers I had talked with at previous Hack Upstates, and we spent a while just catching up and talking about life. It's always good to hear another person's perspective on your situations, and exchange stories. Several of the other hackers remembered me from the first two hackathons, which was cool for me because it meant that my work was starting to get noticed by people.

Overall, the hackathon was a ton of fun. Hack Upstate has always been one of my favorite hackathons, not just because of the change of scenery but also because of the connections made with others. I personally feel that all young developers should go to at least one hackathon before they graduate, both for the networking opportunities it allows and for the "real-world" experience.

[Hack]: |filename|/2013/10/17-hack-upstate-part-1.md
[Upstate]: |filename|/2013/10/30-hack-upstate-part-2.md
[Go Rant]: |filename|/2014/04/05-playing-with-golang.md "Golang Rant"
[Derek's Post]: http://blog.gonyeo.com/hfoss-hack-upstate.html
[Bootleg]: https://github.com/robgssp/movienet "Bootleg"
[plex.tv]: http://plex.tv
[fsnotify]: https://github.com/howeyc/fsnotify
