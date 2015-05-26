.PHONY: docs clean all prod dev test integration-test virtualenv install install-requirements install-test install-fabric install-sphinx

VIRTUALENV_DIR=${PWD}
PIP=${VIRTUALENV_DIR}/bin/pip
PYTHON=${VIRTUALENV_DIR}/bin/python

install:
	virtualenv ${VIRTUALENV_DIR}
	${VIRTUALENV_DIR}/bin/pip install -r requirements.txt
	${VIRTUALENV_DIR}/bin/py.test test

docs:
	rm -rfv docs/_build
	cd docs && make html

clean:
	rm -rfv ${VIRTUALENV_DIR}/bin ${VIRTUALENV_DIR}/include
	rm -rfv ${VIRTUALENV_DIR}/lib ${VIRTUALENV_DIR}/local
	rm -rfv docs/_build
	rm -rfv build
	rm -rfv dist
	rm -fv .DS_Store .coverage
	find anchorman -name '*.pyc' -exec rm -fv {} \;
	find anchorman -name '*.pyo' -exec rm -fv {} \;
	find test -name '*.pyc' -exec rm -fv {} \;
	find test -name '*.pyo' -exec rm -fv {} \;
	find . -depth -name '__pycache__' -exec rm -rfv {} \;
	find . -depth -name '*.egg-info' -exec rm -rfv {} \;

