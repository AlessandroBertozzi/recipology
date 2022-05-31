from src.utility.OntologyBuilder_func import *


class OntoBuilder:

    def __init__(self, onto, name, informations):
        self.onto = onto
        self.class_created = dict()
        self.name_recipe = name.replace(" ", "_").replace("'", "_").replace("(", "_").replace(")", "").replace("®",
                                                                                                               "")
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

    def recipe_individuals(self, onto):

        with onto:
            if find_class(self.onto, self.name_recipe) is None:
                one_selection_operation = find_class(self.onto, self.information["category"])(self.name_recipe)
                return True
            return False

    def ingredient_class(self):

        # find_class(self.onto, self.information["category"])

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

                self.category_ingredient[category](
                    ingredient[0].replace(" ", "_").replace("'", "_").replace("(", "_").replace(")", "").replace("®",
                                                                                                                 ""))

    def selection_operation_individuals(self, onto, name_file_ontology):

        # self.class_created["selection_operation"] = list()
        with onto:
            # selection_operation_name = find_class(self.onto, f"Selection_operation")
            # selection_operation_name = f"onto.{str(selection_operation_name.name)}"
            recipe_name = find_class(self.onto, f"{self.name_recipe}")

            list_selection_operation = list()
            for ingredient in self.information["Ingredient"]:
                one_selection_operation = onto.Selection_operation()
                ingredient_name = find_class(onto,
                                             ingredient[0].replace(" ", "_").replace("'", "_").replace("(",
                                                                                                       "_").replace(
                                                 ")", "").replace("®", ""))
                one_selection_operation.hasIngredient = [ingredient_name]
                one_selection_operation.hasQuantity = [ingredient[1]]

                list_selection_operation.append(
                    str(one_selection_operation).replace(name_file_ontology, "onto").strip())

                recipe_name.is_a.append(self.onto.hasSelectionOperation.value(one_selection_operation))


        # self.class_created["selection_operation"].append(self.name_recipe)

    def add_property(self, onto, name_file_ontology):

        with onto:
            list_ingredients = list()
            name_class = find_class(onto, f"{self.name_recipe}")

            for ingredient in self.information["Ingredient"]:
                ingredient = find_class(onto,
                                        ingredient[0].replace(" ", "_").replace("'", "_").replace("(", "_").replace(")",
                                                                                                                    "").replace(
                                            "®", ""))
                list_ingredients.append(str(ingredient).replace(name_file_ontology, "onto").strip())

                name_class.is_a.append(
                    onto.hasIngredient.some(OneOf([eval(str(ingredient).replace(name_file_ontology, "onto"))])))

            list_ingredients = " , ".join(list_ingredients)
            list_ingredients = "[" + list_ingredients + "]"
            # print(list_ingredients)
            name_class.is_a.append(onto.hasIngredient.only(OneOf(eval(list_ingredients))))
