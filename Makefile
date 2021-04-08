run: frontend/dist
	cd server; \
	docker-compose up --build -d

dev: frontend/dist
	cd server; \
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

frontend/node_modules: frontend/package.json
	cd frontend; npm install

frontend/dist: frontend/node_modules frontend/src/** frontend/src/**/* frontend/public/**
	cd frontend; npm run build
