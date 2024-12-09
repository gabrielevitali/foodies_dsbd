from kafka import  KafkaProducer
import json

def produce_payment_event(payment_event):

    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    producer.send("payment-event", value=payment_event)
    producer.flush()


def produce_compensation_event(compensation_event):

    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # invio l'evento al topic "compensation-event"
    producer.send("compensation-event", value=compensation_event)
    producer.flush()
