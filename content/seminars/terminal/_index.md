+++
title = "Intro to Bash and Vim"
author = "Matt Soucy"
outputs = ["Reveal"]
+++

---

# History of the Command Line

- Back in the good old days people used text interfaces to use computers
- In the late 70s to the early 80s, people invented graphical user interfaces
- Ever since then modern computers have gotten consistently more annoying to use
- With a simple command line interface, developers can focus on the
  functionality of their programs, instead of the gradient on their buttons.
- Closer to the "data flow" style of thought

---

# Operating System

You want to use Linux for this.

If that's not an option, Mac OS X can do.

If you want to follow along, (HIGHLY recommended),
you can use <http://koding.com> or <http://freeshell.net/>
to get a small VM to work on.

---

# Open a terminal

Open a terminal. Hooray you have a prompt!
Most of the time, the default shell you will use is `bash`.

> A shell is your command line.
  It's a program used to interact with your computer via a text interface.

---

# Location, Location, Location

When you're using bash, you're always at a place in your filesystem.
It defaults to your home folder.
This is the `~` you see.
When you change the directory you're in, the `~` will be replaced with where you are.

> `~` always means "the current user's home directory".
  `~foo` means "the user `foo`'s home directory"

---

# Basic commands

Let's interact with some files!

- `ls` will list all the files for you in the folder you're in
- `cd Pictures` will change directories into the Pictures folder in the current
  folder. Now `ls` will show you different files!
- `mv file1 file2` will move file1 into file2. This can be used to change where
  something is, or rename a file. This will overwrite whatever file2 was.
- `cp file1 file2` will copy file1 to file2. This will also overwrite file2.

---

# Shortcuts

As I alluded to earlier, `~` is your home folder. `cd ~` (or just `cd`) will
change your current directory to your home folder, no matter where you are.

`/` is the root of your computer. It's the highest level directory, like `C:` in
Windows land except without the dumb drive letter.

> Why no drive letters? Because on \*nix systems, you can `mount` drives
  anywhere! This is useful when you want to treat another drive/partition
  as if it were part of the existing filesystem.

`.` refers to the current directory you are in.

`..` refers to the parent of the directory you're in. For example, `cd ..` will
go up one level.

---

# Hidden files

On Linux, to hide a file you simply make its name start with a period. That
way, it doesn't show up in `ls`. If you want to see hidden files, use `ls -a`.

> This is actually a case of "accidental bug that became awesome feature"

---

# I forget. How do I ...?

If you forget or don't know the particulars of using a command, just type in
`man command` and it'll pull up the manual page for that command. For example,
take a look at `man mv`

---

# My computer's boring, let's go somewhere else!

`ssh` is a cool tool. It lets you open a shell on a different computer. With it
you can interact with files the exact same way you would on your local computer.

`ssh` stands for *S*ecure *SH*ell.

---

# Machines to try:

Run the command `ssh username@hostname` and enter in your password.

- `shell.csh.rit.edu` is the user machine for CSH, so it's a place where all of
  our members can go and do things.
- `glados.cs.rit.edu` is a CS department machine. Everyone chooses this one at
  first, so it can be quite slow at times
- `gibson.rit.edu` is an outdated Solaris machine, still somewhat usable)
- With a bit of setup, you can connect to your Koding machine as well

---

# Look around

Now `ls` and `cd` around. You're on a different computer! You can interact with
that machine now just as if you were over in the server room with a keyboard
and monitor.

---

# Let's do real things

---

# Find a file

Let's say you want to find the file `tits.jpg`. It's somewhere under your home
directory, but you don't know where. Go to the folder you want to search in, and
type the command `find . -name tits.jpg`

---

# Downloading

Want to download a file to your current directory?

`wget http://pornhub.com/tits.avi`

---

# Copying files between computers

Have a file on your computer you want on rancor?

`scp localfile username@rancor.csh.rit.edu:`

Have a file on rancor you want on your local computer?

`scp username@rancor.csh.rit.edu:remotefile .`

Note: when copying to a remote machine, that `:` at the end is _necessary_!

---

# Editing text files

If you don't know how to use a real editor, for now you can use `nano filename`.
That'll give you a basic editor you can move around in with the arrow keys and
type in.

---

# Web space

CSH offers free web hosting for our members.
Just put files in `~/.html_pages` or `~public_html` on `filer.csh.rit.edu`.
If it's in `.html_pages`, it'll only be accessible by members, and if it's in
`public_html` it'll be available to everyone.

---

# tmux

tmux is a program that "enables a number of terminals to be created, accessed,
and controlled from a single screen." To see what I mean, run the command `tmux`
on rancor, and do some things. Then press `Ctrl`+`b` and then `d`. You're back
outside of tmux now. You can do whatever, log out and back in even, and when you
type in `tmux attach` you'll be dropped back into tmux with the session the same
way you left it.

---

# Gaming

