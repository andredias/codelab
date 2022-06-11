test:
	pytest --cov-report term-missing --cov-report html --cov-branch \
	       --cov app/

lint:
	@echo
	isort --diff -c .
	@echo
	blue --check --diff --color .
	@echo
	flake8 .
	@echo
	mypy .
	@echo
	bandit -qr app/
	@echo
	pip-audit


format:
	isort .
	blue .
	pyupgrade --py310-plus **/*.py
