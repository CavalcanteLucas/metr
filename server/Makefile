down:
	docker-compose down
	docker network prune --force

up:
	docker network create metr-network
	docker-compose up --build

create-admin:
	chmod +x ./scripts/create-admin.sh
	./scripts/create-admin.sh
