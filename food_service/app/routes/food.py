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

    # recupero dati dal corpo della richiesta (json)
    meal = request.get_json().get("meal")
    category = request.get_json().get("category")
    if not meal:
        return jsonify({"error": "Parametro 'meal' mancante"}), 400
    elif not category:
        return jsonify({"error": "Parametro 'categoria' mancante"}), 400

    # connessione a MongoDB
    client = connect_to_db()

    # verifico che la connessione sia andata a buon fine
    if client is None:
        return jsonify({"error": "Connessione a MongoDB fallita"}), 500

    db = client[current_app.config["DB_DATABASE"]]  # seleziono database "meals_db"
    collection = db[current_app.config["DB_COLLECTION"]]  # seleziono collection "meals"

    try:
        # cerca il document corrispondente a "meal"
        result = collection.find_one({"name": meal, "category": category})

        if result:
            response_json = {"name": result["name"],
                             "description": result["description"],
                             "category": result["category"],
                             "price": result["price"],
                             "first_choice": 1}

            return jsonify(response_json), 200

        else: # se non trovo meal cercato, ne cerco un altro della stessa categoria

            result = collection.find_one({"category": category})

            if result: # se ho trovato un piatto della stessa categoria di quella specificata dal client
                response_json = {"name": result["name"],
                                 "description": result["description"],
                                 "category": category,
                                 "price": result["price"],
                                 "first_choice": 0}

                return jsonify(response_json), 200
            else:
                return jsonify({"error": f"Il piatto cercato non è stato trovato. Non è possibile proporti un'alternativa della stessa categoria ({category})"}), 404

    except Exception as e:
        #print(f"Errore durante l'interrogazione: {e}")
        return jsonify({"error": "Errore interno"}), 500

    finally:
        # chiusura connessione al database
        client.close()


@food_routes.route('/manage/delete/<meal>', methods=['DELETE'])
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
    finally:
        # chiusura connessione al database
        client.close()


@food_routes.route('/manage/create', methods=['POST'])
def food_create():
    role = "admin"

    # estraggo, decodifico e verifico la validità del token
    esito = extract_verify_token(request, role)

    # se c'è un errore nel token, restituisco apposito errore
    if esito != True:
        return jsonify(esito), 401

    # recupero dati dal corpo della richiesta
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    category = data.get('category')
    price = int(data.get('price'))

    if not all([name, description, category, price]):
        return jsonify({"error": "Dati incompleti"}), 400

    # verifico che price sia un intero
    if not isinstance(price, int):
        return jsonify({"error": "Il prezzo dev'essere un numero intero"}), 400

    # connessione a MongoDB
    client = connect_to_db()

    # verifico che la connessione sia andata a buon fine
    if client is None:
        return jsonify({"error": "Connessione a MongoDB fallita"}), 500

    db = client[current_app.config["DB_DATABASE"]]
    collection = db[current_app.config["DB_COLLECTION"]]

    try:
        # controllo se il piatto esiste già
        existing_food = collection.find_one({"name": name})
        if existing_food:
            return jsonify({"error": "Il piatto esiste già"}), 409

        # inserisco il nuovo document
        collection.insert_one({
            "name": name,
            "description": description,
            "category": category,
            "price": price
        })

        message = "Piatto creato con successo!"
        return jsonify({"message": message}), 201

    except Exception as e:
        print(f"Errore: {e}")
        return jsonify({"error": "Errore interno"}), 500
    finally:
        # Chiusura connessione al database
        client.close()


@food_routes.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@food_routes.route('/')
def food_service():
    return jsonify({"message":"Welcome to the Food Service via NGINX!"})
