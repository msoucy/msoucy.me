PELICAN=pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py
HTMLDIR=/var/www/html

help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                        (re)generate the web site             '
	@echo '   make clean                       remove the generated files            '
	@echo '   make regenerate                  regenerate files upon modification    '
	@echo '   make publish                     move web pages to production location '
	@echo '                                                                          '


html: clean
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)
	-find output -name ".webassets-cache" | xargs rm -rf
	-rm output/index2.html
	@echo 'Done'

clean:
	find $(OUTPUTDIR) -mindepth 1 -delete

regenerate: clean
	$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

#publish: html
publish:
	rsync -aqz $(OUTPUTDIR)/ $(HTMLDIR)

.PHONY: help html clean regenerate publish
