from flask import current_app
from app import create_app
from kafka import KafkaConsumer
from time import sleep
import json
from app.services.db_service import connect_to_db
from app.services.kafka_producer import produce_payment_event, produce_compensation_event
from app.utils.useful_functions import create_random_id

# crea l'istanza dell'app
app = create_app()


def process_order_event(order_data):

    with app.app_context():  # recupero contesto per eseguire operazione

        current_app.logger.info("[payment service] Sto processando un nuovo order event")

        credito_scalato = False  # flag per tracciare se il credito sia stato scalato oppure no

        connection = connect_to_db()

        try:
            cursor = connection.cursor(dictionary=True)
            username = order_data["username"]
            price = order_data["price"]
            order_id = order_data["order_id"]

            current_app.logger.info(f"[payment service] Sto processando ordine con id: {order_id}")

            cursor.execute("SELECT credito FROM Utenti WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and user["credito"] >= price: # success
                current_app.logger.info(f"[payment service] Sto aggiornando credito dell'utente {username}")

                # detraggo importo dell'ordine dal credito dell'utente
                cursor.execute("UPDATE Utenti SET credito = credito - %s WHERE username = %s", (price, username))

                connection.commit()

                credito_scalato = True
                current_app.logger.info("[payment service] Il credito dell'utente è stato aggiornato")

                payment_id = create_random_id()

                # creo nuova riga pagamento in tabella Pagamenti
                cursor.execute(
                    "INSERT INTO Pagamenti (payment_id, order_id, username, payment_timestamp, amount, status) "
                    "VALUES (%s, %s, %s, NOW(), %s, %s)", (payment_id, order_id, username, price, "SUCCESS")
                )
                connection.commit()

                current_app.logger.info(f"[payment service] Pagamento registrato in db con stato SUCCESS (payment_id = {payment_id}")

                # produco il payment-event
                payment_event = {"order_id": order_id, "status": "success"}
                produce_payment_event(payment_event)
                current_app.logger.info(f"[payment service] Payment-event inviato per ordine {order_id}")

            else: # failure: credito insufficiente

                payment_event = {"order_id": order_id, "status": "failed", "reason": "Insufficient credit"}
                produce_payment_event(payment_event)
                current_app.logger.info(f"[payment service] Payment-event inviato per ordine {order_id} (credito insufficiente)")

        except Exception as e:
            current_app.logger.error(f"[payment service] Errore durante il processo: {e}")

            if credito_scalato:  # produci l'evento di compensazione solo se il credito è stato scalato
                compensation_event = {
                    "order_id": order_id,
                    "username": username,
                    "amount": price,
                    "action": "rollback_payment"
                }
                produce_compensation_event(compensation_event)
                current_app.logger.info(f"[payment service] Inviato compensation-event per rollback per ordine {order_id}")
            else:
                current_app.logger.info(f"[payment service] Nessuna compensazione necessaria per ordine {order_id}")

        finally:
            connection.close()


def consume_order_events():
    with app.app_context():  # Attiva il contesto per il thread
        sleep(10)  # attendo che kafka completi l'avvio


        consumer = KafkaConsumer(
            'order-event',
            bootstrap_servers=['kafka:9092'],
            group_id='payment-service-group',
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )

        current_app.logger.info("[payment service] Pronto per consumare nuovi payment-event")

        for message in consumer:
            current_app.logger.info("[payment service] Consumo nuovo order-event")
            process_order_event(message.value)
