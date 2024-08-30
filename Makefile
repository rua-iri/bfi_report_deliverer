

setup:
	if [ ! -d  reports/ ]; then\
		mkdir reports/\
	else\
		printf "reports/ already exists\n\n";\
	fi &&\
	python3 setup.py

test:
	.venv/bin/python3 -m unittest -v test