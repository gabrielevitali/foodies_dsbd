from flask import jsonify, current_app # oggetto speciale che rappresenta l'istanza dell'applicazione Flask attualmente attiva
import mysql.connector


def connect_to_db():  # MySQL

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


def add_credit_db(username, credit_to_add):
    connection = connect_to_db()

    try:
        cursor = connection.cursor(dictionary=True)

        # aggiorno il credito, sommando quello specificato dall'utente a quello già disponibile
        query = "UPDATE Utenti SET credito = credito + %s WHERE username = %s"
        cursor.execute(query, (credit_to_add, username))
        connection.commit()  # applico modifica

        # recupera il nuovo valore del credito ricaricato
        query = "SELECT credito FROM Utenti WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()  # ottengo risultato della select

        if result:
            new_credit = result["credito"]
            return jsonify({"message": f"Il tuo credito è stato aggiornato. Adesso hai a disposizione €{new_credit}"}), 200
        else:
            return jsonify({"error": "Errore: non è stato possibile aggiornare il credito."}), 404

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Errore interno del server"}), 500

    finally:
        cursor.close()
        connection.close()