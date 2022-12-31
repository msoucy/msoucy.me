---
Title: Awesome WM startup fix
categories: [code]
Date: "2014-09-29"
Tags:
- foss
---

I was browsing the [Awesome WM wiki][Awesome wiki] to try to figure out how to autostart some commands on startup. The code at the end of the "Simple way" section seemed simple, but for some reason refused to work. I tried everything I could think of, blaming the `pgrep` command, but nothing seemed to work. Finally, I got frustrated, and forced Awesome to print out the entire command that was being run, then tried shoving that into my terminal.

It failed.

*[Wat].*

Syntax error on `|`.

Then it hit me.

There are many shells that one can use. Some of them, like [FISH], aren't quite `sh`-compatible. Among the features that `FISH` has, it changes `foo || bar` into `foo; or bar`, which is slightly more verbose but cleaner to read (sometimes). The base command uses `||`.

How do you fix this?

Luckily, `sh` has a special flag - `-c`. Calling `sh -c 'foo'` will pass `foo` to `sh`, so that `sh` parses it instead of whatever shell you're using. This means that I can wrap the entire command in `-c` arguments, and it will work fine:

```lua
function run_once(prg,arg_string,pname,screen)
    if not prg then
        do return nil end
    end

    if not pname then
       pname = prg
    end

    if not arg_string then
        awful.util.spawn_with_shell("sh -c 'pgrep -f -u $USER -x \\'" .. pname .. "\\' || (" .. prg .. ")'",screen)
    else
        awful.util.spawn_with_shell("sh -c 'pgrep -f -u $USER -x \\'" .. pname .. " ".. arg_string .."\\' || (" .. prg .. " " .. arg_string .. ")'",screen)
    end
end

```

[Awesome wiki]: http://awesome.naquadah.org/wiki/Autostart#Simple_way
[Wat]: https://www.destroyallsoftware.com/talks/wat
[FISH]: http://fishshell.com/
