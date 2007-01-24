
PYTHON?=python2.4

all:
	$(PYTHON) setup.py build
debug: clean
	$(PYTHON) setup.py build --debug
	$(PYTHON) setup.py install
install:
	$(PYTHON) setup.py install --prefix=/usr/local
dist: sdist
sdist:
	$(PYTHON) setup.py sdist -f
bdist:
	$(PYTHON) setup.py bdist
clean:
	rm -rf build dist MANIFEST itcc/__init__.py tests/subdirs
	-find . -name *.pyc -exec rm -f {} \;
	-find . -name *.o -exec rm -f {} \;
check:
	python setup.py test

deb:
	DH_ALWAYS_EXCLUDE=.svn debuild

help:
	@echo "you can use following commands:"
	@echo " make; sudo make install"
	@echo " make dist"
	@echo " make bdist"
	@echo " make deb"

TAGS:
	rm -f TAGS
	find ./ -name "*.c" -type f -exec etags -a {} \;
	find ./ -name "*.py" -type f -exec etags -a {} \;

.PHONY: TAGS test clean deb
