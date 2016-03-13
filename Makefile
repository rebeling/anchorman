.PHONY: setup virtualenv install test clean release

VIRTUALENV_DIR=${PWD}/env
APP_NAME=anchorman


help:
	@echo '    setup ........ sets up project'
	@echo '    unittest ..... runs unittest'
	@echo '    clean ........ cleans project'
	@echo '    release ...... releases project to pypi'

setup: virtualenv install

virtualenv:
	if [ ! -e ${VIRTUALENV_DIR}/bin/pip ]; then virtualenv ${VIRTUALENV_DIR} --no-site-packages; fi

install: virtualenv
	${VIRTUALENV_DIR}/bin/pip install -r requirements.txt
	${VIRTUALENV_DIR}/bin/python setup.py develop

test:
	env/bin/py.test --cov-report term-missing --cov=${PWD}/${APP_NAME} test -s

clean:
	rm -rfv .DS_Store .coverage .cache
	rm -Rf **/__pycache__
	find ${PWD} -name '*.pyc' -exec rm -fv {} \;
	find ${PWD} -name '*.pyo' -exec rm -fv {} \;
	rm -Rf env
	rm -Rf dist build
	rm -Rf *.egg-info

release:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
