import threading
from app import create_app
from app.services.kafka_compensation_event_consumer import consume_compensation_events
from app.services.kafka_event_consumer import consume_payment_events
from app.utils.create_thread import create_thread

app = create_app()


# eseguo due operazioni concorrenti:
# a. server HTTP Flask che gestisce le richieste e fornisce risposte ai client
# b. consumer Kafka che in background consuma i messaggi e li elabora
if __name__ == "__main__":

    # avvio dei consumer Kafka in thread separati
    create_thread(consume_payment_events)
    create_thread(consume_compensation_events)


    app.run(host="0.0.0.0", port=5003)
