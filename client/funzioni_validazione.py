import re
from config import * 

def validazione_input(messaggio_input, funzione_validazione, messaggio_errore):
    while True:
        dato = input(messaggio_input)
        if funzione_validazione(dato):
            return dato
        print(messaggio_errore)
        
def verifica_username(username):

    if re.match(REGEX_USERNAME, str(username)) != None:
        return True
    
    return False

def verifica_password(password):

    if re.match(REGEX_PASSWORD, password) != None:
        return True
    
    return False

def verifica_email(email):
    
    if re.match(REGEX_EMAIL, email) != None:
        return True
    
    return False

def verifica_risposta_yes_no(admin):

    if re.match(REGEX_ADMIN, str(admin)) != None:
        return True
    
    return False

def verifica_nome_piatto(nome):

    if re.match(REGEX_NOME_PIATTO, str(nome)) != None:
        return True
    
    return False

def verifica_categoria_piatto(nome):

    if re.match(REGEX_CATEGORIA_PIATTO, str(nome)) != None:
        return True
    
    return False

def verifica_order_id(order_id):

    return True if len(order_id) == 5 else False   
    
