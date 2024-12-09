from flask import current_app
from kafka import KafkaProducer
import json


def produce_order_event(order_id, username, name, price):

    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # creo order-event
    order_event = {
        "order_id": order_id,
        "username": username,
        "meal": name,
        "price": price
    }

    producer.send("order-event", value=order_event)
    producer.flush()

    current_app.logger.info("Ho inviato un nuovo order-event")