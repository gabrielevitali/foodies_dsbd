URL = "http://localhost:80/" # indirizzo e porta di ascolto dell'API Gateway 


# elenco path

# Authentication Service
PATH_LOGIN = "/auth/login"
PATH_SIGNUP = "/auth/signup"

# Food Service
PATH_SEARCH_MEAL = "/food/search" # solo user
PATH_MANAGE_MEALS = "/food/manage" # solo admin

# Order Service
PATH_CREATE_ORDER = "order/create"
PATH_CHECK_ORDER_STATUS = "order/status"

# Payment Service
PATH_ADD_CREDIT = "payment/add"
PATH_MONTH_TOTAL = "payment/total/month"


# elenco regex
REGEX_USERNAME = "^[A-Za-z0-9]{3,10}$"
REGEX_PASSWORD = "^[A-Za-z0-9]{3,10}$"
REGEX_EMAIL = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
REGEX_ADMIN = "^[yYnN]{1}$"
REGEX_NOME_PIATTO = "^[a-zA-Z ]{1,30}$" 
REGEX_CATEGORIA_PIATTO = "^[a-zA-Z ]{1,30}$"