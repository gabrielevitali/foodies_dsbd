from funzioni_validazione import *
from utilities import contatta_server, stampa_menu, stampa_piatto_trovato
from config import *
import json, os


def signup():

    print("\n***Signup***\n")

    # inserimento username, password, email
    username = validazione_input("Inserisci username: ", verifica_username, "Username non valido: deve essere formato da 4 numeri")
    password = validazione_input("Inserisci password: ", verifica_password, "La password deve essere composta da 6 caratteri. Riprova.")
    email = validazione_input("Inserisci email: ", verifica_email, "L'email dev'essere nel formato esempio@email.com. Riprova.")
    admin = validazione_input("Sei admin? (Y/N) ", verifica_risposta_yes_no, "Risposta non valida: inserisci Y/y oppure N/n")

    admin = 1 if admin.lower() == 'y' else 0

    # creo dizionario con dati inseriti in input
    dati = {"username": str(username), "password": str(password), "email": str(email), "admin": admin}

    # client invia al server la password in chiaro
    # (importante: per garantire sicurezza occore usare https)
    # ciò evita attacchi di tipo replay
    # server memorizza in db mysql password cifrata

    esito, risposta = contatta_server(PATH_SIGNUP, json.dumps(dati), method = "POST")

    r = json.loads(risposta)

    if(esito):

        print("\n", r["message"], "\n")

    else:
        print("\n", r['error'], "\n")

        from main import main  # per evitare errore di import circolare
        main()    


def login():

    print("\n***Login***\n")
    
    # inserimento username e password
    username = validazione_input("Inserisci codice ID: ", verifica_username, "ID non valido: deve essere formato da 4 numeri")
    password = validazione_input("Inserisci password: ", verifica_password, "La password deve essere composta da 6 caratteri. Riprova.")

    # creo dizionario con dati inseriti in input
    dati = {"username": str(username), "password": str(password)}

    # password: stesse considerazione fatte per il signup

    esito, risposta = contatta_server(PATH_LOGIN, json.dumps(dati), method = "POST")

    r = json.loads(risposta)

    if(esito): 

        os.environ['TOKEN'] = r["token"]
        print("\n", r["message"], "\n")

    else:
        print("\n", r['error'], "\n")

        from main import main  # per evitare errore di import circolare
        main()    

    
def search_meal():

    print("\n***Cerca piatto***\n")

    # inserimento nome piatto
    meal = validazione_input("Inserisci il nome del piatto desiderato: ", verifica_nome_piatto, "Il nome del piatto può contenere solo caratteri alfabetici")

    # inserimento categoria piatto
    category = validazione_input("Inserisci la categoria del piatto desiderato: ", verifica_categoria_piatto, "La categoria del piatto può contenere solo caratteri alfabetici")

    dati = {"meal": meal, "category": category}

    esito, risposta = contatta_server(PATH_SEARCH_MEAL, json.dumps(dati), token=os.getenv('TOKEN'), method = "POST")

    r = json.loads(risposta)

    if(esito): 

        if r['first_choice'] == 0:
            print("Il piatto cercato non è stato trovato, ma ti proponiamo la seguente alternativa:")
        else:
            print("Ecco i dettagli del piatto richiesto: ")
            
        stampa_piatto_trovato(r)

        risposta = validazione_input("Vuoi procedere con l'ordine? (Y/N) ", verifica_risposta_yes_no, "Risposta non valida: inserisci Y/y oppure N/n")

        if risposta == "Y" or "y":
            return r
        else:
            from main import main  # per evitare errore di import circolare
            main()  
    else:
        print("\n", r["error"], "\n")
        from main import main
        main()    


def create_order(dati):

    print("\n***Crea ordine***\n")

    esito, risposta = contatta_server(PATH_CREATE_ORDER, json.dumps(dati), token=os.getenv('TOKEN'), method = "POST")

    r = json.loads(risposta)

    if(esito): 
        print("\n", r["message"], "\n")

    else:
        print("\n", r['error'], "\n")

        from main import main  # per evitare errore di import circolare
        main()    


