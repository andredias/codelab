test:
	pytest -x --cov-report term-missing --cov-report html --cov-branch \
	       --cov codelab/

lint:
	@echo
	ruff .
	@echo
	blue --check --diff --color .
	@echo
	mypy .
	@echo
	pip-audit


format:
	ruff --silent --exit-zero --fix .
	blue .
