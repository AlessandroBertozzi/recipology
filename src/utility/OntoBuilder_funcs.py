from owlready2 import *


def add_Recipes_classes(onto, name_recipe, informations):
    with onto:
        class Recipes(Thing):
            pass

        class ByCourse(Recipes):
            pass

        Recipes.label.append("Recipes")
        ByCourse.label.append("Recipes by course")


def add_Recipes_courses_categories(onto, name_recipe, informations):
    with onto:

        types.new_class(informations["category"], (onto.ByCourse,))

        onto.search(iri=f"*{informations['category']}")[0].label.append(informations["category"])


def add_recipes_instances(onto, informations, name_recipe):
    with onto:
        name_instance = onto.search(iri=f"*{informations['category']}")[0](name_recipe)
        name_instance.label.append(name_recipe.replace("_", " "))


def add_selection_operation_class(onto, name_recipe, informations):
    with onto:

        class Selection_operation(Thing):
            pass

        Selection_operation.label.append("Selection operation")


def add_base_property(onto, name_recipe, informations):
    with onto:
        class hasSelectionOperation(ObjectProperty):
            pass

        class hasIngredient(ObjectProperty):
            pass

        class hasQuantity(DataProperty):
            range = [str]

        class withIngredient(ObjectProperty):
            pass

    hasSelectionOperation.label.append("Has selection operation")
    hasIngredient.label.append("has ingredient")
    hasQuantity.label.append("has quantity")
    withIngredient.label.append("with ingredient")


def add_selection_operation_instances(onto, name_recipe, informations):
    with onto:
        print(name_recipe)
        recipe_name = onto.search(iri=f"*{name_recipe}")[0]

        list_selection_operation = list()
        for ingredient in informations["Ingredient"]:
            one_selection_operation = onto.Selection_operation()

            ingredient_name = ingredient[0].replace(" ", "_").replace("'", "_").replace("(", "_").replace(")",
                                                                                                          "").replace(
                "®", "")
            ingredient_name = onto.search(iri=f"*{ingredient_name}")[0]

            one_selection_operation.hasIngredient = [ingredient_name]
            one_selection_operation.hasQuantity = [ingredient[1]]
            selection_operation_name = onto.search(iri=f"*{one_selection_operation.name}")[0]

            list_selection_operation.append(selection_operation_name)

        recipe_name.hasSelectionOperation = list_selection_operation


def add_property(onto, name_recipe, informations):
    with onto:
        list_ingredients = list()
        name_class = onto.search(iri=f"*{name_recipe}")[0]

        for ingredient in informations["Ingredient"]:
            ingredient = ingredient[0].replace(" ", "_").replace("'", "_").replace("(", "_").replace(")",
                                                                                                     "").replace(
                "®", "")
            ingredient = onto.search(iri=f"*{ingredient}")[0]
            list_ingredients.append(ingredient)

        name_class.is_a.append(onto.hasIngredient.only(OneOf(list_ingredients)))


def add_diet_classes(onto, name_recipe, informations):
    with onto:
        class ByDiet(onto.search(iri=f"*Recipes")[0]):
            equivalent_to = [onto.search(iri=f"*ByCourse")[0]]

        class energetic_recipes(ByDiet):
            equivalent_to = [
                ByDiet & (onto.withIngredient.some(onto.search(iri=f"*energetic_ingredient")[0]))]

        class vegetarian_recipes(ByDiet):
            equivalent_to = [
                ByDiet & (onto.hasIngredient.only(onto.search(iri=f"*vegetarian_ingredient")[0]))]

        class vegan_recipes(ByDiet):
            equivalent_to = [ByDiet & (onto.hasIngredient.only(onto.search(iri=f"*vegan_ingredient")[0]))]

        class protective_recipes(ByDiet):
            equivalent_to = [
                ByDiet & (onto.withIngredient.some(onto.search(iri=f"*protective_ingredient")[0]))]

        class plastic_recipes(ByDiet):
            equivalent_to = [
                ByDiet & (onto.withIngredient.some(onto.search(iri=f"*plastic_ingredient")[0]))]

        class without_lactose_recipes(ByDiet):
            equivalent_to = [
                ByDiet & (onto.withIngredient.some(onto.search(iri=f"*without_lactose_ingredient")[0]))]

        class meat_or_fish_recipes(ByDiet):
            equivalent_to = [
                ByDiet & (onto.withIngredient.some(onto.search(iri=f"*meat_or_fish_ingredient")[0]))]

        ByDiet.label.append("Recipes divide by diet")
        energetic_recipes.label.append("energetic recipe")
        vegetarian_recipes.label.append("vegetarian recipe")
        vegan_recipes.label.append("vegan recipe")
        protective_recipes.label.append("protective recipe")
        plastic_recipes.label.append("plastic recipe")
        without_lactose_recipes.label.append("without lactose recipe")
        meat_or_fish_recipes.label.append("Meat and fish recipe")


