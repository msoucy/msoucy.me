+++
title = "Intro to Vim"
author = "Matt Soucy"
outputs = ["Reveal"]
+++

---

# What is vim?

- A text editor
- Based on "modes" (unlike most other editors)
- Part programming language, part Editor

---

# What would I use vim for?

---

# Let's write something

- Open vim
    - `vim testfile.txt`
- Go into insert mode
    - When you first open vim if you try to type something, things aren't going to go your way.
	- To be able to write text, press `i`.
- Type something
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

Move the cursor with the `h`, `j`, `k`, and `l` keys.
This keeps your fingers in the center of the keyboard, and means you can work more comfortably and faster.

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

# Normal Mode (Actions)

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

# Normal Mode (Repeating)

## Doing things more than once

You can do things multiple times.
Want to move the cursor in a direction 10 times?
Type in `10` and then hit one of the movement keys.

## Why `dd` instead of just `d`?

The first `d` means "delete", the second `d` means "this line". You can give it
other commands, for example `d5j` will delete the current line and 5 lines below
it. This also applies to yanking.

---

# Vim is a language

You know the following:

- Movements (`$` goes to end of line, `w` goes to the next word, `_` means "entire line")
- Actions (`d` deletes the result of a movement, `y` yanks text)

So, if I say that `dw` deletes one word, what do the following do?

- `d$`
- `yw`
- `y3y` (or `y3_`)

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

- [msoucy](https://github.com/msoucy/dotfiles/blob/master/files/vim/.vim/vimrc).
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
