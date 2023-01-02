---
Title: Extending Pelican with Markdown
categories: [code]
Tags:
- python
Date: "2018-09-03"
---

Recently, I noticed a preview of a blog post. In it, there were some custom embedded macros, that looked like:

```html
{{< mastodon "https://mastodon.social/@msoucy/99825585254720557" >}}
```

These links were becoming expanded to a full Mastodon embed block:

```html
<iframe class="mastodon-embed" src="https://mastodon.social/@msoucy/99825585254720557/embed" style="max-width: 100%; border: 0" width="400"></iframe>
<script async="async" src="https://mastodon.social/embed.js"></script>
```

This syntax turned out to be [Hugo][] syntax called a "shortcode".

Naturally, this seemed like a very handy thing to have on my blog.
I could think of another, similar, use for embedding YouTube videos, with the same syntax.

That's why I started to play with how Pelican parses Markdown.
As it turns out, there's a way to add hooks to the Markdown parser.
Based on a similar project for a [QR code generator][], I came up with a simple extension file called [mdx_snippets][].

Using it, I'm able to embed a snippet using the same syntax.
The actual controller for it is written [in raw python][snippet-masto-driver], and [configuration][] is simple.

It's not a complete implementation of Hugo's shortcodes, but it's enough that I can implement the original motivating factors.

[Hugo]: http://gohugo.io
[QR code generator]: https://github.com/airtonix/python-markdown-qrcode
[mdx_snippets]: https://github.com/msoucy/msoucy.me/blob/d8f22b71aed09f594f4634c69493a52080ebe0a0/mdx_snippets.py
[snippet-masto-driver]: https://github.com/msoucy/msoucy.me/blob/d8f22b71aed09f594f4634c69493a52080ebe0a0/pelicanconf.py#L62-L78
[configuration]: https://github.com/msoucy/msoucy.me/blob/d8f22b71aed09f594f4634c69493a52080ebe0a0/pelicanconf.py#L102
