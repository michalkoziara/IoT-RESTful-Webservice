.PHONY: clean python-packages install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

python-packages:
	pip install -r requirements.txt

install: python-packages

tests:
	python manage.py test

run:
	python manage.py run

all: clean install tests run