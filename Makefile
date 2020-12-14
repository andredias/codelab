run:
	docker-compose up -d redis
	poetry run python server_app.py runserver


extract_translations:
	cd app && pybabel extract -F babel.cfg -o translations/message.pot .
