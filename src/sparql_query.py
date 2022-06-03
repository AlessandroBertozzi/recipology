import owlready2
from owlready2 import *
import random
import pickle


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
            dict_with_results[record[0].name] = {"Ingredients": list()}
        dict_with_results[record[0].name]["Ingredients"].append((record[1].hasIngredient[0].name, record[1].hasQuantity[0]))

    return dict_with_results


def query_for_categories():
    onto = get_ontology("../static/prova_2.owl").load()

    categories = list(default_world.sparql("""
            PREFIX rc: <http://www.semanticweb.org/veronicabertozzi/ontologies/2022/3/untitled-ontology-45#>
            SELECT  ?subject 
            WHERE { ?subject rdfs:subClassOf rc:ByCategory .
            ?subject rdf:type owl:Class .

            }"""))

    tmp_dict = dict()



    for category in categories:
        for name_recipe in category[0].instances():
            if category[0] not in tmp_dict:
                tmp_dict[name_recipe.name] = category[0].name

    return tmp_dict


def combination_category_informations_of_individuals():
    onto = get_ontology("../static/prova_2.owl").load()

    recipes = query_for_selection_individuals()
    categories = query_for_categories()

    for recipe, category in categories.items():

        recipes[recipe]["Category"] = [category]

    return recipes



def query_for_inferred_categories():
    onto_1 = get_ontology("../static/prova_2.owl").load()

    recipe_inferred_categories = list(default_world.sparql("""
            PREFIX rc: <http://www.semanticweb.org/veronicabertozzi/ontologies/2022/3/untitled-ontology-45#>
            SELECT  ?subject 
            WHERE { ?subject rdfs:subClassOf rc:Recipe_by_category .
            }"""))
    general_dict = combination_category_informations_of_individuals()

    onto_2 = get_ontology("../static/recipology_inferred.owl").load()

    with onto_2:
        for category in recipe_inferred_categories:
            for recipe in set(category[0].instances()):
                if "Inferred_categories" not in general_dict[recipe.name].keys():
                    general_dict[recipe.name]["Inferred_categories"] = list()
                general_dict[recipe.name]["Inferred_categories"].append(category[0].name)
    return general_dict











if __name__ == '__main__':
    pass
    # inferred_query = query_for_inferred_categories()
    # normal_query = combination_category_informations_of_individuals()
    # with open('../static/inferred_query.pickle', 'wb') as handle:
    #     pickle.dump(inferred_query, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # with open('../static/normal_query.pickle', 'wb') as handle:
    #     pickle.dump(normal_query, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # # print(combination_category_informations_of_individuals())
