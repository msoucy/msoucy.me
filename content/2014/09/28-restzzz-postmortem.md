Title: RESTZZZ Final Thoughts
Category: code
Tags: advfoss

Since my [previous][RESTZZZ Proposal] [posts][RESTZZZ Update], I've made enough progress with `RESTZZZ` that I've been able to [release] something that I consider a working demo. `RESTZZZ` started as a project with not quite clearly-defined goals, just the objective of creating a more convenient way to access 0mq messages.

The code is still at the same [repository], and released [here][release].

One of the big questions that was asked frequently was "why?" What was the motivating concept that inspired me to make the project?

The original motivation was rather weak - a way to forward important messages received via [Weechat] using the 0mq plugin. This would allow me to read the messages without a full IRC client. Unfortunately, this idea had a rather large problem in that if Weechat were sending messages, then I already had the client open.

Another reason that I thought of came up when my friend [Ross] presented his project idea - originally, he planned on setting up a set of Raspberry Pis to share sensor information in an area. He mentioned potentially having the nodes communicate over 0mq, which my system could listen in on. Unfortunately, his project fell through, but it would theoretically have integrated easily.

I wrote a simple chat program a few years ago, as a way to test my [D bindings] for 0mq. `RESTZZZ` could also easily integrate with that.

There is no easily accessible list of tools using 0mq, but I tried to make the tool as simple to use as possible.

[RESTZZZ Proposal]: |filename|/2014/09/02-advfoss-hack0.md
[RESTZZZ Update]: |filename|/2014/09/16-restzzz-update.md
[release]: https://pypi.python.org/pypi/restzzz
[repository]: http://code.msoucy.me/RESTZZZ
[Weechat]: http://weechat.org
[Ross]: http://blog.helixoide.com/
[D bindings]: https://github.com/msoucy/dzmq
