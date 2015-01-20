all: dist

.PHONY: clean
clean:
	python setup.py clean
	-rm -rf build dist *.egg-info

.PHONY: dist
dist:
	python setup.py sdist

.PHONY: upload
upload:
	python setup.py register
	python setup.py sdist upload
	# python setup.py bdist_egg upload
	# python setup.py bdist_wininst upload
