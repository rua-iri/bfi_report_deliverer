
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3

setup:
	python3 -m venv $(VENV)

	$(PIP) install -r requirements.txt

	sudo apt install wkhtmltopdf
	
	python3 setup.py

unittest:
	$(PYTHON) -m unittest -v test.test

run:
	$(PYTHON) main.py

