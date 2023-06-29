# METR

This project emulates a distributed web application for reporting measurements of heat monitoring devices.

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

First, go ot the `server/` directory. There you will need to create a `.env` file with the content of the `.env.example` file.

Second, yet in the `server/` directory, you will find a `credentials/` sub directory.
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

The server's ontainers have:
- a Django application that exposes a REST API and an admin panel through port 8000 of the host machine (http://localhost:8000);
- a PostgreSQL database server that will persist the data;
- a Redis server that will be used as a message broker for the Celery task queue;
- and a Celery worker that will be responsible for assynchronously process the requests to generate the reports based on the data sent by the device emulator.

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

That will be particularly useful for loggin in on the admin's panel of the Django application to check if the data is being stored correctly.


### Device emulator

Now, (optionally open another terminal,) navigate to the `device` directory, and run:
```
make up
```

It will create the following containers:
- the RabbitMQ server that will be used as a message broker to emulate the communication gateway between the device and the server;
- a process that will emulate the communication gateway, receiving the measurements from the RabbitMQ server and sending them to the server's REST API;
- a process that will emulate the device's sensor, sending measurements to the RabbitMQ server. This process will send a measurement within an interval of 1 to 5 seconds. There are 10 measurements samples. After sending all of them, it will start over from the first one in a loop.

Again, if you want to watch the logs of the device emulator's containers, run:
```
make logs
```

To stop the containers, run:
```
make down
```

## Requiring a report

To require a report, access the endpoint `http://localhost:8000/api/measurements/report/` and press the button "Generate report". Follow the instructions on the screen to download the report.


## Author

This project was developed by [Lucas Cavalcante](https://github.com/CavalcanteLucas).
