+++
title = "Berkeley Software Distribution"
author = "Matt Soucy"
outputs = ["Reveal"]
date = "December 2, 2014"
+++

---

# History

| Version   | Released        | System       |
| :-------- | :-------------- | :----------- |
| 1BSD      | March 9, 1978   | PDP-11       |
| 2BSD      | May 1979        | PDP-11       |
| 3BSD      | End of 1979     |              |
| 4BSD      | November 1980   | VAX          |
| 4.1BSD    | June 1981       | VAX etc.     |
| 4.2BSD    | August 1983     | VAX etc.     |
| 4.3BSD    | June 1986       | VAX etc.     |
| 4.4BSD    | June 1994       | VAX etc.     |

- 1BSD was actually an add-on for Version 6 Unix
- 2.9BSD (1983) - first version that was a full OS on its own
- Originally developed by people at Berkeley
	- Derivatives each developed by different organizations

---

# Derivatives

- Dragonfly BSD
- FreeBSD
	- PcBSD
- NetBSD
- OpenBSD

Support a wide variety of architectures (Itanium, x86-64, MIPS, ...)

---

# Time-sharing

- Originally used as an extension of Version 6 Unix
- Once released as its own OS, used for time-sharing systems

---

# Inter-Process Communication and Context Switching

BSD Sockets

> Unix Philosophy: Everything is a file

Opening sockets is different from opening a "real" file

Sockets read/write using the file interface

Process preemption can lead to migrating a thread to another processor

---

# Compatibility layer

Has a compatibility layer that allows it to run UNIX applications

If the application is using the UNIX syscalls, look them up in the compatibility table instead of BSD's

---

# Standardization

Extending - writing a replacement for a subsystem - requires reading the standard, not the code.

---

# Questions
