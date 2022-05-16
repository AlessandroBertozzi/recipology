from src.utility.OntologyBuilder_func import *


class OntoBuilder:

    def __init__(self, onto, name, informations):
        self.onto = onto
        self.class_created = dict()
        self.name_recipe = name
        self.information = informations
        self.category_ingredient = {
            "1": onto.Ingredient_group_1,
            "2": onto.Ingredient_group_2,
            "3": onto.Ingredient_group_3,
            "4": onto.Ingredient_group_4,
            "5": onto.Ingredient_group_5,
            "6": onto.Beverage,
            "7": onto.Condiment,
        }

    def recipe_class(self):
        # self.class_created["recipes"] = list()

        if find_class(self.onto, self.name_recipe) is None:

            create_new_class(self.name_recipe, find_class(self.onto, self.information["category"]))

            # self.class_created["recipes"].append(self.name_recipe)

    def ingredient_class(self):

        find_class(self.onto, self.information["category"])

        for ingredient in self.information["Ingredient"]:

            if find_class(self.onto, ingredient[0]) is None:
                category = input(f'\nWhat is the category of {ingredient[0].upper()}?\n\n'
                                 '1. Cereali e derivati, tuberi\n'
                                 '2. Frutta e ortaggi\n'
                                 '3. Latte e derivati\n'
                                 '4. Carne, Pesci, Uova e Legumi\n'
                                 '5. Grassi e Oli da condimento\n'
                                 '6. Bere\n'
                                 '7. Condimenti\n\n'
                                 'insert only the number ----> ').strip()

                self.category_ingredient[category](ingredient[0].replace(" ", "_").replace("'", "_").replace("(", "_").replace(")", "").replace("®", ""))


    def selection_operation_class(self):

        # self.class_created["selection_operation"] = list()

        if find_class(self.onto, "Selection_name") is None:

            create_new_class(f"Selection_name", self.onto.SelectionOperation)

        if find_class(self.onto, f"{self.name_recipe}_selection") is None:

            create_new_class(f"{self.name_recipe}_selection", self.onto.Selection_name)

            # self.class_created["selection_operation"].append(self.name_recipe)


    def add_property(self, onto):

        with onto:
            list_ingredients = list()
            name_class = find_class(onto, f"{self.name_recipe}_selection")

            for ingredient in self.information["Ingredient"]:
                ingredient = find_class(onto, ingredient[0].replace(" ", "_").replace("'", "_").replace("(", "_").replace(")", "").replace("®", ""))
                list_ingredients.append(str(ingredient).replace("definitiveversion", "onto").strip())


            list_ingredients = " , ".join(list_ingredients)
            list_ingredients = "[" + list_ingredients + "]"
            print(list_ingredients)
            name_class.is_a.append(onto.hasIngredient.only(OneOf(eval(list_ingredients))))