One of the best games ever created is nethack, and we have our own fork of it.
To play, run the command `telnet nethack.csh.rit.edu`. I'm sure there'll be a
seminar on nethack eventually if you want details on how to play, or talk to me
whenever.

---

# Movies

You can also watch a full movie from the terminal! Just type in `telnet
towel.blinkenlights.nl`

---

# Permissions

---

# File permissions

There are three permissions flags for files, one for reading, one for writing,
and one for executing. You can set each of these flags for three different
groups: the owner, the owner's group, and everyone. If you type in `ls -l`, the
first column shows the permissions on each file.

---

# Understanding permissions

Often the default permissions are fine, but if you want to prevent other people
on rancor from reading your super secret love letters you keep there, I'll show
you how to change them.

You have three sets of three boolean flags. Imagine each flag being represented
with a binary number, 0 is not set and 1 is set. If we had the permissions read
and write but not execute, that would be 110.

So the permissions for a file that everyone can read and write to, but no one
can execute, would be 110 110 110. If you convert the binary numbers to decimal,
it would be 666. This 3 digit binary (octal, actually) number is what's used
when setting permissions.

It can also sometimes be shown as a longer string, like so:

> -rw-rw-rw- == 666
>
> -rwx-rx-rx == 755

---

# Setting permissions

Let's say we have the file tits.avi (remember we downloaded it?), and we want to
give everyone permission to both read from and write to the file, but not
execute the file. The command would be:

`chmod 666 tits.avi`

chmod stands for change mode, or change file mode bits.

---

# Useful permission values:

 - 777: everyone can do everything
 - 700: only you can read, write, or execute the file
 - 755: you can do anything with file, others can read and execute
 - 600: only you can read or write to the file
 - 644: you can read or write to the file, others can read the file

The execute flag means you can run the file as if it's a program, or `cd` into
the directory if it's a directory.

---

# root

On every Linux system, there's a root account. This account has the power to do
whatever it wants. Permissions settings won't keep it out, it can mess with
anyone's files, and has access to everything. This account is often used to
install software, and manage system services. Many distributions are set up to
allow you to run a command as this user with the `sudo` command.

---

# Redirection

---

# Pipes

In Linux when a program goes to print something to the screen, you can instead
send its output directly into another program. This is useful for filtering out
long lists, logging the results of a program, and for many other things.

In Linux, we can connect programs together with the `|` symbol.

---

# `grep`

`curl` is just like the `wget` command we saw earlier, except it prints out what
it downloads instead of saving it into a file. So let's try `curl -s
http://www.pornhub.com/`. That's a lot of text. I wonder if they use jquery...

`curl -s http://www.pornhub.com/ | grep jquery`

---

# `>`

How about if you want to send a program's output to a file? The `>` symbol will
write whatever it gets into a file. So to emulate what wget does:

`curl -s http://www.pornhub.com/ > pornhub.html`

---

# `>>`

The `>` symbol will delete whatever was previously in the file it's writing to.
If you want to instead append to a file, use `>>`.

---

# stderr

When a program prints to the screen, it can do so via stdout or stderr. The pipe
and redirects I've shown you will grab stdout, and ignore stderr. If you want to
grab just stderr, or both, or send stderr to stdout, or other fanciness, I'll
leave that for you guys to look up on your own.


---

# Let's talk vim

---

# What is vim?

---

# What would I use vim for?

---

# Let's write something

- Open vim
    - `vim testfile.txt`
- Go into insert mode
    - When you first open vim if you try to type something, things aren't going to go your way. To be able to type stuff, press `i`.
- Type some stuff
- Leave insert mode
    - Press `Esc` to go back to the normal mode.

---

# Normal Mode

## Moving the cursor

```
      k
    h   l
      j
```

Move the cursor with the `h`, `j`, `k`, and `l` keys. This keeps your fingers in
the center of the keyboard, and means you can work more comfortably and faster.

> These movements are also used in nethack

---

# Normal Mode (Movement)

There are many more movements, including:

- **b**eginning of word
- **e**nd of word
- next **w**ord
- Beginning of line **^**
- End of line **$**
- **t@**, un**t**il whatever character you type instead of **@**

---

# Normal Mode

## Delete (cut) a line

Want to delete a line? That's done with the **d** key. Move your cursor to a line
you don't want anymore, and press `dd`.

## Put (paste) a line

Let's put that line you just deleted somewhere else. Put the cursor somewhere,
and press `p`.

## Yank (copy) a line

Want to duplicate a line? Press `yy` on a line to yank it, and then you can
press `p` wherever you want to put it there.

---

# Normal Mode

## Doing things more than once

You can do things multiple times. Want to move the cursor in a direction 10
times? Type in `10` and then hit one of the movement keys.

## Why `dd` instead of just `d`?

The first `d` means "delete", the second `d` means "this line". You can give it
other commands, for example `d5j` will delete the current line and 5 lines below
it. This also applies to yanking.

---

# Vim is a language

You know the following:

