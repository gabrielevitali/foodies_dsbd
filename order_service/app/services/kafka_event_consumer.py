from flask import current_app
from app import create_app
from kafka import KafkaConsumer, KafkaProducer
from time import sleep
import json
from app.services.db_service import connect_to_db

# Crea l'istanza dell'app
app = create_app()

def process_payment_event(payment_data):

    with app.app_context():  # recupero contesto per eseguire operazione

        current_app.logger.info("[order service] Sto processando un nuovo payment event")

        connection = connect_to_db()

        try:
            cursor = connection.cursor()
            order_id = payment_data["order_id"]
            status = payment_data["status"]

            current_app.logger.info(f"[order service] Eseguo update per order_id={order_id} con status={status}")

            #sleep(15) # simulo attesa tra creazione dell'ordine (pending) e aggiornamento del suo stato (confirmed/failed)

            if status == "success":
                cursor.execute("UPDATE Ordini SET status = %s  WHERE order_id = %s", ("CONFIRMED", order_id))
                current_app.logger.info(f"[order service] Lo stato dell'ordine {order_id} è stato aggiornato da PENDING a SUCCESS")
            else:
                cursor.execute("UPDATE Ordini SET status = %s WHERE order_id = %s", ("FAILED", order_id))
                current_app.logger.info("[order service] Lo stato dell'ordine {order_id} è stato aggiornato da PENDING a FAILED")
            connection.commit()

            #rows_updated = cursor.rowcount
            #current_app.logger.info(f"[order service] Numero righe aggiornate: {rows_updated}")

        except Exception as e:
                    print(f"Error processing payment event: {e}")
        finally:
            connection.close()


# Order Service consuma payment-event
# (e produce order-event in funzione create_order)
def consume_payment_events():

    with app.app_context():  # attivo il contesto per il thread
        sleep(10)  # attendo che kafka completi l'avvio

        consumer = KafkaConsumer(
            'payment-event',
            bootstrap_servers=['kafka:9092'],
            group_id='order-service-group',
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )

        current_app.logger.info("[order service] Pronto per consumare nuovi payment-event")

        for message in consumer:
            current_app.logger.info("[order service] Consumo nuovo payment-event")
            process_payment_event(message.value)
