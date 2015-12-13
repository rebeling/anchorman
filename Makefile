.PHONY: clean docs test all prod virtualenv install install-requirements

VIRTUALENV_DIR=${PWD}/env
PIP=${VIRTUALENV_DIR}/bin/pip
PYTHON=${VIRTUALENV_DIR}/bin/python
APP_PATH=${PWD}
APP_NAME=anchorman

# the `all` target will install everything necessary to develop and deploy
all: prod

# the `prod` target will create the runnable distribution without tests
prod: virtualenv install

virtualenv:
	if [ ! -e ${VIRTUALENV_DIR}/bin/pip ]; then virtualenv ${VIRTUALENV_DIR} --no-site-packages; fi

install: install-requirements
	${PYTHON} setup.py develop

install-requirements: virtualenv
	${PIP} install -r requirements.txt

test:
	env/bin/py.test --cov-report term-missing --cov=${APP_PATH}/${APP_NAME} test -s
	# env/bin/py.test --cov-report=html --cov=${APP_PATH}/${APP_NAME} test -s && mv htmlcov docs/.

docs:
	# the following is included in the repo ...is way to much to set up
	# pyreverse anchorman -p anchorman
	# -pylint ${APP_PATH}/anchorman --rcfile ${APP_PATH}/docs/pylintrc > ${APP_PATH}/docs/pylintreport.rst 2>&1
	# sphinx-apidoc --separate -o docs/auto anchorman
	rm -rfv docs/_build
	cd docs && make html

clean:
	rm -fv .DS_Store .coverage
	rm -rfv docs/_build .cache
	find ${APP_PATH} -name '*.pyc' -exec rm -fv {} \;
	find ${APP_PATH} -name '*.pyo' -exec rm -fv {} \;
	find ${APP_PATH} -name '*,cover' -exec rm -fv {} \;
	rm -Rf *.egg-info
	rm -Rf env
