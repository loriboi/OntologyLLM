from functions import getMovement, dictionary, allcodes

stop = 1
print("STOP per uscire dallo script")
print("MOVEMENTS per visualizzare tutti i possibili componenti e movimenti")
print("CODES per visualizzare i possibili codici per ogni movimento e componente (utili nel funzionamento nel robot per mappare i movimenti)")

while stop:
    text = input("Inserisci una frase da classificare: ")
    if(text == "MOVEMENTS"):
        for key in dictionary.keys():
            print(f"Component: {key}")
            print(f"Possible Movements: {dictionary[key]}")
    elif(text == "CODES"):
        for key in allcodes.keys():
            print(f"key: {key} , value: {allcodes[key]}")
    elif(text == "STOP"):
        stop = 0
    else:
        print(getMovement(text))
    