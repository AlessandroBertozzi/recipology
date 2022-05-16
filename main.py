from src.OntoBuilder import *

if __name__ == "__main__":

    number_of_recipes = 2
    onto = get_ontology("./definitiveversion.owl").load()

    gz = GZScraper()
    list_recipes = gz.recipes_information

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
            builder.add_property(onto)
            onto.save("./Just_food_1.owl")
            print("\n----------------ONTOLOGY SAVED!----------------\n")
            if i == number_of_recipes:
                break
