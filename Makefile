

setup:
	mkdir reports/ \
	python3 setup.py

test:
	python3 -m unittest -v test