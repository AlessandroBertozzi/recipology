from src.OntoBuilder import *

if __name__ == "__main__":

    '''INTERAGISCI SOLO CON QUESTA PARTE QUI!!!!'''
    '''--------------------------------------------------------------------------------------'''

    # Indica il numero della versione del tuo file
    # (esempio: Just_food_1 ---> number_of_version = 1
    # (esempio: Just_food_2 ---> number_of_version = 2)
    number_of_version = 1

    # Indica il nome dell'ontologia senza formato del file path e numero di versione
    # (esempio: Just_food_1.owl ---> name_ontology = Just_food
    # (esempio: Just_food_2.owl ---> name_ontology = Just_food
    # (esempio: definitiveversion.owl ---> name_ontology = definitiveversion)
    name_ontology = "Just_food"

    '''--------------------------------------------------------------------------------------'''
    '''--------------------------------------------------------------------------------------'''





    print(f"\n----------------Scraping a lot of things...----------------\n")
    gz = GZScraper()
    list_recipes = gz.recipes_information

    name_file_ontology = f"{name_ontology}_{number_of_version}"
    onto = get_ontology(f"./{name_file_ontology}.owl").load()
    print(f"\n----------------reading ontology {name_file_ontology}.owl----------------\n")

    with onto:
        i = 0
        for name, informations in list_recipes.items():
            i += 1
            print(f"\n{i}/{len(list_recipes)}")
            builder = OntoBuilder(onto, name, informations)
            builder.recipe_class()
            print(f"\n*{name.upper()}*")
            builder.ingredient_class()
            builder.selection_operation_class()
            builder.add_property(onto, name_file_ontology)
            onto.save(f"./{name_ontology}_{number_of_version + 1}.owl")
            print("\n----------------ONTOLOGY SAVED!----------------\n")