- Movements (`$` goes to end of line, `w` goes to the next word)
- Actions (`d` deletes the result of a movement)

So, if I say that `dw` deletes one word, what does `d$` do?
What about `yw`?

---

# Visual Mode

## Select some text

Counting how many lines or characters you want to delete can be a pain, so I'm
going to show you visual mode. Press `v`, and then move the cursor. You can
highlight text like this, and pressing `d` or `y` will delete or yank
specifically the text you have highlighted.

## Select some lines

Press `V` to go in to Visual Line mode. This means you select lines at
a time, instead of characters.

---

# Searching

## Search forward

Press `/` and then enter in your search query. When you press enter, you'll be
taken to the next occurrence of the search. You can press `n` to go to the next
occurrence, or `N` to go to the previous, and keep going until you find what you
want.

## Search backwards

Same thing as searching forwards, just use `?` instead of `/`.

## Searches are regexes

Your search queries are regular expressions. If you know how to use them, it's a
powerful feature. If you don't you can mostly ignore them (or learn them!), but
be aware you may not get what you want if you start throwing non-alphanumeric
characters into your searches.

---

# Search and replace

## In visual mode

Let's say you have some variable named `foo`, and you want to rename it to
`bar`. The easiest way to do this is a search and replace. Enter visual mode and
select some text, and then type in `:s/foo/bar` and hit `Enter`.

## Globally

Let's say you want to do this on an entire file. Selecting all the lines in
visual mode would be silly, so you can do this: `:%s/foo/bar`

## Tips and tricks

- The first part here is still a regular expression
- It'll only replace the first occurrence it finds on each line. To replace
  more, add `/g` on to the end of it
- The `/` character can actually be anything. You just need to escape that
  character in your searches and replaces.

---

# `:`

## Commands

The `:` character allows you to type in a command to vim. We used it in the last
section for searching and replacing

## Getting help

Don't know what a key does? Type in `:help z` where z is whatever key you're
curious about. The documentation is pretty good, and there's help for just about
anything.

---

# Write and Quit

## Save the file

Don't use `Ctrl` + `s`. Either nothing will happen, or your terminal will freeze
(`Ctrl` + `q` unfreezes). To save the file, type in `:w` and hit `Enter`. You'll
see something like `"testfile.txt" 153L, 4187C written` appear at the bottom of
the screen.

## Quit vim

I don't know why you'd ever do this, but you can enter in `:q` and hit `Enter`
ton quit vim. For added convenience, `:x` will save the file and exit. If you
want to quit vim without saving the file, use `:q!`

---

# Do something globally

You can do a lot of things on an entire file (again, like in the last section)
by typing in `:%` and then the command.

Want to delete an entire file? `:%d`

Want to yank an entire file? `:%y`

---

# How to get better

- Just start using it!
- Run the command `vimtutor` on rancor
- Google is your friend
- Look up some random help page in vim

---

# Advanced usage

## Visual block select

`^v`

- `dyp` are all kinda nifty in it
- `I` will insert some string before the block on every line

---

# vimrc

You can (and should) customize vim.

Put settings in a text file called `~/.vim/vimrc`.
If you want to see what some CSHers have:

- [msoucy](https://github.com/msoucy/dotfiles/blob/master/vim/.vim/vimrc).
- [dgonyeo](https://github.com/dgonyeo/dotfiles/blob/master/.vimrc).
- [vim-sensible](https://github.com/tpope/vim-sensible)
    - Distributed as a plugin, but can copy the file as a base for your `vimrc`

You definitely don't need something as lengthy as these to get started.

---

# Plugins

Vim doesn't do something you want or doesn't behave how you like? There's a
bunch of plugins, and even plugins for managing your plugins.

---

# Macros

Want to do some combinations of key 500000 times? Read up on how to use macros.

---

# Random useful key bindings

- `I` == enter insert mode at the beginning of the line
- `A` == enter insert mode at the end of the line
- `o` means make a new line below the current and put the cursor there in input
  mode
- `s` in visual mode will delete the text you have selected and put you in
  insert mode
- `w` and `e` will jump to the next word (they jump to different locations)
- `b` will jump back a word
- `:` + a number will move the cursor to that line number
- `G` will go to the bottom of the file. `gg` will go to the top.

---

# Multiple files

You can edit multiple files at the same time.

## Window splits

You can view multiple parts of a file at the same time, or have multiple files
on the screen at the same time.

> Note that in vim, and many other tools, `Ctrl+w` is written `^w`

- `^w` and then `s` or `v` will split the screen
- `^w` and then `hjkl` will move between the splits
- `:e` is "edit a file".
  Type in `:e path/to/file` in a split and it'll open the file there.
- `:sp path/to/file` opens a file in a new split

## Tabs

Let me point you to Google.

---

# Edit remote file

If you have ssh access to a machine you can do:

`vim scp://username@machine/path/to/file`

Kudos to Ethan House for showing me this

> This is done with the `netrw` plugin

---

# :q
