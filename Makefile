run:
	docker-compose up -d redis
	poetry run python server_app.py runserver
