Title: Implementing PrettyWeb
Category: code
Tags: advfoss

In the process of implementing [PrettyWeb], I ran into some issues.

The largest being Javascript. I wasn't entirely comfortable with the language, and so my first few drafts of the addon were very rough. I frequently ran into issues where I didn't understand Javascript's syntax - for example, a foreach loop does NOT do what I expected it to. Nor do I have any idea what it DOES do. I also ran into issues where there's no real "cross-platform" Javascript environment, the versions in web browsers are different than rhino, so I couldn't even test anything without creating a web page - I'm used to being able to do everything in the CLI, so this was frustrating for me.

Firefox's addon model was a bit odd at first, because I had to learn entirely new concepts like their [XUL]. I had some help by basing it off of [Cloud-to-Butt], which does something like what I wanted to do - perform some filtering on the existing DOM. The difference between the two, though, is that Cloud-to-Butt works only on DOM "text nodes", while I have more specific requirements - the "text nodes" within a `<pre>` tag directly below the `<body>` tag. This is because Firefox renders plain-text pages inside roughly the following structure:

```html
<html>
 <head>
  <link rel="alternate stylesheet" type="text/css" href="resource://gre-resources/plaintext.css" title="Wrap Long Lines">
 </head>
 <body>
  <pre>
   Contents
  </pre>
 </body>
</html>
```

Because I had the parser (`stmd.js`, which was renamed to `commonmark.js` while I was working on PrettyWeb), and I had the outline, the rest was just putting them together. I ran into problems when submitting to the Firefox Addon website, because CommonMark uses generated Javascript and a format that the Firefox developers don't care for, so I'll be attempting to fix those eventually.

The [code] is available on GitHub.

[PrettyWeb]: {filename}/2014/10/26-prettyweb.md
[XUL]: https://developer.mozilla.org/en-US/docs/Mozilla/Tech/XUL
[Cloud-to-Butt]: https://github.com/Qalthos/cloud-to-butt-mozilla
[code]: https://github.com/msoucy/PrettyWeb "PrettyWeb"
