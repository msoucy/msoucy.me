---
Title: ADVFOSS Hack Proposal 2
Category: code
Tags: advfoss
---

For Hack 2 of the [ADVFOSS] course, we should have two project proposals again.

# libfabd

- **Goal**: D bindings for [libfab]
- **Libraries**: [libfab] itself
- **Distribution**: [dub]

[libfab] is an attempt at rewriting [Fabulous] in C, with the intent of writing Python bindings for it. This project would be "work with the [libfab] developers to create a better API"

# PrePresent

- **Goal**: A tool that pulls your code samples into your presentation
- **Libraries**: Some kind of Python Markdown parser, probably
- **Distribution**: [PyPI]

Create a tool that acts as a preprocessor for Markdown-based presentations, that pulls in code samples from external files. This allows instructors to generate presentations with up-to-date instances of the sample code.

[ADVFOSS]: http://advfoss-ritigm.rhcloud.com/
[libfab]: https://github.com/rossdylan/libfab
[dub]: http://code.dlang.org
[Fabulous]: https://github.com/gcollazo/Fabulous
[PyPI]: https://pypi.python.org/pypi
