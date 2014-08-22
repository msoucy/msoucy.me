Title: Playing with Portable Linux
Category: code

The other day, I came to a realization: I have too many flash drives.
Because of modern network speeds, I hardly have a use for most of them now, and the most use that they've gotten is passing around installers and wifi keys to a set of computers.

Obviously, the only thing to do is put Linux on it.

Since I wanted to try something different, I went with a Slackware-based distribution called Porteus (a fork of Slax). Out of the box, it handled wireless perfectly on the computers I tried it on, and was extremely lightweight - so much so that I've had no problems with grabbing any packages (called modules) that I want.

Modules are made in several different ways:

- Convert a Slackware package
- Convert an rpm or deb
- Create a module from a folder or tarball
- Download from `usm`, which uses slackware and slackware-related repositories and converts the packages

Modules are "installed" simply by using `activate`, which mounts the package. That means no copying, and no slowdown. Though the `deactivate` conflicts with that of `virtualenv`.

Overall, it's an interesting tool, and one that's nice and easy to use for situations when I want to work in my own environment but only have other peoples' computers.
