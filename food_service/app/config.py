import os


# configurazione dell'applicazione
class Config:

    # chiave utilizzata per firmare il token (auth_service utilizza la stessa)
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')

    AUTH_SERVICE = os.getenv('AUTH_SERVICE', "auth_service")

    # configurazione da utilizzare per la connessione a MongoDB
    DB_HOST = os.getenv('ME_CONFIG_MONGODB_SERVER', 'mongo_db')  # corrispondente al nome del service in docker-compose
    DB_PORT = os.getenv('ME_CONFIG_MONGODB_PORT', '27017')  # porta di default
    DB_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME', 'admin')
    DB_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD', 'password')
    DB_AUTH_SOURCE = os.getenv('MONGO_AUTH_SOURCE', 'admin') # usato per l'autenticazione
    DB_DATABASE = os.getenv('MONGO_INITDB_DATABASE', 'meals_db')
    DB_COLLECTION = os.getenv('DB_MONGO_COLLECTION', 'meals')
