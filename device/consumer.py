from datetime import datetime
import json
import logging

import pika
import requests


logging.basicConfig(level=logging.INFO)

RABBITMQ_HOST = 'metr-device-rabbitmq'
QUEUE_NAME = 'measurements'
API_ENDPOINT = 'http://metr-server-app:8000/api/measurements/'


def callback(ch, method, properties, body):
    """
    This function is called every time a message is received from the queue.
    """
    logging.info(f'Received message at {datetime.now().strftime("%H:%M:%S")}')

    try:
        logging.info('Sending data...')
        get_response = requests.post(
            API_ENDPOINT,
            json=json.loads(body.decode('utf-8')),
        )
        logging.info(f'Response status: {get_response.status_code}')
    except requests.exceptions.ConnectionError as e:
        logging.error(e)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def setup_rabbitmq() -> pika.BlockingConnection:
    """
    Create a connection and channel to RabbitMQ.
    """
    connection_params = pika.ConnectionParameters(host=RABBITMQ_HOST)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    return connection, channel


def main() -> None:
    connection, channel = setup_rabbitmq()

    try:
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

        logging.info('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        logging.info('Exiting...')
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == '__main__':
    main()
