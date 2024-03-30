test:
	python -m unittest discover

dev-requirements.txt: dev-requirements.in
	which pip-compile || pip install pip-tools
	pip-compile dev-requirements.in

setup: dev-requirements.txt
	pip install -r dev-requirements.txt

.PHONY: test setup
