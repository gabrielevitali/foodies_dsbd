from threading import Thread

def create_thread(target):

    # avvio del consumer Kafka in un thread separato
    consumer_thread = Thread(target=target)
    consumer_thread.daemon = True
    consumer_thread.start()