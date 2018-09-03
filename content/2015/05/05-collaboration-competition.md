---
Title: Collaboration/Competition in FOSS
Category: code
Tags: bizlegfoss, foss, linux-dev
---

Open source communities are interesting.

Over the last few years, I've been maintaining a project called [dproto][]. The main idea of the project is that it acts like Google's [protoc][], but for the [D programming language][dlang]. Because of either masochism or a desire to learn, it started as a derivative work of [Square's protoparser][square] in Java, but rapidly spun into its own tool, using more of D's features. The biggest difference, though, is that dproto is essentially a compiler-as-a-library - the main code generation just generates a string, and the entire parser is designed to be run at compile time. This means that creating `dprotoc`, the D version of `protoc`, was really just "parse arguments then call the main library parse function", and the structures can be generated at compile time (fairly quickly) with no additional overhead or effort.

Near the beginning of this year, I pushed a [new release][v1.2.0], and I was surprised when I suddenly started getting bug reports and a lot of discussion - it turns out that the new version, coinciding with the new compiler version, brought some existing bugs to light. I admit to being startled when I discovered that [I was the upstream][downstream] that people were waiting for fixes from.

On a completely different discussion in the [D subreddit][], there was a person who was asking about projects that they might be able to look at and help with. I posted a comment in response to someone else's, mentioning that dproto would love to have more people working on it, and was surprised when I got a private message from one of the [painlessjson][] developers, talking about potential collaboration - looking at each others' projects, increasing visibility for both and helping each other out. One critique that was brought up, that I completely agree with, is a lack of documentation and unit tests.

For me, this is huge. [dproto][] and [painlessjson][] are both in the same field, but do different things - [painlessjson][] uses User Defined Attributes to wrap around existing structures and create JSON serialization, while [dproto][] creates new structures based on other data.
After taking a look at it, I have some ideas about how to do some future enhancements, and how to use [painlessjson][] to handle the proto3-defined JSON definition.
Even though both are serialization systems, they follow different formats (well, sort of), and can most likely play nicely together within the same structures - dproto-generated structures can even use painlessjson tags to avoid doing extra work.
Under many situations, two similar libraries would be competing for the same market - but in an open source environment, the two can not only coexist, but be mutually beneficial. This would be an example of *mutualism* in the biology field. (I definitely studied for Biology while I was sick, I swear.)

Collaboration or competition? In an open environment, collaboration is key - even two libraries with similar goals can benefit and learn from each other.

[dproto]: http://github.com/msoucy/dproto
[protoc]: https://github.com/google/protobuf
[dlang]: http://dlang.org
[square]: https://github.com/square/protoparser
[v1.2.0]: https://github.com/msoucy/dproto/releases/tag/v1.2.0
[downstream]: https://github.com/denizzzka/dianna2/issues/21
[D subreddit]: http://www.reddit.com/r/d_language
[painlessjson]: https://github.com/BlackEdder/painlessjson
