import rdflib
import ontology_class
from ontology_class import ontology
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, OWL

path_to_ontology = "ZoraActionsOnto.owl"
namespace_str = "http://www.semanticweb.org/federico-spiga/ontologies/ZoraActions#"
ontology_try = ontology(path=path_to_ontology,namespace=namespace_str)
print(ontology_try.allComponentsActionDict)