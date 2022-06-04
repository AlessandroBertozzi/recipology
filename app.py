from flask import Flask, render_template
from src.Scraper import GZScraper
from src.Connector import Connector
from src.sparql_query import *
from flask import jsonify
import random

# from src.OntologyBuilder import prova_html

app = Flask(__name__)


@app.route("/")
def home_page():

    return render_template('prova.html')



@app.route("/random")
def recipes_information():
    with open("static/inferred_query.pickle", "rb") as f1, open("static/normal_query.pickle", "rb") as f2:
        inferred_query = pickle.load(f1)
        normal_query = pickle.load(f2)
        name_recipe = random.choice(list(normal_query.keys()))

        image_link = {"vegan_recipe": "img/vegan.png",
                      "vegetarian_recipe": "img/vegetarian.png",
                      "protective_recipe": "img/insurance.png",
                      "energetic_recipe": "img/energetic.png",
                      "without_lactose_recipe": "img/lactose-free.png",
                      "plastic_recipe": "img/molecule.png",
                      "meat_fish_recipe": "img/protein.png",
                      }

        return render_template('prova_2.html', name_recipe=name_recipe,
                               inferred_dict=inferred_query[name_recipe], image_link=image_link)



if __name__ == "__main__":

    app.run()