all: dist

.PHONY: clean
clean:
	python setup.py clean
	-rm -rf build dist *.egg-info

.PHONY: check
check:
ifeq ($(COVERAGE),1)
	coverage run --omit='**/test/*' test/test.py
	coverage html --directory=coverage
else
	python test/test.py
endif
	

.PHONY: dist
dist:
	python setup.py sdist

.PHONY: upload
upload:
	python setup.py register
	python setup.py sdist upload
	# python setup.py bdist_egg upload
	# python setup.py bdist_wininst upload
