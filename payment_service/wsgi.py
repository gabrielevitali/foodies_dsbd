from app import create_app
from threading import Thread
from app.services.kafka_consumer import consume_order_events

app = create_app()


# eseguo due operazioni concorrenti:
# a. server HTTP Flask che gestisce le richieste e fornisce risposte ai client
# b. consumer Kafka che in background consuma i messaggi e li elabora
if __name__ == "__main__":

    # avvio del consumer Kafka in un thread separato
    consumer_thread = Thread(target=consume_order_events)
    consumer_thread.daemon = True
    consumer_thread.start()

    app.run(host="0.0.0.0", port=5004, threaded=True)
