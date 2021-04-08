run: frontend
	cd server; \
	docker-compose up --build -d

dev: frontend
	cd server; \
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

frontend:
	cd frontend; \
	npm run build
