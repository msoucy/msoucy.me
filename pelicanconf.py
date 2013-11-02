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

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('RIT FOSSBox', 'http://foss.rit.edu'),
         ('Helixoide Blog', 'http://blog.helixoide.com'),
         ('RIT CSH', 'http://csh.rit.edu/'),
         ('ryansb', 'http://ryansb.com'),
         ('[three]Bean', 'http://threebean.org'),
         )

PLUGIN_PATH = 'plugins'
import minify
PLUGINS = ['assets', 'sitemap', 'multi_part', 'neighbors',  minify]

SITEMAP = {"format": "xml"}

DEFAULT_PAGINATION = 10

ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
ARTICLE_EXCLUDES = ['seminars', 'pages']
STATIC_PATHS = ['images', 'seminars', 'resources']
FILES_TO_COPY = [
    ('extras/resume.pdf', 'resume.pdf'),
    ('extras/msoucy.gpg', 'msoucy.gpg'),
]

MD_EXTENSIONS = ['codehilite','extra', 'sane_lists', 'nl2br']

# Custom settings for the msoucy theme
SEMINARS = (
    ("D", "d"),
    ("PGP", "pgp"),
    ("Evil C", "evilC")
)
AUTHOR_DATA = {
    "email": "msoucy@csh.rit.edu",
    "g+": "http://gplus.to/msoucy",
    "linkedin": "msoucy",
    "github": GITHUB_URL
}

QUICKBAR_COUNT = 3

