from flask import current_app # oggetto speciale che rappresenta l'istanza dell'applicazione Flask attualmente attiva
from pymongo import MongoClient


# funzione che gestisce la connessione a MongoDB e seleziona collection "meals" da "meals_db"
def connect_to_db(): # MongoDB

    try:

        # connessione al client MongoDB
        client = MongoClient(
            host=current_app.config['DB_HOST'],
            port=int(current_app.config['DB_PORT']),
            username=current_app.config["DB_USERNAME"],
            password=current_app.config["DB_PASSWORD"],
            authSource=current_app.config["DB_AUTH_SOURCE"]
        )

        return client

    except Exception as e:
        print(f"Errore durante la connessione a MongoDB: {e}")
        return None
