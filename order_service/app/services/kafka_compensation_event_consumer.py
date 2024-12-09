from flask import current_app
from app import create_app
from kafka import KafkaConsumer, KafkaProducer
from time import sleep
import json
from app.services.db_service import connect_to_db

# Crea l'istanza dell'app
app = create_app()


def process_compensation_event(compensation_data):

    with app.app_context():

        connection = connect_to_db()

        try:
            cursor = connection.cursor()
            order_id = compensation_data["order_id"]
            username = compensation_data["username"]
            amount = compensation_data["amount"]
            action = compensation_data["action"]

            if action == "rollback_payment":

                # ripristino il credito dell'utente
                cursor.execute("UPDATE Utenti SET credito = credito + %s WHERE username = %s", (amount, username))

                # aggiorno lo stato dell'ordine
                cursor.execute("UPDATE Ordini SET status = %s WHERE order_id = %s", ("FAILED", order_id))
                connection.commit()

                current_app.logger.info(f"[order service] Rollback completato per ordine {order_id}: credito ripristinato e stato aggiornato a FAILED")

        except Exception as e:
            current_app.logger.error(f"Errore nel processare il compensation-event: {e}")
        finally:
            connection.close()


def consume_compensation_events():

    with app.app_context():

        consumer = KafkaConsumer(
            'compensation-event',
            bootstrap_servers=['kafka:9092'],
            group_id='order-service-group',
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )

        current_app.logger.info("[order service] Pronto per consumare nuovi compensation-event")

        for message in consumer:
            current_app.logger.info("[order service] Consumo nuovo compensation-event")
            process_compensation_event(message.value)
