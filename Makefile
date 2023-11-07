run: frontend/dist
	docker compose up

dev: frontend/dist
	docker compose -f docker-compose.yml -f docker-compose.test.yml up

build:
	docker compose build

frontend/node_modules: frontend/package.json
	cd frontend; npm install

frontend/dist: frontend/node_modules frontend/src/** frontend/src/**/* frontend/public/**
	cd frontend; npm run build

lint:
	cd backend; poetry run make lint

format:
	cd backend; poetry run make format

audit:
	cd backend; poetry run make audit

test:
	@ docker compose -f docker-compose.yml -f docker-compose.test.yml up -d redis codebox
	cd backend; poetry run make test

install_hooks:
	@ scripts/install_hooks.sh
