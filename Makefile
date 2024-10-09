
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3

setup:
	if [ ! -d  reports/ ]; then\
		mkdir reports/\
	else\
		printf "reports/ already exists\n\n";\
	fi &&\
	python3 setup.py

unittest:
	$(PYTHON) -m unittest -v test.test

run:
	$(PYTHON) main.py

