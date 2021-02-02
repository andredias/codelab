run:
	# docker run -d -p 6379:6379 --rm --name redis redis:alpine
	ENV=development hypercorn --reload --config=hypercorn.toml 'app:create_app(".env")'


test:
	ENV=testing pytest -x -v --cov-report term-missing --cov-report html --cov-branch --cov app/
