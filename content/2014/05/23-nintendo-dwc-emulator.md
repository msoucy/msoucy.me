Title: Pull Request: Nintendo DWC Emulator
Category: code
Tags: hfoss,foss,python

I've found that I enjoy cleaning up code - specifically, code that was written for a language it clearly isn't being programmed in.
The classic example happened when I was grading CS1 assignments in Python - the people who had come from a Java-based background were a bit clueless about the way certain things worked, and so would often reimplement things that are built in to the syntax or libraries.

A recent [Ars Technica post][Ars post] mentioned that some developers were reverse-engineering the servers used to play Nintendo DS games over wifi, since Nintendo shut down the servers.
After looking at [the code], I started getting flashbacks to my grading days.

Instead of Java style, I found something more startling - C style. Using indices to byte strings everywhere, declaring variables manually...I knew something had to be done.

So I filed a [pull request]. It ended up being both "larger than I thought" and "not large enough".
Unfortunately, trying to do too much while the project is under active development on the mainline causes merge problems, so this [pull request] is the first of what may be many.


[Ars post]: http://arstechnica.com/gaming/2014/05/hackers-return-some-online-gameplay-to-wii-ds-following-nintendo-shutdown/
[the code]: http://github.com/polaris-/dwc_network_server_emulator
[pull request]: https://github.com/polaris-/dwc_network_server_emulator/pull/16
