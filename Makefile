.PHONY: TAGS test

PYTHON?=python2.4

all:
	$(PYTHON) setup.py build
debug: clean
	$(PYTHON) setup.py build --debug
	$(PYTHON) setup.py install
install:
	$(PYTHON) setup.py install --root $(DESTDIR)/
sdist:
	$(PYTHON) setup.py sdist
bdist:
	$(PYTHON) setup.py bdist
clean:
	rm -rf build dist MANIFEST
	-find . -name *.pyc -exec rm -f {} \;
	-find . -name *.o -exec rm -f {} \;
test:
	(cd tests && $(MAKE) test)
TAGS:
	rm -f TAGS
	find ./ -name "*.c" -type f -exec etags -a {} \;
	find ./ -name "*.py" -type f -exec etags -a {} \;

.PHONY: test clean
