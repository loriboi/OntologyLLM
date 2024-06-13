# Integration with LLM (1)

## Description

This repository contains files for integrating with an LLM (Large Language Model) to classify actions. The files and their purposes are described below.

## Files in the Repository

- **app.py**: Creates a server with the `/getmovement` endpoint for calls from Zora.
- **config.py**: Allows you to insert the OpenAI API key.
- **functions.py**: Manages the function calling.
- **ontology_class.py**: Manages the ontology.
- **test.py**: Can be run to perform tests on the functions.
- **ZoraActionsOnto.owl**: Ontology of movements.
- **requirements.txt**: Used to install the necessary libraries.

## Setup

### Create the Environment and Install Libraries

1. Download the repository:
```bash
git clone https://github.com/loriboi/OntologyLLM.git
```
2. Set up the environment and install the requirements
```bash
cd OntologyLLM
python -m venv env
cd env/Scripts
activate
cd ../..
pip install -r requirements.txt
```
3. Edit config.py to insert the apiKey="your apikey" (recommended gpt-3.5-turbo-16k)
4. Start the test script:
```bash
python test.py
``` 
   - MOVEMENTS to obtain the all possible movements of the robot
   - CODES to obtain all the associated codes
   - STOP for exit the script
   - a generic command "eg. Hey Zora, raise your arms", to obtain the classification
   - If you ask something that is not a command you will obtain a delfault keyword "ASKGPT"

