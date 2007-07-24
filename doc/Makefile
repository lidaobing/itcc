all: itcc.xhtml

%.xhtml: %.rst
	rst2html $< $@

install: itcc.xhtml
	scp $^ lidb@sz001:www/
