Title: RESTZZZ Status Update
Category: code
Tags: advfoss
Series: RESTZZZ

Although it's been a couple of weeks, I have a bit of a status update on the [project] from before.

First of all, I decided to rename the project from ZHTTP (which, to me, implies HTTP over ZMQ, which is already something with existing implementations) to RESTZZZ. This was done to reflect what the project is actually doing more closely: not strictly HTTP itself, but creating a RESTful API for 0mq transports.

The basic idea behind RESTful APIs is that you use the existing HTTP actions to alter some sort of server-wide state:

- `GET` is used for retrieving data
- `POST` is used for creating new resources (mostly)
- `PUT` is used for updating existing resources (mostly)
- `DELETE` removes a resource

For RESTZZZ, I decided that only `GET` and `POST` were actually relevant - `GET` will ask the given socket to retrieve the next message, and `POST` will publish a message on the given socket. Sockets are mapped to connections via a configuration file.

Thanks to my mentor, I was made aware of some existing Python libraries that vastly simplified my code. [Cornice] is a REST framework for [Pyramid] that makes the code LOOK like the API itself. It removed the need for me to have to parse out the HTTP headers. As someone who is used to using just the standard library for a language, and as few other libraries as possible, I hadn't even thought of it.

Currently, RESTZZZ is somewhat functional - it can load from a configuration file, connect each socket to a given endpoint, subscribe properly, and respond to REST calls with appropriate responses. When responding to a GET, it returns a JSON object that contains the data. This isn't perfect, but since it's impossible to fully map the two protocols perfectly, this is a fairly close and simple solution.

Things that I still need to do include allowing one socket to support connecting to multiple endpoints, for aggregating data sources easily.

[project]: {filename}/2014/09/02-advfoss-hack0.md
[source]: http://code.msoucy.me/RESTZZZ
[Cornice]: http://cornice.readthedocs.org/en/latest/
[Pyramid]: http://www.pylonsproject.org/
