.PHONY: test
test: pep8 clean
	@coverage report
	@python setup.py test

.PHONY: tox-test
tox-test: environment
	@tox

.PHONY: environment
environment:
	@pip install -r requirements_dev.txt --use-mirrors
	@pip install -r requirements.txt --use-mirrors
	@pip install numexpr==2.3 --use-mirrors
	@python setup.py develop

.PHONY: install
install:
	@python setup.py install

.PHONY: pep8
pep8:
	@flake8 mining bin db test --ignore=F403,F401

.PHONY: sdist
sdist: test
	@python setup.py sdist upload

.PHONY: clean
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
