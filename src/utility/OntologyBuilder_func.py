from owlready2 import *
from src.Scraper import GZScraper






def create_new_class(name, upper_class):
    types.new_class(name, (upper_class,))


def find_class(onto, name):
    for onto_class in onto.classes():
        if str(onto_class).split(".")[1].lower() == name.lower():
            return onto_class

    for onto_individual in onto.individuals():
        if str(onto_individual).split(".")[1].lower() == name.replace(" ", "_").replace("'", "_").replace("(", "_").replace(")", "").replace("®", "").lower():
            return onto_individual
