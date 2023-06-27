from datetime import datetime
import json
import logging
import random
import sys
import time

import pika


logging.basicConfig(level=logging.INFO)

DATA_PATH = './data/data.json'
RABBITMQ_HOST = 'metr-device-rabbitmq'
QUEUE_NAME = 'measurements'


def nap() -> None:
    """
    Sleep for a random amount of time between 1 and 5 seconds.
    """
    a_time = random.randint(1, 5)
    logging.info(f'Sleeping for {a_time} seconds...')
    time.sleep(a_time)


def setup_rabbitmq() -> pika.BlockingConnection:
    """
    Create a connection and channel to RabbitMQ.
    """
    connection_params = pika.ConnectionParameters(host=RABBITMQ_HOST)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    return connection, channel


def publish_message(channel, message_data):
    """
    Publish a message to the RabbitMQ queue.
    """
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(message_data),
        properties=pika.BasicProperties(delivery_mode=2),
    )


def main() -> None:
    with open(DATA_PATH) as f:
        data = json.load(f)

    connection, channel = setup_rabbitmq()

    try:
        while True:
            for i, measurement_data in enumerate(data):
                nap()
                publish_message(channel, measurement_data)
                logging.info(
                    f'Sent measurement #{i+1} at {datetime.now().strftime("%H:%M:%S")}'
                )

    except KeyboardInterrupt:
        logging.info('Exiting...')
        sys.exit(0)

    finally:
        connection.close()


if __name__ == '__main__':
    main()
