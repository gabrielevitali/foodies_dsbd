import bcrypt


# input: password in chiaro ; output: valore hash corrispondente
def hash_password(password):

    # genero un salt casuale
    salt = bcrypt.gensalt()

    # genero valore hash mediante il salt casuale
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


# input: password in chiaro e password cifrata ; output: boolean
def verify_password(plain_password, hashed_password):
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Errore durante la verifica della password: {e}")
        return False
