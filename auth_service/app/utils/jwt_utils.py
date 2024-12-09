from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from flask import current_app
import jwt


# funzione che genera un JWT per un dato utente, associando una firma digitale
# input: username ; output: token JWT firmato
def generate_token(username, admin):

    current_local_time = datetime.now(timezone.utc).astimezone(ZoneInfo("Europe/Rome"))

    role = "user" if admin == 0 else "admin"

    payload = {
        "sub": username,  # subject
        "iss": "auth_service",  # issuer che ha rilasciato il token
        "iat": current_local_time,  # timestamp di emissione del token
        "exp": current_local_time + timedelta(hours=current_app.config['DEFAULT_HOURS']),  # timestamp di scadenza (es. 3 ore)
        "role": role  # ruolo per discriminare user generico da admin
    }

    # genera il token firmato con la SECRET_KEY
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

    return token
