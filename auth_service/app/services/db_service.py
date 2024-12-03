import mysql.connector
from flask import current_app # oggetto speciale che rappresenta l'istanza dell'applicazione Flask attualmente attiva


def connect_to_db(): # MySQL

    # current_app viene utilizzato per accedere all'applicazione corrente
    try:
        connection = mysql.connector.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME']
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Errore durante la connessione al DB: {err}")
        return None
