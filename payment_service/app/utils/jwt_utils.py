from flask import current_app, jsonify
import jwt

# funzione che decodifica e verifica validità token JWT
# input: token JWT ; output: se token è valido, restituisce payload in chiaro, altrimenti un errore
def verify_token(token, role):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

        # verifico che l'issuer sia corretto
        if payload.get("iss") != current_app.config['AUTH_SERVICE']: # verifico che il token sia stato generato da auth_service
            return {"error": "Issuer non valido"}
        elif payload.get("role") != role:
            return {"error": "Non sei autorizzato."}

        return True, payload['sub']  # payload è un dizionario
    except jwt.ExpiredSignatureError:
        return {"error": "Token scaduto"}
    except jwt.InvalidTokenError:
        return {"error": "Token non valido"}


def extract_verify_token(request, role="user"):
    # recupero token dall'header Authorization
    auth_header = request.headers.get('Authorization')

    # verifico che nell'header Authorization sia stato inserito un token valido
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token mancante o non valido"}), 401

    # estraggo il token dall'header (rimozione di "Bearer ")
    token = auth_header.split(" ")[1]

    return verify_token(token, role)
