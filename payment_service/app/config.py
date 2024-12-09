import os


# configurazione dell'applicazione
class Config:

    # chiave utilizzata per firmare il token (food_service utilizza la stessa)
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')

    AUTH_SERVICE = os.getenv('AUTH_SERVICE', "auth_service")
    YEAR = os.getenv("YEAR", 2024)

    # configurazione per connessione al db MySQL
    DB_HOST = os.getenv('DB_SQL_HOST', 'mysql-db')
    DB_USER = os.getenv('DB_SQL_USER', 'user')
    DB_PASSWORD = os.getenv('DB_SQL_PASSWORD', 'resu')
    DB_NAME = os.getenv('DB_SQL_NAME', 'foodies_db')
