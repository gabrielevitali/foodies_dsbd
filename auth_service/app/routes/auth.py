from flask import Blueprint, jsonify, request
from app.services.db_service import connect_to_db
from app.utils.hash_utils import hash_password, verify_password
from app.utils.jwt_utils import generate_token


auth_routes = Blueprint('auth', __name__)


@auth_routes.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@auth_routes.route('/', methods=['GET'])
def auth_service():
    return jsonify({"message":"Welcome to the Auth Service via NGINX!"})


@auth_routes.route('/signup', methods=['POST'])
def signup():

    # recupero dati dal body della richiesta
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")  # password in chiaro (per evitare replay attack)
    email = data.get("email")  # solo per potenziali usi futuri
    admin = data.get("admin")  # valore di default: False

    # verifico se username o password siano mancanti
    if not username or not password or not email:
        return jsonify({"error": "Username/password/email/admin mancante"}), 400

    # connessione al database
    connection = connect_to_db()

    if not connection:
        return jsonify({"error": "Connessione al DB fallita"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # controllo se l'username ricevuto sia già in uso
        cursor.execute("SELECT username FROM Utenti WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({"error": "Username già in uso"}), 409  # conflict

        hashed_password = hash_password(password)  # genera l'hash della password

        credito = 400 if admin == 0 else 0

        # inserimento del nuovo utente
        cursor.execute(
            "INSERT INTO Utenti (username, password, email, admin, credito) VALUES (%s, %s, %s, %s, %s)",
            (username, hashed_password, email, admin, credito)
        )

        connection.commit()

        return jsonify({"message": "Registrazione completata con successo!"}), 201  # utente creato

    except Exception as e:
        print(f"Errore durante la registrazione: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Errore interno"}), 500
    finally:
        cursor.close()
        connection.close()

@auth_routes.route('/login', methods=['POST'])
def login():

    # recupero dati dal body della richiesta
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")  # password in chiaro (per evitare replay attack)

    # verifico se username o password siano mancanti
    if not username or not password:
        return jsonify({"error": "Username o password mancante"}), 400

    connection = connect_to_db()
    if not connection:
        return jsonify({"error": "Connessione al DB fallita"}), 500

    try:
        cursor = connection.cursor(dictionary=True)  # restituisce risultati in forma di dizionario
        cursor.execute("SELECT password, admin FROM Utenti WHERE username = %s", (username,))
        user_db = cursor.fetchone()

        if user_db: # se è stato trovato username cercato
            if verify_password(password, user_db["password"]): # se le password corrispondono:
                token = generate_token(username, user_db["admin"])
                return jsonify({"message": "Login eseguito con successo", "token": token}), 200
            else:
                import traceback
                traceback.print_exc()
                return jsonify({"error": "Password errata"}), 401
        else: # se l'username cercato non è stato trovato
            return jsonify({"error": "Username non trovato"}), 401
    finally:
        cursor.close()
        connection.close()
