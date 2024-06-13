from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, OWL
from collections import defaultdict
import json
import pprint

body_part_map = {
    ("ZoraLeftArm", "ZoraRightArm"): "BothArms",
    ("ZoraLeftEye", "ZoraRightEye"): "BothEyes",
    ("ZoraLeftHand", "ZoraRightHand"): "BothHands"
}

def initializeOntology():
    path_to_ontology = "ZoraActionsOnto.owl"
    namespace_str = "http://www.semanticweb.org/federico-spiga/ontologies/ZoraActions#"
    ontology_try = ontology(path=path_to_ontology,namespace=namespace_str)
    return ontology_try

def longest_common_prefix(strings):
    if not strings:
        return ""
    shortest_str = min(strings, key=len)
    for i, char in enumerate(shortest_str):
        for other in strings:
            if other[i] != char:
                return shortest_str[:i]
    return shortest_str

def find_code(ZORA, graph, element_uri):
    element = URIRef(element_uri)
    return graph.value(element, ZORA.code)

class ontology:
    def __init__(self,**kwargs):
        self.path = kwargs['path']
        self.ROBOT = Namespace(kwargs['namespace'])
        self.g = Graph()
        self.g.parse(self.path, format="xml")
        self.allElements()
        self.baseActionTitles()
        self.simpleActionTitles()
        self.compundActionTitles()
        self.kindofactions()
        self.baseComponentsAction()
        self.compundComponentsAction()
        self.simpleComponentsAction()
        self.allComponentsAction()
        self.createMap()

    def getBaseActions(self):
        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX zora: <http://www.semanticweb.org/federico-spiga/ontologies/ZoraActions#>

        SELECT ?subClass ?label ?comment
        WHERE {
        ?subClass rdfs:subClassOf zora:BaseAction .
        OPTIONAL { ?subClass rdfs:label ?label }
        OPTIONAL { ?subClass rdfs:comment ?comment }
        }
        """
        # Esegui la query SPARQL
        results = self.g.query(query)

    # Processa i risultati
        subclasses = []
        for row in results:
            subclass_uri = str(row.subClass)
            subclass_name = subclass_uri.split("#")[-1]  # Estrai la parte dopo il '#'
            subclass_info = {
            "name": subclass_name
            }
            subclasses.append(subclass_info)

    # Stampa i risultati
        list_classes = []
        for subclass in subclasses:
            list_classes.append(subclass['name'])

        return list_classes

    def query_action_objects(self,action_type):   
    # Costruisci la query SPARQL dinamicamente
        query_template = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ZoraActions: <http://www.semanticweb.org/federico-spiga/ontologies/ZoraActions#>

        SELECT ?object ?code
        WHERE {
        ?object rdf:type ZoraActions:%s .
        ?object ZoraActions:code ?code .
        }
        """ % action_type

    # Esegui la query SPARQL
        results = self.g.query(query_template)

    # Crea un dizionario per i risultati
        action_codes = {}
        for row in results:
            object_name = str(row.object).split("#")[-1]
            action_codes[object_name] = int(row.code)
        return action_codes

    def getActionsCodes(self,action_types):
        all_actions = {}
        for action_type in action_types:
            all_actions[action_type] = self.query_action_objects(action_type)

        return all_actions
    
    def getCompoundActions(self):
        query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX zora: <http://www.semanticweb.org/federico-spiga/ontologies/ZoraActions#>

    SELECT ?subClass ?label ?comment
    WHERE {
    ?subClass rdfs:subClassOf zora:CompoundAction .
    OPTIONAL { ?subClass rdfs:label ?label }
    OPTIONAL { ?subClass rdfs:comment ?comment }
    }
    """

    # Esegui la query SPARQL
        results = self.g.query(query)

    # Processa i risultati
        subclasses = []
        for row in results:
            subclass_uri = str(row.subClass)
            subclass_name = subclass_uri.split("#")[-1]  # Estrai la parte dopo il '#'
            subclass_info = {
            "name": subclass_name
            }
            subclasses.append(subclass_info)

        # Stampa i risultati
        list_classes = []
        for subclass in subclasses:
            list_classes.append(subclass['name'])

        return list_classes
    
    def individualElements(self):
        # Query SPARQL per ottenere gli URI degli elementi
        query = """
        SELECT ?element
        WHERE {
            ?element rdf:type owl:NamedIndividual .
        }
        """
    # Esegui la query SPARQL
        elements_to_find = []
        for row in self.g.query(query):
            elements_to_find.append(str(row.element))

        elements_with_codes = []
        for element in elements_to_find:
            code = find_code(self.ZORA,self.g, element)
            if code:
                elements_with_codes.append((element.split("#")[-1], code))

        # Separa gli elementi in base alle prime quattro lettere
        grouped_elements = defaultdict(list)
        for element, code in elements_with_codes:
            key = element[:3]
            grouped_elements[key].append((element, code))

        # Trova la parte in comune e rinomina i gruppi
        renamed_groups = {}
        for key, items in grouped_elements.items():
            common_prefix = longest_common_prefix([item[0] for item in items])
            renamed_groups[common_prefix] = items

        # Stampa gli elementi raggruppati con i nuovi nomi dei gruppi
        for group_name, items in renamed_groups.items():
            print(f'Gruppo: {group_name}')
            for element, code in items:
                print(f'  Elemento: {element}, Codice: {code}')
    #aggiunge all'oggetto tutti i gruppi, i nomi dei gruppi, le liste di movimenti per ogni gruppo
    def allElements(self):
        # Query SPARQL per ottenere gli URI degli elementi e il loro tipo
        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?element ?type
        WHERE {
            ?element rdf:type owl:NamedIndividual .
            ?element rdf:type ?type .
            FILTER(?type != owl:NamedIndividual)  # Exclude owl:NamedIndividual type itself
        }
        """
        elements_to_find = []
        for row in self.g.query(query):
            element_uri = str(row.element)
            element_type = str(row.type).split("#")[-1]
            elements_to_find.append((element_uri, element_type))

        elements_with_codes = []
        for element_uri, element_type in elements_to_find:
            code = find_code(self.ROBOT, self.g, element_uri)
            if code:
                elements_with_codes.append((element_uri.split("#")[-1], element_type, code))

        # Separa gli elementi in base al tipo
        grouped_elements = defaultdict(list)
        for element, element_type, code in elements_with_codes:
            grouped_elements[element_type].append((element, code))

        results = {}
        self.grouped_elements = grouped_elements
        # Stampa gl i elementi raggruppati per tipo con nome e codice
        for group_name, items in grouped_elements.items():
            results[group_name] = []
            setattr(self, group_name, [])
            for element, code in items:
                results[group_name].append({element:str(code)})
                getattr(self,group_name).append({element:str(code)})

        self.groups = results
        
        names = []
        for group_name, items in grouped_elements.items():
            names.append(group_name)
        self.groupnames = names
        
        return results
        
    def baseActionTitles(self):
        #get baseAction and set in self
        # Definisci la query SPARQL per estrarre gli URI all'interno dell'elemento owl:unionOf
        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX zora: <http://www.semanticweb.org/federico-spiga/ontologies/ZoraActions#>

        SELECT ?member
        WHERE {
        zora:BaseAction owl:equivalentClass ?equivClass .
        ?equivClass owl:unionOf ?collection .
        ?collection rdf:rest*/rdf:first ?member .
        }
        """

        # Esegui la query SPARQL
        results = self.g.query(query)

        # Estrai l'ultima parte degli URI dai risultati
        last_parts = [str(row.member).split('#')[-1] for row in results]

        baseActions = []
        # Stampa l'ultima parte degli URI
        for part in last_parts:
            baseActions.append(part)

        self.baseActionsList = baseActions
        return

    def simpleActionTitles(self):
        #get simpleAction and set in self
        # Definisci la query SPARQL per estrarre gli URI all'interno dell'elemento owl:unionOf per SimpleAction
        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX zora: <http://www.semanticweb.org/federico-spiga/ontologies/ZoraActions#>

        SELECT ?member
        WHERE {
        zora:SimpleAction owl:equivalentClass ?equivClass .
        ?equivClass owl:unionOf ?collection .
        ?collection rdf:rest*/rdf:first ?member .
        }
        """

        # Esegui la query SPARQL
        results = self.g.query(query)

        # Estrai l'ultima parte degli URI dai risultati
        last_parts = [str(row.member).split('#')[-1] for row in results]

        allactions = []
        # Stampa l'ultima parte degli URI
        for part in last_parts:
            allactions.append(part)

        actions = [azione for azione in allactions if azione not in self.baseActionsList]
        self.simpleActionsList = actions

        return

    def compundActionTitles(self):
        # Definisci la query SPARQL per ottenere gli elementi all'interno dell'elemento owl:unionOf per CompoundAction
        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX zora: <http://www.semanticweb.org/federico-spiga/ontologies/ZoraActions#>

        SELECT ?member
        WHERE {
        zora:CompoundAction owl:equivalentClass ?equivClass .
        ?equivClass owl:unionOf ?collection .
        ?collection rdf:rest*/rdf:first ?member .
        }
        """

        # Esegui la query SPARQL
        results = self.g.query(query)

        # Estrai l'ultima parte degli URI dai risultati
        last_parts = [str(row.member).split('#')[-1] for row in results]
        
        actions = []
        # Stampa l'ultima parte degli URI
        for part in last_parts:
            actions.append(part)
        
        self.compundActionsList = actions

        return        
    
    def kindofactions(self):
        filtered_data = {key: self.groups[key] for key in self.baseActionsList}
        self.baseActions = filtered_data
        # Comprensione di dizionario per estrarre solo le chiavi specificate
        filtered_data = {key: self.groups[key] for key in self.compundActionsList}
        self.compundActions = filtered_data
        filtered_data = {key: self.groups[key] for key in self.simpleActionsList}
        self.simpleActions = filtered_data

    def componentsTitle(self):
        listofcomponents = self.baseActionsList+self.compundActionsList+self.simpleActionsList
        print(listofcomponents)
        removemovements = self.groupnames
        
        movements = [elemento for elemento in removemovements if elemento not in listofcomponents]

        print(movements) 

        return removemovements
    
    def baseComponentsAction(self):
        grouped_results = {}
        for action_class in self.baseActionsList:
            query="""
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX zora: <http://www.semanticweb.org/federico-spiga/ontologies/ZoraActions#>

            SELECT ?action ?involves
            WHERE {{
            ?action rdf:type zora:%s.
            ?action zora:involves ?involves .
            }}
            """ % action_class

            results = self.g.query(query)

            for row in results:
                involves_fragment = str(row.involves).split('#')[-1]
                action_fragment = str(row.action).split('#')[-1].replace("Action", "")  # Rimuoviamo "Action"
        
                if involves_fragment not in grouped_results:
                    grouped_results[involves_fragment] = set()  # Usiamo un set per evitare duplicati
        
                grouped_results[involves_fragment].add(action_fragment)

        # Rimuovi "Action" dal dizionario
        for key, value in grouped_results.items():
            grouped_results[key] = list(value)

        self.baseComponentsActionDict = grouped_results

    def compundComponentsAction(self):
        compund_actions_involvesBoth = {}
        # Itera sulla lista delle classi
        for action_class in self.compundActionsList:
            query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX zora: <http://www.semanticweb.org/federico-spiga/ontologies/ZoraActions#>

            SELECT ?individual ?involvesBoth
            WHERE {{
                ?individual rdf:type zora:{} .
                ?individual zora:involvesBoth ?involvesBoth .
            }}
            """.format(action_class)
            
            results = self.g.query(query)

            # Raggruppa i risultati
            for row in results:
                individual_fragment = str(row.individual).split('#')[-1]
                involvesBoth_fragment = str(row.involvesBoth).split('#')[-1]

                # Aggiungi al dizionario
                if individual_fragment not in compund_actions_involvesBoth:
                    compund_actions_involvesBoth[individual_fragment] = []

                compund_actions_involvesBoth[individual_fragment].append(involvesBoth_fragment)

        # Funzione per sostituire i valori specifici con combinati
        def get_combined_involves(values):
            for (left, right), combined in body_part_map.items():
                if left in values and right in values:
                    values = [v for v in values if v not in {left, right}]
                    values.append(combined)
            return values

        # Raggruppa per involvesBoth combinato
        grouped_by_involvesBoth = {}

        for individual, involves_list in compund_actions_involvesBoth.items():
            combined_involves = get_combined_involves(involves_list)
            combined_involves_key = ','.join(sorted(combined_involves))

            if combined_involves_key not in grouped_by_involvesBoth:
                grouped_by_involvesBoth[combined_involves_key] = []

            grouped_by_involvesBoth[combined_involves_key].append(individual)

        # Stampa i risultati raggruppati
        # Rimuovi "Action" dal dizionario
        for key, value in grouped_by_involvesBoth.items():
            grouped_by_involvesBoth[key] = list(value)

        self.compundComponentsActionDict = grouped_by_involvesBoth

    def simpleComponentsAction(self):
        grouped_results = {}
        for action_class in self.simpleActionsList:
            query="""
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX zora: <http://www.semanticweb.org/federico-spiga/ontologies/ZoraActions#>

            SELECT ?action ?involves
            WHERE {{
            ?action rdf:type zora:%s.
            ?action zora:involves ?involves .
            }}
            """ % action_class

            results = self.g.query(query)

            for row in results:
                involves_fragment = str(row.involves).split('#')[-1]
                action_fragment = str(row.action).split('#')[-1].replace("Action", "")  # Rimuoviamo "Action"
        
                if involves_fragment not in grouped_results:
                    grouped_results[involves_fragment] = set()  # Usiamo un set per evitare duplicati
        
                grouped_results[involves_fragment].add(action_fragment)

        # Rimuovi "Action" dal dizionario
        for key, value in grouped_results.items():
            grouped_results[key] = list(value)
        
        self.simpleComponentsActionDict = grouped_results
    
    def allComponentsAction(self):
        self.allComponentsActionDict = {**self.baseComponentsActionDict,**self.simpleComponentsActionDict,**self.compundComponentsActionDict}
    
    def createMap(self):
        for(part1,part2), combined_part in body_part_map.items():
            for action_list in self.groups.values():
                value1 = value2 = None
                for action in action_list:
                    if part1 in action:
                        value1 = action[part1]
                    elif part2 in action:
                        value2 = action[part2]
                
                if value1 is not None and value2 is not None:
                    combined_value = value1+value2
                    action_list.append({combined_part: combined_value})

        combined_dict = {}
        for key, action_list in self.groups.items():
            for action in action_list:
                combined_dict.update(action)
        
        self.mapcodes = combined_dict
        
    def get_codes(self, listofkeys):
        codes = []
        for key in listofkeys:
            if key in self.mapcodes:
                codes.append(self.mapcodes[key])
        return '-'.join(codes)





