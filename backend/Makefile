run:
	# docker run -d -p 6379:6379 --rm --name redis redis:alpine
	ENV=development hypercorn --reload --config=hypercorn.toml 'app:create_app(".env")'

check:
	@echo
	isort --diff -c --skip-glob '.venv' .
	@echo
	yapf -vv --diff --recursive --style ../yapf.ini --exclude '*.venv' .
	@echo
	mypy --ignore-missing-imports .
	@echo
	flake8 --config flake8.ini --max-line-length 120 --exclude '.hg,.vscode,.venv,__pycache__,docs,.mypy_cache' --count .

test_:
	ENV=testing pytest -x --default-async-timeout 100 --cov-report term-missing --cov-report html --cov-branch --cov app/

test: check test_
