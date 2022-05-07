from owlready2 import *
from Scraper import GZScraper

onto = get_ontology("../definitiveversion.owl").load()

gz = GZScraper()
list_recipes = gz.recipes_information

# print(list_recipes)


for i in list_recipes.keys():
    with onto:
        my_new_class = types.new_class(i, (onto.Antipasti,))

# Create a new class
for my_class in onto.classes():

    if my_class is onto.Antipasti:
        print(onto.search(subclass_of=onto.Antipasti))

onto.save("../definitiveversion_2.owl")
