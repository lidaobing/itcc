.PHONY: TAGS test
all:
	python setup.py build
debug: clean
	python setup.py build --debug
	python setup.py install
install:
	python setup.py install
sdist:
	python setup.py sdist
bdist:
	python setup.py bdist
clean:
	rm -rf build dist MANIFEST
	-find . -name *.pyc | xargs rm -f
	-find . -name *.o | xargs rm -f
check:
	-(cd src/Molecular; pychecker *.py)
	-(cd src/Tools; pychecker *.py)
	-(cd src/Tinker; pychecker *.py)
	-(cd src/CCS2; pychecker *.py)

test:
	(cd test; python test.py)
testv:
	(cd test; python test.py -v)
TAGS:
	rm -f TAGS
	find ./ -name "*.c" -type f -exec etags -a {} \;
	find ./ -name "*.py" -type f -exec etags -a {} \;
