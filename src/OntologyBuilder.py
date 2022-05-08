from owlready2 import *
from src.Scraper import GZScraper



def main():
    onto = get_ontology("./definitiveversion.owl").load()

    gz = GZScraper()
    list_recipes = gz.recipes_information

    # * class creation
    for name_recipe, informations in list_recipes.items():
        with onto:

            category_ingredient = {
                "1": onto.Ingredient_group_1,
                "2": onto.Ingredient_group_2,
                "3": onto.Ingredient_group_3,
                "4": onto.Ingredient_group_4,
                "5": onto.Ingredient_group_5,
            }
            print(name_recipe)
            create_new_class(name_recipe, find_class(onto, informations["category"]))

            for ingredient in informations["Ingredient"]:
                # category = input(f'What is the category of { ingredient[0] } (insert only the number)?\n'
                #                  '1. Cereali e derivati, tuberi\n'
                #                  '2. Frutta e ortaggi\n'
                #                  '3. Latte e derivati\n'
                #                  '4. Carne, Pesci, Uova e Legumi\n'
                #                  '5. Grassi e Oli da condimento\n').strip()
                # create_new_class(ingredient[0].replace(" ", "_"), category_ingredient[category])
                create_new_class(ingredient[0].replace(" ", "_").replace("'", "_").replace("(", "_").replace(")", "").replace("®", ""), onto.Ingredient_name)



    # * property creation
    for name_recipe, informations in list_recipes.items():
        list_ingredients = list()
        with onto:
            name_class = find_class(onto, name_recipe)

            for ingredient in informations["Ingredient"]:
                ingredient = find_class(onto, ingredient[0].replace(" ", "_").replace("'", "_").replace("(", "_").replace(")", "").replace("®", ""))
                name_class.is_a.append(onto.hasIngredient.some(ingredient))
                list_ingredients.append(str(ingredient).replace("definitiveversion", "onto").strip())


            list_ingredients = " & ".join(list_ingredients)
            print(list_ingredients)
            name_class.is_a.append(onto.hasIngredient.only(eval(list_ingredients)))









    for my_class in onto.classes():

        if my_class is onto.Antipasti:
            print(onto.search(subclass_of=onto.Primi))
            print(onto.search(subclass_of=onto.Ingredient_group_3))

    onto.save("./Just_food.owl")


def create_new_class(name, upper_class):
    types.new_class(name, (upper_class,))


def find_class(onto, name):
    for onto_class in onto.classes():
        # print(str(onto_class).split(".")[1].lower(), name.lower())
        if str(onto_class).split(".")[1].lower() == name.lower():



            return onto_class


