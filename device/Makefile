up:
	docker-compose up metr-device-rabbitmq --build -d && \
	sleep 4 && \
	docker-compose up metr-device-gateway --build -d
	sleep 4 && \
	docker-compose up metr-device-sensor --build -d

down:
	docker-compose down

logs:
	docker-compose logs -f
