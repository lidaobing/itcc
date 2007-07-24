all: itcc.xhtml news.xhtml

%.xhtml: %.rst
	rst2html -t -g --cloak-email-addresses --section-numbering $< tmp.xhtml
	(head -$$(expr $$(cat tmp.xhtml | wc -l) "-" 2) tmp.xhtml; cat myfoot; tail -2 tmp.xhtml) > $@
	rm -f tmp.xhtml

install: itcc.xhtml news.xhtml
	scp itcc.xhtml lidb@sz001:www/itcc/index.html
	scp news.xhtml lidb@sz001:www/itcc/
