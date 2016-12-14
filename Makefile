.PHONY: setup virtualenv install test clean release graph

VIRTUALENV_DIR=${PWD}/env
APP_NAME=anchorman

help:
	@echo '    setup ........ sets up project'
	@echo '    test ......... runs unittest'
	@echo '    clean ........ cleans project'
	@echo '    release ...... releases project to pypi'
	@echo '    graph ........ graph of project'
	@echo '    metric ....... code metric at landscap.io'
	@echo '    pypi ......... project on pypi'

setup: virtualenv install

virtualenv:
	if [ ! -e ${VIRTUALENV_DIR}/bin/pip ]; then virtualenv ${VIRTUALENV_DIR} --no-site-packages; fi

install: virtualenv
	${VIRTUALENV_DIR}/bin/pip install -r requirements.txt
	${VIRTUALENV_DIR}/bin/python setup.py develop --always-unzip

test:
	env/bin/py.test --cov-report term-missing --cov=${PWD}/${APP_NAME} test -s -vv

clean:
	rm -rfv .DS_Store .coverage .cache
	rm -Rf **/__pycache__
	find ${PWD} -name '*.pyc' -exec rm -fv {} \;
	find ${PWD} -name '*.pyo' -exec rm -fv {} \;
	rm -Rf env
	rm -Rf dist build
	rm -Rf *.egg-info
	rm -Rf .eggs

release:
	# check this out http://peterdowns.com/posts/first-time-with-pypi.html
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi

graph:
	pycallgraph --max-depth 5 graphviz -- ./anchorman/__init__.py
	open pycallgraph.png

metric:
	open https://landscape.io/github/rebeling/anchorman

pypi:
	open https://pypi.python.org/pypi/anchorman
