#!/usr/bin/env python

"""
Snippet markdown filter
========================

- Copyright (c) 2018 Matt Soucy

## Format

```
{{< tagname "data" >}}
```
"""

import markdown


class SnippetExtension(markdown.Extension):
    """ Snippet Extension for Python-Markdown. """

    def __init__(self, configs):
        """
        Create an instance of the Snippet extension

        Keyword arguments:
        * configs: A dict of configuration settings passed in by the user.
        """
        # Set extension defaults
        self.config = {
            'handlers': [{}, 'Handler callbacks']
        }
        # Override defaults with user settings
        self.setConfigs(configs)

    def add_inline(self, md, name, pattern_class, pattern):
        """
        Add new functionality to the Markdown instance.

        Keyword arguments:
        * md: The Markdown instance.
        * md_globals: markdown's global variables.
        """
        objPattern = pattern_class(pattern, self.config)
        objPattern.md = md
        objPattern.ext = self
        md.inlinePatterns.add(name, objPattern, "<reference")

    def extendMarkdown(self, md, md_globals):
        prefix = r'\{\{<\s*'
        tag = '((?:[a-z][a-z]+))'
        space = r'\s+'
        text = '(".*?")'
        suffix = r'\s*>\}\}'
        fullRe = prefix + tag + space + text + suffix
        self.add_inline(md, "mastodon", BasicSnippetPattern, fullRe)


class BasicSnippetPattern(markdown.inlinepatterns.Pattern):
    def __init__(self, pattern, config):
        self.pattern = pattern
        self.config = config
        super(BasicSnippetPattern, self).__init__(pattern)

    def handleMatch(self, match):

        if match:
            # Group 1 is "everything before this"
            tag = str(match.group(2))
            # Remove the quotes
            text = str(match.group(3))[1:-1]

            handlerList = self.config['handlers'][0]
            func = handlerList.get(tag, lambda id: id)

            return func(text)
        else:
            return ""


def makeExtension(*args, **kwargs):
    return SnippetExtension(*args, **kwargs)


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
    print("-" * 8)
    md = markdown.Markdown(extensions=['snippet'])
    print(md.convert(__doc__))

