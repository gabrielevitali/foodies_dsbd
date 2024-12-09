from utilities import stampa_menu
from funzioni import *


def main():
    token = None

    stampa_menu(opzioni_menu_avvio)
    opzione = input("Scelta: ")

    while opzione != 8:
        try:
            opzione = int(opzione)
            if opzione == 1:
                signup()
            elif opzione == 2:
                login()
            elif opzione == 3:
                piatto = search_meal() # solo user generico
                create_order(piatto)
            elif opzione == 4:
                check_order_status() # solo user generico
            elif opzione == 5:
                add_credit() # solo user generico
            elif opzione == 6:
                check_month_total() # solo user generico        
            elif opzione == 7:
                routine_gestisci_piatti() # solo admin
            elif opzione == 8:
                print("\nGrazie per aver utilizzato Foodies! Arrivederci!")
                exit()
            else:
                raise ValueError
        except ValueError:
            print("Inserisci un'opzione valida")

        opzione = input("Scelta: ")


opzioni_menu_avvio = ["\nBenvenuto in Foodies!\n", "1. Signup" , "2. Login", "3. Cerca piatto [user]", "4. Monitora stato dell'ordine [user]", "5. Ricarica il tuo credito [user]", "6. Verifica la cifra totale spesa nel mese specificato [user]", "7. Gestisci piatti [admin]", "8. Esci da Foodies\n"]

        
if __name__ == "__main__":
    main()
