---
Title: I broke tmux
Category: code
Date: "2014-03-19"
---

Normally I like making things, but on occasion I've been known to break them.

Today it was [tmux].

As it turns out, some updates change the protocol. When this happens, the updated application can't connect to sessions on the old protocol.

Luckily, there's an easy fix, at least in Linux:

	:::sh
	/proc/$(pgrep tmux)/exe kill-server

Hope you didn't have anything important there! If you did, you can use:

	:::sh
	/proc/$(pgrep tmux)/exe attach
	# Manually kill the required programs, cleanup, etc

[tmux]: http://tmux.sourceforge.net/
