



def cat_url(list_of_categories):
    dict_url = dict()
    for category in list_of_categories:
        if category == "Primi piatti":
            category = category.split(" ")[0]

        category = category.replace(' ', '-')
        dict_url[f"Catalogue/{category}"] = f"https://www.giallozafferano.it/ricette-cat/{category}/"
        for number_of_page in range(1, 11):
            dict_url[f"Catalogue/{category}_{number_of_page}"] = f"https://www.giallozafferano.it/ricette-cat/page{number_of_page}/{category}/"
    return dict_url


def recipes_url(list_of_categories):
    dict_url = dict()
    for recipe in list_of_categories:
        recipe = recipe[0].replace(" ", "-").replace("(", "").replace(")", "")
        dict_url[f"Recipes/{recipe}"] = f"https://www.giallozafferano.it/{recipe}.html"

    return dict_url


def dict_categories(list_names_categories):
    dict_category = dict()
    for recipe in list_names_categories:
        dict_category[recipe[0]] = recipe[1]

    return dict_category


def manage_quantity(quantity):

    if len(quantity) == 1:
        return quantity[0]

    elif len(quantity) == 2:
        return " ".join(quantity)

    else:
        new_list = [quantity[-1], quantity[-2]]
        return " ".join(new_list)





