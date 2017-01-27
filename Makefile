.PHONY: setup virtualenv install test clean release graph clean_pyc clean_build

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
	env/bin/py.test --cov-report term-missing --cov=${PWD}/${APP_NAME} tests -s -vv 

testonly:
	env/bin/py.test tests -s -vv 


testprofile:
	# env/bin/py.test --profile test/test_settings.py -s -vv
	env/bin/py.test --profile tests/test_real_example.py -s -vv
	# env/bin/py.test test/test_settings.py --profile-svg

testprofile2:
	env/bin/py.test --profile tests/test_settings.py -s -vv

testapp:
	env/bin/py.test tests/test_settings.py -s -vv

testcase:
	env/bin/py.test tests/test_case.py -s -vv

clean_pyc:
	find . -name '*.pyc' -exec rm -fv {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

clean_build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

clean: clean_build clean_pyc
	rm -rfv .DS_Store .coverage .cache
	rm -Rf **/__pycache__
	rm -Rf env
	rm -Rf .eggs
	rm -Rf .tox
	rm -Rf prof

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
