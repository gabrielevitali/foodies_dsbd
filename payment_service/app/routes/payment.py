from flask import Blueprint, jsonify, request, current_app
from app.services.db_service import connect_to_db, add_credit_db
from app.utils.jwt_utils import extract_verify_token

payment_routes = Blueprint('payment', __name__)

@payment_routes.route('/add', methods=['POST'])
def add_credit():

    # estraggo, decodifico e verifico la validità del token
    esito, username = extract_verify_token(request)

    # se c'è un errore nel token, restituisco apposito errore
    if esito != True:
        return jsonify(esito), 401


    try:
        # recupero dati dal corpo della richiesta (json)
        credit_to_add = request.get_json().get("credit")

        if credit_to_add is None:
            return jsonify({"error": "Parametro 'credit' mancante"}), 400

        credit_to_add = int(credit_to_add)
        if credit_to_add <= 0:
            return jsonify({"error": "Il valore di 'credit' dev'essere positivo"}), 400

    except (ValueError):
        return jsonify({"error": "Parametro 'credit' non valido. Deve essere un numero positivo"}), 400

    return add_credit_db(username, credit_to_add)


@payment_routes.route('/total/month/<month>', methods=['GET'])
def get_total_month_payment(month):

    # estraggo, decodifico e verifico la validità del token
    esito, username = extract_verify_token(request)

    # se c'è un errore nel token, restituisco apposito errore
    if esito != True:
        return jsonify(esito), 401

    connection = connect_to_db()

    try:
        cursor = connection.cursor(dictionary=True)

        year = current_app.config["YEAR"]
        query = "SELECT SUM(amount) AS total_amount  FROM Pagamenti WHERE username = %s AND MONTH(payment_timestamp) = %s AND YEAR(payment_timestamp) = %s;"
        cursor.execute(query, (username, month, year,))
        result= cursor.fetchone()

        if result:
            if result['total_amount'] is not None:
                return jsonify({"message": f"La spesa totale ammonta a {result['total_amount']}"}), 200
            else:
                return jsonify({"message": "La spesa totale ammonta a 0.00"}), 200
        else:
            return jsonify({"error": f"Errore"}), 404

    finally:
        cursor.close()
        connection.close()


@payment_routes.route('/details/<payment_id>', methods=['GET'])
def get_payment_details(payment_id):

    # estraggo, decodifico e verifico la validità del token
    esito, _ = extract_verify_token(request)

    # se c'è un errore nel token, restituisco apposito errore
    if esito != True:
        return jsonify(esito), 401

    connection = connect_to_db()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Pagamenti WHERE payment_id = %s", (payment_id,))
        payment = cursor.fetchone()

        if payment:
            return jsonify({"payment_id": payment_id, "status": payment["status"]}), 200
        else:
            return jsonify({"error": f"Non è stato trovato alcun pagamento avente id {payment_id}"}), 404
    finally:
        cursor.close()
        connection.close()


@payment_routes.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@payment_routes.route('/')
def payment_service():
    return jsonify({"message":"Welcome to the Payment Service via NGINX!"})