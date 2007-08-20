all: bdist_egg

bdist_egg:
	python2.4 setup.py bdist_egg
	python2.5 setup.py bdist_egg

install:
	python2.5 setup.py install
	python2.4 setup.py install

install2:
	mkdir -p $(HOME)/public_html/
	for file in dist/*.egg; do \
		cp $$file $(HOME)/public_html/; \
		ip=$(shell python -c "import socket; print socket.gethostbyaddr(socket.gethostname())[-1][0]"); \
		echo http://$$ip/~$(USER)/$$(basename $$file); \
	done
check:
	python setup.py test

TAGS:
	rm -f TAGS
	find ./ -name "*.c" -type f -exec etags -a {} \;
	find ./ -name "*.py" -type f -exec etags -a {} \;
