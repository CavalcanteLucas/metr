# METR

This project emulates a distributed web application for reporting measurements of heat monitoring devices.

The figure below illustrates the architecture of the project.

![image](https://github.com/CavalcanteLucas/metr/assets/17774383/49d6d626-24d9-4f65-bc62-a4c275d28fef)


## Running the project locally

### Requirements

To run the project locally you need to have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed. After cloning this repository, follow the steps below:

Open a terminal and navigate to the project's root directory. There you will find two directories: `device/` and `server/`.
```
.
├── device
├── README.md
└── server
```

First, go to the `server/` directory. There you will need to create a `.env` file with the content of the `.env.example` file.

Second, yet in the `server/` directory, you will find a `credentials/` subdirectory.
```
.
├── device
├── README.md
└── server
    ├── credentials
    │   └── example-credentials.json
    ...
```

There you will need to create a `credentials.json` file with a valid service account key, as illustrated in the `example-credentials.json` file.

### Server

After that, we are good. Go back to the `server` directory and run the following command:
```
make build
```

It will create:
- the network that will connect the device's and server's containers;
- the database volume;
- and to build the server's containers.

The server's containers have:
- a Django application that exposes a REST API and an admin panel through port 8000 of the host machine (http://localhost:8000);
- a PostgreSQL database server that will persist the data;
- a Redis server that will be used as a message broker for the Celery task queue;
- and a Celery worker responsible for asynchronously processing the requests to generate the reports based on the data sent by the device emulator.

To start the containers, run:
```
make up
```

If you want to watch the logs of the server's containers, run:
```
make logs
```

For convenience, you can run the following command to create an admin user with the credentials `admin:admin`:
```
make create-admin
```

That will be particularly useful for logging in on the admin panel of the Django application to check if the data is being stored correctly.


### Device emulator

Now, (optionally open another terminal,) navigate to the `device` directory, and run:
```
make up
```

It will create the following containers:
- the RabbitMQ server that will be used as a message broker to emulate the communication gateway between the device and the server;
- a process that will emulate the communication gateway, receiving the measurements from the RabbitMQ server and sending them to the server's REST API;
- a process that will emulate the device's sensor, sending measurements to the RabbitMQ server. This process will send a measurement within an interval of 1 to 5 seconds. There are 10 measurement samples. After sending all of them, it will start over from the first one in a loop.

Again, if you want to watch the logs of the device emulator's containers, run:
```
make logs
```

To stop the containers, run:
```
make down
```

## Requiring a report

To require a report, with the application running, access the endpoint `http://localhost:8000/api/measurements/report/` and press the button "Generate report".

![image](https://github.com/CavalcanteLucas/metr/assets/17774383/57b9b76c-b540-4555-a6ce-1ffdc50f9d4a)

Follow the instructions on the screen to download the report.

## Additional information

### Workflow for registering measurements

1. The device emulator sends a measurement to the RabbitMQ server;
2. The communication gateway receives the measurement from the RabbitMQ server;
3. The communication gateway sends the measurement to the server's API;
4. The server's API stores the measurement in the database;
5. The server's API sends an HTTP response to the communication gateway.

![image](https://github.com/CavalcanteLucas/metr/assets/17774383/f40add1d-2c16-4b25-accb-da2d3a555713)


### Workflow for generating reports

1. The user requires a report through the server's REST API;
2. The server's API sends a message to the Redis broker;
3. The server's API sends an HTTP response to the user;
4. The Celery worker receives the message from the Redis broker;
5. The Celery worker queries the database for the measurements;
6. The Celery worker generates the report and uploads it to the bucket.

![image](https://github.com/CavalcanteLucas/metr/assets/17774383/87f13ccf-6dfd-4be1-8720-b3106eb063fb)


## Author

This project was developed by [Lucas Cavalcante](https://github.com/CavalcanteLucas).
