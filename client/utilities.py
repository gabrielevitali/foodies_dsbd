import requests, bcrypt
from config import URL


def stampa_menu(strings):
    for string in strings:
        print(string)
        

def stampa_piatto_trovato(piatto):

        print("\n\t\tnome piatto: " + piatto['name'])
        print("\t\tcategoria: " + piatto['category'])
        print("\t\tdescrizione: " + piatto['description'])
        print("\t\tprezzo: €" + str(piatto['price']) + "\n")
        

def gestione_errori(funzione):
    def wrapper(*args, **kwargs):
        try:
            return funzione(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            print("\nErrore durante la richiesta al server:", e)
            print("\nChiusura in corso...")
            exit()
    return wrapper


@gestione_errori 
def contatta_server(path, dati=None, token=None, method = "GET"):
    
    headers = {
        "Content-Type": "application/json"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    if method == "GET":
        r = requests.get(URL + path, headers=headers)
    elif method == "POST":
        r = requests.post(URL + path, data=dati, headers=headers)
    elif method == "DELETE":
        r = requests.delete(URL+path, headers=headers)

    if r.status_code in [200,201]:
        return True, r.text
    else:
        return False, r.text