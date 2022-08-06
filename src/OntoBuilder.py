from owlready2 import *


class OntoBuilder:

    def __init__(self, onto, path, scraper, steps):
        print("Loading ontology")
        self.onto = get_ontology(onto).load()
        print("Loading Scraper class")
        self.scraper = scraper
        print("Loading all the steps")
        self.steps = steps
        print("Loaded all recipes informations")
        self.informations = self.scraper.recipes_information
        print("Loaded path for the final ontology")
        self.path = path

    def run(self):

        for name, information in self.informations.items():
            for transformer in self.steps:

                transformer(self.onto, name, information)
            self.onto.save(self.path)
            print(f"{name} ingredients saved".upper())


