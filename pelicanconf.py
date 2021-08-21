#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from collections import OrderedDict

THEME = 'themes/msoucy'
AUTHOR = 'Matt Soucy'
SITENAME = 'msoucy.me'
TAGLINE = 'Code, games, and sarcasm'
SITEURL = ''

PATH = 'content'
GITHUB_URL = 'https://github.com/msoucy/'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
        ('FOSS@RIT', 'https://fossrit.github.io'),
        ('RIT CSH', 'http://csh.rit.edu'),
        # ('Helixoide Blog', 'http://blog.helixoide.com'),
        ('ryansb', 'http://rsb.io'),
        ('[three]Bean', 'http://threebean.org'),
        # ('DGonyeo', 'http://blog.gonyeo.com'),
        # ('loothelion', 'http://loothelion.rocks'),
        ('coldsauce', 'https://blog.stefanaleksic.com'),
 )

PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'pelican.plugins.webassets',
    'pelican.plugins.neighbors',
    'pelican.plugins.render_math',
    'pelican.plugins.series',
    'pelican.plugins.sitemap',
    'filetime_from_git',
    'pelican-open_graph',
    'shortcodes',
]

SITEMAP = {"format": "xml"}

PATH_METADATA = r'(?P<date>\d{4}/\d{2}/(\d{2})?)-(?P<slug>.*)\.md'
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + "index.html"
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
ARTICLE_EXCLUDES = ['seminars', 'pages']
STATIC_PATHS = ['images', 'seminars', 'extras']

EXTRA_PATH_METADATA = {
    "extras/keybase.txt": {"path": "keybase.txt"}
}
# RELATIVE_URLS = True


def mastodonSnippet(text):
    from urllib import parse
    from markdown.util import etree

    wrapper = etree.Element('div')

    element = etree.SubElement(wrapper, 'iframe')
    element.set('src', text + '/embed')
    element.set('class', 'mastodon-embed')
    element.set('style', 'max-width: 100%; border: 0')
    element.set('width', '400')

    embedElement = etree.SubElement(wrapper, 'script')
    embedElement.set('async', 'async')
    url = parse.urlparse(text)
    embedUrl = parse.urlunparse(('https', url.netloc, 'embed.js', '', '', ''))
    embedElement.set("src", embedUrl)

    return wrapper


def youtubeSnippet(text):
    from markdown.util import etree

    video = etree.Element('iframe')
    video.set('width', '560')
    video.set('height', '315')
    video.set('src', 'https://www.youtube-nocookie.com/embed/' + text +
              '?rel=0')
    video.set('frameborder', '0')
    video.set('allow', 'autoplay; encrypted-media')
    video.set('allowfullscreen', 'allowfullscreen')
    return video


def gistSnippet(text):
    from markdown.util import etree

    tag = etree.Element('script')
    tag.set('src', 'https://gist.github.com/' + text + '.js')
    return tag


MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {},
        'markdown.extensions.extra': {},
        'markdown.extensions.sane_lists': {},
        'mdx_snippets': {
            'configs': {
                'handlers': {
                    'gist': gistSnippet,
                    'mastodon': mastodonSnippet,
                    'youtube': youtubeSnippet
                }
            }
        }
    }
}
DEFAULT_DATE = "fs"

# Custom settings for the msoucy theme
SEMINARS = (
    ('"Evil" C and C++', "evilC"),
    ("The D Programming Language", "d"),
    ("PGP Keysigning Party", "pgp"),
    ("Fixing the CS Curriculum with Python", "python"),
    ("Style Guidelines", "style"),
    ("Injecting code into Python", "inject"),
    ("Using Python with C Libraries", "cpy"),
    ("Lightning Talk on Firefox Packaging", "mozpack"),
    ("Using Aspect-Oriented Observers", "aspects"),
    ("Build Systems Suck", "bss"),
    ("Using Git in an FRC Team", "git-frc"),
)
AUTHOR_DATA = OrderedDict([
    ("about", "/about"),
    ("email", "mailto:web@msoucy.me"),
    ("resume", SITEURL + "/extras/resume.pdf"),
    ("github", GITHUB_URL),
    ("linkedin", "https://www.linkedin.com/in/msoucy"),
    ("mastodon", "https://mastodon.social/@msoucy"),
    ("twitter", "https://twitter.com/msoucy93"),
])
FBADMINS = "1188604437"

WEBASSET_SOURCE_PATHS = [
    'static',
]