def check_order_status():

    print("\n***Monitora stato dell'ordine***\n")

    # inserimento order id
    order_id = input("Inserisci id dell'ordine che vuoi monitorare: ")

    esito, risposta = contatta_server(PATH_CHECK_ORDER_STATUS+ '/' + order_id, token=os.getenv('TOKEN'), method = "GET")

    r = json.loads(risposta)

    if(esito):
        order_id = r["order_id"]
        status = r["status"]

        print(f"\nIl tuo ordine {order_id} ha stato: {status} .\n")

    else:
        print("\n", r['error'], "\n")

        from main import main  # per evitare errore di import circolare
        main()    


def add_credit():

    print("\n***Ricarica credito***\n")
    
    # inserimento credito
    credito = input("Di quanto vuoi ricaricare il tuo credito? €")
    
    # creo dizionario con dati inseriti in input
    dati = {"credit": str(credito)}

    esito, risposta = contatta_server(PATH_ADD_CREDIT, json.dumps(dati), token=os.getenv('TOKEN'), method = "POST")

    r = json.loads(risposta)

    if(esito):

        print("\n", r["message"], "\n")

    else:
        print("\n", r['error'], "\n")

        from main import main  # per evitare errore di import circolare
        main()    


def check_month_total():
    
    print("\n***Verifica spesa totale nel mese specificato***\n")

     # inserimento mese
    month = input("Inserisci il mese per cui voi calcolare la spesa totale (numero da 1 a 12): ")

    esito, risposta = contatta_server(PATH_MONTH_TOTAL + "/" + month, token=os.getenv('TOKEN'), method = "GET")

    r = json.loads(risposta)

    if(esito):

        print("\n", r["message"], "\n")

    else:
        print("\n", r['error'], "\n")

        from main import main  # per evitare errore di import circolare
        main()    


def crea_piatto():
    
    print("\n***Crea piatto***\n")

    # inserimento nome piatto
    name = validazione_input("Inserisci il nome del piatto che vuoi creare: ", verifica_nome_piatto, "Il nome del piatto può contenere solo caratteri alfabetici")
    description = input("Inserisci descrizione: ")
    category = input("Inserisci categoria: ")
    price = input("Inserisci prezzo: ")

    dati = {"name": name, "description": description, "category": category, "price": price}

    esito, risposta = contatta_server(PATH_MANAGE_MEALS + '/create', json.dumps(dati), os.getenv('TOKEN'), "POST")

    r = json.loads(risposta)

    if(esito): 
        print(f"\nPiatto '{name}' inserito con successo.\n")
        routine_gestisci_piatti()
    else:
        print("\n", r['error'], "\n")

        from main import main  # per evitare errore di import circolare
        main()    


def elimina_piatto():
    
    print("\n***Elimina piatto***\n")

    # inserimento nome piatto
    meal = validazione_input("Inserisci il nome del piatto che vuoi cancellare: ", verifica_nome_piatto, "Il nome del piatto può contenere solo caratteri alfabetici")

    esito, risposta = contatta_server(path=PATH_MANAGE_MEALS + '/delete/' + meal, token=os.getenv('TOKEN'), method="DELETE")

    print("\n" + risposta)

    if esito:  # se l'esito è positivo, stampa una risposta di successo
            print(f"\nPiatto '{meal}' eliminato con successo.")
            routine_gestisci_piatti()
    else:
        print(f"\nErrore: {risposta}")
        routine_gestisci_piatti()


def routine_gestisci_piatti():

    print("\n***Gestisci piatti***\n")

    stampa_menu(opzioni_menu_gestisci_piatti)
    opzione = input("Scelta: ")
    while opzione != 4:
        try:
            opzione = int(opzione)
            if opzione == 1:
                crea_piatto()
            elif opzione == 2:
                elimina_piatto()
            elif opzione == 3:
                from main import main
                main()
            elif opzione == 4:
                print("Grazie per aver utilizzato Foodies!")
                exit()
            else:
                raise ValueError
        except ValueError:
            print("\nHai inserito un'opzione non valida. Riprova.")


opzioni_menu_gestisci_piatti = ["1. Crea nuovo piatto" , "2. Elimina piatto ", "3. Torna al menù principale", "4. Esci da Foodies\n"]

