#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

THEME = 'themes/msoucy'
AUTHOR = u'Matt Soucy'
SITENAME = u'insoucyant'
TAGLINE = u'Code, music, and sarcasm'
SITEURL = 'http://msoucy.me'

GITHUB_URL = 'https://github.com/msoucy/'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

PATH = 'content'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('RIT FOSSBox', 'http://foss.rit.edu'),
         ('Helixoide Blog', 'http://blog.helixoide.com'),
         ('RIT CSH', 'http://csh.rit.edu'),
         ('ryansb', 'http://rsb.io'),
         ('[three]Bean', 'http://threebean.org'),
         )

PLUGIN_PATH = 'plugins'
#import minify
PLUGINS = [
    'assets',
    'sitemap',
    'multi_part',
    'neighbors',
]

SITEMAP = {"format": "xml"}

#DEFAULT_PAGINATION = 10

PATH_METADATA = r'(?P<date>\d{4}/\d{2}/(\d{2})?)-(?P<slug>.*)\.md'
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
ARTICLE_EXCLUDES = ['seminars', 'pages']
STATIC_PATHS = ['images', 'seminars', 'resources', 'extras']

MD_EXTENSIONS = ['codehilite','extra', 'sane_lists', 'nl2br']
DEFAULT_DATE = "fs"

# Custom settings for the msoucy theme
SEMINARS = (
    ("D", "D"),
    ("PGP", "pgp"),
    ("Evil C", "evilC"),
    ("Style Guidelines", "style"),
    ("Python++", "python"),
)
AUTHOR_DATA = {
    "email": "msoucy@csh.rit.edu",
    "g+": "http://gplus.to/msoucy",
    "linkedin": "msoucy",
    "github": GITHUB_URL
}
DISQUS_SITENAME = 'insoucyant'
