all: itcc.xhtml news.xhtml

%.xhtml: %.rst
	rst2html --cloak-email-addresses --section-numbering $< $@

install: itcc.xhtml news.xhtml
	scp itcc.xhtml lidb@sz001:www/itcc/index.html
	scp news.xhtml lidb@sz001:www/itcc/
