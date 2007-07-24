all: itcc.xhtml news.xhtml

%.xhtml: %.rst
	rst2html $< $@

news.xhtml: ../NEWS
	rst2html $< $@

install: itcc.xhtml news.xhtml
	scp $^ lidb@sz001:www/itcc/index.html
	scp news.xhtml lidb@sz001:www/itcc/
