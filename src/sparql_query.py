import owlready2
from owlready2 import *
import random


def main():
    onto = get_ontology("../static/prova_2.owl").load()





def query_for_selection_individuals():
    onto = get_ontology("../static/prova_2.owl").load()
    query = list(default_world.sparql("""
            PREFIX rc: <http://www.semanticweb.org/veronicabertozzi/ontologies/2022/3/untitled-ontology-45#>
            SELECT  ?subject ?value
            WHERE { ?subject rdf:type ?object .
            ?object owl:onProperty rc:hasSelectionOperation .
            ?object owl:hasValue ?value .
            }"""))

    dict_with_results = dict()
    for record in query:
        if record[0].name not in dict_with_results:
            dict_with_results[record[0].name] = list()
        dict_with_results[record[0].name].append((record[1].hasIngredient[0].name, record[1].hasQuantity[0]))

    print(dict_with_results)


def query_for_categories():
    pass



def query_for_inferred_categories():
    # owlready2.JAVA_EXE = "C:\\Program Files\\Java\\jre1.8.0_333\\bin\\java.exe"
    # sync_reasoner_hermit(infer_property_values=True)
    pass


if __name__ == '__main__':
    query_for_selection_individuals()
