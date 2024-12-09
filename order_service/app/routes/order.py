
from flask import Blueprint, jsonify, request, current_app
from app.services.db_service import connect_to_db
from app.services.kafka_producer import produce_order_event
from app.utils.jwt_utils import extract_verify_token
from app.utils.useful_functions import create_random_id


order_routes = Blueprint('order', __name__)


@order_routes.route('/create', methods=['POST'])
def create_order():

    # estraggo, decodifico e verifico la validità del token
    esito, username = extract_verify_token(request)

    # se c'è un errore nel token, restituisco apposito errore
    if esito != True:
        return jsonify(esito), 401

    # recupero dati dal corpo della richiesta (json)
    name = request.get_json().get("name")
    category = request.get_json().get("category")
    price = request.get_json().get("price")

    if not all([name, category, price]):
        return jsonify({"error": "Parametro 'name'/'category'/'description'/'price' mancante"}), 400

    connection = connect_to_db()
    if not connection:
        return jsonify({"error": "Connessione al DB fallita"}), 500

    try:
        cursor = connection.cursor(dictionary=True)  # restituisce risultati in forma di dizionario
        cursor.execute("SELECT username FROM Utenti WHERE username = %s", (username,))
        user_db = cursor.fetchone()

        if user_db: # se è stato trovato username cercato

            connection = connect_to_db()

            try:
                cursor = connection.cursor()

                order_id = create_random_id()
                # inserisco in database nuovo ordine (senza specificare order_id, in quanto generato in automatico)
                cursor.execute(
                    "INSERT INTO Ordini (order_id, username, status, created_at, amount, meal) "
                    "VALUES (%s, %s, %s, NOW(), %s, %s)",
                    (order_id, username, "PENDING", price, name) # creo ordine con stato "PENDING"
                )

                connection.commit()

                current_app.logger.info(f"[order service] Inserito in db ordine con id {order_id} per l'utente {username}")

                produce_order_event(order_id, username, name, price)

                return jsonify({"message": f"Nuovo ordine creato con id: {order_id}. Resta aggiornato verificando lo stato dell'ordine.", "order_id": order_id}), 201

            except Exception as e:
                connection.rollback()
                return jsonify({"error": str(e)}), 500

            finally:
                connection.close()

        else: # se l'username cercato non è stato trovato
            return jsonify({"error": "Errore nella richiesta (Username non trovato)"}), 401
    finally:
        cursor.close()
        connection.close()


@order_routes.route('/status/<order_id>', methods=['GET'])
def check_order_status(order_id):

    # estraggo, decodifico e verifico la validità del token
    esito,username = extract_verify_token(request) # in questo caso, username è inutilizzato

    # se c'è un errore nel token, restituisco apposito errore
    if esito != True:
        return jsonify(esito), 401

    connection = connect_to_db()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT status FROM Ordini WHERE order_id = %s", (order_id,))
        order = cursor.fetchone()

        if order:
            return jsonify({"order_id": order_id, "status": order["status"]}), 200
        else:
            return jsonify({"error": f"Non è stato trovato alcun ordine avente id {order_id}"}), 404
    finally:
        cursor.close()
        connection.close()


@order_routes.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@order_routes.route('/')
def order_service():
    return jsonify({"message":"Welcome to the Order Service via NGINX!"})