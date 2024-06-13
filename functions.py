import os
import json
import openai
from datetime import datetime, timedelta
from openai import OpenAI
import requests
from ontology_class import initializeOntology, ontology
from config import apiKey

o = initializeOntology()
dictionary = o.allComponentsActionDict
allcodes = o.mapcodes



client = OpenAI(api_key=apiKey)

class MovimentoNonRiconosciuto(Exception):
    def __init__(self, messaggio):
        super().__init__(messaggio)
        self.messaggio = messaggio

function_descriptions = [
    {
        "name": "get_movement_info",
        "description": "Get the component and the movement from the dictionary"+str(dictionary),
        "parameters": {
            "type": "object",
            "properties": {
                "component": {
                    "type": "string",
                    "description": "The component to move, e.g. ZoraHead",
                },
                "movement": {
                    "type": "string",
                    "description": "The movement, e.g. left",
                }
            },
            "required": ["component", "movement"],
        },
    }
]

def get_movement_info(component, movement):
    """Get the component and the movement from the dictionary"""
    infos = {
        "component": component,
        "movement": movement
    }

    return json.loads(infos)


def getCommand(user_prompt):
    try:
        completion = client.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                messages=[{"role": "user", "content": user_prompt}],
                functions=function_descriptions,
                function_call="auto",
            )
        output = completion.choices[0].message
        component = json.loads(output.function_call.arguments).get("component")
        movement = json.loads(output.function_call.arguments).get("movement")
        list_components = [component, movement]
        return list_components
    except AttributeError:
        print("Nessun movimento disponibile")
        return "Default"

def inference(user_prompt):
    try:
        result = getCommand(user_prompt)
        if result is None:
            result = "Default"
        else:
            print(result)
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
    finally:
        return result
    
def codes(user_list):
    str = o.get_codes(user_list)
    return str

def getMovement(user_prompt):
    result = inference(user_prompt)
    if result != "Default":
        code = codes(result)
        return code
    else:
        code = "ASKGPT"
        return code