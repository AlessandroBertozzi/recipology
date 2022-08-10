from flask import Flask, render_template, request, jsonify
from owlready2 import *
import pandas as pd

app = Flask(__name__)
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))


@app.route("/")
def home_page():
    return render_template('prova.html')


@app.route("/free_query", methods=['POST'])
def recipes_information():
    if request.method == 'POST':
        try:
            data = f"""{request.data.decode("utf-8")}"""

            go = get_ontology("./recipology_inferred.owl").load()
            print(data)

            a = list(default_world.sparql(data))

            return jsonify(a)

        except:
            return jsonify(dict({"response": "SYNTAX ERROR"}))


@app.route("/recipes/<recipe_name>", methods=["GET"])
def get_recipes_by_name(recipe_name):
    recipe_name = recipe_name.split(",")
    recipe_name = [name.strip().replace("'", " ") for name in recipe_name]
    sparql_query_recipes = """

            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX recipology: 	<http://www.semanticweb.org/return_name/ontologies/2022/1/recipology#>
            SELECT ?Recipe_label ?Ingredient_label

            WHERE {
            ?Individual a owl:NamedIndividual.
            ?Individual recipology:hasSelectionOperation ?SelectionOperationID.
            ?SelectionOperationID recipology:hasQuantity ?quantity.
            ?SelectionOperationID recipology:hasIngredient ?ingredient.
            OPTIONAL { ?Individual rdfs:label ?Recipe_label}
            OPTIONAL { ?ingredient rdfs:label ?Ingredient_label}

            }

        """

    sparql_query_categories = """
                    PREFIX rdf:
                    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX owl:
                    <http://www.w3.org/2002/07/owl#>
                    PREFIX rdfs:
                    <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX recipology:
                    <http://www.semanticweb.org/return_name/ontologies/2022/1/recipology#>
                    PREFIX recipes:
                    <http://www.semanticweb.org/return_name/ontologies/2022/1/recipes#>
                    SELECT DISTINCT ?Recipe_label ?category_label

                    WHERE {
                    ?Individual rdf:type recipology:ByDiet.
                    ?Individual rdf:type ?category_diet.
                    ?category_diet rdfs:subClassOf recipology:ByDiet.
                    OPTIONAL { ?Individual rdfs:label ?Recipe_label}
                    OPTIONAL { ?category_diet rdfs:label ?category_label}


    }

        """

    get_ontology("./recipology_inferred.owl").load()
    data_categories = list(default_world.sparql(sparql_query_categories))
    data_recipes = list(default_world.sparql(sparql_query_recipes))

    df_categories = pd.DataFrame(data_categories, columns=['Recipes', 'Categories'])

    df = pd.DataFrame(data_recipes, columns=['Recipes', 'Ingredients'])
    if 'all' not in recipe_name:
        df = df[(df.Recipes.isin(recipe_name))]

    df = df.groupby('Recipes')['Ingredients'].apply(list).reset_index(name='Ingredients')
    df_categories = df_categories.groupby('Recipes')['Categories'].apply(list).reset_index(name='Categories')


    dict_recipes = df.to_dict("records")
    dict_categories = df_categories.to_dict("records")

    for recipe_in_dict_recipes in dict_recipes:
        for recipe_in_dict_categories in dict_categories:
            if recipe_in_dict_categories["Recipes"] == recipe_in_dict_recipes["Recipes"]:
                recipe_in_dict_recipes["Categories"] = recipe_in_dict_categories["Categories"]
                break

    return jsonify(dict_recipes)


