build:
	docker network create metr-network
	docker volume create metr-postgres-data
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

create-admin:
	chmod +x ./scripts/create-admin.sh
	./scripts/create-admin.sh
