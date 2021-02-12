run:
	# docker run -d -p 6379:6379 --rm --name redis redis:alpine
	ENV=development hypercorn --reload --config=hypercorn.toml 'app:create_app(".env")'

check:
	@echo
	isort --diff -c --skip-glob '*.venv' .
	@echo
	yapf -vv --diff --recursive --style ../yapf.ini --exclude '*.venv' .
	@echo
	mypy fastapi_api
	mypy quart_api
	@echo
	flake8 --config flake8.ini .

test: check
	ENV=testing pytest -s -x -v --cov-report term-missing --cov-report html --cov-branch --cov app/