@app.route("/ingredients/<ingredient_name>", methods=["GET"])
def get_recipes_by_ingredient(ingredient_name):
    ingredient_name = ingredient_name.split(",")
    ingredient_name = [name.strip().replace("'", " ") for name in ingredient_name]
    sparql_query_recipes = """

            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX recipology: 	<http://www.semanticweb.org/return_name/ontologies/2022/1/recipology#>
            SELECT ?Recipe_label ?Ingredient_label

            WHERE {
            ?Individual a owl:NamedIndividual.
            ?Individual recipology:hasSelectionOperation ?SelectionOperationID.
            ?SelectionOperationID recipology:hasQuantity ?quantity.
            ?SelectionOperationID recipology:hasIngredient ?ingredient.
            OPTIONAL { ?Individual rdfs:label ?Recipe_label}
            OPTIONAL { ?ingredient rdfs:label ?Ingredient_label}

            }

        """

    sparql_query_categories = """
                    PREFIX rdf:
                    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX owl:
                    <http://www.w3.org/2002/07/owl#>
                    PREFIX rdfs:
                    <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX recipology:
                    <http://www.semanticweb.org/return_name/ontologies/2022/1/recipology#>
                    PREFIX recipes:
                    <http://www.semanticweb.org/return_name/ontologies/2022/1/recipes#>
                    SELECT DISTINCT ?Recipe_label ?category_label

                    WHERE {
                    ?Individual rdf:type recipology:ByDiet.
                    ?Individual rdf:type ?category_diet.
                    ?category_diet rdfs:subClassOf recipology:ByDiet.
                    OPTIONAL { ?Individual rdfs:label ?Recipe_label}
                    OPTIONAL { ?category_diet rdfs:label ?category_label}


    }

        """

    get_ontology("./recipology_inferred.owl").load()
    data_categories = list(default_world.sparql(sparql_query_categories))
    data_recipes = list(default_world.sparql(sparql_query_recipes))

    df_categories = pd.DataFrame(data_categories, columns=['Recipes', 'Categories'])

    df = pd.DataFrame(data_recipes, columns=['Recipes', 'Ingredients'])

    if 'all' not in ingredient_name:
        df_ingredients_filtered = df[(df.Ingredients.isin(ingredient_name))]
        df = df[(df.Recipes.isin(list(df_ingredients_filtered.Recipes)))]

    df = df.groupby('Recipes')['Ingredients'].apply(list).reset_index(name='Ingredients')
    df_categories = df_categories.groupby('Recipes')['Categories'].apply(list).reset_index(name='Categories')


    dict_recipes = df.to_dict("records")
    dict_categories = df_categories.to_dict("records")

    for recipe_in_dict_recipes in dict_recipes:
        for recipe_in_dict_categories in dict_categories:
            if recipe_in_dict_categories["Recipes"] == recipe_in_dict_recipes["Recipes"]:
                recipe_in_dict_recipes["Categories"] = recipe_in_dict_categories["Categories"]
                break

    return jsonify(dict_recipes)


@app.route("/categories/<category_name>", methods=["GET"])
def get_recipes_by_category(category_name):
    category_name = category_name.split(",")
    category_name = [name.strip().replace("'", " ") for name in category_name]
    sparql_query_recipes = """

        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX recipology: 	<http://www.semanticweb.org/return_name/ontologies/2022/1/recipology#>
        SELECT ?Recipe_label ?Ingredient_label

        WHERE {
        ?Individual a owl:NamedIndividual.
        ?Individual recipology:hasSelectionOperation ?SelectionOperationID.
        ?SelectionOperationID recipology:hasQuantity ?quantity.
        ?SelectionOperationID recipology:hasIngredient ?ingredient.
        OPTIONAL { ?Individual rdfs:label ?Recipe_label}
        OPTIONAL { ?ingredient rdfs:label ?Ingredient_label}

        }

    """

    sparql_query_categories = """
                PREFIX rdf:
                <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl:
                <http://www.w3.org/2002/07/owl#>
                PREFIX rdfs:
                <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX recipology:
                <http://www.semanticweb.org/return_name/ontologies/2022/1/recipology#>
                PREFIX recipes:
                <http://www.semanticweb.org/return_name/ontologies/2022/1/recipes#>
                SELECT DISTINCT ?Recipe_label ?category_label
                
                WHERE {
                ?Individual rdf:type recipology:ByDiet.
                ?Individual rdf:type ?category_diet.
                ?category_diet rdfs:subClassOf recipology:ByDiet.
                OPTIONAL { ?Individual rdfs:label ?Recipe_label}
                OPTIONAL { ?category_diet rdfs:label ?category_label}


}

    """

    get_ontology("./recipology_inferred.owl").load()
    data_categories = list(default_world.sparql(sparql_query_categories))
    data_recipes = list(default_world.sparql(sparql_query_recipes))

    df_categories = pd.DataFrame(data_categories, columns=['Recipes', 'Categories'])
    df_recipes = pd.DataFrame(data_recipes, columns=['Recipes', 'Ingredients'])

    if 'all' not in category_name:
        df_categories_filtered = df_categories[(df_categories.Categories.isin(category_name))]
        df_recipes = df_recipes[(df_recipes.Recipes.isin(list(df_categories_filtered.Recipes)))]

    df_recipes = df_recipes.groupby('Recipes')['Ingredients'].apply(list).reset_index(name='Ingredients')
    df_categories = df_categories.groupby('Recipes')['Categories'].apply(list).reset_index(name='Categories')

    dict_recipes = df_recipes.to_dict("records")
    dict_categories = df_categories.to_dict("records")

    for recipe_in_dict_recipes in dict_recipes:
        for recipe_in_dict_categories in dict_categories:
            if recipe_in_dict_categories["Recipes"] == recipe_in_dict_recipes["Recipes"]:
                recipe_in_dict_recipes["Categories"] = recipe_in_dict_categories["Categories"]
                break

    return jsonify(dict_recipes)


if __name__ == "__main__":
    app.run()
