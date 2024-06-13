Integration with LLM (1)

Nella repository sono presenti diversi files:
- app.py crea un server con l'endpoint /getmovement per la chiamata che avverrà da zora
- config.py dove è possibile inserire l'apikey di openai
- functions.py si occupa di gestire le function calling
- ontology_class.py si occupa di gestire l'ontologia
- test.py può essere lanciato per effettuare i test sulle functions
- ZoraActionsOnto.owl ontologia dei movimenti
- requirements.txt serve per installare le librerie necessarie

Il primo step da fare è creare l'environment e installare le librerie 
 python -m venv env
 python env/Scripts
 activate
 cd ../..
 pip install -r requirements.txt

Dopodichè si è pronti per lanciare il test.py  
 python test.py

A questo punto si può chiedere di classificare delle azioni

NB: non sono stati gestiti i colori degli occhi
