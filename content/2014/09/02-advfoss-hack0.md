Title: Advanced FOSS: Hack 0
Category: code
Tags: advfoss
Parts: RESTZZZ

# Hack 1: ZTTP

ZTTP is designed to be a [0mq]-to-HTTP bridge. The idea is that it would provide a way to push data to a server over 0mq to stream out to clients via HTTP.

It relies on zmq and http.server libraries, possibly others depending on storage plans.

It will be uploaded to [pypi], and is meant to be simple enough to run on a Raspberry Pi. The anticipated license will be BSD 3-clause.

My upstream mentor will be [Ryan Brown], a crazy Python hacker who has familiarity with HTTP servers in Python and whom I've worked with in the past.

Milestones:

- Week 1
	- 0mq listener component
	- Basic web server components
- Week 2
	- Listener is connected to server
	- Stores data until it's read
	- Server reads and populates basic templates
- Week 3
	- Testing with basic templates
	- Complete documentation
- Week 4
	- Clean up code
	- Release on PyPi

[0mq]: http://zeromq.org
[pypi]: http://pypi.python.org
[Ryan Brown]: http://rsb.io
