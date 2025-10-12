.PHONY: build release-test release

build:
	rm -rf dist/
	python3 -m build

release-test: build
	echo "Uploading to https://test.pypi.org/project/dynamic-doc-sh/"
	python3 -m twine upload --repository testpypi dist/*

release: build
	echo "Uploading to https://pypi.org/project/dynamic-doc-sh/"
	python3 -m twine upload --repository pypi dist/*
