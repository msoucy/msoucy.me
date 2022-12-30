---
Title: RepBot - A lesson in refactoring
Date: 2014-02-05 18:10
Category: code
---

For the last two years, I have been slowly developing an IRC bot to track a recurring joke.

In many Algol-based languages, `x++` is shorthand for `x += 1`, which is shorthand for `x = x + 1`. Within several of the groups I'm a part of, we use `name++` to mean "*name* did something awesome/cool/worthy of praise/approval", a general "positive reputation" mark. We also use `name--` for the opposite kind of events.

In the #rit-foss channel, there is a bot that (among other things) keeps track of "karma". As a joke, I started writing my own bot to do that for another channel. It grew rather haphazardly:

  -	 A script to run it as my IRC user, a plugin for my client
  -	 A separate bot, one large file
  -	 A separate bot, separating (somewhat) the reputation storage from the IRC system 

Needless to say, these have had some rough growth. The next step is a planned near-rewrite, which involves breaking out most of the features into separate subsystems. The goal is to build an app that can handle I/O from multiple sources, and using any number of different backends.

At the core of the program is the main bot system.
This handles the main logic of "convert an incoming string into an internal format", which it then passes to any backend that had been plugged in.
I/O is now handled by a set of classes that pulls from some source and has a common interface for output.

This project is one that I'm working on for CSH now - the refactoring and adapting is something that I don't quite have experience with.
Another thing that I'll be (hopefully) adding is support for a proper database, as opposed to a YAML file. This refactor (almost a rewrite) should make it extremely simple to add support like this, as easy as "extend the Backend class"

My code can be found [on GitHub][RepBot], where people can play with the code, check it out, offer enhancements, etc

[RepBot]: http://github.com/msoucy/RepBot
