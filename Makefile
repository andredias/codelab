run: frontend/dist
	docker compose up

dev:
	docker compose -f docker compose.yml -f docker compose.test.yml up

build:
	docker compose build

frontend/node_modules: frontend/package.json
	cd frontend; npm install

frontend/dist: frontend/node_modules frontend/src/** frontend/src/**/* frontend/public/**
	cd frontend; npm run build

lint:
	cd backend; poetry run make lint

test:
	cd backend; poetry run make test

install_hooks:
	@ scripts/install_hooks.sh
