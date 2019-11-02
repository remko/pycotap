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
	python3 setup.py sdist

.PHONY: upload
upload:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

.PHONY: test-upload
test-upload:
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
