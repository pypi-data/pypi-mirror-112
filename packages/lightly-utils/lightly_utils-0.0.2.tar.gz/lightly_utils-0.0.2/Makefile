# Copyright (c) 2021. Lightly AG and its affiliates.
# All Rights Reserved

.PHONY: clean clean-build clean-pyc clean-out docs help
.DEFAULT_GOAL := help

help:
	@echo clean
	@echo dist
	@echo install
	@echo lint
	@echo test
	@echo testCov
	@echo uninstall

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

dist: clean
	python setup.py sdist bdist_wheel
	ls -l dist

install: clean
	pip install .

lint:
	flake8 lightly_utils

test:
	pytest tests/

testCov:
	python -m pytest --cov=../utils/lightly_utils --cov-report=xml

uninstall:
	pip uninstall lightly_utils

