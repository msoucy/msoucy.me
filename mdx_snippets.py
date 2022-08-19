#!/usr/bin/env python

"""
Snippet markdown filter
========================

- Copyright (c) 2018 Matt Soucy

## Format

{{< tagname "data" >}}
"""

import markdown


class SnippetExtension(markdown.Extension):
    """ Snippet Extension for Python-Markdown. """

    def __init__(self, **kwargs):
        """
        Create an instance of the Snippet extension

        Keyword arguments:
        * configs: A dict of configuration settings passed in by the user.
        """
        # Set extension defaults
        self.config = {
            'handlers': [{}, "Handler callbacks"]
        }
        # Override defaults with user settings
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        """
        Add new functionality to the Markdown instance.

        Keyword arguments:
        * md: The Markdown instance.
        """
        prefix = r'\{\{<\s*'
        tag = '((?:[a-z][a-z]+))'
        space = r'\s+'
        text = '"(.*?)"'
        suffix = r'\s*>\}\}'
        fullRe = prefix + tag + space + text + suffix
        md.inlinePatterns.register(
            SnippetPattern(fullRe, self.getConfig("handlers", {}), md),
            "snippets", 0)


class SnippetPattern(markdown.inlinepatterns.InlineProcessor):

    def __init__(self, pattern, handlers, md=None):
        self.pattern = pattern
        self.handlers = handlers
        super().__init__(pattern, md)

    def handleMatch(self, match, data):

        tag = str(match.group(1))
        text = str(match.group(2))

        func = self.handlers.get(tag, lambda id: id)

        return func(text), match.start(0), match.end(0)


def makeExtension(*args, **kwargs):
    return SnippetExtension(*args, **kwargs)


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
    print("-" * 8)
    handlers = {"tagname": lambda id: id+id}
    md = markdown.Markdown(extensions=[SnippetExtension(handlers=handlers)])
    print(md.convert(__doc__))

