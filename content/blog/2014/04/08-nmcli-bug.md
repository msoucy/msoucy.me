---
Title: Little fixes add up - nmcli
Category: code
Date: "2014-04-08"
Tags:
- hfoss
---

Sometimes you have to seek out opportunities, and sometimes they fall into your lap.

A while ago, I made the switch to [Awesome WM] instead of [Cinnamon], due to some crashing issues. (Certain X11 features, like adjusting the backlight, using xscreensaver, opening a terminal in cinnamon, caused the entire computer to hang.) Those issues turned out to be due to a kernel bug, but now I'm too used to Awesome to switch back to Cinnamon for any of the most dire needs (like incredibly-easy control over a window's size, for testing things that need to resize gracefully).

Shortly after that, I decided to reinstall Fedora entirely. Used to Awesome, I decided to go for a minimal install, just Awesome and the basics. This had some interesting side effects, such as getting lightdm instead of gdm for the desktop manager. More interesting, though is that Awesome is rather minimal in regards to default settings - there's no built-in applet for networking, like in Gnome/Cinnamon.

Enter `nmcli`.

This wonderful little tool is a relatively convenient way to interface with NetworkManager without a GUI - it's literally the Network Manager CLI. I was using it to change some DNS settings yesterday, and all of a sudden I encountered a little something:

> Connection 'rit' (...) sucessfully saved

Something in that line caught my eye.

They were un`success`ful in their `success` message. Is that a good hint?

I looked up where the source was located, jumped on IRC to ask about submitting a patch, and then dove into the code - a quick `grep -r 'sucess' .` was enough to point out what I needed - the bulk of the code had already been fixed, but there were a few spots where the string hadn't been updated.

GNU `gettext` is a utility that allows for localization. Basically, you give it a `msgid`, and in each language's file, you use `msgid`-`msgstr` pairs to say "This string looks like this in this language". This relies on the `msgid` being identical in each part of the code. When "sucess" didn't become "success" in all cases, it could potentially cause problems with certain localizations.

[The patch] is available here - it's small, but still exciting to me!

[Awesome WM]: http://awesome.naquadah.org/wiki/Main_Page
[Cinnamon]: http://cinnamon.linuxmint.com
[The patch]: http://cgit.freedesktop.org/NetworkManager/NetworkManager/commit/?id=3c211760c564233571da6381caa7f727b79bab14