def add_ingredients_classes(onto, name_recipe, informations):
    with onto:
        class Ingredients(Thing):
            pass

        class Ingredients_by_food_groups(Ingredients):
            pass

        class Beverages(Ingredients_by_food_groups):
            pass

        class Condiments(Ingredients_by_food_groups):
            pass

        class Ingredients_group_1(Ingredients_by_food_groups):
            pass

        class Ingredients_group_2(Ingredients_by_food_groups):
            pass

        class Ingredients_group_3(Ingredients_by_food_groups):
            pass

        class Ingredients_group_4(Ingredients_by_food_groups):
            pass

        class Ingredients_group_5(Ingredients_by_food_groups):
            pass

        Ingredients.label.append("Ingredients")
        Ingredients_by_food_groups.label.append("ByFoodGroups")
        Beverages.label.append("Beverages")
        Condiments.label.append("Condiments")
        Ingredients_group_1.label.append("Group-1")
        Ingredients_group_2.label.append("Group-2")
        Ingredients_group_3.label.append("Group-3")
        Ingredients_group_4.label.append("Group-4")
        Ingredients_group_5.label.append("Group-5")

        class Ingredients_by_category(Ingredients):
            equivalent_to = [Ingredients_by_food_groups]

        class cheesy_ingredients(Ingredients_by_category):
            equivalent_to = [Ingredients_by_category & Ingredients_group_3]

        class ketogenic_ingredients(Ingredients_by_category):
            pass

        class meat_or_fish_ingredients(Ingredients_by_category):
            equivalent_to = [Ingredients_by_category & (Ingredients_group_4 & Ingredients_by_category)]

        class vegan_ingredients(Ingredients_by_category):
            equivalent_to = [
                Ingredients_by_category & (Beverages or Condiments or Ingredients_group_2 or Ingredients_group_5)]

        class vegetarian_ingredients(Ingredients_by_category):
            equivalent_to = [
                Ingredients_by_category & (Beverages | Condiments | Ingredients_group_2 | Ingredients_group_5)]

        class without_lactose_ingredients(Ingredients_by_category):
            equivalent_to = [
                Ingredients_by_category & (Beverages | Condiments | Ingredients_group_2 | Ingredients_group_5)]

        Ingredients_by_category.label.append("ByCategory")
        cheesy_ingredients.label.append("Cheesy")
        ketogenic_ingredients.label.append("Ketogenic")
        meat_or_fish_ingredients.label.append("Meat/Fish")
        vegan_ingredients.label.append("Vegan")
        vegetarian_ingredients.label.append("Vegetarian")
        without_lactose_ingredients.label.append("No lactose")

        class Ingredients_by_function(Ingredients):
            equivalent_to = [Ingredients_by_food_groups]

        class energetic_ingredients(Ingredients_by_function):
            equivalent_to = [Ingredients_by_function & (Ingredients_group_1 & Ingredients_group_5)]

        class plastic_ingredients(Ingredients_by_function):
            equivalent_to = [Ingredients_by_function & (Ingredients_group_3 & Ingredients_group_4)]

        class protective_ingredients(Ingredients_by_function):
            equivalent_to = [Ingredients_by_function & Ingredients_group_2]

        Ingredients_by_function.label.append("ByFunction")
        energetic_ingredients.label.append("Energetic")
        plastic_ingredients.label.append("Plastic")
        protective_ingredients.label.append("Protective")


def add_ingredients_instances(onto, name_recipe, informations):
    with onto:
        category_ingredient = {
            "1": onto.Ingredients_group_1,
            "2": onto.Ingredients_group_2,
            "3": onto.Ingredients_group_3,
            "4": onto.Ingredients_group_4,
            "5": onto.Ingredients_group_5,
            "6": onto.Beverages,
            "7": onto.Condiments,
        }

    for ingredient in informations["Ingredient"]:

        ingredient_renamed = ingredient[0].lower() \
            .replace(" ", "_") \
            .replace("'", "_") \
            .replace("(", "_") \
            .replace(")", "") \
            .replace("®", "") \
            .replace("__", "_")

        try:

            onto.search(iri=f"*{ingredient_renamed}")[0]

        except IndexError:

            category = input(f'\nWhat is the category of {ingredient[0].upper()}?\n\n'
                             '1. Cereali e derivati, tuberi\n'
                             '2. Frutta e ortaggi\n'
                             '3. Latte e derivati\n'
                             '4. Carne, Pesci, Uova e Legumi\n'
                             '5. Grassi e Oli da condimento\n'
                             '6. Bere\n'
                             '7. Condimenti\n\n'
                             'insert only the number ----> ').strip()

            name_category = category_ingredient[str(category)]
            name_category(ingredient_renamed)
            onto.search(iri=f"*{ingredient_renamed}")[0].label.append(ingredient[0])
