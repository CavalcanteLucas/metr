down:
	docker-compose down

up:
	docker network create metr-network
	docker-compose up --build

prune-net:
	docker network prune --force

create-admin:
	chmod +x ./scripts/create-admin.sh
	./scripts/create-admin.sh
