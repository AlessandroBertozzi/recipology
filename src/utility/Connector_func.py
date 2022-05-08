import json
import urllib3
import os
import requests



def spys_proxy():

    if not os.path.exists("./src/utility/list_daily_proxy.json"):
        proxy_website = "https://spys.me/proxy.txt"

        print("Scraping proxy...")

        data = requests.get(proxy_website)
        list_daily_proxy = list()
        for i in data.text.split("\n\n")[1].split("\n"):
            if "Free" not in i and i != "\r":
                proxy = i.split(" ")[0]
                proxy = proxy.split(":")
                proxy = {"IP": proxy[0], "PORT": proxy[1]}
                list_daily_proxy.append(proxy)
        f = open("./src/utility/list_daily_proxy.json", "w")

        print("Saving proxies list...")

        json.dump(list_daily_proxy, f)

        return list_daily_proxy

    else:

        print("Open proxies list...")

        list_daily_proxy = open_json("./src/utility/list_daily_proxy.json")

        return list_daily_proxy


def try_proxy(item, url):
    try:
        proxy = urllib3.ProxyManager(f"http://{item['IP']}:{item['PORT']}/")
        response = proxy.request("GET", url)
        response.close()
        return response

    except Exception:

        return None


def make_request(url, proxy_list):

    response = try_proxy(proxy_list, url)

    if response is None:
        print(f"bad response")
    else:
        print(f"{proxy_list['IP']}:{proxy_list['PORT']}, is working")
        return response.data


def to_html(name_html, data_response):
    print("Start to save response in html format")

    print(f"saving as {name_html} in /data/html/")

    file = open(f"./data/html/{name_html}.html", "wb")
    file.write(data_response)
    file.close()
    print("Succeeded!")


def open_json(file_path, mode="read", data=None):
    if mode == "read":
        f = open(file_path)

        data = json.load(f)
        f.close()

        return data

    else:
        f = open(file_path, "w")
        json.dump(data, f)


if __name__ == "__main__":
    pass
