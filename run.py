from src.OntoBuilder import *
from src.Scraper import *
from src.utility.OntoBuilder_funcs import *


onto_path.append("C:/Users/aless/Desktop/food_ontology_project/data/ontologies/")


path_onto_recipes = "pop.owl"

builder = OntoBuilder(
    onto="empty_ontology.owl",
    path=path_onto_recipes,
    scraper=GZScraper(),
    steps=[
        add_ingredients_classes,
        add_ingredients_instances
    ])

builder.run()

path_onto_ingredients = "recipes.owl"

builder = OntoBuilder(
    onto="empty_ontology.owl",
    path=path_onto_ingredients,
    scraper=GZScraper(),
    steps=[
        add_Recipes_classes,
        add_Recipes_courses_categories,
        add_recipes_instances
    ])

builder.run()


onto_recipology = get_ontology("empty_ontology.owl").load()

onto_ingredients = get_ontology(path_onto_ingredients).load()
onto_recipology.imported_ontologies.append(onto_ingredients)

onto_recipes = get_ontology(path_onto_recipes).load()
onto_recipology.imported_ontologies.append(onto_recipes)

onto_recipology.save("./recipollo.owl")

builder = OntoBuilder(
    onto="./recipollo.owl",
    path="./recipollo.owl",
    scraper=GZScraper(),
    steps=[
        add_selection_operation_class,
        add_base_property,
        add_selection_operation_instances,
        add_property,
        add_diet_classes
    ])

builder.run()
