#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

THEME = 'themes/msoucy'
AUTHOR = u'Matt Soucy'
SITENAME = u'msoucy.me'
TAGLINE = u'Code, games, and sarcasm'
SITEURL = 'http://msoucy.me'
META_IMAGE = SITEURL + '/images/me.png'

GITHUB_URL = 'https://github.com/msoucy/'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

PATH = 'content'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (
        ('RIT FOSSBox', 'http://foss.rit.edu'),
        ('RIT CSH', 'http://csh.rit.edu'),
        ('Helixoide Blog', 'http://blog.helixoide.com'),
        ('ryansb', 'http://rsb.io'),
        ('[three]Bean', 'http://threebean.org'),
        ('DGonyeo', 'http://blog.gonyeo.com'),
        ('loothelion', 'http://loothelion.rocks'),
 )

PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'assets',
    'sitemap',
    'series',
    'neighbors',
    'render_math',
]

SITEMAP = {"format": "xml"}

PATH_METADATA = r'(?P<date>\d{4}/\d{2}/(\d{2})?)-(?P<slug>.*)\.md'
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + "index.html"
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
ARTICLE_EXCLUDES = ['seminars', 'pages']
STATIC_PATHS = ['images', 'seminars', 'resources', 'extras']

EXTRA_PATH_METADATA = {
    "extras/keybase.txt": {"path": "keybase.txt"}
}

MD_EXTENSIONS = ['codehilite', 'extra', 'sane_lists']
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
AUTHOR_DATA = {
    "email": "msoucy@csh.rit.edu",
    "g+": "http://gplus.to/msoucy",
    "linkedin": "msoucy",
    "github": GITHUB_URL,
    "twitter": "msoucy93"
}

ASSET_SOURCE_PATHS = (
    'static',
)
