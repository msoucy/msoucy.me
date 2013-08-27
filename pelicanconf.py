#!/usr/bin/env python
# -*- coding: utf-8 -*- #

THEME = 'themes/msoucy'
AUTHOR = u'Matt Soucy'
SITENAME = u'insoucyant'
SITEURL = 'http://skaia.csh.rit.edu'

RELATIVE_URLS = True

GITHUB_URL = 'https://github.com/msoucy/'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

# Blogroll
LINKS = (('RIT FOSSBox', 'http://foss.rit.edu'),
         ('Helixoide Blog', 'http://blog.helixoide.com'),
         ('RIT CSH', 'http://csh.rit.edu/'),
         ('ryansb', 'http://ryansb.com'),
         ('[three]Bean', 'http://threebean.org'),
         )

PLUGIN_PATH = 'plugins'
import minify
PLUGINS = ['assets', 'sitemap', minify]

#FEED_ALL_ATOM = "atom.xml"
TRANSLATION_FEED_ATOM = None
DIRECT_TEMPLATES = ('index', )
#TAG_SAVE_AS, AUTHOR_SAVE_AS, CATEGORY_SAVE_AS = False, False, False

DEFAULT_PAGINATION = 10

ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
ARTICLE_EXCLUDES = ['seminars', 'pages']
STATIC_PATHS = ['images', 'seminars', 'resources']
FILES_TO_COPY = [
    ('extras/resume.pdf', 'resume.pdf'),
    ('extras/ryansb.gpg', 'ryansb.gpg'),
]
