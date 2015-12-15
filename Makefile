.PHONY: clean test all prod virtualenv install install-requirements

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

clean:
	rm -fv .DS_Store .coverage
	rm -rfv .cache
	find ${APP_PATH} -name '*.pyc' -exec rm -fv {} \;
	find ${APP_PATH} -name '*.pyo' -exec rm -fv {} \;
	rm -Rf *.egg-info
	rm -Rf env
