

class OntoExecutor:

    def __init__(self, list_steps, builder_class):
        self.builder = builder_class
        self.steps = list_steps



    def exec(self):

        self.builder.recipe_class()

        self.builder.ingredient_class()



