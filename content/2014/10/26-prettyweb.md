---
Title: Hack 1: PrettyWeb concept
Category: code
Tags: advfoss
---

For Hack 1 for the Advanced FOSS class, I decided to go with the first of [my ideas]. I did the bulk of that work at [Hack Upstate], but never really posted about it.

The project came to be known as PrettyWeb. The basic idea is that there are tons of files on the web that are "plain text", and it would be awesome if there were a way to view those files more conveniently. I ended up creating a Firefox plugin that relied on [CommonMark], from the [CommonMark] project. (CommonMark was formerly known as Standard Markdown, or `stmd`, but there were some issues with the name)

PrettyWeb is meant to be a way to view any page that appears as "plaintext" using Markdown. To avoid issues where things were being parsed at inopportune moments, it has an optional button one can add that allows a quick enable/disable.

Tonight I took a look at the existing code, and attempted to get it up to date with the new organization for CommonMark. This week I'll be packaging it up and attempting to publish it on Mozilla's [addon directory]

[my ideas]: {filename}/2014/09/29-advfoss-hack1.md
[Hack Upstate]: {filename}/2014/10/09-hack-upstate-fall-2014.md
[CommonMark]: http://commonmark.org/
[addon directory]: https://addons.mozilla.org/en-US/firefox/
