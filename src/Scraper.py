from bs4 import BeautifulSoup
from src.Connector import Connector
from src.utility.Scraper_func import cat_url, recipes_url, manage_quantity


class GZScraper:

    def __init__(self):

        self.html_catergory = Connector({"Main_page/main_page": "https://www.giallozafferano.it/"}).data
        self.categories = self.all_recipes_category()
        self.html_catalogue = Connector(cat_url(self.categories)).data
        self.name_recipes = self.all_recipes_names()
        self.html_catalogue_info = Connector(recipes_url(self.name_recipes[:100])).data
        self.recipes_information = self.all_recipes_information()

    def all_recipes_category(self):

        if isinstance(self.html_catergory, dict):
            soup = BeautifulSoup(self.html_catergory["Main_page/main_page"], 'html.parser')
        else:
            soup = BeautifulSoup(self.html_catergory, 'html.parser')
        foo = soup.find("li", {"class": "gz-header-has-children"})
        list_element = foo.find("ul").find_all("li")
        new_list = []
        try:
            for q in list_element:
                new_list.append(q.a.text)
        except TypeError:
            pass

        return new_list

    def all_recipes_names(self):

        list_recipes_names = list()
        if isinstance(self.html_catalogue, dict):
            for name_page, html_page in self.html_catalogue.items():
                soup = BeautifulSoup(html_page, 'html.parser')

                foo = soup.find_all("h2", {"class": "gz-title"})
                for name in foo:
                    if name is not None and name.text not in list_recipes_names:
                        list_recipes_names.append(name.text)
        return list_recipes_names

    def all_recipes_information(self):

        dict_recipes_names = dict()
        if isinstance(self.html_catalogue_info, dict):
            for name_page, html_page in self.html_catalogue_info.items():
                soup = BeautifulSoup(html_page, 'html.parser')
                title = soup.find("h1", {"class": "gz-title-recipe"})
                data = soup.find_all("span", {"class": "gz-name-featured-data"})
                steps = soup.find_all("div", {"class": "gz-content-recipe-step"})

                if title is not None:
                    foo = soup.find_all("dd", {"class": "gz-ingredient"})
                    dict_recipes_names[title.text] = {"Ingredient": []}
                    f = 0
                    dict_recipes_names[title.text]["Steps"] = []
                    for step in steps:
                        f = f + 1
                        try:
                            step.span.decompose()
                        except AttributeError:
                            pass

                        dict_recipes_names[title.text]["Steps"].append(step.p.text.replace(u'\xa0', u''))

                    for el in data:
                        name_data = el.text.replace('"', '').replace(":", "").strip().split()[0]
                        dict_recipes_names[title.text][name_data] = el.strong.text
                    for name in foo:
                        if name is not None:
                            dict_recipes_names[title.text]["Ingredient"].append(
                                (name.a.text.strip(),
                                 manage_quantity(name.span.text.replace("\n", " ").replace("\t", "").strip().split())))

        return dict_recipes_names


if __name__ == "__main__":
    pass
