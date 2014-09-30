Title: ADVFOSS Hack Proposal 1
Category: code
Tags: advfoss

For Hack 1 of the [ADVFOSS] course, we need to have two different proposals. Both of mine are relatively simple ideas based on "replacing/enhancing web technology"

# Proposal 1

- **Name**: MarkItUp
- **Goal**: Create a plugin for FireFox that renders Markdown as HTML
- **Libraries**: stmd.js from [CommonMark]
- **Distribution**: the Firefox Addons site

The idea is that the addon would take any page sent using any of the MIME types `text/x-markdown`, `text/markdown`, `text/vnd.daringfireball.markdown`, or `text/plain`, and attempt to parse it to produce HTML that the browser user sees. (In the case of `text/plain`, if rendering fails just show HTML)

# Proposal 2

- **Name**: BaaS - Buzzer as a Service
- **Goal**: Create a tool that allows people to queue up "emotions", such as annoyance, disgust, amusement, praise, etc. on a Raspberry Pi, and have the Pi display an image showing the overall mood of the room, with appropriate noises (buzzer noise for shock or disgust, for instance)
- ** Libraries**: Some library that allows for media playing and graphics drawing. Can probably be written in Python.
- Distribution: [PyPI]

[ADVFOSS]: http://advfoss-ritigm.rhcloud.com/
[CommonMark]: http://commonmark.org/
[PyPI]: https://pypi.python.org/
