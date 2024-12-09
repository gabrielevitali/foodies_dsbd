import os

# configurazione dell'applicazione
class Config:

    # chiave utilizzata per firmare il token (food_service utilizza la stessa)
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')

    # configurazione per connessione al db MySQL
    DB_HOST = os.getenv('MYSQL_HOST', 'mysql-db')
    DB_NAME = os.getenv('MYSQL_DATABASE', 'foodies_db')
    DB_USER = os.getenv('MYSQL_USER', 'user')
    DB_PASSWORD = os.getenv('MYSQL_PASSWORD', 'resu')

    # configurazione applicazione
    DEFAULT_CREDIT = os.getenv('DEFAULT_CREDIT', 400.00)
    DEFAULT_HOURS = os.getenv("DEFAULT_HOURS", 3)
