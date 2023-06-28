down:
	docker-compose down

up-gateway:
	docker-compose up metr-device-rabbitmq --build -d && \
	sleep 2 && \
	docker-compose up metr-device-gateway --build

up-sensor:
	docker-compose up metr-device-sensor --build
