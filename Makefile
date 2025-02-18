all: dist

.PHONY: clean
clean:
	python3 setup.py clean
	-rm -rf build dist *.egg-info coverage

.PHONY: test
test:
ifeq ($(COVERAGE),1)
	coverage run --omit='**/test/*,**/site-packages/**' test/test.py
	coverage html --directory=coverage
	coverage json -o coverage/coverage.json
	./scripts/coverage-badge.py coverage/coverage.json coverage/coverage.svg
	coverage report
else
	python3 test/test.py
endif
	
.PHONY: lint
lint:
	ruff check
	pylint pycotap scripts

.PHONY: dist
dist:
	python3 setup.py sdist

.PHONY: upload
upload: clean
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

.PHONY: test-upload
test-upload:
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
