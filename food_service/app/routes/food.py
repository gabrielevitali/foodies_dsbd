from flask import Blueprint, jsonify, request, current_app
from app.services.db_service import connect_to_db
from app.utils.jwt_utils import extract_verify_token


food_routes = Blueprint('food', __name__)


@food_routes.route('/search', methods=['POST'])
def food_search():

    # estraggo, decodifico e verifico la validità del token
    esito = extract_verify_token(request)

    # se c'è un errore nel token, restituisco apposito errore
    if esito != True:
        return jsonify(esito), 401

        # recupero la stringa "meal" dal corpo della richiesta (json)
    meal = request.get_json().get("meal")
    if not meal:
        return jsonify({"error": "Parametro 'meal' mancante"}), 400

    # connessione a MongoDB
    client = connect_to_db()

    # verifico che la connessione sia andata a buon fine
    if client is None:
        return jsonify({"error": "Connessione a MongoDB fallita"}), 500

    db = client[current_app.config["DB_DATABASE"]]  # seleziono database "meals_db"
    collection = db[current_app.config["DB_COLLECTION"]]  # seleziono collection "meals"

    try:
        # cerca il document corrispondente a "meal"
        result = collection.find_one({"name": meal})

        #result['price']

        if result:
            return jsonify({"name": result["name"], "description":result["description"]}), 200
        else:
            return jsonify({"error": "Piatto non trovato"}), 404

    except Exception as e:
        #import traceback
        #traceback.print_exc()
        #print(f"Errore durante l'interrogazione: {e}")
        return jsonify({"error": "Errore interno"}), 500


@food_routes.route('/manage/<meal>', methods=['DELETE'])
def food_delete(meal):
    role = "admin"

    # estraggo, decodifico e verifico la validità del token
    esito = extract_verify_token(request, role)

    # se c'è un errore nel token, restituisco apposito errore
    if esito != True:
        return jsonify(esito), 401

    # connessione a MongoDB
    client = connect_to_db()

    # verifico che la connessione sia andata a buon fine
    if client is None:
        return jsonify({"error": "Connessione a MongoDB fallita"}), 500

    db = client[current_app.config["DB_DATABASE"]]  # seleziono database "meals_db"
    collection = db[current_app.config["DB_COLLECTION"]]  # seleziono collection "meals"

    try:
        result = collection.delete_one({"name": meal})
        if result.deleted_count > 0:
            return jsonify({"message": f"Meal '{meal}' cancellato con successo!"}), 200
        else:
            return jsonify({"error": "Meal non trovato"}), 404
    except Exception as e:
        print(f"Errore: {e}")
        return jsonify({"error": "Errore interno"}), 500


@food_routes.route('/manage/<meal>', methods=['PUT'])
def food_create_or_update(meal):
    role = "admin"

    # estraggo, decodifico e verifico la validità del token
    esito = extract_verify_token(request, role)

    # se c'è un errore nel token, restituisco apposito errore
    if esito != True:
        return jsonify(esito), 401

    # connessione a MongoDB
    client = connect_to_db()

    # verifico che la connessione sia andata a buon fine
    if client is None:
        return jsonify({"error": "Connessione a MongoDB fallita"}), 500

    db = client[current_app.config["DB_DATABASE"]]
    collection = db[current_app.config["DB_COLLECTION"]]

    try:
        # recupero dati dal corpo della richiesta
        data = request.get_json()
        description = data.get('description')
        price = data.get('price')

        # Validazione input
        if not description or not price:
            return jsonify({"error": "Dati mancanti o incompleti"}), 400

        # verifico che price sia un intero
        if not isinstance(price, int):
            return jsonify({"error": "Il prezzo dev'essere un numero intero"}), 400

        # creazione o aggiornamento del document nella collection meal
        result = collection.update_one(
            {"name": meal},  # Criterio di selezione (chiave primaria)
            {"$set": {"description": description, "price": price}},  # dati da aggiornare
            upsert=True  # se il documento non esiste già, viene creato
        )

        if result.upserted_id:
            message = "Piatto creato con successo!"
        elif result.matched_count > 0:
            message = "Piatto aggiornato con successo!"
        else:
            message = "Nessuna modifica necessaria."

        return jsonify({"message": message}), 200

    except Exception as e:
        print(f"Errore: {e}")
        return jsonify({"error": "Errore interno"}), 500


@food_routes.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@food_routes.route('/')
def food_service():
    return jsonify({"message":"Welcome to the Food Service via NGINX!"})
