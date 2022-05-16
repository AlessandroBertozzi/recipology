from src.OntoBuilder import *






if __name__ == "__main__":


    onto = get_ontology("./definitiveversion.owl").load()

    gz = GZScraper()
    list_recipes = gz.recipes_information

    with onto:
        for name, informations in list_recipes.items():
            builder = OntoBuilder(onto, name, informations)
            builder.recipe_class()
            builder.ingredient_class()
            builder.selection_operation_class()
            builder.add_property(onto)
            onto.save("./Just_food_1.owl")
            print("ontology saved!")
            break


